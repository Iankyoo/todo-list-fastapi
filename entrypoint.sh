#!/bin/sh

echo "Waiting for database..."
# Verifica apenas se o banco está aceitando conexões na porta (opcional mas seguro)
# Se preferir manter o teste via Python, garanta que o DATABASE_URL esteja correto:
until poetry run python -c "
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
import os
import sys

async def test():
    try:
        url = os.getenv('DATABASE_URL')
        engine = create_async_engine(url)
        async with engine.connect() as conn:
            # O segredo está no text('SELECT 1')
            await conn.execute(text('SELECT 1'))
        await engine.dispose()
    except Exception as e:
        print(f'Connection failed: {e}')
        sys.exit(1)

asyncio.run(test())
"; do
  echo "Retrying in 2s..."
  sleep 2
done

echo "Database is ready!"

echo "Running migrations..."

poetry run alembic upgrade head || exit 1

echo "Starting app..."
exec poetry run uvicorn fast_zero.app:app --host 0.0.0.0 --port 8000