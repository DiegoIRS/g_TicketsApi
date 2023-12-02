# g_TicketsApi

Entrevista técnica - Backend
Evaluación técnica consiste en el desarrollo de un servicio, que debe exponer una API REST a través de HTTP utilizando JSON para el traspaso de mensajes.

Video Explicativo:
https://www.youtube.com/watch?v=a9GqvfMCPmk&ab_channel=DiegoRojas


1 http://127.0.0.1:5000/events
2 http://127.0.0.1:5000/event/1
3 http://localhost:5000/purchase

        Boby Post:
        {
            "cliente_id": 1,
            "evento_id": 1,
            "monto_pagado": 10000,
            "fecha_compra": "2023-04-01"
        }

4 http://localhost:5000/orders/1
                                        
 # Instalacion:  

Se requiere de estas bibliotecas:
    pip install Flask supabase-py datetime

**La base de datos en Supabase ya esta integrada mediante Tokens y se mantendra activa**

 # Ejecucion:  

 Solo se le da Play/F5/Run/ o ejecutar mediante el comando:  'python app.py' o 'py app.py'

        