from services.auth_service import authenticate_user


user = authenticate_user(
    email="admin@admin.com",
    password="123456"
)

if user:
    print("Login realizado com sucesso.")
    print(user.nome)
    print(user.role)

else:
    print("Usuário ou senha inválidos.")