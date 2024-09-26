from flask import Flask, render_template, request, jsonify
import ast
import openai
import mccabe
import io
import re
import json
from collections import Counter
import logging

# Inicializar la aplicación Flask
app = Flask(__name__)

# Configurar la API de OpenAI
openai.api_key = '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'

# Configurar logging para errores
logging.basicConfig(filename='app.log', level=logging.ERROR)

# -----------------------------------------
# Funciones del Tutor Virtual con gpt-4o-mini
# -----------------------------------------

# Función para generar la auditoría basada en la norma ISO 12207
def generar_auditoria_proceso_gpt(codigo_estudiante, file_extension):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un auditor de código especializado en la Norma ISO 12207 - Auditoría del Proceso (Revisión de Buenas Prácticas). Debes auditar el código proporcionado."
                },
                {
                    "role": "user",
                    "content": f"Aquí está el código que debes auditar: \n\n// Extensión del archivo: {file_extension}\n\n{codigo_estudiante}"
                }
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        logging.error(f"Error al generar auditoría de proceso con OpenAI GPT: {str(e)}")
        return f"Error al generar auditoría de proceso con OpenAI GPT: {str(e)}"


# Función para generar la auditoría basada en la norma ISO 27001
def generar_auditoria_seguridad_gpt(codigo_estudiante, file_extension):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un auditor de código especializado en la Norma ISO 27001 - Auditoría de Seguridad. Debes auditar el código proporcionado."
                },
                {
                    "role": "user",
                    "content": f"Aquí está el código que debes auditar: \n\n// Extensión del archivo: {file_extension}\n\n{codigo_estudiante}"
                }
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        logging.error(f"Error al generar auditoría de seguridad con OpenAI GPT: {str(e)}")
        return f"Error al generar auditoría de seguridad con OpenAI GPT: {str(e)}"


# Función para generar la auditoría basada en la norma ISO 25010
def generar_auditoria_calidad_gpt(codigo_estudiante, file_extension):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un auditor de código especializado en la Norma ISO 25010 - Auditoría de Calidad (Mantenibilidad, Eficiencia, Portabilidad). Debes auditar el código proporcionado."
                },
                {
                    "role": "user",
                    "content": f"Aquí está el código que debes auditar: \n\n// Extensión del archivo: {file_extension}\n\n{codigo_estudiante}"
                }
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        logging.error(f"Error al generar auditoría de calidad con OpenAI GPT: {str(e)}")
        return f"Error al generar auditoría de calidad con OpenAI GPT: {str(e)}"


# Función para generar la retroalimentación como tutor virtual
def generar_retroalimentacion_gpt(codigo_estudiante, file_extension):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un tutor de programación especializado en todos los lenguajes de programación. Debes realizar una retroalimentación del siguiente código, explicando su funcionamiento y haciendo preguntas evaluativas."
                },
                {
                    "role": "user",
                    "content": f"Aquí está el código que debes revisar y retroalimentar: \n\n// Extensión del archivo: {file_extension}\n\n{codigo_estudiante}"
                }
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        logging.error(f"Error al generar retroalimentación con OpenAI GPT: {str(e)}")
        return f"Error al generar retroalimentación con OpenAI GPT: {str(e)}"


# Función para generar preguntas evaluativas del código
def generar_preguntas_evaluativas_gpt(codigo_estudiante, file_extension):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un tutor de programación especializado en generar preguntas evaluativas sobre cualquier código. Debes generar preguntas sobre el código proporcionado."
                },
                {
                    "role": "user",
                    "content": f"Aquí está el código para el cual debes generar preguntas evaluativas: \n\n// Extensión del archivo: {file_extension}\n\n{codigo_estudiante}"
                }
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        logging.error(f"Error al generar preguntas evaluativas con OpenAI GPT: {str(e)}")
        return f"Error al generar preguntas evaluativas con OpenAI GPT: {str(e)}"


# -----------------------------------------
# Rutas de la Interfaz Web
# -----------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/procesar', methods=['POST'])
def procesar_codigo():
    try:
        # Aquí va el código para procesar la solicitud POST
        codigo_estudiante = request.form['codigo']
        file_extension = request.form['extension']
        # Realiza las auditorías con GPT-4 y devuelve los resultados
        auditoria_calidad = generar_auditoria_calidad_gpt(codigo_estudiante, file_extension)
        auditoria_seguridad = generar_auditoria_seguridad_gpt(codigo_estudiante, file_extension)
        auditoria_proceso = generar_auditoria_proceso_gpt(codigo_estudiante, file_extension)
        retroalimentacion_gpt = generar_retroalimentacion_gpt(codigo_estudiante, file_extension)
        preguntas_evaluativas_gpt = generar_preguntas_evaluativas_gpt(codigo_estudiante, file_extension)

        # Respuesta en JSON
        auditoria = {
            "codigo": codigo_estudiante,
            "auditoria_calidad": auditoria_calidad,
            "auditoria_seguridad": auditoria_seguridad,
            "auditoria_proceso": auditoria_proceso,
            "retroalimentacion": retroalimentacion_gpt,
            "preguntas_evaluativas": preguntas_evaluativas_gpt
        }

        return jsonify(auditoria)

    except Exception as e:
        logging.error(f"Error general en el procesamiento del código: {str(e)}")
        return jsonify({"error": "Error en el servidor. Revisa los logs para más detalles."}), 500


# Correr la aplicación
if __name__ == '__main__':
    app.run(debug=True)
