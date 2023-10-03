# PI_MLOPs_Oswaldo

***
## Descripción general
Este proyecto es la realizacion de un MVP producto minimo viable, el contexto en el que se desarrolla éste proyecto es para situaciones de emergencia donde se da prioridad a crear funciones de consulta en una API que pueda ser consumida en un servidor como lo es Render. Esto con el fin de ofrecer un producto con diferentes funciones en corto período de tiempo.

## Requisitos previos
Este git es para ser utilizado por Render, por lo que solo existen 3 modulos importantes que son:
### -FastAPI
para poder realizar lo principal que es las funciones de la API.
### -Uvicorn
esencial para hacer el "deploy" de las funciones de la API.
### -Pandas
el modulo necesario para que las funciones trabajen.
### -Scikit-learn
Para poder realizar el modelo de Machine Learning

### Uso
El uso es simple: La liga que en el que se encuentra este repositorio se puede utilizar en Render directamente para realizar un servicio web. Render tiene la opcion de utilizar nuestro repositorio directamente siempre y cuando sea de dominio publico. 

Al utilizar la liga de repositorio solo necesitamos ponerle un nombre a nuestro servicio, elegir un servidor cercano a nuestra ubicación; en mi caso no se me da la geografia y escogí Oregon cuando el mas cercano era Ohio, de igual manera es importante que pueda instalar nuestro ambiente virtual del archivo "requirementes.txt" asi que puede que tengamos que hacer el commit cambiando nuestras versiones conforme Render lo solicite. Y en la sección de "Start Command" ponemos "uvicorn main:app --host 0.0.0.0 --port 8000 
***
## Descripción general
Este proyecto es la realizacion de un MVP producto minimo viable, el contexto en el que se desarrolla éste proyecto es para situaciones de emergencia donde se da prioridad a crear funciones de consulta en una API que pueda ser consumida en un servidor como lo es Render. Esto con el fin de ofrecer un producto con diferentes funciones en corto período de tiempo.

## Requisitos previos
Este git es para ser utilizado por Render, por lo que solo puse 3 modulos importantes que son:
### -FastAPI
para poder realizar lo principal que es las funciones de la API.
### -Uvicorn
esencial para hacer el "deploy" de las funciones de la API.
### -Pandas
el modulo necesario para que las funciones trabajen.

### Uso
El uso es simple: La liga que en el que se encuentra este repositorio se puede utilizar en Render directamente para realizar un servicio web. Render tiene la opcion de utilizar nuestro repositorio directamente siempre y cuando sea de dominio publico. 

Al utilizar la liga de repositorio solo necesitamos ponerle un nombre a nuestro servicio, elegir un servidor cercano a nuestra ubicación; en mi caso no se me da la geografia y escogí Oregon cuando el mas cercano era Ohio, de igual manera es importante que pueda instalar nuestro ambiente virtual del archivo "requirementes.txt" asi que puede que tengamos que hacer el commit cambiando nuestras versiones conforme Render lo solicite. Y en la sección de "Start Command" ponemos "uvicorn main:app --host 0.0.0.0 --port 8000 



