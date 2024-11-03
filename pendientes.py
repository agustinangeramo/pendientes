import streamlit as st
import pandas as pd

# Título de la aplicación
st.title("Pizarra de Pendientes")

# Crear un DataFrame vacío si no existe en session_state
if 'tareas' not in st.session_state:
    st.session_state.tareas = pd.DataFrame(columns=["Habitacion", "Apellido y Nombre", "Procedimiento", "Observación", "Prioridad"])

# Formulario para agregar nuevas tareas
with st.container():
    st.subheader("Agregar Nueva Tarea")
    
    # Crear contenedores para los campos
    col1, col2 = st.columns(2)  # Dividir en dos columnas

    with col1:
        habitacion = st.text_input("Habitación")
        apellido_nombre = st.text_input("Apellido y Nombre")
        procedimiento = st.text_input("Procedimiento")

    with col2:
        observacion = st.text_area("Observación")
        prioridad = st.selectbox("Prioridad", ["Baja (Verde)", "Media (Naranja)", "Alta (Rojo)"])

    # Botón de envío para agregar la tarea
    if st.button("Agregar Tarea"):
        # Agregar la tarea al DataFrame usando pd.concat
        nueva_tarea = pd.DataFrame({
            "Habitacion": [habitacion],
            "Apellido y Nombre": [apellido_nombre],
            "Procedimiento": [procedimiento],
            "Observación": [observacion],
            "Prioridad": [prioridad]
        })
        st.session_state.tareas = pd.concat([st.session_state.tareas, nueva_tarea], ignore_index=True)
        st.success("Tarea agregada exitosamente")

        # Restablecer los campos a valores predeterminados
        st.experimental_rerun()  # Esto recargará la aplicación, reiniciando el estado

# Función para aplicar colores en función de la prioridad
def colorear_fila(fila):
    color = "background-color: "
    # Define colors and font styles based on priority
    if fila["Prioridad"] == "Alta (Rojo)":
        color += "#FF9999"  # Rojo oscuro
    elif fila["Prioridad"] == "Media (Naranja)":
        color += "#FFCC99"  # Naranja oscuro
    else:
        color += "#66CC66"  # Verde oscuro
    # Apply bold text and black color
    style = f"{color}; color: black; font-weight: bold;"
    return [style] * len(fila)

# Mostrar las tareas en una tabla con colores
st.subheader("Lista de Tareas")
if not st.session_state.tareas.empty:
    st.dataframe(st.session_state.tareas.style.apply(colorear_fila, axis=1))
else:
    st.info("No hay tareas para mostrar.")

# Botón para borrar todas las tareas
if st.button("Borrar todas las tareas"):
    st.session_state.tareas = pd.DataFrame(columns=["Habitacion", "Apellido y Nombre", "Procedimiento", "Observación", "Prioridad"])
    st.warning("Todas las tareas han sido borradas")

# Mostrar input para seleccionar la tarea a borrar solo si hay tareas
if len(st.session_state.tareas) > 0:
    indice_tarea = st.number_input("Número de tarea a borrar (Índice de fila)", min_value=0, max_value=len(st.session_state.tareas)-1, step=1)
    if st.button("Borrar tarea seleccionada"):
        st.session_state.tareas = st.session_state.tareas.drop(indice_tarea).reset_index(drop=True)
        st.success("Tarea borrada exitosamente")
