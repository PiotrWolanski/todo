# Task Manager (Flask)

Prosta aplikacja webowa do zarządzania zadaniami (ToDo).
Funkcje:
- dodawanie zadań,
- oznaczanie jako wykonane / cofanie,
- usuwanie,
- czyszczenie wykonanych,
- filtrowanie widoku (wszystkie / aktywne / wykonane),
- trwały zapis danych do pliku JSON.

## Technologie
- Python 3.x
- Flask
- Bootstrap (CDN)

## Uruchomienie
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python app.py
