# Aplikacja do analizy metadanych plików

Aplikacja webowa w Pythonie do analizy metadanych plików wykorzystująca ExifTool.

## Wersja stabilna 1.3 (2025-05-16)

- Usunięto powtarzające się nagłówki na stronie głównej
- Ulepszone formatowanie wyników analizy
- Poprawiony kolor tekstu "Analizowane" na biały
- Usunięto niepotrzebne sekcje z interfejsu użytkownika
- Ulepszone wyświetlanie raportów
- Dodano ikonkę statusu uploadu
- Lepsze zarządzanie wyświetlaniem sekcji

## Wymagania

- Python 3.8+
- ExifTool (do zainstalowania z https://exiftool.org/)
- Wszystkie zależności z requirements.txt

## Instalacja

1. Zainstaluj ExifTool
2. Sklonuj repozytorium
3. Zainstaluj zależności:
   ```
   pip install -r requirements.txt
   ```
4. Uruchom aplikację:
   ```
   python app.py
   ```

## Użycie

Aplikacja działa na http://localhost:5000

1. Przejdź do strony głównej
2. Wybierz pliki do analizy (obsługiwane formaty: .txt, .doc, .docx, .pdf, .png, .jpg, .bmp)
3. Kliknij "Analizuj"
4. Pobierz raport w formacie PDF lub TXT

## Struktura projektu

```
.
├── app.py              # Główna aplikacja Flask
├── static/             # Pliki statyczne (CSS, JS)
│   ├── css/
│   └── js/
├── templates/          # Szablony HTML
│   └── index.html
├── uploads/            # Tymczasowe pliki użytkownika
├── reports/           # Wygenerowane raporty
└── utils.py           # Obsługa ExifTool i eksportów

## Konfiguracja

### Zmienne środowiskowe

Aby skonfigurować aplikację, utwórz plik `.env` z następującymi zmiennymi:

```
