from database.connection import SessionLocal

from database.models import (
    User,
    Tenant
)

from utils.security import hash_password


db = SessionLocal()


# =========================================================
# VERIFICA SE JÁ EXISTE ADMIN
# =========================================================

existing_admin = db.query(User).filter(
    User.email == "admin@admin.com"
).first()


if existing_admin:

    print("⚠️ Administrador já existe.")

else:

    # =====================================================
    # CRIA TENANT
    # =====================================================

    tenant = Tenant(
        empresa="Administrador Global",
        planta="Matriz"
    )

    db.add(tenant)

    db.commit()

    db.refresh(tenant)

    # =====================================================
    # CRIA ADMIN
    # =====================================================

    admin = User(
        nome="Administrador",
        email="admin@admin.com",
        senha=hash_password("123456"),
        role="master",
        tenant_id=tenant.id
    )

    db.add(admin)

    db.commit()

    print("✅ Administrador criado com sucesso.")


db.close()