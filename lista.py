import streamlit as st
import pandas as pd
import os

# Nombre del archivo CSV para almacenar las tareas
CSV_FILE = "tareas.csv"

# Función para cargar las tareas desde el archivo CSV
def cargar_tareas():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["N", "Habitacion", "Apellido y Nombre", "Procedimiento", "Observación", "Prioridad", "Completada"])

# Función para guardar las tareas en el archivo CSV
def guardar_tareas(tareas):
    tareas.to_csv(CSV_FILE, index=False)

# Cargar las tareas en session_state al iniciar la aplicación
if 'tareas' not in st.session_state:
    st.session_state.tareas = cargar_tareas()

# Título de la aplicación
st.title("Pizarra de Pendientes")

# Formulario para agregar nuevas tareas
with st.container():
    st.subheader("Agregar Nueva Tarea")
    
    # Crear contenedores para los campos
    col1, col2 = st.columns(2)

    with col1:
        habitacion = st.text_input("Habitación")
        apellido_nombre = st.text_input("Apellido y Nombre")
        procedimiento = st.text_input("Procedimiento")

    with col2:
        observacion = st.text_area("Observación")
        prioridad = st.selectbox("Prioridad", ["Baja (Verde)", "Media (Naranja)", "Alta (Rojo)"])

    # Botón de envío para agregar la tarea
    if st.button("Agregar Tarea"):
        # Obtener el siguiente número de tarea
        numero_tarea = len(st.session_state.tareas) + 1
        # Crear el nuevo DataFrame para la tarea
        nueva_tarea = pd.DataFrame({
            "N": [numero_tarea],
            "Habitacion": [habitacion],
            "Apellido y Nombre": [apellido_nombre],
            "Procedimiento": [procedimiento],
            "Observación": [observacion],
            "Prioridad": [prioridad],
            "Completada": [False]
        })
        # Concatenar la nueva tarea y guardar
        st.session_state.tareas = pd.concat([st.session_state.tareas, nueva_tarea], ignore_index=True)
        guardar_tareas(st.session_state.tareas)
        st.success("Tarea agregada exitosamente")
        st.experimental_rerun()

# Función para aplicar colores en función de la prioridad y el estado de completada
def colorear_fila(fila):
    if fila["Completada"]:
        return ["background-color: #D3D3D3; color: black; font-weight: bold;"] * len(fila)
    color = {"Alta (Rojo)": "#FF9999", "Media (Naranja)": "#FFCC99", "Baja (Verde)": "#66CC66"}.get(fila["Prioridad"], "#FFFFFF")
    return [f"background-color: {color}; color: black; font-weight: bold;"] * len(fila)

# Mostrar las tareas en una tabla con colores
st.subheader("Lista de Tareas")
if not st.session_state.tareas.empty:
    for index, row in st.session_state.tareas.iterrows():
        col1, col2 = st.columns([5, 1])
        with col1:
            completada = st.checkbox("", value=row["Completada"], key=f"check_{index}")
            if completada != row["Completada"]:
                st.session_state.tareas.at[index, "Completada"] = completada
                guardar_tareas(st.session_state.tareas)
                st.experimental_rerun()

            styled_row = row.to_frame().T.style.apply(colorear_fila, axis=1)
            st.dataframe(styled_row, use_container_width=True, hide_index=True)
        with col2:
            if st.button("🗑️", key=f"delete_{index}") and not st.session_state.tareas.empty:
                st.session_state.tareas = st.session_state.tareas.drop(index).reset_index(drop=True)
                st.session_state.tareas["N"] = range(1, len(st.session_state.tareas) + 1)
                guardar_tareas(st.session_state.tareas)
                st.success("Tarea borrada exitosamente")
                st.experimental_rerun()
else:
    st.info("No hay tareas para mostrar.")

# Botón para borrar todas las tareas
if st.button("Borrar todas las tareas"):
    st.session_state.tareas = pd.DataFrame(columns=["N", "Habitacion", "Apellido y Nombre", "Procedimiento", "Observación", "Prioridad", "Completada"])
    guardar_tareas(st.session_state.tareas)
    st.warning("Todas las tareas han sido borradas")
