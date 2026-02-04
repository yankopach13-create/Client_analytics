import streamlit as st

st.set_page_config(
    page_title="Клиентский анализ",
    page_icon="👥",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    /* Значок info — i в сером круге */
    [data-testid="stPopover"] > button {
        background-color: #6b7280 !important;
        color: white !important;
        border-radius: 50% !important;
        min-width: 28px !important;
        width: 28px !important;
        padding: 0 !important;
        font-style: italic !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("👥 Клиентский анализ")
st.markdown("Выберите инструмент для работы с данными:")
st.markdown("---")

tools = [
    (
        "Когортный анализ - анализ поведения когорт клиентов",
        "https://cohortanalysisbelvape.streamlit.app/",
        "Инструмент для анализа групп клиентов (когорт) по данным из Qlik. Построение матриц возвращаемости на продукт, оттока, присутствия в другом продукте и оттока из сети.",
    ),
]

for name, url, tooltip_text in tools:
    col_info, col_btn = st.columns([0.06, 0.94])
    with col_info:
        with st.popover("i", help=tooltip_text):
            st.caption(tooltip_text)
    with col_btn:
        st.link_button(name, url, type="primary", use_container_width=True)
