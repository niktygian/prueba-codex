from flask import Blueprint, render_template, request, redirect, url_for
from models import ordenes as ordenes_model
from models import equipos as equipos_model
from models import diagnosticos as diagnosticos_model
from models import mediciones as mediciones_model
from models import componentes as componentes_model

bp = Blueprint("ordenes", __name__, url_prefix="/ordenes")


@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ordenes_model.crear(request.form)
        return redirect(url_for("ordenes.index"))

    q = request.args.get("q")
    ordenes = ordenes_model.listar(q)
    equipos = equipos_model.listar()
    return render_template("ordenes.html", ordenes=ordenes, equipos=equipos, estados=ordenes_model.ESTADOS, q=q or "")


@bp.route("/<int:orden_id>", methods=["GET", "POST"])
def detalle(orden_id):
    orden = ordenes_model.obtener(orden_id)
    if request.method == "POST":
        accion = request.form.get("accion")
        if accion == "actualizar_orden":
            ordenes_model.actualizar(orden_id, request.form)
        elif accion == "agregar_diagnostico":
            diagnosticos_model.crear(request.form)
        elif accion == "agregar_medicion":
            mediciones_model.crear(request.form)
        elif accion == "usar_componente":
            componentes_model.usar_componente_en_orden(
                orden_id,
                request.form.get("inventario_id"),
                request.form.get("cantidad"),
            )
        return redirect(url_for("ordenes.detalle", orden_id=orden_id))

    diagnosticos = diagnosticos_model.listar_por_orden(orden_id)
    mediciones = mediciones_model.listar_por_orden(orden_id)
    inventario = componentes_model.listar_componentes()
    usados = componentes_model.componentes_usados(orden_id)
    return render_template(
        "diagnostico.html",
        orden=orden,
        diagnosticos=diagnosticos,
        mediciones=mediciones,
        inventario=inventario,
        usados=usados,
        estados=ordenes_model.ESTADOS,
    )
