from database.connection import engine


try:

    connection = engine.connect()

    print("✅ PostgreSQL conectado com sucesso!")

    connection.close()

except Exception as e:

    print("❌ Erro ao conectar:")
    print(e)