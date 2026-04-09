from flask import Blueprint, render_template, request, redirect, url_for, flash
from database.db import db
from database.modelPagos import ModelPagos

pagos = Blueprint('pagos', __name__, url_prefix='/pagos')

@pagos.route('/factura/<int:id_reserva>', methods=['GET'])
def ver_factura(id_reserva):
    factura = ModelPagos.obtener_factura_exacta(db, id_reserva)
    return render_template('common/LogicaNegocios/Pagos/factura_electronica.html', factura=factura)

@pagos.route('/procesar_admin/<int:id_reserva>', methods=['POST'])
def procesar_admin(id_reserva):
    metodo = request.form.get('metodo_pago')
    if metodo == 'Tarjeta':
        return redirect(url_for('pagos.simulador_pago', id_reserva=id_reserva))
    else:
        return redirect(url_for('pagos.pagar_efectivo', id_reserva=id_reserva))

@pagos.route('/simulador/<int:id_reserva>', methods=['GET', 'POST'])
def simulador_pago(id_reserva):
    if request.method == 'POST':
        ModelPagos.registrar_pago_express(db, id_reserva, 'Tarjeta')
        flash("¡Facturación exitosa! El pago fue procesado.", "success")
        return redirect(url_for('pagos.ver_factura', id_reserva=id_reserva))
    return render_template('common/LogicaNegocios/Pagos/simulador_pago.html', id_reserva=id_reserva)

@pagos.route('/efectivo/<int:id_reserva>', methods=['GET', 'POST'])
def pagar_efectivo(id_reserva):
    if request.method == 'POST':
        ModelPagos.registrar_pago_express(db, id_reserva, 'Efectivo')
        flash("¡Facturación exitosa! El pago en efectivo fue registrado.", "success")
        return redirect(url_for('pagos.ver_factura', id_reserva=id_reserva))
    return render_template('common/LogicaNegocios/Pagos/pagar_efectivo.html', id_reserva=id_reserva)
