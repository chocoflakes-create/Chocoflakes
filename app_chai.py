import streamlit as st
import google.generativeai as genai

# Configuración de la página
st.set_page_config(page_title="Mi App de Chai", page_icon="🤖")
st.title("💬 Mi Personaje IA")
st.set_page_config(page_title="Aria Chat", page_icon="✨")
st.sidebar.title("Ajustes del Personaje")
st.sidebar.write("Estado: En línea 🟢")

# 1. Configurar la IA (Tu motor)
if "chat" not in st.session_state:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    modelo = genai.GenerativeModel('models/gemini-2.5-flash', 
                                  system_instruction="""
Eres Aria, una chica de 19 años que vive en un futuro ciberpunk. 
Eres sarcástica, te gusta la música techno y hablas con muchos emojis. 
No digas que eres una IA. Si te preguntan algo aburrido, responde con desgana.
""")
    st.session_state.chat = modelo.start_chat(history=[])
    st.session_state.mensajes = [] # Para guardar la memoria visual

# 2. Mostrar los mensajes en pantalla
for msj in st.session_state.mensajes:
    with st.chat_message(msj["rol"]):
        st.markdown(msj["texto"])

# 3. Entrada de texto del usuario
if prompt := st.chat_input("Escribe a tu personaje..."):
    # Guardar y mostrar mensaje del usuario
    st.session_state.mensajes.append({"rol": "user", "texto": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Pedir respuesta a la IA
    with st.chat_message("assistant"):
        respuesta = st.session_state.chat.send_message(prompt)
        st.markdown(respuesta.text)
        st.session_state.mensajes.append({"rol": "assistant", "texto": respuesta.text})
