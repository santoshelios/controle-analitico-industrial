from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    DateTime,
    Numeric
)

from sqlalchemy.orm import relationship

from datetime import datetime

from database.connection import Base


# =========================================================
# TENANTS
# =========================================================

class Tenant(Base):

    __tablename__ = "tenants"

    id = Column(
        Integer,
        primary_key=True
    )

    empresa = Column(
        String,
        nullable=False
    )

    planta = Column(
        String,
        nullable=False
    )

    status = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    users = relationship(
        "User",
        back_populates="tenant"
    )


# =========================================================
# USERS
# =========================================================

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True
    )

    nome = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    senha = Column(
        String,
        nullable=False
    )

    role = Column(
        String,
        nullable=False
    )

    tenant_id = Column(
        Integer,
        ForeignKey("tenants.id"),
        nullable=False
    )

    ativo = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    tenant = relationship(
        "Tenant",
        back_populates="users"
    )

# =========================================================
# PLANTS
# =========================================================

class Plant(Base):

    __tablename__ = "plants"

    id = Column(
        Integer,
        primary_key=True
    )

    nome = Column(
        String,
        nullable=False
    )

    tenant_id = Column(
        Integer,
        ForeignKey("tenants.id"),
        nullable=False
    )

    ativo = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    tenant = relationship("Tenant")

# =========================================================
# COLLECTION POINTS
# =========================================================

class CollectionPoint(Base):

    __tablename__ = "collection_points"

    id = Column(
        Integer,
        primary_key=True
    )

    nome = Column(
        String,
        nullable=False
    )

    descricao = Column(
        String
    )

    # Relaciona ponto à planta
    plant_id = Column(
        Integer,
        ForeignKey("plants.id"),
        nullable=False
    )

    ativo = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    plant = relationship("Plant")

# =========================================================
# PARAMETERS
# =========================================================

class Parameter(Base):

    __tablename__ = "parameters"

    id = Column(
        Integer,
        primary_key=True
    )

    # Nome do parâmetro
    nome = Column(
        String,
        nullable=False
    )

    # Unidade de medida
    unidade = Column(
        String,
        nullable=False
    )

    # Limite mínimo aceitável
    limite_min = Column(
        String
    )

    # Limite máximo aceitável
    limite_max = Column(
        String
    )

    # Quantidade de casas decimais
    casas_decimais = Column(
        Integer,
        default=2
    )

    ativo = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

# =========================================================
# COLLECTIONS
# =========================================================

class Collection(Base):

    __tablename__ = "collections"

    id = Column(
        Integer,
        primary_key=True
    )

    # Relaciona coleta à planta
    plant_id = Column(
        Integer,
        ForeignKey("plants.id"),
        nullable=False
    )

    # Relaciona coleta ao ponto
    collection_point_id = Column(
        Integer,
        ForeignKey("collection_points.id"),
        nullable=False
    )

    # Usuário responsável pela coleta
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    # Data e hora da coleta
    data_coleta = Column(
        DateTime,
        default=datetime.utcnow
    )

    # Observações gerais
    observacao = Column(
        String
    )

    # Status da coleta
    status = Column(
        String,
        default="concluida"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    plant = relationship("Plant")

    collection_point = relationship("CollectionPoint")

    user = relationship("User")

# =========================================================
# COLLECTION RESULTS
# =========================================================

class CollectionResult(Base):

    __tablename__ = "collection_results"

    id = Column(
        Integer,
        primary_key=True
    )

    # Relaciona resultado à coleta
    collection_id = Column(
        Integer,
        ForeignKey("collections.id"),
        nullable=False
    )

    # Relaciona resultado ao parâmetro
    parameter_id = Column(
        Integer,
        ForeignKey("parameters.id"),
        nullable=False
    )

    # Valor da análise
    valor = Column(
        Numeric(10, 2),
        nullable=False
    )

    # Indica conformidade automática
    conforme = Column(
        Boolean,
        default=True
    )

    # Observação específica do resultado
    observacao = Column(
        String
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    collection = relationship("Collection")

    parameter = relationship("Parameter")