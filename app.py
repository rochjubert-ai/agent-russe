
import os
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Mon professeur de russe",
    page_icon="🇷🇺"
)

st.subheader("🎙️ Conversation orale")

audio = st.audio_input("Parle à ton professeur en russe")

if audio:
    st.audio(audio)

st.title("🇷🇺 Mon professeur de russe")
st.caption("Ton professeur personnel, de débutant à avancé.")

st.sidebar.header("Mon apprentissage")
st.sidebar.write("Objectif : 1 heure de russe par jour")
st.sidebar.write("Niveau : débutant")

api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))

if not api_key:
    st.info(
        "Ton professeur doit encore être connecté "
        "à son intelligence artificielle."
    )
    st.stop()

client = OpenAI(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

instructions = """Tu es un professeur de russe personnel, patient et exigeant.
Ton élève est débutant absolu et parle français.

Enseigne progressivement :
- l'alphabet cyrillique et la prononciation ;
- le vocabulaire courant ;
- la grammaire russe ;
- la compréhension et l'expression ;
- les dialogues de la vie quotidienne.

Pour chaque nouveau mot, donne :
1. Le mot en russe.
2. Sa prononciation approximative en français.
3. Sa traduction française.
4. Un exemple simple.

Pose des questions et attends les réponses de l'élève.
Corrige ses erreurs avec une explication claire.
Réutilise les mots déjà appris dans les exercices.
Adapte la difficulté aux réponses de l'élève.
Réponds principalement en français au début, puis
augmente progressivement la part du russe.
Commence par une courte évaluation du niveau.


"""

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


question = st.chat_input("Écris ici ton message...")

if st.button("🎙️ Transcrire et envoyer") and audio:
    try:
        transcription = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=audio
        )
        question = transcription.text
        st.success("Voici ce que j'ai compris : " + question)
    except Exception as error:
        st.error("Erreur de transcription : " + str(error))


if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    
    with st.chat_message("assistant"):
        with st.spinner("Ton professeur réfléchit..."):
            try:
                response = client.chat.completions.create(
                    model=os.getenv(
                        "OPENAI_MODEL", "gpt-4.1-mini"
                    ),
                    messages=[
                        {"role": "system", "content": instructions},
                        *st.session_state.messages
                    ]
                )

                answer = response.choices[0].message.content
                st.markdown(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as error:
                st.exception(error)

            
                
                
