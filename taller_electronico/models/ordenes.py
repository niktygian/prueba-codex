from .db import get_db

ESTADOS = [
    "recibido",
    "diagnóstico",
    "esperando repuesto",
    "en reparación",
    "pruebas",
    "listo",
    "entregado",
]


def listar(filtro=None):
    db = get_db()
    base = """
        SELECT o.*, e.tipo_equipo, e.marca, e.modelo, c.nombre AS cliente_nombre
        FROM ordenes_reparacion o
        JOIN equipos e ON e.id = o.equipo_id
        JOIN clientes c ON c.id = e.cliente_id
    """
    if filtro:
        q = f"%{filtro}%"
        return db.execute(
            base
            + """
            WHERE c.nombre LIKE ? OR e.modelo LIKE ? OR o.falla_reportada LIKE ? OR CAST(o.id AS TEXT) LIKE ?
            ORDER BY o.id DESC
            """,
            (q, q, q, q),
        ).fetchall()
    return db.execute(base + " ORDER BY o.id DESC").fetchall()


def obtener(orden_id):
    return get_db().execute("SELECT * FROM ordenes_reparacion WHERE id=?", (orden_id,)).fetchone()


def crear(data):
    db = get_db()
    cur = db.execute(
        """
        INSERT INTO ordenes_reparacion
        (equipo_id, tecnico_asignado, estado, falla_reportada, diagnostico, solucion, precio_estimado, precio_final, fecha_entrega)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.get("equipo_id"),
            data.get("tecnico_asignado"),
            data.get("estado", "recibido"),
            data.get("falla_reportada"),
            data.get("diagnostico"),
            data.get("solucion"),
            data.get("precio_estimado") or None,
            data.get("precio_final") or None,
            data.get("fecha_entrega") or None,
        ),
    )
    db.commit()
    return cur.lastrowid


def actualizar(orden_id, data):
    db = get_db()
    db.execute(
        """
        UPDATE ordenes_reparacion
        SET tecnico_asignado=?, estado=?, falla_reportada=?, diagnostico=?, solucion=?,
            precio_estimado=?, precio_final=?, fecha_entrega=?
        WHERE id=?
        """,
        (
            data.get("tecnico_asignado"),
            data.get("estado"),
            data.get("falla_reportada"),
            data.get("diagnostico"),
            data.get("solucion"),
            data.get("precio_estimado") or None,
            data.get("precio_final") or None,
            data.get("fecha_entrega") or None,
            orden_id,
        ),
    )
    db.commit()


def estadisticas_dashboard():
    db = get_db()
    stats = {}
    stats["equipos_hoy"] = db.execute(
        "SELECT COUNT(*) AS total FROM ordenes_reparacion WHERE date(fecha_ingreso)=date('now')"
    ).fetchone()["total"]
    for estado_key in ["diagnóstico", "en reparación", "listo"]:
        label = estado_key.replace(" ", "_").replace("ó", "o")
        stats[label] = db.execute(
            "SELECT COUNT(*) AS total FROM ordenes_reparacion WHERE estado=?", (estado_key,)
        ).fetchone()["total"]
    stats["ingresos_mes"] = db.execute(
        """
        SELECT COALESCE(SUM(precio_final),0) AS total
        FROM ordenes_reparacion
        WHERE strftime('%Y-%m', fecha_ingreso)=strftime('%Y-%m','now')
        """
    ).fetchone()["total"]
    return stats
