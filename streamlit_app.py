import streamlit as st

st.set_page_config(
    page_title="Клиентский анализ",
    page_icon="👥",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.title("👥 Клиентский анализ")
st.markdown("Выберите инструмент для работы с данными:")
st.markdown("---")

tools = [
    ("Когортный анализ", "https://cohortanalysisbelvape.streamlit.app/", "Анализ поведения когорт клиентов", "Описание будет добавлено"),
]

for name, url, desc, tooltip_text in tools:
    col_info, col_btn = st.columns([0.06, 0.94])
    with col_info:
        with st.tooltip(tooltip_text):
            st.markdown("ℹ️")
    with col_btn:
        st.link_button(f"**{name}** — {desc}", url, use_container_width=True)
