from .db import get_db


def listar_por_orden(orden_id):
    return get_db().execute(
        "SELECT * FROM diagnosticos WHERE orden_id=? ORDER BY fecha DESC", (orden_id,)
    ).fetchall()


def crear(data):
    db = get_db()
    db.execute(
        """
        INSERT INTO diagnosticos (orden_id, prueba_realizada, resultado, tecnico)
        VALUES (?, ?, ?, ?)
        """,
        (data.get("orden_id"), data.get("prueba_realizada"), data.get("resultado"), data.get("tecnico")),
    )
    db.commit()
