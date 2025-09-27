import streamlit as st
import pandas as pd
import io

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Herramienta de Limpieza de Encuestas (v2.1)",
    layout="centered",
    initial_sidebar_state="auto"
)

def limpiar_y_descargar_csv(uploaded_file):
    """
    Función principal para realizar la limpieza del archivo CSV,
    ajustada para manejar filas vacías iniciales y asegurar la doble decodificación.
    """
    try:
        # 1. Doble Decodificación para Corregir Caracteres Especiales
        archivo_binario = uploaded_file.getvalue()
        # Decodificar de bytes a texto con utf-8, luego a bytes con latin-1, y de vuelta a texto con latin-1
        archivo_corregido_texto = archivo_binario.decode('utf-8', errors='ignore').encode('latin-1', errors='ignore').decode('latin-1')
        archivo_io = io.StringIO(archivo_corregido_texto)
        
        # 2. Determinar la Fila de Inicio de Encabezados Reales
        lineas = archivo_io.getvalue().split('\n')
        
        # Initialize with a "not found" value
        header_start_index = -1
        
        for i, linea in enumerate(lineas):
            # CORRECCIÓN: Busca cualquier línea que no esté completamente vacía
            # (después de quitar comas y espacios en blanco).
            if len(linea.replace(',', '').strip()) > 0:
                header_start_index = i
                break
        
        # Si después del bucle no se encontró ninguna línea con contenido, muestra el error.
        if header_start_index == -1:
            st.error("No se pudo identificar la fila inicial de los encabezados. El archivo podría estar completamente vacío o mal formado.")
            return None
        
        skip_rows_count = header_start_index
        
        # 3. Lectura de las Filas de Encabezado (Fila 1 y Fila 2)
        archivo_io.seek(0)
        df_headers = pd.read_csv(archivo_io, header=None, nrows=2, skiprows=skip_rows_count, sep=',')

        # 4. Lectura de los Datos
        archivo_io.seek(0)
        # Los datos comienzan dos filas después del inicio de los encabezados.
        df = pd.read_csv(archivo_io, header=None, skiprows=skip_rows_count + 2, sep=',') 
        
        # 5. Concatenación de Encabezados
        nuevos_headers = []
        fila_0 = df_headers.iloc[0].astype(str).tolist()
        fila_1 = df_headers.iloc[1].astype(str).tolist()
        
        # Asegurarse de que las listas de encabezados sean lo suficientemente largas
        max_len = max(len(fila_0), len(fila_1), len(df.columns))
        fila_0 += [''] * (max_len - len(fila_0))
        fila_1 += [''] * (max_len - len(fila_1))

        for h1, h2 in zip(fila_0, fila_1):
            h1 = h1.strip()
            h2 = h2.strip()
            
            if h2 and h2.lower() not in ['nan', '']:
                nuevo_header = f"{h1} - {h2}"
            else:
                nuevo_header = h1
            
            nuevos_headers.append(nuevo_header)

        # Recortar la lista de encabezados para que coincida exactamente
        # con el número de columnas de datos.
        df.columns = nuevos_headers[:len(df.columns)]

        # 6. Preparar el Archivo Limpio para Descarga
        output = io.BytesIO()
        # Usar 'utf-8-sig' para máxima compatibilidad con Excel (BOM)
        df.to_csv(output, index=False, encoding='utf-8-sig')
        output.seek(0)
        
        return output

    except Exception as e:
        st.error(f"Ocurrió un error inesperado durante el procesamiento. Por favor, verifica el formato del archivo: {e}")
        return None

# --- Interfaz de Usuario de Streamlit ---

st.title("🛠️ Limpiador Automático de Encuestas CSV")

st.markdown("""
Esta herramienta procesa tu archivo **DATA.csv** automáticamente, ajustado para estructuras complejas:
1.  **Corrige la codificación** de caracteres (e.g., "Ã³" a "ó", "Ã±" a "ñ").
2.  **Detecta y salta** las filas vacías iniciales de forma flexible.
3.  **Combina las primeras dos filas con texto** para crear encabezados únicos y descriptivos.
""")

uploaded_file = st.file_uploader(
    "Sube tu archivo CSV",
    type=["csv"],
    accept_multiple_files=False
)

if uploaded_file is not None:
    st.info("Archivo cargado. Procesando automáticamente...")
    
    csv_limpio = limpiar_y_descargar_csv(uploaded_file)
    
    if csv_limpio:
        st.success("✅ ¡Limpieza completada! Tu archivo está listo para descargar.")
        
        st.download_button(
            label="Descargar CSV Limpio",
            data=csv_limpio,
            file_name='DATA_limpio.csv',
            mime='text/csv'
        )
        st.balloons()
