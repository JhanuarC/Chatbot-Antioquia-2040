#Por favor instala las siguientes librerías antes de ejecutar el código:
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

#Cargar variables de entorno (API Key)
load_dotenv()#Iba a usar una variable de entorno para la API Key, pero por simplicidad la dejo directamente en el código. No dejen la api key expuesta en un proyecto real.
genai.configure(api_key="")#Pongan la API key, recomiendo gemini porque es gratis

try:
    df_municipios = pd.read_csv("Catedra G8/base_mock.csv")#Cambien el path si el archivo CSV no está en la misma carpeta que este script
except FileNotFoundError:
    print("Error: No se encontró el archivo CSV.")
    exit()

# Definir la "Herramienta" (Función que el Agente puede usar)
def consultar_datos_municipio(nombre_municipio: str) -> str:
    """
    Busca los indicadores de salud, educación y pobreza de un municipio de Antioquia.
    Útil para diagnosticar el estado actual antes de proponer inversiones.
    """
    # Filtrar el dataframe por el nombre del municipio (ignorando mayúsculas/minúsculas)
    municipio_data = df_municipios[df_municipios['municipio'].str.lower() == nombre_municipio.lower()]
    
    if municipio_data.empty:
        return f"No se encontraron datos para el municipio: {nombre_municipio}."
    
    # Convertir los datos a un formato de texto que la IA entienda fácilmente
    datos_dict = municipio_data.iloc[0].to_dict()
    return str(datos_dict)

#Rol del agente: Asistente de Planificación para Agenda Antioquia 2040
instruccion_sistema = """
Eres el 'Asistente de Planificación Agenda Antioquia 2040'. 
Tu objetivo es ayudar a reducir la pobreza extrema aumentando los ingresos de la población.
Para lograr esto, ten en cuenta que para que una persona trabaje necesita educación, salud y oferta laboral.
Sigue esta lógica:
1. Usa la herramienta 'consultar_datos_municipio' para obtener el diagnóstico.
2. Analiza los niveles de deserción escolar, desnutrición y pobreza.
3. Sugiere dónde debe enfocarse el gasto público (salud, educación o proyectos productivos) para mejorar las condiciones de trabajo y aumentar el PIB municipal.
Responde de manera técnica, estructurada y basándote ÚNICAMENTE en los datos consultados.
"""


model = genai.GenerativeModel(
    model_name="gemini-3-flash-preview",#Pueden cambiarlo por el gemini-2.5-flash, pero el 3 tiene mejor capacidad de razonamiento.
    system_instruction=instruccion_sistema,
    tools=[consultar_datos_municipio] 
)

#Iniciar la conversación
chat = model.start_chat(enable_automatic_function_calling=True)


#Configurar el servidor FastAPI para conectar con el frontend
app = FastAPI()

#Esto conecta el HTML del frontend con el backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    mensaje: str

@app.post("/ask")
async def ask_gemini(request: ChatRequest):
    respuesta = chat.send_message(request.mensaje)
    return {"respuesta": respuesta.text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
