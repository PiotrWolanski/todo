# 📝 Task Manager (Flask)

Prosta aplikacja webowa do zarządzania zadaniami (ToDo), rozwijana jako projekt do nauki budowania aplikacji oraz pracy z Dockerem.

---

## 🚀 Funkcje

- ➕ Dodawanie zadań  
- ✅ Oznaczanie jako wykonane / cofanie  
- ❌ Usuwanie zadań  
- 🧹 Czyszczenie wykonanych  
- 🔍 Filtrowanie (wszystkie / aktywne / wykonane)  
- 🔥 Priorytety (P1 / P2 / P3)  
- ⏱️ Szacowany czas zadania (estimated time)  
- 💾 Trwały zapis danych (JSON + Docker volume)  

---

## 🛠️ Technologie

- Python 3.x  
- Flask  
- Bootstrap (CDN)  
- Docker  

---

## ▶️ Uruchomienie

### 1. Zbuduj obraz Dockera
```bash
docker build -t flask-todo .
```

### 2. Uruchom aplikacje
```bash
docker run -p 5000:5000 -v "${PWD}/data:/app/data" flask-todo
```

### 3. Otwórz w przeglądarce
Po uruchomieniu aplikacja będzie dostępna pod:
http://localhost:5000
