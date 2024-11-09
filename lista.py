import streamlit as st
import pandas as pd
import os

# Nombre del archivo CSV para almacenar las tareas y seguimientos
CSV_FILE_TAREAS = "tareas.csv"
CSV_FILE_SEGUIMIENTOS = "seguimientos.csv"

# Función para cargar las tareas desde el archivo CSV
def cargar_tareas():
    if os.path.exists(CSV_FILE_TAREAS):
        return pd.read_csv(CSV_FILE_TAREAS)
    else:
        return pd.DataFrame(columns=["N", "Habitacion", "Apellido y Nombre", "Procedimiento", "Observación", "Prioridad", "Completada"])

# Función para cargar los seguimientos desde el archivo CSV
def cargar_seguimientos():
    if os.path.exists(CSV_FILE_SEGUIMIENTOS):
        return pd.read_csv(CSV_FILE_SEGUIMIENTOS)
    else:
        return pd.DataFrame(columns=["N", "Habitacion", "Apellido y Nombre", "Procedimiento", "Observación", "Prioridad", "Completada"])

# Función para guardar las tareas o los seguimientos en sus respectivos archivos CSV
def guardar_tareas(tareas):
    tareas.to_csv(CSV_FILE_TAREAS, index=False)

def guardar_seguimientos(seguimientos):
    seguimientos.to_csv(CSV_FILE_SEGUIMIENTOS, index=False)

# Cargar las tareas y los seguimientos en session_state al iniciar la aplicación
if 'tareas' not in st.session_state:
    st.session_state.tareas = cargar_tareas()

if 'seguimientos' not in st.session_state:
    st.session_state.seguimientos = cargar_seguimientos()

# Título de la aplicación
st.title("Pizarra de Pendientes")

# Formulario para agregar nuevas tareas
with st.container():
    st.subheader("Agregar Nueva Tarea")
    
    # Crear contenedores para los campos
    col1, col2 = st.columns(2)

    with col1:
        habitacion = st.text_input("Habitación", key="habitacion_tarea")
        apellido_nombre = st.text_input("Apellido y Nombre", key="apellido_nombre_tarea")
        procedimiento = st.text_input("Procedimiento", key="procedimiento_tarea")

    with col2:
        observacion = st.text_area("Observación", key="observacion_tarea")
        prioridad = st.selectbox("Prioridad", ["Baja (Verde)", "Media (Naranja)", "Alta (Rojo)"], key="prioridad_tarea")

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

# Título de la lista de tareas y recuento de tareas pendientes y finalizadas
st.subheader("Lista de Tareas")
tareas_pendientes = st.session_state.tareas[st.session_state.tareas["Completada"] == False].shape[0]
tareas_finalizadas = st.session_state.tareas[st.session_state.tareas["Completada"] == True].shape[0]
st.write(f"Tareas pendientes: {tareas_pendientes}")
st.write(f"Tareas finalizadas: {tareas_finalizadas}")

# Función para aplicar colores en función de la prioridad y el estado de completada
def colorear_fila(fila):
    if fila["Completada"]:
        return ["background-color: #D3D3D3; color: black; font-weight: bold;"] * len(fila)
    color = {"Alta (Rojo)": "#FF9999", "Media (Naranja)": "#FFCC99", "Baja (Verde)": "#66CC66"}.get(fila["Prioridad"], "#FFFFFF")
    return [f"background-color: {color}; color: black; font-weight: bold;"] * len(fila)

# Función para ordenar las tareas
def ordenar_tareas(tareas):
    # Definir el orden de prioridad: alta, media, baja
    prioridad_order = {"Alta (Rojo)": 1, "Media (Naranja)": 2, "Baja (Verde)": 3}
    
    # Añadir columna de prioridad numérica para ordenar
    tareas["Prioridad_Num"] = tareas["Prioridad"].map(prioridad_order)
    
    # Ordenar primero por completada (False primero), luego por prioridad numérica
    tareas = tareas.sort_values(by=["Completada", "Prioridad_Num"], ascending=[True, True])
    
    # Eliminar la columna de prioridad numérica
    tareas = tareas.drop(columns=["Prioridad_Num"])
    
    return tareas

# Ordenar las tareas cada vez que se muestren
st.session_state.tareas = ordenar_tareas(st.session_state.tareas)

# Mostrar las tareas ordenadas
if not st.session_state.tareas.empty:
    for index, row in st.session_state.tareas.iterrows():
        col1, col2 = st.columns([5, 1])
        with col1:
            # Mostrar un cuadrado vacío (⧫) cuando la tarea esté pendiente y un check lleno (✔) cuando esté completada
            if not row["Completada"]:
                # Botón con check vacío
                if st.button(f"⧫ Tarea Pendiente", key=f"check_{index}"):  # Tarea pendiente
                    st.session_state.tareas.at[index, "Completada"] = True
                    guardar_tareas(st.session_state.tareas)
                    st.experimental_rerun()
            else:
                # Botón con check lleno
                if st.button(f"✔ Tarea Finalizada", key=f"check_{index}"):  # Tarea finalizada
                    st.session_state.tareas.at[index, "Completada"] = False
                    guardar_tareas(st.session_state.tareas)
                    st.experimental_rerun()

            styled_row = row.to_frame().T.style.apply(colorear_fila, axis=1)
            st.dataframe(styled_row, use_container_width=True, hide_index=True)
        with col2:
            if st.button("🗑️ Eliminar tarea", key=f"delete_{index}") and not st.session_state.tareas.empty:
                st.session_state.tareas = st.session_state.tareas.drop(index).reset_index(drop=True)
                st.session_state.tareas["N"] = range(1, len(st.session_state.tareas) + 1)
                guardar_tareas(st.session_state.tareas)
                st.success("Tarea borrada exitosamente")
                st.experimental_rerun()

            # Botón para mover la tarea a seguimiento
            if st.button("➡️ Seguimiento", key=f"move_{index}"):
                tarea_a_seguimiento = st.session_state.tareas.loc[index]
                # Eliminar la tarea de la lista de tareas y agregarla a la lista de seguimientos
                st.session_state.seguimientos = pd.concat([st.session_state.seguimientos, tarea_a_seguimiento.to_frame().T], ignore_index=True)
                st.session_state.tareas = st.session_state.tareas.drop(index).reset_index(drop=True)
                st.session_state.tareas["N"] = range(1, len(st.session_state.tareas) + 1)
                guardar_tareas(st.session_state.tareas)
                guardar_seguimientos(st.session_state.seguimientos)
                st.success("Tarea movida a Seguimiento")
                st.experimental_rerun()

                # Agregar botón "Notas" para modificar la observación de la tarea
            if st.button("📓 Notas", key=f"notas_{index}"):
                # Campo de texto para las notas adicionales
                notas_adicionales = st.text_area(f"Agregar Notas para {row['Apellido y Nombre']}", value=row["Observación"], key=f"notas_text_{index}")

                # Guardar las notas cuando se modifique
                if notas_adicionales != row["Observación"]:
                    st.session_state.tareas.at[index, "Observación"] = notas_adicionales
                    guardar_tareas(st.session_state.tareas)
                    st.success("Notas actualizadas exitosamente")
                    st.experimental_rerun()

else:
    st.info("No hay tareas para mostrar.")

# Sección para agregar seguimiento
with st.container():
    st.subheader("Agregar Nuevo Seguimiento")
    
    # Crear contenedores para los campos
    col1, col2 = st.columns(2)

    with col1:
        habitacion = st.text_input("Habitación", key="habitacion_seguimiento")
        apellido_nombre = st.text_input("Apellido y Nombre", key="apellido_nombre_seguimiento")
        procedimiento = st.text_input("Procedimiento", key="procedimiento_seguimiento")

    with col2:
        observacion = st.text_area("Observación", key="observacion_seguimiento")
        prioridad = st.selectbox("Prioridad", ["Baja (Verde)", "Media (Naranja)", "Alta (Rojo)"], key="prioridad_seguimiento")

    # Botón de envío para agregar el seguimiento
    if st.button("Agregar Seguimiento"):
        # Obtener el siguiente número de seguimiento
        numero_seguimiento = len(st.session_state.seguimientos) + 1
        # Crear el nuevo DataFrame para el seguimiento
        nuevo_seguimiento = pd.DataFrame({
            "N": [numero_seguimiento],
            "Habitacion": [habitacion],
            "Apellido y Nombre": [apellido_nombre],
            "Procedimiento": [procedimiento],
            "Observación": [observacion],
            "Prioridad": [prioridad],
            "Completada": [False]
        })
        # Concatenar el nuevo seguimiento y guardar
        st.session_state.seguimientos = pd.concat([st.session_state.seguimientos, nuevo_seguimiento], ignore_index=True)
        guardar_seguimientos(st.session_state.seguimientos)
        st.success("Seguimiento agregado exitosamente")
        st.experimental_rerun()

# Mostrar la lista de seguimientos
st.subheader("Seguimiento de Pacientes Internados")
if not st.session_state.seguimientos.empty:
    for index, row in st.session_state.seguimientos.iterrows():
        col1, col2 = st.columns([5, 1])
        with col1:
            # Ya no hay casilla de verificación, solo aplicar los estilos de color a la fila
            styled_row = row.to_frame().T.style.apply(colorear_fila, axis=1)
            st.dataframe(styled_row, use_container_width=True, hide_index=True)

        with col2:
            if st.button(f"🗑️ Eliminar", key=f"delete_seguimiento_{index}") and not st.session_state.seguimientos.empty:
                st.session_state.seguimientos = st.session_state.seguimientos.drop(index).reset_index(drop=True)
                st.session_state.seguimientos["N"] = range(1, len(st.session_state.seguimientos) + 1)
                guardar_seguimientos(st.session_state.seguimientos)
                st.success("Seguimiento borrado exitosamente")
                st.experimental_rerun()

            # Agregar botón "Notas" para modificar la observación del seguimiento
            if st.button(f"📓 Notas", key=f"notas_seguimiento_{index}"):
                # Campo de texto para las notas adicionales
                notas_adicionales = st.text_area(f"Agregar Notas para {row['Apellido y Nombre']}", value=row["Observación"], key=f"notas_seguimiento_text_{index}")

                # Guardar las notas cuando se modifique
                if notas_adicionales != row["Observación"]:
                    st.session_state.seguimientos.at[index, "Observación"] = notas_adicionales
                    guardar_seguimientos(st.session_state.seguimientos)
                    st.success("Notas actualizadas exitosamente")
                    st.experimental_rerun()

else:
    st.info("No hay seguimientos para mostrar.")
