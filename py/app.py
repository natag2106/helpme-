from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import os
import hashlib
from flask_mail import Mail, Message
from datetime import datetime, timedelta
import secrets
from dotenv import load_dotenv
import random
from flask import render_template
import requests
#from sqlalchemy import create_engine
#engine = create_engine("mysql+pymysql://root:@localhost/votaciones", pool_size=10, max_overflow=20)
def obtener_ubicacion(ip):
    try:
        response = requests.get(f'https://ipapi.co/{ip}/json/')
        if response.status_code == 200:
            datos = response.json()
            ciudad = datos.get('city', 'Desconocida')
            region = datos.get('region', 'Desconocida')
            pais = datos.get('country_name', 'Desconocido')
            return f"{ciudad}, {region}, {pais}"
        else:
            return "Ubicación no disponible"
    except Exception as e:
        print("Error al obtener ubicación:", e)
        return "Ubicación no disponible"



load_dotenv()





app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')

CORS(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_DEFAULT_SENDER'] = ('Sistema de información', 'no-responder@helpme.co')
admin_email = os.getenv('ADMIN_EMAIL')

mail = Mail(app)

def generar_token_numerico():
    bloques = [str(random.randint(100, 999)) for _ in range(3)]
    return '-'.join(bloques)

token = generar_token_numerico()

def get_connection():
    return pymysql.connect(host='localhost', user='root', passwd='', db='helpme')


@app.route('/registro-psicologo', methods=['POST'])
def registro_psicologo():
    data = request.json
    nombre=data["nombre"].strip().lower()
    tarjeta=data["Tarjeta"].strip()
    especialidad=data["especialidad"].strip().lower()
    correo = data['correo'].strip().lower()
    contrasena = data['contrasena'].strip()
    contrasena_cifrada = hashlib.sha256(contrasena.encode()).hexdigest()
    print(f"Recibiendo datos - Correo: {correo}, Contraseña: {contrasena_cifrada}")

    conexion = get_connection()
    cursor = conexion.cursor()

    try:
        cursor.execute("SELECT * FROM psicologos WHERE email = %s", (correo,))
        if cursor.fetchone():
            return jsonify({"status": "error", "mensaje": "Correo ya registrado"}), 400
        

        cursor.execute("INSERT INTO psicologos (email, password, nombre, tarjeta_profesional, especialidad) VALUES (%s, %s, %s, %s, %s)", (correo, contrasena_cifrada, nombre, tarjeta, especialidad))
        conexion.commit()
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 40px auto;
                    background-color: #ffffff;
                    border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    overflow: hidden;
                    padding: 30px;
                    text-align: center;
                }}
                .logo {{
                    width: 120px;
                    margin: 0 auto 20px;
                }}
                .logo img {{
                    width: 100%;
                }}
                h2 {{
                    color: #333;
                }}
                p {{
                    color: #666;
                    font-size: 16px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>¡Bienvenido Doctor/a a la app HelpMe!</h2>
                <p>Tu registro se ha completado con éxito.</p>
                <p>Ahora puedes iniciar sesión y empezar con la atención de pacientes.</p>
                <p><strong>Correo registrado:</strong> {correo}</p>
            </div>
        </body>
        </html>
        """
        mensaje = Message(subject="Registro exitoso en la app de HelpMe", recipients=[correo], html=html)
        mail.send(mensaje)
        return jsonify({"status": "ok", "mensaje": "Usuario registrado"})

    except Exception as e:
        return jsonify({"status": "error", "mensaje": f"Error al registrar usuario: {str(e)}"}), 500

    finally:
        cursor.close()
        conexion.close()

@app.route('/registro-paciente', methods=['POST'])
def registro_paciente():
    data = request.json
    nombre = data["nombre"]
    correo = data['email'].strip().lower()
    contrasena = data['password'].strip()
    contrasena_cifrada = hashlib.sha256(contrasena.encode()).hexdigest()
    print(f"Recibiendo datos - Correo: {correo}, Contraseña: {contrasena_cifrada}")

    conexion = get_connection()
    cursor = conexion.cursor()

    try:
        cursor.execute("SELECT * FROM pacientes WHERE email = %s", (correo,))
        if cursor.fetchone():
            return jsonify({"status": "error", "mensaje": "Correo ya registrado"}), 400
        

        cursor.execute("INSERT INTO pacientes (email, password, nombre) VALUES (%s, %s, %s)", (correo, contrasena_cifrada, nombre))
        conexion.commit()
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 40px auto;
                    background-color: #ffffff;
                    border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    overflow: hidden;
                    padding: 30px;
                    text-align: center;
                }}
                .logo {{
                    width: 120px;
                    margin: 0 auto 20px;
                }}
                .logo img {{
                    width: 100%;
                }}
                h2 {{
                    color: #333;
                }}
                p {{
                    color: #666;
                    font-size: 16px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>¡Bienvenido a la app HelpMe!</h2>
                <p>Tu registro se ha completado con éxito.</p>
                <p>Ahora puedes iniciar sesión y elegir a tu psicologo de preferencia.</p>
                <p><strong>Correo registrado:</strong> {correo}</p>
            </div>
        </body>
        </html>
        """
        mensaje = Message(subject="Registro exitoso en la app de HelpMe", recipients=[correo], html=html)
        mail.send(mensaje)
        return jsonify({"status": "ok", "mensaje": "Usuario registrado"})

    except Exception as e:
        return jsonify({"status": "error", "mensaje": f"Error al registrar usuario: {str(e)}"}), 500

    finally:
        cursor.close()
        conexion.close()

@app.route('/login-usuario', methods=['POST'])
def login_usuario():
    data = request.json
    correo = data['email'].strip()
    contrasena = data['password'].strip()
    contrasena_cifrada = hashlib.sha256(contrasena.encode()).hexdigest()

    conexion = get_connection()
    cursor = conexion.cursor()

    try:
        cursor.execute("SELECT id, password FROM pacientes WHERE email=%s", (correo,))
        usuario = cursor.fetchone()

        if usuario and usuario[1] == contrasena_cifrada:
            usuario_id = usuario[0]
            ip = request.remote_addr
            user_agent = request.headers.get('User-Agent')
            fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ubicacion = obtener_ubicacion(ip)
            cursor.execute("""
                INSERT INTO logins (paciente_id, ip, ubicacion, navegador, fecha)
                VALUES (%s, %s, %s, %s, %s)
            """, (usuario_id, ip, ubicacion, user_agent, fecha))
            conexion.commit()
            msg = Message(
                subject="Nuevo inicio de sesión detectado",
                recipients=[correo],
                body=f"""Hola,

Se ha iniciado sesión en tu cuenta de HelpMe.

📍 IP: {ip}
🌐 Ubicación: {ubicacion}
🖥️ Navegador: {user_agent}
🕒 Fecha y hora: {fecha}

Si fuiste tú, no necesitas hacer nada. Si no reconoces esta actividad, cambia tu contraseña o contacta con el administrador.

Sistema de HelpMe"""
            )
            try:
                mail.send(msg)
            except Exception as e:
                print("Error al enviar correo de inicio de sesión:", e)

            return jsonify({"status": "ok", "paciente_id": usuario_id})

        
        elif usuario:
            return jsonify({"status": "error", "mensaje": "Contraseña incorrecta"}), 401
        else:
            return jsonify({"status": "error", "mensaje": "Correo no encontrado"}), 404

    except Exception as e:
        return jsonify({"status": "error", "mensaje": f"Error en el servidor: {str(e)}"}), 500

    finally:
        cursor.close()
        conexion.close()


@app.route('/login-psicologo', methods=['POST'])
def login_psicologo():
    data = request.json
    correo = data['email'].strip()
    contrasena = data['password'].strip()
    contrasena_cifrada = hashlib.sha256(contrasena.encode()).hexdigest()

    conexion = get_connection()
    cursor = conexion.cursor()

    try:
        cursor.execute("SELECT id, password FROM psicologos WHERE email=%s", (correo,))
        usuario = cursor.fetchone()

        if usuario and usuario[1] == contrasena_cifrada:
            usuario_id = usuario[0]
            ip = request.remote_addr
            user_agent = request.headers.get('User-Agent')
            fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ubicacion = obtener_ubicacion(ip)

            cursor.execute("""
                INSERT INTO login_psicologo (psicologo_id, ip, ubicacion, navegador, fecha)
                VALUES (%s, %s, %s, %s, %s)
            """, (usuario_id, ip, ubicacion, user_agent, fecha))
            conexion.commit()

            # Opcional: envío de correo
            try:
                msg = Message(
                    subject="Nuevo inicio de sesión detectado",
                    recipients=[correo],
                    body=f"""Hola,

Se ha iniciado sesión en tu cuenta de HelpMe.

📍 IP: {ip}
🌐 Ubicación: {ubicacion}
🖥️ Navegador: {user_agent}
🕒 Fecha y hora: {fecha}

Si fuiste tú, no necesitas hacer nada. Si no reconoces esta actividad, cambia tu contraseña o contacta con el administrador.
"""
                )
                mail.send(msg)
            except Exception as e:
                print("Error al enviar correo de inicio de sesión:", e)

            return jsonify({"status": "ok", "usuario_id": usuario_id})
        
        elif usuario:
            return jsonify({"status": "error", "mensaje": "Contraseña incorrecta"}), 401
        else:
            return jsonify({"status": "error", "mensaje": "Correo no encontrado"}), 404

    except Exception as e:
        return jsonify({"status": "error", "mensaje": f"Error en el servidor: {str(e)}"}), 500

    finally:
        cursor.close()
        conexion.close()
@app.route('/obtener_psicologos', methods=['GET'])
def obtener_psicologos():
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, especialidad FROM psicologos")
    psicologos = cursor.fetchall()
    conexion.close()
    lista_psicologos = []
    for p in psicologos:
        lista_psicologos.append({
            'id': p[0],
            'nombre': p[1],
            'especialidad': p[2]
        })
    
    return jsonify({'status': 'ok', 'psicologos': lista_psicologos})

@app.route('/reservar', methods=['POST'])
def reservar():
    data = request.json
    pacientes_id = data.get('pacientes_id')
    psicologo_id = data.get('psicologo_id')
    fecha = data.get('fecha')
    hora = data.get('hora')
    tema = data.get('tema', '').strip()

    # Validación de datos
    if not all([pacientes_id, psicologo_id, fecha, hora, tema]):
        return jsonify({"status": "error", "mensaje": "Faltan datos obligatorios"}), 400

    conexion = get_connection()
    cursor = conexion.cursor()

    try:
        # Verificar existencia de paciente
        cursor.execute("SELECT nombre, email FROM pacientes WHERE id = %s", (pacientes_id,))
        paciente = cursor.fetchone()

        # Verificar existencia de psicólogo
        cursor.execute("SELECT nombre, email FROM psicologos WHERE id = %s", (psicologo_id,))
        psicologo = cursor.fetchone()

        if not paciente or not psicologo:
            return jsonify({"status": "error", "mensaje": "Paciente o psicólogo no encontrado"}), 404

        # Verificar si el psicólogo ya tiene una reserva en ese horario
        cursor.execute("""
            SELECT COUNT(*) FROM reservas
            WHERE psicologo_id = %s AND fecha = %s AND hora = %s
        """, (psicologo_id, fecha, hora))

        if cursor.fetchone()[0] > 0:
            return jsonify({"status": "error", "mensaje": "Ese horario ya está ocupado"}), 409

        # Registrar nueva reserva
        cursor.execute("""
            INSERT INTO reservas (pacientes_id, psicologo_id, fecha, hora, tema, estado)
            VALUES (%s, %s, %s, %s, %s, 'pendiente')
        """, (pacientes_id, psicologo_id, fecha, hora, tema))
        conexion.commit()

        reserva_id = cursor.lastrowid

        # Datos del paciente y psicólogo
        nombre_paciente, correo_paciente = paciente
        nombre_psicologo, correo_psicologo = psicologo

        # Crear correos
        msg_paciente = Message(
            subject="✅ Confirmación de reserva - HelpMe",
            recipients=[correo_paciente],
            body=f"""Hola {nombre_paciente},

Tu reserva ha sido registrada exitosamente en HelpMe.

🧠 Psicólogo asignado: {nombre_psicologo}
📅 Fecha: {fecha}
⏰ Hora: {hora}
📝 Tema: {tema}

Por favor, conéctate puntualmente en la fecha indicada.

— Sistema HelpMe
"""
        )

        msg_psicologo = Message(
            subject="📩 Nueva reserva asignada - HelpMe",
            recipients=[correo_psicologo],
            body=f"""Hola {nombre_psicologo},

Tienes una nueva reserva asignada por el paciente {nombre_paciente}.

📅 Fecha: {fecha}
⏰ Hora: {hora}
📝 Tema: {tema}

Revisa tu panel de HelpMe para más información.

— Sistema HelpMe
"""
        )
        try:
            mail.send(msg_paciente)
            mail.send(msg_psicologo)
        except Exception as e:
            print("⚠️ Error al enviar correos:", e)

        return jsonify({
            "status": "ok",
            "mensaje": "Reserva creada y correos enviados correctamente",
            "reserva_id": reserva_id
        })

    except Exception as e:
        print("❌ Error al registrar reserva:", e)
        return jsonify({"status": "error", "mensaje": f"Error en servidor: {str(e)}"}), 500
    finally:
        cursor.close()
        conexion.close()


@app.route('/validar_usuario', methods=['POST'])
def validar_usuario():
    data = request.json
    usuario_id = data.get('paciente_id')

    conexion = get_connection()
    cursor = conexion.cursor()

    try:
        cursor.execute("SELECT id FROM pacientes WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()

        if usuario:
            return jsonify({"status": "ok", "mensaje": "Usuario válido"})
        else:
            return jsonify({"status": "error", "mensaje": "Usuario inválido"}), 401

    except Exception as e:
        return jsonify({"status": "error", "mensaje": f"Error en validación: {str(e)}"}), 500
    finally:
        cursor.close()
        conexion.close()
@app.route('/obtener_usuario', methods=['POST'])
def obtener_usuario():
    data = request.json
    usuario_id = data.get('paciente_id')

    conexion = get_connection()
    cursor = conexion.cursor()

    try:
        cursor.execute("SELECT nombre FROM pacientes WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()

        if usuario:
            return jsonify({"status": "ok", "nombre": usuario[0]})
        else:
            return jsonify({"status": "error", "mensaje": "Usuario no encontrado"}), 404

    except Exception as e:
        return jsonify({"status": "error", "mensaje": f"Error al obtener usuario: {str(e)}"}), 500
    finally:
        cursor.close()
        conexion.close() 

@app.route('/validar_usuario_psicologo', methods=['POST'])
def validar_usuario_psicologo():
    data = request.json
    psicologo_id = data.get('psicologo_id')

    conexion = get_connection()
    cursor = conexion.cursor()

    try:
        cursor.execute("SELECT id FROM psicologos WHERE id = %s", (psicologo_id,))
        usuario = cursor.fetchone()

        if usuario:
            return jsonify({"status": "ok", "mensaje": "Psicólogo válido"})
        else:
            return jsonify({"status": "error", "mensaje": "Psicólogo inválido"}), 401

    except Exception as e:
        return jsonify({"status": "error", "mensaje": f"Error en validación: {str(e)}"}), 500
    finally:
        cursor.close()
        conexion.close()


@app.route('/obtener_usuario_psicologo', methods=['POST'])
def obtener_usuario_psicologo():
    data = request.json
    psicologo_id = data.get('psicologo_id')

    conexion = get_connection()
    cursor = conexion.cursor()

    try:
        cursor.execute("SELECT nombre FROM psicologos WHERE id = %s", (psicologo_id,))
        usuario = cursor.fetchone()

        if usuario:
            return jsonify({"status": "ok", "nombre": usuario[0]})
        else:
            return jsonify({"status": "error", "mensaje": "Psicólogo no encontrado"}), 404

    except Exception as e:
        return jsonify({"status": "error", "mensaje": f"Error al obtener psicólogo: {str(e)}"}), 500
    finally:
        cursor.close()
        conexion.close()


@app.route('/recuperar_contrasena', methods=['GET', 'POST'])
def recuperar_contrasena():
    if request.method == 'GET':

        return render_template('recuperar_contrasena.html')
    try:
        data = request.json
        print("Datos recibidos:", data)
        if not data:
            return jsonify({"mensaje": "Datos no proporcionados"}), 400

        correo = data.get("correo")
        token = data.get("token")
        nueva_contrasena = data.get("nueva_contrasena")
        nueva_contrasena_cifrada = hashlib.sha256(nueva_contrasena.encode()).hexdigest()
        if not correo or not token or not nueva_contrasena:
            return jsonify({"mensaje": "Faltan datos requeridos"}), 400

        conexion = get_connection()
        cursor = conexion.cursor()

        print(f"Token recibido: '{token}'")
        cursor.execute("""
            SELECT id FROM tokens_recuperacion 
            WHERE correo = %s AND token = %s AND expiracion > NOW()
        """, (correo, token))
        resultado = cursor.fetchone()

        if resultado is None:
            return jsonify({"mensaje": "Token inválido o expirado"}), 400

        cursor.execute("""
            UPDATE usuarios SET contrasena = %s WHERE correo = %s
        """, (nueva_contrasena_cifrada, correo))

        cursor.execute("""
            DELETE FROM tokens_recuperacion WHERE correo = %s
        """, (correo,))

        conexion.commit()

        msg = Message(
            subject="Tu contraseña ha sido restablecida",
            recipients=[correo],
            body=f"Hola,\n\nTu contraseña ha sido restablecida exitosamente. Si no solicitaste este cambio, por favor contacta con el administrador.\n\nGracias.\nSistema de Votación Estudiantil"
        )
        mail.send(msg)

        return jsonify({"mensaje": "Contraseña restablecida exitosamente"}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"mensaje": "Error interno en el servidor"}), 500

    finally:
        try:
            cursor.close()
            conexion.close()
        except:
            pass

@app.route('/solicitud_cambio', methods=['POST'])
def solicitud_cambio():
    
    if not request.is_json:
        return jsonify({"status": "error", "mensaje": "El contenido debe ser JSON"}), 400

    data = request.get_json()
    
    
    if not data:
        return jsonify({"status": "error", "mensaje": "No se recibieron datos"}), 400

    nombre = data.get('nombre', '').strip()
    email = data.get('email', '').strip().lower()
    mensaje = data.get('mensaje', '').strip()
    asunto= data.get('asunto', '').strip()
    if not nombre or not email or not mensaje:
        return jsonify({"status": "error", "mensaje": "Faltan datos requeridos"}), 400

    conexion = get_connection()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            "INSERT INTO solicitudes (nombre, email, mensaje, asunto, fecha) VALUES (%s, %s, %s, NOW())",
            (nombre, email, mensaje, asunto)
        )
        conexion.commit()
        solicitud_id = cursor.lastrowid

        msg_usuario = Message(
            subject="Confirmación de solicitud",
            recipients=[email],
            body=f"""Hola {nombre},

Gracias por tu solicitud. Hemos recibido tu solicitud con el siguiente ID: {solicitud_id}.
Nuestro equipo estará revisando tu solicitud en breve.

Descripción de tu mensaje:
{mensaje}

Atentamente,
El equipo de soporte
"""
        )
        mail.send(msg_usuario)
        admin_email = os.getenv('ADMIN_EMAIL')
        if admin_email:
            msg_admin = Message(
                subject="Nueva Solicitud recibida",
                recipients=[admin_email],
                body=f"""Nueva Solicitud recibida:

ID de la solicitud: {solicitud_id}
Nombre: {nombre}
Correo: {email}
Mensaje:
{mensaje}

Estado: Pendiente.
"""
            )
            mail.send(msg_admin)

        return jsonify({
            "status": "ok",
            "mensaje": "Solicitud guardada y correos enviados",
            "ticket_id": solicitud_id
        })

    except Exception as e:
        print(f"Error en backend: {e}")
        return jsonify({"status": "error", "mensaje": "Error interno del servidor"}), 500
    finally:
        cursor.close()
        conexion.close()

@app.route('/solicitar_recuperacion', methods=['POST'])
def solicitar_recuperacion():
    data = request.json
    correo = data.get('correo','').strip().lower()
    print(data, correo)
    conexion = get_connection()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
    SELECT id, 'paciente' AS tipo FROM pacientes WHERE email = %s
    UNION ALL
    SELECT id, 'psicologo' AS tipo FROM psicologos WHERE email = %s
""", (correo, correo))

        usuario = cursor.fetchone()
        if not usuario:
            return jsonify({"status": "error", "mensaje": "Correo no registrado"}), 404

        
        una_hora_atras = datetime.now() - timedelta(hours=1)
        cursor.execute("""
            SELECT COUNT(*) FROM tokens_recuperacion 
            WHERE correo = %s AND fecha_creacion > %s
        """, (correo, una_hora_atras))
        cantidad = cursor.fetchone()[0]

        if cantidad >= 3:
            return jsonify({"status": "error", "mensaje": "Límite de solicitudes de recuperación alcanzado. Intenta más tarde."}), 429

        token = generar_token_numerico()
        expiracion = datetime.now() + timedelta(minutes=15)

        cursor.execute("INSERT INTO tokens_recuperacion (correo, token, expiracion, fecha_creacion) VALUES (%s, %s, %s, %s)",
                    (correo, token, expiracion, datetime.now()))
        conexion.commit()

        msg = Message("Recuperación de contraseña", recipients=[correo])
        msg.body = f"""
Hola,

Tu token de recuperación de contraseña es: {token}

Este token es válido por 15 minutos. Si no solicitaste este código, ignora este mensaje.

Atentamente,
Sistema de Votación Estudiantil
"""

        mail.send(msg)

        return jsonify({"status": "ok", "mensaje": "Token enviado al correo"})

    except Exception as e:
        print("Error en recuperación:", e)
        return jsonify({"status": "error", "mensaje": f"Error al generar token: {str(e)}"}), 500
    finally:
        cursor.close()
        conexion.close()


# =========================
# 📩 RUTAS DEL SISTEMA DE MENSAJES
# =========================

@app.route('/chats', methods=['GET'])
def ver_chats():
    psicologo_id = request.args.get('psicologo_id', type=int)
    if not psicologo_id:
        return jsonify({'error': 'Falta el ID del psicólogo'}), 400

    db = get_connection()
    cursor = db.cursor(pymysql.cursors.DictCursor)

    cursor.execute("""
        SELECT 
            r.id AS chat_id,
            p.id AS paciente_id,
            p.nombre AS paciente_nombre
        FROM reservas r
        JOIN pacientes p ON r.pacientes_id = p.id
        WHERE r.psicologo_id = %s
        ORDER BY r.fecha DESC
    """, (psicologo_id,))

    chats = cursor.fetchall()

    cursor.close()
    db.close()
    return jsonify(chats)


@app.route('/enviar_mensaje', methods=['POST'])
def enviar_mensaje():
    data = request.get_json()

    id_psicologo = data.get('psicologo_id')
    id_paciente = data.get('paciente_id')
    mensaje = data.get('mensaje')

    # Verificación de datos
    if not id_psicologo or not id_paciente or not mensaje:
        return jsonify({'status': 'error', 'message': 'Faltan datos requeridos'}), 400

    try:
        db = get_connection()
        cursor = db.cursor()

        # Guardar el mensaje
        cursor.execute("""
            INSERT INTO mensajes (id_psicologo, id_paciente, remitente, mensaje)
            VALUES (%s, %s, %s, %s)
        """, (id_psicologo, id_paciente, 'psicologo', mensaje))

        db.commit()
        cursor.close()
        db.close()

        return jsonify({'status': 'ok', 'message': 'Mensaje enviado correctamente'})

    except Exception as e:
        print("Error al guardar el mensaje:", e)
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/obtener_mensajes/<int:paciente_id>', methods=['POST'])
def obtener_mensajes(paciente_id):
    try:
        data = request.get_json()
        psicologo_id = data.get('psicologo_id')

        print("🧠 paciente_id:", paciente_id)
        print("🧠 psicologo_id:", psicologo_id)

        if not psicologo_id:
            return jsonify({'status': 'error', 'message': 'Falta el ID del psicólogo'}), 400

        db = get_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""
            SELECT mensaje, remitente, fecha_envio
            FROM mensajes
            WHERE id_psicologo = %s AND id_paciente = %s
            ORDER BY fecha_envio ASC
        """, (psicologo_id, paciente_id))

        mensajes = cursor.fetchall()
        print("📨 mensajes encontrados:", len(mensajes))

        cursor.close()
        db.close()

        return jsonify({'status': 'ok', 'mensajes': mensajes})

    except Exception as e:
        print("❌ Error al obtener mensajes:", e)
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/obtener_reservas/<int:psicologo_id>')
def obtener_reservas(psicologo_id):
    try:
        db = get_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)

        # Traer solo las reservas del psicólogo logueado
        cursor.execute("""
            SELECT 
                r.id,
                r.fecha,
                r.hora,
                r.tema,
                r.estado,
                p.nombre AS paciente
            FROM reservas r
            JOIN pacientes p ON r.pacientes_id = p.id
            WHERE r.psicologo_id = %s
        """, (psicologo_id,))

        reservas = cursor.fetchall()
        cursor.close()
        db.close()

        # Transformar los datos al formato que necesita FullCalendar
        eventos = []
        for r in reservas:
            eventos.append({
                "title": f"Cita con {r['paciente']}",
                "start": f"{r['fecha']}T{r['hora']}",
                "extendedProps": {
                    "paciente": r['paciente'],
                    "notas": r['tema'],
                    "estado": r['estado']
                }
            })

        return jsonify(eventos)

    except Exception as e:
        print("Error al obtener reservas:", e)
        return jsonify({'status': 'error', 'message': str(e)}), 500


# =========================
# 📩 RUTAS DEL SISTEMA DE MENSAJES PACIENTES
# =========================

@app.route('/chats_paciente', methods=['GET'])
def ver_chats_paciente():
    paciente_id = request.args.get('paciente_id', type=int)
    if not paciente_id:
        return jsonify({'error': 'Falta el ID del paciente'}), 400

    db = get_connection()
    cursor = db.cursor(pymysql.cursors.DictCursor)

    cursor.execute("""
        SELECT r.id AS chat_id, ps.id AS psicologo_id, ps.nombre AS psicologo_nombre
        FROM reservas r
        JOIN psicologos ps ON r.psicologo_id = ps.id
        WHERE r.pacientes_id = %s
        ORDER BY r.fecha DESC
    """, (paciente_id,))

    chats = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(chats)


@app.route('/enviar_mensaje_paciente', methods=['POST'])
def enviar_mensaje_paciente():
    data = request.get_json()
    id_psicologo = data.get('psicologo_id')
    id_paciente = data.get('paciente_id')
    mensaje = data.get('mensaje')

    if not id_psicologo or not id_paciente or not mensaje:
        return jsonify({'status':'error','message':'Faltan datos'}),400

    try:
        db = get_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO mensajes (id_psicologo, id_paciente, remitente, mensaje)
            VALUES (%s, %s, %s, %s)
        """, (id_psicologo, id_paciente, 'paciente', mensaje))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({'status':'ok','message':'Mensaje enviado'})
    except Exception as e:
        return jsonify({'status':'error','message': str(e)}),500

@app.route('/obtener_mensajes_paciente/<int:psicologo_id>', methods=['POST'])
def obtener_mensajes_paciente(psicologo_id):
    data = request.get_json()
    paciente_id = data.get('paciente_id')
    if not paciente_id:
        return jsonify({'status':'error','message':'Falta el ID del paciente'}),400

    db = get_connection()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT mensaje, remitente, fecha_envio
        FROM mensajes
        WHERE id_psicologo=%s AND id_paciente=%s
        ORDER BY fecha_envio ASC
    """,(psicologo_id,paciente_id))
    mensajes = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify({'status':'ok','mensajes':mensajes})

@app.route('/obtener_reservas_paciente/<int:paciente_id>')
def obtener_reservas_paciente(paciente_id):
    db = get_connection()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT r.id, r.fecha, r.hora, r.tema, r.estado, ps.nombre AS psicologo
        FROM reservas r
        JOIN psicologos ps ON r.psicologo_id = ps.id
        WHERE r.pacientes_id = %s
    """,(paciente_id,))
    reservas = cursor.fetchall()
    cursor.close()
    db.close()

    eventos = []
    for r in reservas:
        eventos.append({
            "title": f"Cita con {r['psicologo']}",
            "start": f"{r['fecha']}T{r['hora']}",
            "extendedProps": {
                "psicologo": r['psicologo'],
                "notas": r['tema'],
                "estado": r['estado']
            }
        })
    return jsonify(eventos)



if __name__ == '__main__':
    app.run(debug=True)


