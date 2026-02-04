import streamlit as st

st.set_page_config(
    page_title="Клиентский анализ",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.title("📊 Клиентский анализ")
st.markdown("Выберите инструмент для работы с данными:")
st.markdown("---")

tools = [
    ("Когортный анализ", "https://cohortanalysisbelvape.streamlit.app/", "Анализ поведения когорт клиентов"),
]

for name, url, desc in tools:
    st.markdown(f"[**{name}** — {desc}]({url})")
