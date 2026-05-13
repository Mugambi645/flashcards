# 📚 Flashcards App

A simple yet powerful **Django-based flashcards** application designed for effective learning and memorization using the **Spaced Repetition System (SRS)**.

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

## ✨ Features

- Create, edit, delete, and review flashcards
- Spaced Repetition System with 5 learning boxes (Leitner-style)
- Clean and responsive UI
- SQLite database (no extra setup needed)
- Docker & Docker Compose support
- Modern packaging with `uv`

## 🚀 Quick Start

### Option 1: Local Development (Recommended)

```bash
# Clone the repository
git clone https://github.com/Mugambi645/flashcards.git
cd flashcards

# Install dependencies
uv sync

# Run migrations
uv run python manage.py migrate

# Start the development server
uv run python manage.py runserver
```
- Then open your browser and go to: http://127.0.0.1:8000

### Option 2: Using Docker

```bash
docker-compose up --build
```

- The app will be available at http://localhost:8000

## 🛠 Tech Stack

- Backend: Django
- Frontend: HTML, CSS, JavaScript
- Database: SQLite
- Containerization: Docker + Docker Compose
- Package Manager: uv

## 📁 Project Structure

flashcards-app/
├── flashcards/          # Main Django project
├── cards/               # Main flashcards app
├── db/                  # Database folder
├── templates/
├── manage.py
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

### 🤝 Contributing
Feel free to fork the project, open issues, or submit pull requests.