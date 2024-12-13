from django.shortcuts import render

# Create your views here.
import os
from llama_index.llms.gemini import Gemini
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Configurar la clave de API
GOOGLE_API_KEY = "AIzaSyANKRunVr3c24k7LBNKhTAMuzurgEPqhK0"  # Coloca tu API Key aquí
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Inicializar el modelo Gemini
model = Gemini(model="models/gemini-1.5-flash", api_key=GOOGLE_API_KEY)






import os
from llama_index.llms.gemini import Gemini
import time

from llama_index.core.llms import ChatMessage

GOOGLE_API_KEY = "AIzaSyANKRunVr3c24k7LBNKhTAMuzurgEPqhK0"  # add your GOOGLE API key here
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

model = Gemini(model="models/gemini-1.5-flash", api_key=GOOGLE_API_KEY)
# Función para el Agente 1
def agente_1(lista_requerimientos,mensaje_estudiante):
    prompt = f"""
    Actúa como un agente asistente estratégico en el ámbito de los lenguajes humanos. Su principal rol es identificar posibles brechas de conocimiento en el dominio de los lenguajes, tales como patrones, similitudes o diferencias, que puedan indicar áreas donde se puede desarrollar nuevo conocimiento. El agente analiza los materiales de aprendizaje (mensajes, respuestas o comportamientos) para determinar áreas de exploración que puedan mejorar la comprensión.

    El agente no interactúa directamente con el estudiante, sino que evalúa los materiales de aprendizaje proporcionados (por ejemplo, ejemplos o términos discutidos) y sugiere una lista de opciones estratégicas para profundizar en el tema. Debe enfocarse en reconocer conexiones lógicas, patrones lingüísticos y resaltar áreas que puedan facilitar una experiencia de aprendizaje más profunda o llevar a la creación de nuevo conocimiento.

    Tarea:
    El agente *no debe* introducir temas que no estén relacionados con la conversación actual, sino que debe guiar al usuario a través de un proceso de aprendizaje estructurado e iterativo basado en la discusión existente. El objetivo es proporcionar información sobre fenómenos lingüísticos, como etimología, significados culturales, patrones de uso y roles gramaticales. El agente priorizará áreas que fomenten el aprendizaje reflexivo, la co-creación de conocimiento y el pensamiento crítico colaborativo.

    Contexto:
    Especificidad: Lenguas humanas, Tema: Expresiones locales. El agente debe guiar hacia un aprendizaje reflexivo, la co-creación de conocimiento y el pensamiento crítico colaborativo sugiriendo áreas de investigación más profunda.

    Formato:
    El resultado debe ser una lista priorizada de caminos de desarrollo en formato JSON. Cada opción debe centrarse en fomentar una comprensión más profunda del tema actual. El agente sugerirá caminos estructurados de aprendizaje, como explorar campos semánticos, estructuras sintácticas o variaciones culturales, basados en el contexto y lenguaje utilizado.

    Ejemplo de salida:
    [
    {{
        "tema": "Etimología de 'patacala'",
        "descripción": "Explorar los orígenes de la palabra 'patacala' y su evolución dentro del idioma, particularmente en relación con los dialectos regionales."
    }},
    {{
        "tema": "Variaciones culturales en el uso",
        "descripción": "Investigar cómo se usa 'patacala' en distintas regiones de habla hispana y su significado en la cultura de Arequipa."
    }},
    {{
        "tema": "Análisis gramatical de la frase",
        "descripción": "Examinar la sintaxis de 'el niño camina patacala' y 'el niño anda patacala', explicando las estructuras gramaticales involucradas."
    }}
    ]

    El mensaje recibido del estudiante es el siguiente:

    "Mensaje Estudiante: {mensaje_estudiante}"

    Y la lista de temas que se deben desarrollar es la siguiente enlazado a si han sido abordados o conversados hasta el momento con True o False:

    "Lista de Requerimientos: {lista_requerimientos}"
    """
    response = model.complete(prompt)
    #print(response)
    return response

# Función para el Agente 2
def agente_2(nivel_identificado_usuario, descripcion_usuario_edad_nivel_educativo, dificultades_tecnicas_favorables_para_estudiante, tecnicas_recomendadas_a_usar_sesion, temas_descripciones_sugerencia_proxima_respuesta):
    prompt_2 =  f"""
    Ahora actúa como un compañero de estudio del nivel {nivel_identificado_usuario}, que corresponde a {descripcion_usuario_edad_nivel_educativo}. Este compañero tiene el siguiente perfil como estudiante: {dificultades_tecnicas_favorables_para_estudiante}. Tu tarea es decidir qué técnica utilizar para responder, considerando las técnicas recomendadas para la sesión: {tecnicas_recomendadas_a_usar_sesion}.

    Tu objetivo es combinar estas dos perspectivas: las técnicas recomendadas y las que son más favorables para tu compañero, realizando comparaciones sobre cómo se pueden aplicar al tema en cuestión. Tu respuesta debe fomentar el desarrollo de nuevo conocimiento por parte de tu compañero sin proporcionarle soluciones directas. Más bien, deberías ofrecer ideas y plantear preguntas que le ayuden a explorar y reflexionar.

    Además, utiliza las opciones sugeridas para la próxima respuesta como guía: {temas_descripciones_sugerencia_proxima_respuesta}. El objetivo es actuar como un compañero reflexivo y colaborativo, proporcionando ejemplos, planteando dudas y sugiriendo caminos, pero siempre dejando espacio para que el compañero desarrolle las ideas.

    """
    response = model.complete(prompt_2)
    #print(response.text)
    return response

def agente_3(mensaje_estudiante,lista_requerimientos, sugerencia_proxima_respuesta, chat):
    prompt_3 =  f"""
    Eres un compañero de estudios, tu tarea es continuar la conversación de manera fluida, natural y amena. El objetivo es fomentar el aprendizaje mediante ideas, sugerencias y preguntas abiertas que ayuden a la persona a reflexionar y avanzar en su aprendizaje, sin ser excesivamente técnico o presentar soluciones directas. Siempre debes presentar nuevas ideas, suposiciones y posibilidades, sin dar respuestas definitivas ni mostrar un conocimiento superior.

    ### Instrucciones clave:
    1. **Estrategia de conversación:**  
    - La conversación debe mantenerse dentro del marco del tema de la sesión, según la lista proporcionada en `lista_requerimientos`{lista_requerimientos}.  
    - **No des soluciones directas.** Solo ofrece sugerencias, dudas, preguntas abiertas o puntos de vista que provoquen reflexión.
    - **Mantén el tono como un compañero amigable**, no como un experto. Puedes agregar alguna "razón personal" o una pequeña historia para dar más naturalidad a tus respuestas.

    2. **Estrategia de técnicas de aprendizaje:**  
    - Elige entre las técnicas sugeridas en 'sugerencia_proxima_respuesta' {sugerencia_proxima_respuesta}, ajustándote al **nivel de profundidad** y al **perfil del estudiante**. Evita ser demasiado formal o complejo, pero asegúrate de no hacer que el estudiante se sienta incomprendido.

    3. **Interacción con el chat y sesión:**
    - Mantén un enfoque en los temas de la sesión y asegúrate de que las respuestas sigan desarrollando el tema sin irse demasiado por las ramas.  
    - Utiliza el `chat`{chat} actual para integrar lo que ya se ha hablado, asegurándote de que las respuestas sean continuaciones lógicas y fluidas.
    - **No realices preguntas que no ayuden a avanzar el conocimiento** o que sean demasiado triviales. El objetivo es continuar el aprendizaje, no solo hacer preguntas por hacer.

    4. **Control del tono:**  
    - **Sutilmente ajusta el tono** de la conversación según el flujo de la misma. Si el estudiante se muestra interesado, puedes intensificar ligeramente el nivel de complejidad. Si está más relajado o distraído, baja el nivel para que se sienta cómodo.

    """
    messages = [
    ChatMessage(role="assistant", content=prompt_3),
    ChatMessage(role="user", content=mensaje_estudiante)
    ]
    response = model.chat(messages)
    #print(response.text)
    return response


# Bucle continuo
def ejecutar_programa2():
    lista_requerimientos = {
        "descripcion": "Es una lista de temas que se deben realizar durante la sesión...",
        "lista": [{"calapata": True}, {"calacunca": False}, {"huishi": False}, {"lomiar": False}]
    }

    nivel_identificado_usuario = {
        "nivel": "básico",
        "descripción": "español nativo"
    }

    descripcion_usuario_edad_nivel_educativo = {
        "usuario": "Yeimy Huanca",
        "edad": 15,
        "nivel_educativo": "4to de secundaria"
    }

    dificultades_tecnicas_favorables_para_estudiante = {
        "dificultades": ["no sabe formular muchas frases pero entiende significados"],
        "tecnicas_favorables": ["comparación semántica"]
    }

    tecnicas_recomendadas_a_usar_sesion = {
        "lista_de_tecnicas": ["ejemplos", "analogías"]
    }
    
    chat = []  # Historial de la conversación

    # Capturar mensaje inicial del estudiante
    mensaje_estudiante = input("Ingrese el mensaje inicial del estudiante: ")

    while True:
        # Agregar el mensaje del estudiante al historial
        chat.append({"role": "user", "content": mensaje_estudiante})

        # Paso 1: Agente 1 genera sugerencias
        temas_sugeridos = agente_1(lista_requerimientos, mensaje_estudiante)

        # Paso 2: Agente 2 genera la respuesta
        respuesta_base = agente_2(
            nivel_identificado_usuario,
            descripcion_usuario_edad_nivel_educativo,
            dificultades_tecnicas_favorables_para_estudiante,
            tecnicas_recomendadas_a_usar_sesion,
            temas_sugeridos
        )

        # Agregar la respuesta del agente 2 al historial
        chat.append({"role": "assistant", "content": respuesta_base})

        # Paso 3: Agente 3 genera la respuesta contextualizada
        respuesta_contextualizada = agente_3(
            mensaje_estudiante, 
            lista_requerimientos, 
            respuesta_base, 
            chat
        )

        # Agregar la respuesta del agente 3 al historial
        chat.append({"role": "assistant", "content": respuesta_contextualizada})

        # Mostrar la respuesta del agente 3
        print("Respuesta del Agente 3:")
        print(respuesta_contextualizada)

        # Simulación de espera o ingreso de nuevos datos
        mensaje_nuevo = input("Ingrese el nuevo mensaje del estudiante o presione Enter para continuar con el anterior: ")
        if mensaje_nuevo:  # Si el usuario ingresa un nuevo mensaje, actualiza
            mensaje_estudiante = mensaje_nuevo

        time.sleep(2)  # Espera 2 segundos antes de la próxima iteración










@csrf_exempt
def chat_with_gemini(request):
    if request.method == "POST":
        print("metodo post")
        data = json.loads(request.body)
        # Obtener el mensaje del usu= json.loads(request.body)
        user_message = data.get("message", "")
        print(user_message)
        if not user_message:
            return JsonResponse({"error": "No se envió un mensaje"}, status=400)
        
        # Generar respuesta utilizando Gemini
        try:
            response = model.complete(prompt=user_message)
            print(response)
            return JsonResponse({"response": response.text})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)

