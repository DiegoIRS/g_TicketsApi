#Sistema de Gestión de Eventos y Ventas de Tickets

import credenciales
from flask import Flask, jsonify, request
from datetime import datetime
from supabase import create_client, Client

app = Flask(__name__)

supabase: Client = create_client(credenciales.url, credenciales.key)

@app.route('/events', methods=['GET'])
def get_events():
    response = supabase.table("eventos").select("*").eq("bit_disponible", 1).execute()

    # Verifica si hay un atributo de 'data' y 'error' en la respuesta
    if hasattr(response, 'data') and response.data:
        return jsonify(response.data), 200
    elif hasattr(response, 'error') and response.error:
        return jsonify({'error': str(response.error)}), 500
    else:
        return jsonify({'error': 'Error desconocido'}), 500


@app.route('/event/<int:evento_id>', methods=['GET'])
def get_event(evento_id):
    # Obtener la información 
    evento_info = supabase.table("eventos").select("*").eq("evento_id", evento_id).execute()

    # Obtener detalles 
    evento_detalles = supabase.table("evento_detalles").select("*").eq("evento_id", evento_id).execute()

    # Comprobar si se obtuvo la información correctamente
    if hasattr(evento_info, 'data') and evento_info.data and hasattr(evento_detalles, 'data') and evento_detalles.data:
        # Juntamos la información del evento y sus detalles
        evento_completo = {
            'evento': evento_info.data,
            'detalles': evento_detalles.data
        }
        return jsonify(evento_completo), 200
    else:
        return jsonify({'error': 'No se pudo obtener la información del evento'}), 500
    
@app.route('/purchase', methods=['POST'])
def purchase_ticket():
    data = request.json
    cliente_id = data['cliente_id']
    evento_id = data['evento_id']
    monto_pagado = data['monto_pagado']

    # Verificar disponibilidad del evento
    evento = supabase.table("eventos").select("bit_disponible").eq("evento_id", evento_id).execute()
    if not evento.data or evento.data[0]['bit_disponible'] != 1:
        return jsonify({'error': 'Evento no disponible'}), 400

    # Verificar tickets disponibles y el precio
    detalles = supabase.table("evento_detalles").select("tickets_disponibles, evento_precio").eq("evento_id", evento_id).execute()
    if not detalles.data or detalles.data[0]['tickets_disponibles'] < 1:
        return jsonify({'error': 'No hay tickets disponibles'}), 400
    if detalles.data[0]['evento_precio'] != monto_pagado:
        return jsonify({'error': 'Monto pagado incorrecto'}), 400

    # Registrar la compra
    fecha_compra = datetime.now().strftime('%Y-%m-%d')
    nueva_compra = {
        'cliente_id': cliente_id,
        'evento_id': evento_id,
        'fecha_compra': fecha_compra
    }
    compra = supabase.table("cliente_compras").insert(nueva_compra).execute()

    # Verificar si la inserción fue exitosa
    if not (hasattr(compra, 'data') and compra.data):
        return jsonify({'error': 'Error al realizar la compra'}), 500

    # Actualizar cantidad de tickets disponibles
    nuevos_tickets_disponibles = detalles.data[0]['tickets_disponibles'] - 1
    supabase.table("evento_detalles").update({'tickets_disponibles': nuevos_tickets_disponibles}).eq("evento_id", evento_id).execute()

    # Actualizar bit_disponible si no hay más tickets
    if nuevos_tickets_disponibles == 0:
        supabase.table("eventos").update({'bit_disponible': 0}).eq("evento_id", evento_id).execute()

    return jsonify(compra.data), 201

@app.route('/orders/<int:cliente_id>', methods=['GET'])
def get_orders(cliente_id):
    # Realiza la consulta a la tabla cliente_compras
    response = supabase.table("cliente_compras").select("*").eq("cliente_id", cliente_id).execute()

    # Verifica si se obtuvieron datos
    if hasattr(response, 'data') and response.data:
        return jsonify(response.data), 200
    else:
        # Maneja el caso en que no se encuentren datos o haya un error
        return jsonify({'error': 'No se encontraron compras para el cliente especificado'}), 404

if __name__ == '__main__':
    app.run(debug=True)
