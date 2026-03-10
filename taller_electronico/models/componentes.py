from .db import get_db


def listar_componentes(filtro=None):
    db = get_db()
    if filtro:
        q = f"%{filtro}%"
        return db.execute(
            """
            SELECT c.*, i.id as inventario_id, i.stock, i.ubicacion, i.precio_compra, i.proveedor, i.stock_minimo
            FROM componentes c
            LEFT JOIN inventario i ON i.componente_id=c.id
            WHERE c.nombre LIKE ? OR c.tipo LIKE ? OR c.codigo_smd LIKE ?
            ORDER BY c.id DESC
            """,
            (q, q, q),
        ).fetchall()
    return db.execute(
        """
        SELECT c.*, i.id as inventario_id, i.stock, i.ubicacion, i.precio_compra, i.proveedor, i.stock_minimo
        FROM componentes c LEFT JOIN inventario i ON i.componente_id=c.id
        ORDER BY c.id DESC
        """
    ).fetchall()


def crear_componente_y_stock(data):
    db = get_db()
    cur = db.execute(
        """
        INSERT INTO componentes (nombre, tipo, encapsulado, descripcion, codigo_smd, datasheet)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            data.get("nombre"),
            data.get("tipo"),
            data.get("encapsulado"),
            data.get("descripcion"),
            data.get("codigo_smd"),
            data.get("datasheet"),
        ),
    )
    componente_id = cur.lastrowid
    db.execute(
        """
        INSERT INTO inventario (componente_id, stock, ubicacion, precio_compra, proveedor, stock_minimo)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            componente_id,
            int(data.get("stock") or 0),
            data.get("ubicacion"),
            data.get("precio_compra") or 0,
            data.get("proveedor"),
            int(data.get("stock_minimo") or 0),
        ),
    )
    db.commit()


def alertas_stock_bajo():
    return get_db().execute(
        """
        SELECT c.nombre, i.stock, i.stock_minimo
        FROM inventario i JOIN componentes c ON c.id=i.componente_id
        WHERE i.stock <= i.stock_minimo
        ORDER BY i.stock ASC
        """
    ).fetchall()


def usar_componente_en_orden(orden_id, inventario_id, cantidad):
    db = get_db()
    cantidad = int(cantidad)
    item = db.execute("SELECT stock FROM inventario WHERE id=?", (inventario_id,)).fetchone()
    if not item:
        raise ValueError("Ítem de inventario no encontrado")
    if item["stock"] < cantidad:
        raise ValueError("Stock insuficiente")

    db.execute("UPDATE inventario SET stock = stock - ? WHERE id=?", (cantidad, inventario_id))
    db.execute(
        "INSERT INTO orden_componentes (orden_id, inventario_id, cantidad) VALUES (?, ?, ?)",
        (orden_id, inventario_id, cantidad),
    )
    db.commit()


def componentes_usados(orden_id):
    return get_db().execute(
        """
        SELECT oc.cantidad, oc.fecha_uso, c.nombre
        FROM orden_componentes oc
        JOIN inventario i ON i.id = oc.inventario_id
        JOIN componentes c ON c.id = i.componente_id
        WHERE oc.orden_id=?
        ORDER BY oc.fecha_uso DESC
        """,
        (orden_id,),
    ).fetchall()
