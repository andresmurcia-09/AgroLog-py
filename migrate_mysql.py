from app.infrastructure.mysql.connection import get_mysql_connection
from datetime import datetime


def migrate_database():
    try:
        connection = get_mysql_connection()
        cursor = connection.cursor()

        # Crear tablas
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            apellido VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            hashed_password VARCHAR(100) NOT NULL,
            fecha_registro DATETIME NOT NULL,
            activo BOOLEAN NOT NULL DEFAULT TRUE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS parcelas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            ubicacion VARCHAR(200),
            superficie FLOAT,
            usuario_id INT NOT NULL,
            fecha_registro DATETIME NOT NULL,
            activo BOOLEAN NOT NULL DEFAULT TRUE,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cultivos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            variedad VARCHAR(100),
            fecha_siembra DATE,
            fecha_cosecha_estimada DATE,
            parcela_id INT NOT NULL,
            fecha_registro DATETIME NOT NULL,
            activo BOOLEAN NOT NULL DEFAULT TRUE,
            FOREIGN KEY (parcela_id) REFERENCES parcelas(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos_fitosanitarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            tipo VARCHAR(50) NOT NULL,
            fabricante VARCHAR(100),
            principio_activo VARCHAR(100),
            dosis_recomendada VARCHAR(100),
            periodo_carencia INT,
            usuario_id INT NOT NULL,
            fecha_registro DATETIME NOT NULL,
            activo BOOLEAN NOT NULL DEFAULT TRUE,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS aplicaciones (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fecha_aplicacion DATE NOT NULL,
            producto_id INT NOT NULL,
            cultivo_id INT NOT NULL,
            dosis_aplicada FLOAT NOT NULL,
            unidad_medida VARCHAR(20) NOT NULL,
            area_tratada FLOAT,
            motivo VARCHAR(200),
            observaciones TEXT,
            fecha_segura_reingreso DATE,
            usuario_id INT NOT NULL,
            fecha_registro DATETIME NOT NULL,
            FOREIGN KEY (producto_id) REFERENCES productos_fitosanitarios(id),
            FOREIGN KEY (cultivo_id) REFERENCES cultivos(id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS recordatorios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            aplicacion_id INT NOT NULL,
            fecha_recordatorio DATE NOT NULL,
            tipo VARCHAR(50) NOT NULL,
            mensaje VARCHAR(200) NOT NULL,
            completado BOOLEAN NOT NULL DEFAULT FALSE,
            fecha_registro DATETIME NOT NULL,
            FOREIGN KEY (aplicacion_id) REFERENCES aplicaciones(id)
        )
        """)

        # Insertar usuario admin por defecto si no existe
        cursor.execute("SELECT COUNT(*) as count FROM usuarios")
        result = cursor.fetchone()
        if result['count'] == 0:
            hashed_password = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # password: password
            cursor.execute("""
            INSERT INTO usuarios (nombre, apellido, email, hashed_password, fecha_registro, activo)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, ("Admin", "Usuario", "admin@example.com", hashed_password, datetime.now(), True))

        connection.commit()
        cursor.close()
        connection.close()

        print("Migración completada exitosamente")
        return True

    except Exception as e:
        print(f"Error durante la migración: {e}")
        return False


if __name__ == "__main__":
    print("Iniciando migración de la base de datos...")
    migrate_database()