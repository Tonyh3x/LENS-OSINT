# LENS OSINT ANALYZER DATA - Prezentacja Aplikacji

## 1. Przegląd Ogólny
LENS OSINT ANALYZER DATA to zaawansowana aplikacja webowa do analizy metadanych plików, wykorzystująca technologię ExifTool. Aplikacja umożliwia użytkownikom przetwarzanie i analizę różnych typów plików, generowanie raportów oraz eksport wyników w formacie PDF i TXT.

## 2. Funkcjonalności

### 2.1 Przetwarzanie Plików
- Obsługa wielu formatów plików (txt, doc, docx, pdf, png, jpg, jpeg, bmp)
- Limit 5 plików na raz dla bezpieczeństwa
- Wykrywanie i analiza metadanych plików
- Wyświetlanie rozmiaru pliku w czytelnej formie (KB, MB, GB)

### 2.2 Interfejs Użytkownika
- Intuicyjny interfejs drag&drop
- Status uploadu z ikonką
- Dynamiczne wyświetlanie sekcji (ukrywanie niepotrzebnych)
- Wyraźne formatowanie wyników analizy
- Przyciski do pobierania raportów PDF i TXT

### 2.3 Generowanie Raportów
- Automatyczne generowanie raportów PDF i TXT
- Formatowanie metadanych
- Sortowanie kluczy alfabetycznie
- Wyświetlanie dodatkowych informacji:
  - Rozmiar pliku
  - Hash SHA256
  - Uprawnienia pliku
  - Właściciel i grupa pliku

## 3. Technologia

### 3.1 Stos Technologiczny
- Python 3.x
- Flask (framework webowy)
- ExifTool (analiza metadanych)
- Bootstrap 5.3 (UI framework)
- JavaScript (interaktywność)
- ReportLab (generowanie PDF)

### 3.2 Architektura
- Serwer Flask obsługujący przesyłanie plików
- Asynchroniczne przetwarzanie plików
- Obsługa błędów i raportów
- Bezpieczeństwo i walidacja plików

## 4. Historia Wersji

### 4.1 Wersja 1.4 (2025-05-16)
- Dodano możliwość pobierania raportów PDF i TXT
- Poprawiono obsługę ścieżek do raportów
- Usunięto powtarzające się nagłówki
- Ulepszone formatowanie wyników analizy
- Poprawiony kolor tekstu "Analizowane"
- Lepsze zarządzanie wyświetlaniem sekcji

### 4.2 Wersja 1.3 (2025-05-16)
- Usunięto powtarzające się nagłówki
- Ulepszone formatowanie wyników analizy
- Poprawiony kolor tekstu "Analizowane"
- Usunięto niepotrzebne sekcje
- Lepsze zarządzanie wyświetlaniem sekcji

### 4.3 Wersja 1.2 (2025-05-12)
- Dodano limit 5 plików na raz
- Usunięto system logowania
- Zwiększone bezpieczeństwo
- Ulepszone wyświetlanie wyników

## 5. Bezpieczeństwo
- Walidacja typów plików
- Limit liczby przesyłanych plików
- Bezpieczne zapisywanie plików
- Obsługa błędów i wyjątków
- Logowanie działań

## 6. Perspektywy Rozwoju
- Dodanie więcej formatów plików
- Rozszerzenie analizy metadanych
- Dalsze ulepszenia UI
- Dodanie funkcji eksportu
- Integracja z systemem zarządzania plikami
