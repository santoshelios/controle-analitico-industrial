from db_connection import get_connection

conn = get_connection()

cursor = conn.cursor()

# =====================================================
# USERS
# =====================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS users (

    id SERIAL PRIMARY KEY,

    nome VARCHAR(200),

    usuario VARCHAR(100),

    senha VARCHAR(200),

    perfil VARCHAR(50),

    status VARCHAR(50),

    plantas TEXT
)

""")

# =====================================================
# PARAMETERS
# =====================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS parameters (

    id SERIAL PRIMARY KEY,

    nome VARCHAR(200),

    unidade VARCHAR(50),

    limite_min FLOAT,

    limite_max FLOAT,

    categoria VARCHAR(100),

    tipo_operacional VARCHAR(100)
)

""")

# =====================================================
# COLLECTION POINTS
# =====================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS collection_points (

    id SERIAL PRIMARY KEY,

    nome VARCHAR(200),

    setor VARCHAR(200),

    planta VARCHAR(200),

    tipo VARCHAR(100)
)

""")

# =====================================================
# COLLECTIONS
# =====================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS collections (

    id SERIAL PRIMARY KEY,

    data_coleta DATE,

    hora_coleta TIME,

    ponto VARCHAR(200),

    operador VARCHAR(200),

    status VARCHAR(100),

    resultados JSONB
)

""")

conn.commit()

cursor.close()

conn.close()

print("Tabelas criadas com sucesso.")