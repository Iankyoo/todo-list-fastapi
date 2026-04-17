#!/bin/sh

echo "⏳ Waiting for database..."

while ! nc -z fastzero_database 5432; do
  sleep 1
done

echo "✅ Database is up!"

# Pequeno delay extra (Postgres às vezes aceita socket antes de estar pronto)
sleep 2

echo "🚀 Running migrations..."
poetry run alembic upgrade head || exit 1

echo "🔥 Starting app..."
poetry run uvicorn fast_zero.app:app --host 0.0.0.0 --port 8000