import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_wtf.csrf import CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix
import subprocess
import json
from datetime import datetime
import sys
import logging
from reportlab.lib.styles import getSampleStyleSheet

# Konfiguracja zabezpieczeń
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

csrf = CSRFProtect(app)

# Konfiguracja Flaska
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'your-secret-key'),
    MAX_CONTENT_LENGTH=10 * 1024 * 1024,  # 10MB limit
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=3600  # 1 godzina
)

# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Konfiguracja logowania
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Konfiguracja ścieżek
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['REPORTS_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['REPORTS_FOLDER'], exist_ok=True)

def run_exiftool(file_path, timeout=5):
    try:
        # Sprawdź, czy plik istnieje
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return None

        # Uruchom ExifTool z dodatkowymi flagami i limitem czasu
        result = subprocess.run(
            ['exiftool', 
             '-j', 
             '-G',  # Grupuj według tagów
             '-u',  # Użyj URL dla linków
             '-n',  # Wyświetl wartości numeryczne
             '-s',  # Tylko wartości
             '-a',  # Wszystkie wystąpienia
             '-struct',  # Struktura danych
             '-charset', 'UTF8',  # Kodowanie UTF8
             file_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )
    try:
        # Sprawdź, czy plik istnieje
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return None

        # Uruchom ExifTool z dodatkowymi flagami
        result = subprocess.run(['exiftool', 
                               '-j', 
                               '-G',  # Grupuj według tagów
                               '-u',  # Użyj URL dla linków
                               '-n',  # Wyświetl wartości numeryczne
                               '-s',  # Tylko wartości
                               '-a',  # Wszystkie wystąpienia
                               '-struct',  # Struktura danych
                               '-charset', 'UTF8',  # Kodowanie UTF8
                               file_path],
                              capture_output=True,
                              text=True)

        if result.returncode == 0:
            try:
                # Parsuj JSON
                metadata = json.loads(result.stdout)
                if metadata:
                    # Dodaj informacje o pliku
                    metadata[0]['FileSize'] = os.path.getsize(file_path)
                    metadata[0]['FileHash'] = get_file_hash(file_path)
                    metadata[0]['FilePermissions'] = oct(os.stat(file_path).st_mode & 0o777)
                    metadata[0]['FileOwner'] = os.stat(file_path).st_uid
                    metadata[0]['FileGroup'] = os.stat(file_path).st_gid
                    return metadata[0]
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing JSON: {str(e)}")
                return None
        else:
            logger.error(f"ExifTool error: {result.stderr}")
            return None

    except Exception as e:
        logger.error(f"Error running ExifTool: {str(e)}")
        return None

# Pomocnicza funkcja do obliczania hasha pliku
def get_file_hash(file_path):
    import hashlib
    try:
        with open(file_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception as e:
        logger.error(f"Error calculating file hash: {str(e)}")
        return None

def generate_pdf_report(data, timestamp):
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        
        report_path = os.path.join(app.config['REPORTS_FOLDER'], f"report_{timestamp}.pdf")
        doc = SimpleDocTemplate(report_path, pagesize=letter)
        
        elements = []
        styles = getSampleStyleSheet()
        
        # Tytuł
        elements.append(Paragraph("LENS OSINT ANALYZER DATA REPORT", styles['Title']))
        elements.append(Spacer(1, 20))
        
        # Data i czas
        elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Dane plików
        for item in data:
            elements.append(Paragraph(f"File: {item.get('SourceFile', 'Unknown')}", styles['Heading2']))
            elements.append(Spacer(1, 12))
            
            # Wyświetl wszystkie dostępne metadane
            metadata_keys = list(item.keys())
            metadata_keys.sort()  # Sortowanie kluczy alfabetycznie
            
            for key in metadata_keys:
                if key in ['SourceFile', 'FileSize', 'FileHash', 'FilePermissions', 'FileOwner', 'FileGroup']:
                    # Dodatkowe formatowanie dla kluczowych pól
                    if key == 'FileSize':
                        size = item[key]
                        if size >= 1073741824:  # GB
                            size_str = f"{size/1073741824:.2f} GB"
                        elif size >= 1048576:  # MB
                            size_str = f"{size/1048576:.2f} MB"
                        elif size >= 1024:  # KB
                            size_str = f"{size/1024:.2f} KB"
                        else:
                            size_str = f"{size} B"
                        elements.append(Paragraph(f"{key}: {size_str}", styles['Normal']))
                    elif key == 'FilePermissions':
                        elements.append(Paragraph(f"{key}: {item[key]}", styles['Normal']))
                    elif key == 'FileHash':
                        elements.append(Paragraph(f"{key}: {item[key]}", styles['Normal']))
                    else:
                        elements.append(Paragraph(f"{key}: {item[key]}", styles['Normal']))
                else:
                    # Dla pozostałych pól
                    elements.append(Paragraph(f"{key}: {item[key]}", styles['Normal']))
            
            elements.append(Spacer(1, 20))
        
        doc.build(elements)
        logger.info(f"Generated PDF report: {report_path}")
        return report_path

    except Exception as e:
        logger.error(f"Error generating PDF report: {str(e)}")
        return None

def generate_txt_report(data, timestamp):
    try:
        report_path = os.path.join(app.config['REPORTS_FOLDER'], f"report_{timestamp}.txt")
        
        with open(report_path, 'w') as f:
            f.write("LENS OSINT ANALYZER DATA REPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for item in data:
                f.write(f"File: {item.get('SourceFile', 'Unknown')}\n\n")
                
                # Wyświetl wszystkie dostępne metadane
                metadata_keys = list(item.keys())
                metadata_keys.sort()  # Sortowanie kluczy alfabetycznie
                
                for key in metadata_keys:
                    if key in ['FileSize']:
                        # Formatowanie rozmiaru pliku
                        size = item[key]
                        if size >= 1073741824:  # GB
                            size_str = f"{size/1073741824:.2f} GB"
                        elif size >= 1048576:  # MB
                            size_str = f"{size/1048576:.2f} MB"
                        elif size >= 1024:  # KB
                            size_str = f"{size/1024:.2f} KB"
                        else:
                            size_str = f"{size} B"
                        f.write(f"{key}: {size_str}\n")
                    else:
                        f.write(f"{key}: {item[key]}\n")
                
                f.write("\n")
        
        logger.info(f"Generated TXT report: {report_path}")
        return report_path

    except Exception as e:
        logger.error(f"Error generating TXT report: {str(e)}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/analyze', methods=['POST'])
def analyze_files():
    try:
        # Walidacja CSRF token
        csrf.protect()
        
        # Sprawdzenie wielkości pliku przed zapisem
        if request.content_length > app.config['MAX_CONTENT_LENGTH']:
            return jsonify({
                'error': 'File too large',
                'results': [],
                'errors': ['Maximum file size is 10MB'],
                'pdf_report': None,
                'txt_report': None
            }), 413

        if 'files[]' not in request.files:
            logger.error("No files provided in request")
            return jsonify({
                'error': 'No files provided',
                'results': [],
                'errors': ['No files provided'],
                'pdf_report': None,
                'txt_report': None
            }), 400
    try:
        logger.info("Received file upload request")
        
        if 'files[]' not in request.files:
            logger.error("No files provided in request")
            return jsonify({
                'error': 'No files provided',
                'results': [],
                'errors': ['No files provided'],
                'pdf_report': None,
                'txt_report': None
            }), 400

        files = request.files.getlist('files[]')
        if len(files) > 5:
            logger.error(f"Too many files: {len(files)}")
            return jsonify({
                'error': 'Maximum 5 files allowed',
                'results': [],
                'errors': ['Maximum 5 files allowed'],
                'pdf_report': None,
                'txt_report': None
            }), 400

        results = []
        errors = []
        
        for file in files:
            if file and file.filename:
                try:
                    # Dodatkowa walidacja nazwy pliku
                    filename = secure_filename(file.filename)
                    if not filename:
                        logger.error(f"Invalid filename: {file.filename}")
                        errors.append(f"Invalid filename: {file.filename}")
                        continue

                    # Sprawdź rozszerzenie pliku
                    allowed_extensions = {'txt', 'doc', 'docx', 'pdf', 'png', 'jpg', 'jpeg', 'bmp'}
                    if not filename.lower().endswith(tuple(allowed_extensions)):
                        logger.error(f"Invalid file extension: {filename}")
                        errors.append(f"Invalid file type: {filename}")
                        continue

                    # Zapis pliku z limitem czasu
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    try:
                        with open(file_path, 'wb') as f:
                            f.write(file.read())
                        logger.info(f"Saved file: {file_path}")
                    except Exception as e:
                        logger.error(f"Error saving file {filename}: {str(e)}")
                        errors.append(f"Error saving file {filename}: {str(e)}")
                        continue

                    # Analiza pliku z limitem czasu
                    try:
                        result = run_exiftool(file_path, timeout=5)
                        if result:
                            results.append(result)
                        else:
                            errors.append(f"Error analyzing file: {filename}")
                    except subprocess.TimeoutExpired:
                        logger.error(f"Timeout analyzing file: {filename}")
                        errors.append(f"Timeout analyzing file: {filename}")
                    except Exception as e:
                        logger.error(f"Error analyzing file {filename}: {str(e)}")
                        errors.append(f"Error analyzing file {filename}: {str(e)}")

                except Exception as e:
                    logger.error(f"Error processing file {filename}: {str(e)}")
                    errors.append(f"Error processing file {filename}: {str(e)}")

        results = []
        errors = []
        
        for file in files:
            if file and file.filename:
                try:
                    # Sprawdź rozszerzenie pliku
                    allowed_extensions = {'txt', 'doc', 'docx', 'pdf', 'png', 'jpg', 'jpeg', 'bmp'}
                    if not file.filename.lower().endswith(tuple(allowed_extensions)):
                        logger.error(f"Invalid file extension: {file.filename}")
                        errors.append(f"Invalid file type: {file.filename}")
                        continue

                    # Zapis pliku
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                    try:
                        file.save(file_path)
                        logger.info(f"Saved file: {file_path}")
                    except Exception as e:
                        logger.error(f"Error saving file {file.filename}: {str(e)}")
                        errors.append(f"Error saving file {file.filename}: {str(e)}")
                        continue

                    # Analiza pliku
                    try:
                        result = run_exiftool(file_path)
                        if result:
                            results.append(result)
                        else:
                            errors.append(f"Error analyzing file: {file.filename}")
                    except Exception as e:
                        logger.error(f"Error analyzing file {file.filename}: {str(e)}")
                        errors.append(f"Error analyzing file {file.filename}: {str(e)}")

                except Exception as e:
                    logger.error(f"Error processing file {file.filename}: {str(e)}")
                    errors.append(f"Error processing file {file.filename}: {str(e)}")

        # Generowanie raportów PDF i TXT
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        pdf_report = None
        txt_report = None
        
        if results:
            try:
                if not os.path.exists(app.config['REPORTS_FOLDER']):
                    os.makedirs(app.config['REPORTS_FOLDER'])

                # Generuj PDF
                pdf_path = os.path.join(app.config['REPORTS_FOLDER'], f"report_{timestamp}.pdf")
                pdf_report = generate_pdf_report(results, timestamp)
                
                # Generuj TXT
                txt_path = os.path.join(app.config['REPORTS_FOLDER'], f"report_{timestamp}.txt")
                txt_report = generate_txt_report(results, timestamp)

                # Zwracamy ścieżki do plików bez pełnej ścieżki systemowej
                if pdf_report:
                    pdf_report = pdf_report.replace(os.path.dirname(os.path.abspath(__file__)), '')
                if txt_report:
                    txt_report = txt_report.replace(os.path.dirname(os.path.abspath(__file__)), '')

            except Exception as e:
                logger.error(f"Error generating reports: {str(e)}")
                errors.append(f"Error generating reports: {str(e)}")

        return jsonify({
            'results': results,
            'errors': errors,
            'pdf_report': pdf_report,
            'txt_report': txt_report
        })

    except Exception as e:
        logger.error(f"Error in analyze_files: {str(e)}")
        return jsonify({
            'error': str(e),
            'results': [],
            'errors': [str(e)],
            'pdf_report': None,
            'txt_report': None
        }), 500

@app.route('/reports/<filename>')
def download_report(filename):
    try:
        logger.debug(f"Próba pobrania pliku: {filename}")
        return send_from_directory(app.config['REPORTS_FOLDER'], filename, as_attachment=True)
    except Exception as e:
        logger.error(f"Błąd podczas pobierania pliku: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logger.info("Starting application")
    app.run(debug=True, host='0.0.0.0', port=5000)
