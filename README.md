# 🛠️ Limpiador Automático de Encuestas CSV

Esta es una aplicación simple de **Streamlit** diseñada para automatizar la limpieza y estandarización de archivos CSV generados por plataformas de encuestas (como Qualtrics o similares) que a menudo presentan problemas de formato.

## ✨ Características Principales

1.  **Doble Encabezado Unificado**: Combina automáticamente las primeras dos filas de encabezados del CSV (típicas de las plataformas de encuestas) en una única fila de nombres de columna descriptivos (ejemplo: `Pregunta Larga - Sub-Opción`).
2.  **Manejo de Metadatos Iniciales**: Detecta y salta automáticamente cualquier número de filas iniciales completamente vacías o de metadatos hasta encontrar los encabezados reales.
3.  **Corrección de Codificación**: Realiza una doble decodificación para corregir caracteres especiales mal codificados, asegurando que tildes, eñes y otros símbolos se muestren correctamente.

## 🚀 Cómo usar

1.  Sube el archivo CSV de tu encuesta sin modificar a la aplicación.
2.  La herramienta lo procesará automáticamente.
3.  Descarga el archivo `DATA_limpio.csv`. ¡Listo para el análisis!

## 💻 Ejecución Local

Si deseas ejecutar esta aplicación en tu propia máquina:

1.  **Clona el repositorio:**
    ```bash
    git clone [TU_URL_DEL_REPOSITORIO]
    cd [NOMBRE_DEL_REPOSITORIO]
    ```
2.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Ejecuta la aplicación:**
    ```bash
    streamlit run app.py
    ```

## ☁️ Despliegue en Streamlit Community Cloud

Puedes acceder y usar la aplicación directamente aquí:

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)]([AQUÍ_VA_EL_LINK_DE_TU_APP_DESPLEGADA])
