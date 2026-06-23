from sqlalchemy import create_engine

DATABASE_URL = "postgresql://admin:admin@postgres:5432/acme"

engine = create_engine(DATABASE_URL)