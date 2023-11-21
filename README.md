# SprintCoders_project
 Repository for our REST Api project "FotoRahmen"
Перед початком роботи переконайтеся, що встановлені наступні компоненти та залежності з pyproject.toml

## Встановлення та налаштування

1. Склонуйте репозиторій проекту на свій локальний комп'ютер.
2. Встановіть необхідні залежності
3. В каталозі проекту створіть файл .env та додайте туди свої дані за таким шаблоном у файлі env.example
4. Створіть підключення до бази даних Postgres та Redis за допомогою команди docker-compose up
5. Запустіть сервер командою uvicorn main:app --reload
6. Відкрийте документацію Swagger за посиланням http://localhost:8000/docs або використовуйте вже задеплоєний застосунок за адресою https://pywebteam-7-project-zhowtenkooleksi.replit.app/
