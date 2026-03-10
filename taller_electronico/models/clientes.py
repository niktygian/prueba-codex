from .db import get_db


def listar(filtro=None):
    db = get_db()
    if filtro:
        q = f"%{filtro}%"
        return db.execute(
            """
            SELECT * FROM clientes
            WHERE nombre LIKE ? OR telefono LIKE ? OR email LIKE ?
            ORDER BY id DESC
            """,
            (q, q, q),
        ).fetchall()
    return db.execute("SELECT * FROM clientes ORDER BY id DESC").fetchall()


def obtener(cliente_id):
    return get_db().execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,)).fetchone()


def crear(data):
    db = get_db()
    cur = db.execute(
        """
        INSERT INTO clientes (nombre, telefono, whatsapp, email, direccion, observaciones)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            data.get("nombre"),
            data.get("telefono"),
            data.get("whatsapp"),
            data.get("email"),
            data.get("direccion"),
            data.get("observaciones"),
        ),
    )
    db.commit()
    return cur.lastrowid


def actualizar(cliente_id, data):
    db = get_db()
    db.execute(
        """
        UPDATE clientes
        SET nombre=?, telefono=?, whatsapp=?, email=?, direccion=?, observaciones=?
        WHERE id=?
        """,
        (
            data.get("nombre"),
            data.get("telefono"),
            data.get("whatsapp"),
            data.get("email"),
            data.get("direccion"),
            data.get("observaciones"),
            cliente_id,
        ),
    )
    db.commit()


def historial_reparaciones(cliente_id):
    return get_db().execute(
        """
        SELECT o.id as orden_id, o.fecha_ingreso, o.estado, o.falla_reportada, o.precio_final,
               e.tipo_equipo, e.marca, e.modelo
        FROM ordenes_reparacion o
        JOIN equipos e ON e.id = o.equipo_id
        WHERE e.cliente_id = ?
        ORDER BY o.fecha_ingreso DESC
        """,
        (cliente_id,),
    ).fetchall()
