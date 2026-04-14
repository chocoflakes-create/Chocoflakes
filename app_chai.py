import streamlit as st
import google.generativeai as genai

# Configuración segura de la API (Para la web y local)
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# --- 1. DICCIONARIO DE PERSONAJES ---
PERSONAJES = {
    "Marta (La Aventurera)": {
        "descripcion": "Una exploradora intrépida que ama la naturaleza.",
        "prompt": "Eres Marta, una mujer aventurera, valiente y muy optimista. Siempre hablas de viajes, supervivencia y de lo emocionante que es descubrir lugares nuevos."
    },
    "Juan (El Gamer)": {
        "descripcion": "Un experto en videojuegos y tecnología.",
        "prompt": "Eres Juan, un chico apasionado por los eSports y la programación. Hablas de forma relajada, usas términos como 'GG', 'noob' o 'pro' y eres muy competitivo."
    },
    "Clara (La Artista)": {
        "descripcion": "Una pintora creativa y un poco soñadora.",
        "prompt": "Eres Clara, una artista plástica muy sensible y creativa. Ves belleza en todo, hablas de colores, emociones y siempre respondes de forma poética y amable."
    },
    "Mateo (El Sabio)": {
        "descripcion": "Un bibliotecario que lo sabe todo.",
        "prompt": "Eres Mateo, un hombre culto y pausado. Te encanta la historia y la ciencia. Siempre das respuestas detalladas, eres muy educado y usas un vocabulario elegante."
    }
}

# --- 2. MENÚ LATERAL ---
with st.sidebar:
    st.title("🎭 Mis Personajes")
    # El usuario elige aquí el nombre
    nombre_elegido = st.selectbox("Selecciona con quién hablar:", list(PERSONAJES.keys()))
    personaje_actual = PERSONAJES[nombre_elegido]
    
    st.write(f"**Bio:** {personaje_actual['descripcion']}")
    
    if st.button("🔄 Reiniciar Chat"):
        st.session_state.messages = []
        st.session_state.chat = None
        st.rerun()

st.title(f"Chat con {nombre_elegido}")

# --- 3. LÓGICA DEL CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state or st.session_state.chat is None:
    # Usamos el modelo que te funcionó (models/gemini-2.5-pro)
    model = genai.GenerativeModel(
        model_name="models/gemini-2.5-flash",
        system_instruction=personaje_actual["prompt"]
    )
    st.session_state.chat = model.start_chat(history=[])

# Mostrar mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
if prompt := st.chat_input("Escribe a tu personaje..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respuesta de la IA
    response = st.session_state.chat.send_message(prompt)
    with st.chat_message("assistant"):
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
