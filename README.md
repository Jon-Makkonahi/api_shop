# api_shop

Можно создать любую заведомую БД PostgeSQL

Выполнить эти команды, для создания миграций


alembic init -t async app/migrations

Так как будут созданы следующие данные
В результате будут созданы следующие файлы:

alembic.ini: Конфигурационный файл в корне проекта, задающий настройки подключения к базе данных и пути к миграциям.
app/migrations/env.py: Определяет, как Alembic подключается к базе данных и какие модели SQLAlchemy использовать.
app/migrations/script.py.mako: Шаблон для генерации скриптов миграций, задающий их структуру (функции upgrade() и downgrade()).
app/migrations/versions/: Папка для хранения скриптов миграций (пока пустая).
app/migrations/README: Краткое описание директории миграций.

То в alembiс.ini нужно прописать необходимый адрес до вашей БД
sqlalchemy.url = postgresql+asyncpg://user:password@127.0.0.1 (или другой сервер):5432/(название вашей БД)


Запустить миграции
alembic revision --autogenerate -m "initial schema"
alembic upgrade head


Запустить сервер
uvicorn app.main:app --reload --port 8000

при создании JWT токенов необходимо в корневой папке апп создать файл .env и поместить туда секретный ключ
SECRET_KEY=
