from .db import get_db


def listar(filtro=None):
    db = get_db()
    if filtro:
        q = f"%{filtro}%"
        return db.execute(
            """
            SELECT e.*, c.nombre as cliente_nombre
            FROM equipos e
            JOIN clientes c ON c.id = e.cliente_id
            WHERE c.nombre LIKE ? OR e.modelo LIKE ? OR e.numero_serie LIKE ? OR e.imei LIKE ?
            ORDER BY e.id DESC
            """,
            (q, q, q, q),
        ).fetchall()
    return db.execute(
        """
        SELECT e.*, c.nombre as cliente_nombre
        FROM equipos e JOIN clientes c ON c.id = e.cliente_id
        ORDER BY e.id DESC
        """
    ).fetchall()


def crear(data):
    db = get_db()
    cur = db.execute(
        """
        INSERT INTO equipos (cliente_id, tipo_equipo, marca, modelo, numero_serie, imei, accesorios, estado_fisico, observaciones)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.get("cliente_id"),
            data.get("tipo_equipo"),
            data.get("marca"),
            data.get("modelo"),
            data.get("numero_serie"),
            data.get("imei"),
            data.get("accesorios"),
            data.get("estado_fisico"),
            data.get("observaciones"),
        ),
    )
    db.commit()
    return cur.lastrowid


def obtener(equipo_id):
    return get_db().execute("SELECT * FROM equipos WHERE id = ?", (equipo_id,)).fetchone()
