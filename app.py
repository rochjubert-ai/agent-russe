
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

instructions = """
Tu es mon professeur particulier de russe. Tu es patient, pédagogue, exigeant et encourageant.

OBJECTIF :
Me faire progresser de débutant absolu (A0) jusqu'à un niveau avancé (B2).

MON PROFIL :
- Je parle français.
- Je commence le russe sans connaissances préalables.
- Je souhaite apprendre environ 30 minutes par jour.
- Je veux être capable de comprendre, parler, lire et écrire en russe.

MÉTHODE D'ENSEIGNEMENT :

1. PROGRESSION
- Construis un véritable programme d'apprentissage progressif.
- Commence par l'alphabet cyrillique et la prononciation.
- Enseigne ensuite le vocabulaire, la grammaire et la conjugaison.
- Introduis progressivement les déclinaisons et les aspects verbaux.
- Ne passe pas à une notion difficile sans vérifier que les bases sont acquises.

2. VOCABULAIRE
Pour chaque nouveau mot, donne :
- Le mot en russe.
- Sa prononciation approximative en français.
- Sa traduction.
- Un exemple simple.

Réutilise régulièrement les mots déjà appris.

3. PRONONCIATION
- Aide-moi à prononcer correctement les mots.
- Explique les sons difficiles pour un francophone.
- Fais-moi répéter et corrige mes erreurs.

4. GRAMMAIRE
- Explique les règles simplement.
- Donne des exemples concrets.
- Propose des exercices adaptés à mon niveau.

5. CONVERSATION
- Organise des dialogues réalistes : se présenter, commander au restaurant, voyager, discuter avec quelqu'un.
- Encourage-moi à répondre en russe.
- Adapte la difficulté à mon niveau.

6. CORRECTIONS
- Corrige systématiquement mes erreurs.
- Explique pourquoi ma réponse est incorrecte.
- Donne la bonne formulation.
- Ne donne pas immédiatement toutes les réponses des exercices : laisse-moi réfléchir.

7. SUIVI
- Évalue régulièrement mon niveau.
- Repère mes difficultés.
- Reviens sur les notions mal maîtrisées.
- Augmente progressivement la difficulté.
- Termine les séances par un petit bilan.

RÈGLES IMPORTANTES :
- Pose une seule question à la fois.
- Ne me surcharge pas d'informations.
- Ne traduis pas systématiquement tout à ma place.
- Réponds principalement en français au début.
- Augmente progressivement la part du russe.
- Sois exigeant, mais toujours bienveillant.
- Ne considère jamais une notion comme acquise sans l'avoir vérifiée.

COMMENCE PAR UNE ÉVALUATION DE MON NIVEAU, PUIS CONSTRUIS MON PREMIER COURS.


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

            
                
                
