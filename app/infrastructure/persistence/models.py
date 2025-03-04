from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Text, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.infrastructure.persistence.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(100), nullable=False)
    fecha_registro = Column(DateTime, default=func.now(), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)

    parcelas = relationship("Parcela", back_populates="usuario", cascade="all, delete-orphan")
    productos = relationship("ProductoFitosanitario", back_populates="usuario", cascade="all, delete-orphan")
    aplicaciones = relationship("Aplicacion", back_populates="usuario", cascade="all, delete-orphan")


class Parcela(Base):
    __tablename__ = "parcelas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    ubicacion = Column(String(200))
    superficie = Column(Float)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha_registro = Column(DateTime, default=func.now(), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)

    usuario = relationship("Usuario", back_populates="parcelas")
    cultivos = relationship("Cultivo", back_populates="parcela", cascade="all, delete-orphan")


class Cultivo(Base):
    __tablename__ = "cultivos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    variedad = Column(String(100))
    fecha_siembra = Column(Date)
    fecha_cosecha_estimada = Column(Date)
    parcela_id = Column(Integer, ForeignKey("parcelas.id"), nullable=False)
    fecha_registro = Column(DateTime, default=func.now(), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)

    parcela = relationship("Parcela", back_populates="cultivos")
    aplicaciones = relationship("Aplicacion", back_populates="cultivo", cascade="all, delete-orphan")


class ProductoFitosanitario(Base):
    __tablename__ = "productos_fitosanitarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    tipo = Column(String(50), nullable=False)
    fabricante = Column(String(100))
    principio_activo = Column(String(100))
    dosis_recomendada = Column(String(100))
    periodo_carencia = Column(Integer)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha_registro = Column(DateTime, default=func.now(), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)

    usuario = relationship("Usuario", back_populates="productos")
    aplicaciones = relationship("Aplicacion", back_populates="producto", cascade="all, delete-orphan")


class Aplicacion(Base):
    __tablename__ = "aplicaciones"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fecha_aplicacion = Column(Date, nullable=False)
    producto_id = Column(Integer, ForeignKey("productos_fitosanitarios.id"), nullable=False)
    cultivo_id = Column(Integer, ForeignKey("cultivos.id"), nullable=False)
    dosis_aplicada = Column(Float, nullable=False)
    unidad_medida = Column(String(20), nullable=False)
    area_tratada = Column(Float)
    motivo = Column(String(200))
    observaciones = Column(Text)
    fecha_segura_reingreso = Column(Date)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha_registro = Column(DateTime, default=func.now(), nullable=False)

    producto = relationship("ProductoFitosanitario", back_populates="aplicaciones")
    cultivo = relationship("Cultivo", back_populates="aplicaciones")
    usuario = relationship("Usuario", back_populates="aplicaciones")
    recordatorios = relationship("Recordatorio", back_populates="aplicacion", cascade="all, delete-orphan")


class Recordatorio(Base):
    __tablename__ = "recordatorios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    aplicacion_id = Column(Integer, ForeignKey("aplicaciones.id"), nullable=False)
    fecha_recordatorio = Column(Date, nullable=False)
    tipo = Column(String(50), nullable=False)
    mensaje = Column(String(200), nullable=False)
    completado = Column(Boolean, default=False, nullable=False)
    fecha_registro = Column(DateTime, default=func.now(), nullable=False)

    aplicacion = relationship("Aplicacion", back_populates="recordatorios")