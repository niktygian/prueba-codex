from flask import Blueprint, render_template, request, redirect, url_for
from models import clientes as clientes_model

bp = Blueprint("clientes", __name__, url_prefix="/clientes")


@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        clientes_model.crear(request.form)
        return redirect(url_for("clientes.index"))

    q = request.args.get("q")
    clientes = clientes_model.listar(q)
    return render_template("clientes.html", clientes=clientes, q=q or "")


@bp.route("/<int:cliente_id>/editar", methods=["GET", "POST"])
def editar(cliente_id):
    if request.method == "POST":
        clientes_model.actualizar(cliente_id, request.form)
        return redirect(url_for("clientes.index"))

    cliente = clientes_model.obtener(cliente_id)
    historial = clientes_model.historial_reparaciones(cliente_id)
    return render_template("clientes.html", cliente_editar=cliente, historial=historial, clientes=clientes_model.listar())
