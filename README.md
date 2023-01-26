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
1. git clone https://github.com/ma-mut/pokebot.git
2. conda create -n <entorno_virtual> python=3.8.13
3. conda activate <entorno_virtual>
4. pip install -r requirements.txt
5. pip install rasa 
6. rasa train
7. rasa run actions --cors "*" --debug
PARA VER WIDGET DESDE INDEX.HTML
- desde paso 7:
8. rasa run -m models --enable-api --log-file out.log --cors "*"
9. abrir index.html en navegador por defecto
PARA CONSULTA A TRAVÉS DE API:
- desde paso 7:
8. rasa run --enable-api --cors "*"
9. usar Postman o curl desde la terminal para la consulta
```

_**Notas: Entrenamiento y Resultados:**_ 

- Se usa **SpacyEntityExtractor** y su entidad "PER" para el reconocimiento de nombres propios de personas, por lo que este reconocimiento estará limitado por el alcance de este recurso y la falta de reconocimiento no corresponde a una mala implementación, sino a la mera capacidad del extractor para reconocer el nombre correspondiente.
- Se usa **DucklingEntityExtractor** para extraer las entidades "time", "number", "url", "duration", aunque sin una cantidad suficiente de frases de entrenamiento de uso real en que aparezcan estas entidades siendo empleadas. La respuesta por defecto frente al reconocimiento es el envío en mensaje del contenido reconocido.
- Se usa **DIETClassifier** para el reconocimiento de nombres de Pokémon, junto a un entrenamiento significativo que permita reconocer todos los nombres de Pokémon existentes.
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