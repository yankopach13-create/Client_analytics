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
    (
        "Когортный анализ",
        "https://cohortanalysisbelvape.streamlit.app/",
        "Анализ поведения когорт клиентов",
        "Инструмент для анализа групп клиентов (когорт) по данным из Qlik. Построение матриц возвращаемости на продукт, оттока, присутствия в другом продукте и оттока из сети.",
    ),
]

for name, url, desc, tooltip_text in tools:
    col_info, col_btn = st.columns([0.06, 0.94])
    with col_info:
        st.markdown(
            f'<span title="{tooltip_text}" style="display: inline-flex; align-items: center; justify-content: center; width: 20px; height: 20px; border-radius: 50%; background: #6b7280; color: white; font-size: 12px; font-weight: bold; font-style: italic; cursor: help;">i</span>',
            unsafe_allow_html=True,
        )
    with col_btn:
        st.link_button(f"**{name}** — {desc}", url, use_container_width=True)
