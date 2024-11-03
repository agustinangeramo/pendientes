import streamlit as st
import pandas as pd

# Título de la aplicación
st.title("Pizarra de Pendientes")

# Crear un DataFrame vacío si no existe en session_state
if 'tareas' not in st.session_state:
    st.session_state.tareas = pd.DataFrame(columns=["N", "Habitacion", "Apellido y Nombre", "Procedimiento", "Observación", "Prioridad", "Completada"])

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
        # Obtener el siguiente número de tarea
        numero_tarea = len(st.session_state.tareas) + 1  # +1 para que empiece en 1
        # Agregar la tarea al DataFrame usando pd.concat
        nueva_tarea = pd.DataFrame({
            "N": [numero_tarea],
            "Habitacion": [habitacion],
            "Apellido y Nombre": [apellido_nombre],
            "Procedimiento": [procedimiento],
            "Observación": [observacion],
            "Prioridad": [prioridad],
            "Completada": [False]  # Inicialmente no completada
        })
        st.session_state.tareas = pd.concat([st.session_state.tareas, nueva_tarea], ignore_index=True)
        st.success("Tarea agregada exitosamente")

        # Restablecer los campos a valores predeterminados
        st.experimental_rerun()

# Función para aplicar colores en función de la prioridad y el estado de completada
def colorear_fila(fila):
    if fila["Completada"]:
        color = "background-color: #D3D3D3; color: black; font-weight: bold;"  # Gris
    else:
        color = "background-color: "
        # Define colors based on priority
        if fila["Prioridad"] == "Alta (Rojo)":
            color += "#FF9999"  # Rojo oscuro
        elif fila["Prioridad"] == "Media (Naranja)":
            color += "#FFCC99"  # Naranja oscuro
        else:
            color += "#66CC66"  # Verde oscuro
        color += "; color: black; font-weight: bold;"  # Texto negro
    return [color] * len(fila)

# Mostrar las tareas en una tabla con colores
st.subheader("Lista de Tareas")
if not st.session_state.tareas.empty:
    # Crear un contenedor para las tareas
    for index, row in st.session_state.tareas.iterrows():
        col1, col2 = st.columns([5, 1])  # Definir proporciones de columnas
        with col1:
            # Casilla de verificación para marcar la tarea como completada
            completada = st.checkbox("", value=row["Completada"], key=f"check_{index}")
            if completada != row["Completada"]:
                # Actualizar el estado de completada en el DataFrame
                st.session_state.tareas.at[index, "Completada"] = completada
            
            # Mostrar la tarea con el estilo aplicado
            styled_row = row.to_frame().T.style.apply(colorear_fila, axis=1)
            st.dataframe(styled_row, use_container_width=True, hide_index=True)
        with col2:
            # Botón para eliminar la tarea
            if st.button("🗑️", key=f"delete_{index}") and st.session_state.tareas.shape[0] > 0:
                st.session_state.tareas = st.session_state.tareas.drop(index).reset_index(drop=True)
                # Actualizar los números de tarea
                st.session_state.tareas["N"] = range(1, len(st.session_state.tareas) + 1)
                st.success("Tarea borrada exitosamente")
                st.experimental_rerun()  # Recargar para reflejar el cambio
else:
    st.info("No hay tareas para mostrar.")

# Botón para borrar todas las tareas
if st.button("Borrar todas las tareas"):
    st.session_state.tareas = pd.DataFrame(columns=["N", "Habitacion", "Apellido y Nombre", "Procedimiento", "Observación", "Prioridad", "Completada"])
    st.warning("Todas las tareas han sido borradas")
