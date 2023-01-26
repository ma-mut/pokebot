# Prueba Databot #

_** STACK BÁSICO **_

- Rasa Version      :         3.2.8
- Minimum Compatible Version: 3.0.0
- Rasa SDK Version  :         3.2.1
- Python Version    :         3.8.13
- Operating System  :         macOS-12.6-x86_64-i386-64bit

_**Notas:**_ 

- Se recomienda el uso de entornos virtuales en python (de preferencia: conda)

_**Instrucciones de ejecución del proyecto:**_

```
1. conda create -n <entorno_virtual> python=3.8.13
2. git clone https://github.com/ma-mut/pokebot.git pokebot
3. *en terminal* cd pokebot
4. conda activate <entorno_virtual>
5. pip install -r requirements.txt
6. pip install rasa
7. rasa train
8. docker run -p 8000:8000 rasa/duckling
9. rasa run actions --cors "*" --debug
10. rasa run -m models --enable-api --log-file out.log --cors "*"
PARA VER WIDGET DESDE INDEX.HTML
- desde paso 10:
11. abrir index.html en navegador por defecto
PARA CONSULTA A TRAVÉS DE API:
- desde paso 10:
11. usar Postman o curl desde la terminal para la consulta
```

_**Funcionamiento**_

Para los detalles de funcionamiento, ir al directorio: [images](/images/README.md)

_**Notas: Entrenamiento y Resultados:**_ 

- Se usa **SpacyEntityExtractor** y su entidad *"PER"* para el reconocimiento de nombres propios de personas, por lo que este reconocimiento estará limitado por el alcance de este recurso y la falta de reconocimiento no corresponde a una mala implementación, sino a la mera capacidad del extractor para reconocer el nombre correspondiente.
- Se usa **DucklingEntityExtractor** para extraer las entidades *"time", "number", "url", "duration"*, aunque sin una cantidad suficiente de frases de entrenamiento de uso real en que aparezcan estas entidades siendo empleadas. Al reconocer alguna de estas entidades, la respuesta contiene un mensaje de texto con el contenido reconocido (string que toma de referencia el JSON obtenido de respuesta).
- Se usa **RegexEntityExtractor** para el reconocimiento de nombres de Pokémon, junto a un entrenamiento de tipo *lookup table* que permita reconocer el mayor número de nombres de Pokémon posible.
- Se usa el **Rasa Official Widget** (index.html) para mostrar el funcionamiento básico de este prototipo. Esto implica que no se realizaron adecuaciones específicas para el front-end.
- Al lanzar algunos comandos  o *rasa run -m models --enable-api --log-file out.log --cors "*"* pueden recibirse 2 advertencias:
    - ```rasa train``` // ```rasa run -m models --enable-api --log-file out.log --cors "*"``` // ```rasa run --enable-api --cors "*"``` :  1 warning relacionado con la existencia de la intent *"faq"* en distintos archivos domain, lo cual no genera error de funcionamiento, sino que es una consecuencia de utilizar una *retrieval_intent*
    - ```rasa run -m models --enable-api --log-file out.log --cors "*"```: 1 error relacionado con la librería sanic, específicamente al levantar el widget, que es un error que no impide la prueba y funcionamiento a través del widget oficial, pero que requeriría de un ajuste en las versiones de distintas librerías.
- Las FAQs para probar son: 
    1. quién eres, 
    2. quién te creó, 
    3. eres una máquina, 
    4. qué puedes hacer. 
- La falta o carencia de entrenamiento para las intenciones por defecto "out-of-scope" y/o "nlu_fallback", así como también la configuración del umbral de confianza (Fallback Classifier threshold) podrían implicar el reconocimiento incorrecto o "forzado" de algunos inputs de usuario.

