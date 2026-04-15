# Chatbot Antioquia 2040
Este es el código para el chatbot para la plataforma Antioquia 2040

##  ¿Que es Antioquia 2040?

Para 2040, Antioquia quiere ser un territorio en el que todas las personas puedan vivir con
dignidad, bienestar y sin discriminación, donde haya oportunidades que permitan cerrar las
brechas de desarrollo entre la población, garantizando las necesidades básicas. Para alcanzar
este objetivo, se fijaron 4 ítems:
1. Garantizar la seguridad a la población, buscando la convivencia pacífica.
2. Ofrecer el acceso a salud de calidad.
3. Asegurar el acceso a la alimentación, reduciendo el hambre y la desnutrición.
4. Reducir la población en condición de pobreza extrema.

##  Logica del Chatbot
Este un agente que utiliza a gemini (aunque este se puede cambiar facilmente en el backend.py) para el razonamiento del chatbot, se le da una base de datos con los datos recolectados de todos los municipios de Antioquia, los datos recolectados para cada documento son los siguientes:


* Subregion

* PIB en millones de pesos

* Porcentaje de pobreza multidimensional

* Porcentaje de desercion escolar

* Casos de desnutricion aguda

* Capacidad hospitilaria en IPS

Basado en estos datos, el chatbot razonara una respuesta a cualquier pregunta respecto a Antioquia.

## Como usar el Chatbot
Lo primero es instalar las dependencias del chatbot

```
pip install -r requirements.txt
```

Instaladas las dependencias, se debe añadir una api key para poder acceder al modelo, esto se hace modificando el backend.py en la linea 11
```
genai.configure(api_key="")#Pongan la API key, recomiendo gemini porque es gratis
```

Luego, si se necesita, se puede modificar el modelo usado en la linea 49
```
model = genai.GenerativeModel(
    model_name="gemini-3-flash-preview",
    ...
```
Luego de esto se ejcuta el codigo y se corre el arcivo index.html


