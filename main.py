import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# ======================
# CONFIG
# ======================
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    st.error("❌ OPENAI_API_KEY não encontrada")
    st.stop()

client = OpenAI(api_key=API_KEY)

st.set_page_config(
    page_title="EducaBot • Matemática",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ======================
# CSS — VISUAL EDUCACIONAL PREMIUM
# ======================
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }

.stApp {
    background: radial-gradient(circle at top, #020617, #000);
    color: #E5E7EB;
}

/* HEADER */
.title-wrapper {
    max-width: 820px;
    margin: auto;
    padding: 30px 0 10px 0;
    display: flex;
    align-items: center;
    gap: 12px;
}

.title-emoji {
    font-size: 2.6rem;
    filter: drop-shadow(0 0 6px rgba(59,130,246,0.6));
}

.title-text {
    font-size: 2.6rem;
    font-weight: 900;
    letter-spacing: -1px;
    background: linear-gradient(90deg, #3b82f6, #60a5fa, #38bdf8);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientMove 6s ease infinite;
}

.subtitle {
    max-width: 820px;
    margin: auto;
    margin-top: 6px;
    font-size: 1.05rem;
    color: #94a3b8;
    animation: fadeUp 0.8s ease forwards;
}

@keyframes gradientMove {
    0% { background-position: 0% }
    50% { background-position: 100% }
    100% { background-position: 0% }
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

/* CHAT */
.chat-container {
    max-width: 820px;
    margin: auto;
    padding-bottom: 160px;
}

/* USER */
.user-bubble {
    background: linear-gradient(135deg, #2563eb, #3b82f6);
    color: white;
    padding: 14px 18px;
    border-radius: 20px 20px 4px 20px;
    margin: 10px 0;
    margin-left: auto;
    width: fit-content;
    max-width: 80%;
    box-shadow: 0 8px 20px rgba(59,130,246,0.35);
}

/* BOT */
.bot-bubble {
    background: #020617;
    border: 1px solid rgba(59,130,246,0.25);
    padding: 16px 18px;
    border-radius: 20px 20px 20px 4px;
    margin: 12px 0;
    width: fit-content;
    max-width: 85%;
}

.bot-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 6px;
}

.avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: radial-gradient(circle, #3b82f6, #1e40af);
    box-shadow: 0 0 14px rgba(59,130,246,0.7);
}

/* INPUT */
.input-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(2,6,23,0.94);
    backdrop-filter: blur(10px);
    padding: 15px;
    border-top: 1px solid #1E293B;
}

/* TYPING */
.typing {
    display: flex;
    align-items: center;
    gap: 6px;
    color: #94a3b8;
    font-size: 0.95rem;
    margin: 8px 0;
}

.dot {
    width: 6px;
    height: 6px;
    background: #3b82f6;
    border-radius: 50%;
    animation: blink 1.4s infinite both;
}

.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes blink {
    0% { opacity: 0.2; }
    20% { opacity: 1; }
    100% { opacity: 0.2; }
}
</style>
""", unsafe_allow_html=True)

# ======================
# SESSION STATE
# ======================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ======================
# HEADER
# ======================
st.markdown("""
<div class="title-wrapper">
    <span class="title-emoji">🧠</span>
    <span class="title-text">EducaBot — Matemática</span>
</div>
<div class="subtitle">
    Aprenda no seu ritmo. Entenda de verdade. Sem medo de errar.
</div>
""", unsafe_allow_html=True)

st.caption("📚 Seu histórico de aprendizado é mantido durante toda a conversa.")

# ======================
# ONBOARDING
# ======================
if not st.session_state.messages:
    st.session_state.messages.append({
        "role": "assistant",
        "content": (
            "👋 **Oi! Eu sou o EducaBot.**<br><br>"
            "Vou te ajudar a aprender matemática no seu ritmo, sem pressa.<br><br>"
            "<b>Você pode:</b><br>"
            "📘 Mandar um exercício<br>"
            "✏️ Pedir um conteúdo<br>"
            "❓ Dizer: <i>não sei matemática</i><br><br>"
            "Vamos começar? 😊"
        )
    })

# ======================
# CHAT
# ======================
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div class="bot-bubble">
            <div class="bot-header">
                <div class="avatar"></div>
                <b>EducaBot</b>
            </div>
            {msg["content"]}
        </div>
        ''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ======================
# INPUT
# ======================
st.markdown('<div class="input-bar">', unsafe_allow_html=True)
with st.form("chat_form", clear_on_submit=True):
    user_text = st.text_input(
        "",
        placeholder="Digite sua dúvida de matemática…",
        label_visibility="collapsed"
    )
    send = st.form_submit_button("Enviar")
st.markdown('</div>', unsafe_allow_html=True)

# ======================
# STREAMING
# ======================
if send and user_text.strip():
    st.session_state.messages.append({"role": "user", "content": user_text})

    typing_placeholder = st.empty()
    typing_placeholder.markdown("""
    <div class="typing">
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
        <span>EducaBot está digitando…</span>
    </div>
    """, unsafe_allow_html=True)

    bot_placeholder = st.empty()
    full_response = ""
    first_token = True

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Você é o EducaBot, um professor de matemática paciente e didático. "
                    "Explique sempre em passos numerados e claros. "
                    "Use exemplos simples e perguntas de verificação. "
                    "Considere que o ano atual é 2026 e nunca mencione datas antigas."
                )
            },
            *st.session_state.messages
        ],
        stream=True
    )

    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            if first_token:
                typing_placeholder.empty()
                first_token = False

            full_response += delta
            bot_placeholder.markdown(f'''
            <div class="bot-bubble">
                <div class="bot-header">
                    <div class="avatar"></div>
                    <b>EducaBot</b>
                </div>
                {full_response}
            </div>
            ''', unsafe_allow_html=True)

    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response
    })

    st.rerun()
