from urllib.parse import quote_plus

from sqlalchemy import create_engine

from sqlalchemy.orm import (
    sessionmaker,
    declarative_base
)


# =========================================================
# SENHA
# =========================================================

password = quote_plus("npg_QDpI9scwdYK3")


# =========================================================
# DATABASE URL
# =========================================================

DATABASE_URL = (
    f"postgresql+psycopg2://neondb_owner:{password}@ep-square-bar-acex0xja-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require"
)


# =========================================================
# ENGINE
# =========================================================

engine = create_engine(

    DATABASE_URL,

    pool_pre_ping=True,

    pool_recycle=300
)


# =========================================================
# SESSION
# =========================================================

SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine
)


# =========================================================
# BASE
# =========================================================

Base = declarative_base()