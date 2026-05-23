from database.connection import engine
from database.models import Base


print("🚀 Criando tabelas...")


Base.metadata.create_all(bind=engine)


print("✅ Tabelas criadas com sucesso!")