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
docker build -t flask-todo .
docker run -p 5000:5000 -v "${PWD}\data:/app/data" flask-todo

// testuję Dockera
