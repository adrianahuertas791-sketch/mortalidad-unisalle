Markdown
# Dashboard Interactivo de Mortalidad No Fetal en Colombia (2019)

**UNIVERSIDAD DE LA SALLE**  
**Maestría en Inteligencia Artificial**  
**Asignatura:** Aplicaciones 1  
**Estudiante:** Adriana Milena Huertas — C.C. 53.093.953  
**Docente:** Cristian Bermudez 
**Bogotá D.C., Mayo de 2026**  

---

## 1. URLs de Acceso al Proyecto

*   **Repositorio de Código Fuente (GitHub):** (https://github.com/adrianahuertas791-sketch/mortalidad-unisalle)
*   **Aplicación Web Interactiva en Producción:** https://mortalidad-unisalle.onrender.com/

---

## 2. Manual de Arquitectura de Software y Ejecución

### Arquitectura de la Solución
El proyecto se fundamenta en una arquitectura de desarrollo web basada en microservicios analíticos bajo el lenguaje **Python 3.9**. Se compone de dos capas principales:

1.  **Capa de Extracción, Transformación y Carga (ETL):** Centralizada en el script `crear_base.py`. Se encarga de la ingesta de los archivos planos de origen (`.xlsx`), la limpieza crítica de cadenas de texto, la estandarización forzada de códigos territoriales DANE a 5 dígitos, y el formateo computacional de las coordenadas geográficas (Latitud y Longitud) reemplazando caracteres inválidos. Su salida genera un dataset optimizado para reducir la carga en memoria.
2.  **Capa Analítica e Interfaz de Usuario (Dashboard):** Soportada en `app.py`. Utiliza el framework **Dash por Plotly** acoplado a un servidor WSGI (**Gunicorn**) para producción. La lógica se divide en un *Layout* reactivo estructurado en contenedores HTML/Dash Components y un *Callback* síncrono encargado de procesar los filtros dinámicos en tiempo real utilizando la librería **Pandas**, devolviendo los graficadores vectoriales montados en **Plotly Express**.

### Diagrama de Flujo de Datos
`Fuentes Excel (DANE/Divipola) ➔ crear_base.py (ETL) ➔ Dataset Optimizado ➔ app.py (Dash/Pandas) ➔ Servidor Gunicorn ➔ Cliente Web`

---

## 3. Introducción
Este proyecto implementa una aplicación interactiva web destinada al análisis visual de las estadísticas vitales de Colombia, específicamente enfocada en la mortalidad no fetal registrada durante el año 2019. El propósito consiste en transformar los microdatos fuentes del DANE en información geográfica y estadística comprensible, facilitando la identificación de los patrones de mortalidad por regiones, géneros y ciclos de vida.

## 4. Objetivo
Con esta aplicación se busca resolver la dificultad de interpretar grandes volúmenes de datos tabulares mediante una interfaz dinámica y gráfica. El objetivo principal es permitir que el usuario filtre y visualise de manera inmediata e intuitiva la distribución de causas de muerte, la cantidad de defunciones por municipio y las tendencias mensuales, asegurando que los códigos territoriales de la Divipola se mantengan integrados para garantizar una georreferenciación precisa.

## 5. Estructura del Proyecto
Este repositorio está organizado de tal forma que se garantiza su ejecución tanto en entornos locales como en la nube:

*   `app.py`: Archivo principal que contiene la interfaz de usuario (Layout) y la lógica de reactividad (Callbacks) desarrollada en Dash.
*   `crear_base.py`: Script de procesamiento utilizado como ETL para limpiar los archivos Excel originales, estandarizar códigos DANE, corregir coordenadas y generar la base de datos optimizada.
*   `requirements.txt`: Archivo de configuración con las librerías y versiones exactas necesarias para el entorno de ejecución.
*   `Procfile`: Archivo de configuración requerido para permitir el despliegue en servidores WSGI (producción).
*   `Datasets/`: Carpeta que almacena los archivos de datos normalizados:
    *   `NoFetal2019_Modificado.xlsx` (Generado por el script ETL).
    *   `Divipola.xlsx` (Datos político-administrativos y coordenadas).
    *   `CodigosDeMuerte.xlsx` (Clasificación CIE-10).

## 6. Software y Herramientas Utilizadas
*   **Python (v3.9):** Lenguaje de programación base.
*   **Dash por Plotly:** Framework principal para la creación de interfaces analíticas y web.
*   **Pandas:** Librería especializada en la manipulación, limpieza y unión de estructuras de datos.
*   **Plotly Express:** Motor gráfico para generar los mapas interactivos y las visualizaciones.

## 7. Requisitos del Entorno
Librerías detalladas y empaquetadas en el archivo `requirements.txt`:
*   `Dash==2.11.0`
*   `pandas==2.0.0`
*   `plotly==5.15.0`
*   `openpyxl` (Para la lectura y escritura de archivos Excel).
*   `gunicorn` (Para el despliegue y soporte en producción).

## 8. Instalación y Ejecución Local
Para ejecutar el proyecto localmente, siga estos pasos en su terminal:
1. Clonar el repositorio desde GitHub.
2. Abrir una terminal en la carpeta raíz del proyecto.
3. Instalar las dependencias con el comando:  
   `pip install -r requirements.txt`
4. Ejecutar la aplicación con el comando:  
   `python app.py`
5. Abrir el navegador e ingresar a la dirección local:  
   `http://127.0.0.1:8099`

## 9. Despliegue en la Nube (PaaS)
La aplicación fue desplegada empleando la infraestructura de **GitHub Cloud (Codespaces)**. El proceso de despliegue consistió en:
1. Vinculación del repositorio maestro de GitHub.
2. Configuración de un contenedor con entorno aislado de Python 3.
3. Instación automatizada de las dependencias registradas en el servidor remoto.
4. Exposición del puerto 8099 mediante un proxy inverso para generar una URL pública interactiva y accesible para la evaluación docente.

---

## 10. Visualizaciones y Análisis de Resultados

### A) Panel de Control y Mapa de Calor
El mapa interactivo permite identificar de forma visual que los departamentos con mayor densidad poblacional presentan el mayor volumen de registros, pero el filtro municipal revela focos específicos de causas de muerte vinculadas a factores regionales. Se valida de forma conjunta que, de un total de 244 mil defunciones a nivel nacional, el municipio de **Santiago de Cali** presenta 18 mil de ellas, representándose como el municipio con la mayor concentración de homicidios en Colombia.

<img width="720" height="361" alt="MAPA1" src="https://github.com/user-attachments/assets/9148d67e-61e1-4f97-82d4-fcbbf3bfcdd4" />
<img width="720" height="314" alt="Mapa2" src="https://github.com/user-attachments/assets/38e3d0e5-0fc9-4729-b6f1-48ff80d61d32" />
<img width="720" height="244" alt="mapa 3" src="https://github.com/user-attachments/assets/5102b5b1-95ba-4cc4-8d09-8337c013650b" />



### B) Análisis de Ciclo de Vida y Género
Las visualizaciones demuestran una mayor prevalencia de mortalidad en hombres en etapas de **adultez temprana** debido a causas externas (como homicidios y accidentes), mientras que en la categoría de **vejez**, las enfermedades del sistema circulatorio son predominantes de forma equitativa entre ambos géneros.
<img width="720" height="188" alt="mapa 4 genero" src="https://github.com/user-attachments/assets/cdfdece1-bb14-4c96-adb1-9b7e51b07ce3" />

<img width="720" height="233" alt="moralidad por categoria" src="https://github.com/user-attachments/assets/906a852c-cef2-4fc9-975f-9617d1eac418" />


Adicionalmente, en el análisis de los municipios con menor índice de mortalidad destaca **Alto Baudó** con una participación cercana al 10% dentro del Top 10 de baja tasa de defunciones. El comportamiento de homicidios ratifica una brecha estructural, evidenciando un nivel significativamente mayor en hombres que en mujeres. Asimismo, se corrobora mediante las métricas del Dashboard que la principal causa de muerte generalizada en el país se asocia a patologías crónicas de la vejez.

<img width="720" height="339" alt="top 10 dptos" src="https://github.com/user-attachments/assets/bb11f363-bb78-46e1-84c3-1803f9c481f9" />


---

## 11. Referencias Bibliográficas
*   Dash for Python Documentation. (2026). *Dash layout, callbacks and interactive graphing*. Plotly Technologies Inc. Recuperado de https://dash.plotly.com/
*   Grinberg, M. (2018). *Flask Web Development: Developing Web Applications with Python* (2nd ed.). O'Reilly Media.
*   DANE. (2019). *Estadísticas Vitales - Mortalidad No Fetal*. Departamento Administrativo Nac

