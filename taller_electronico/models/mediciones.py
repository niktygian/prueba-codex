from .db import get_db


def listar_por_orden(orden_id):
    return get_db().execute(
        "SELECT * FROM mediciones WHERE orden_id=? ORDER BY id DESC", (orden_id,)
    ).fetchall()


def crear(data):
    db = get_db()
    db.execute(
        """
        INSERT INTO mediciones (orden_id, punto_prueba, tipo_medicion, valor, unidad, observaciones)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            data.get("orden_id"),
            data.get("punto_prueba"),
            data.get("tipo_medicion"),
            data.get("valor") or None,
            data.get("unidad"),
            data.get("observaciones"),
        ),
    )
    db.commit()
