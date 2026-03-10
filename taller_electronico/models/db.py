import os
import sqlite3
from flask import g

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "taller.db")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_schema():
    db = sqlite3.connect(DB_PATH)
    db.execute("PRAGMA foreign_keys = ON")
    db.executescript(
        """


        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            rol TEXT NOT NULL DEFAULT 'tecnico',
            activo INTEGER NOT NULL DEFAULT 1,
            fecha_alta TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT,
            whatsapp TEXT,
            email TEXT,
            direccion TEXT,
            observaciones TEXT,
            fecha_alta TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS equipos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            tipo_equipo TEXT NOT NULL,
            marca TEXT,
            modelo TEXT,
            numero_serie TEXT,
            imei TEXT,
            accesorios TEXT,
            estado_fisico TEXT,
            observaciones TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS ordenes_reparacion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipo_id INTEGER NOT NULL,
            fecha_ingreso TEXT NOT NULL DEFAULT (datetime('now')),
            tecnico_asignado TEXT,
            estado TEXT NOT NULL DEFAULT 'recibido',
            falla_reportada TEXT,
            diagnostico TEXT,
            solucion TEXT,
            precio_estimado REAL,
            precio_final REAL,
            fecha_entrega TEXT,
            FOREIGN KEY (equipo_id) REFERENCES equipos(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS diagnosticos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            orden_id INTEGER NOT NULL,
            prueba_realizada TEXT NOT NULL,
            resultado TEXT,
            tecnico TEXT,
            fecha TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (orden_id) REFERENCES ordenes_reparacion(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS mediciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            orden_id INTEGER NOT NULL,
            punto_prueba TEXT NOT NULL,
            tipo_medicion TEXT NOT NULL,
            valor REAL,
            unidad TEXT,
            observaciones TEXT,
            FOREIGN KEY (orden_id) REFERENCES ordenes_reparacion(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS componentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo TEXT,
            encapsulado TEXT,
            descripcion TEXT,
            codigo_smd TEXT,
            datasheet TEXT
        );

        CREATE TABLE IF NOT EXISTS inventario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            componente_id INTEGER NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            ubicacion TEXT,
            precio_compra REAL,
            proveedor TEXT,
            stock_minimo INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (componente_id) REFERENCES componentes(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS orden_componentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            orden_id INTEGER NOT NULL,
            inventario_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL CHECK(cantidad > 0),
            fecha_uso TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (orden_id) REFERENCES ordenes_reparacion(id) ON DELETE CASCADE,
            FOREIGN KEY (inventario_id) REFERENCES inventario(id) ON DELETE CASCADE
        );
        """
    )
    db.commit()
    db.close()
