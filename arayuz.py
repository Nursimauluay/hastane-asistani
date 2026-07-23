import streamlit as st
import requests

st.set_page_config(page_title="HASTANE ASİSTANI", page_icon="🏥", layout="centered")

st.title("🤖 Akıllı Navigasyon Asistanı")
st.write("Lütfen gitmek istediğiniz poliklinik veya odayı sorunuz.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if kullanici_sorusu := st.chat_input("Nasıl yardımcı olabilirim?"):
    with st.chat_message("user"):
        st.markdown(kullanici_sorusu)
    st.session_state.messages.append({"role": "user", "content": kullanici_sorusu})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            response = requests.post("http://localhost:5000/api/sor", json={"soru": kullanici_sorusu}, timeout=10)
            if response.status_code == 200:
                ai_cevabi = response.json().get("cevap", "Cevap yok.")
                # Karakterleri temizle
                message_placeholder.markdown(ai_cevabi)
                st.session_state.messages.append({"role": "assistant", "content": ai_cevabi})
        except:
            message_placeholder.error("Sunucuya bağlanılamadı.")