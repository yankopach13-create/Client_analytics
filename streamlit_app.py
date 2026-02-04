import streamlit as st

st.set_page_config(
    page_title="Клиентский анализ",
    page_icon="👥",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    .info-wrapper {
        position: relative;
        display: inline-flex;
        align-items: center;
    }
    .info-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: #6b7280;
        color: white;
        font-size: 12px;
        font-weight: bold;
        font-style: italic;
        cursor: help;
    }
    .info-tooltip {
        visibility: hidden;
        opacity: 0;
        position: absolute;
        right: 100%;
        top: 50%;
        transform: translateY(-50%);
        margin-right: 10px;
        padding: 14px 18px;
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 10px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.15), 0 2px 8px rgba(0,0,0,0.08);
        font-size: 14px;
        line-height: 1.55;
        width: 420px;
        max-width: 90vw;
        z-index: 9999;
        border: 1px solid #e2e8f0;
        color: #334155;
        transition: opacity 0.2s ease, visibility 0.2s ease;
    }
    .info-tooltip::before {
        content: '';
        position: absolute;
        right: -6px;
        left: auto;
        top: 50%;
        transform: translateY(-50%);
        border: 6px solid transparent;
        border-left-color: #e2e8f0;
    }
    .info-wrapper:hover .info-tooltip {
        visibility: visible;
        opacity: 1;
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
        st.markdown(
            f'<div class="info-wrapper"><span class="info-icon">i</span><span class="info-tooltip">{tooltip_text}</span></div>',
            unsafe_allow_html=True,
        )
    with col_btn:
        st.link_button(name, url, use_container_width=True)
