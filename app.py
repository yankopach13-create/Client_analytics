import streamlit as st

# Настройка страницы
st.set_page_config(
    page_title="Аналитика клиентов",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Аналитика клиентов")
st.markdown("---")

st.markdown("""
### Выберите инструмент для анализа:
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="text-align: center; padding: 20px; border: 2px solid #e0e0e0; border-radius: 10px; background: #f8f9fa;">
        <h2>📊 Когортный анализ</h2>
        <p>Анализ возвращаемости и оттока клиентов</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("📊 Когортный анализ", use_container_width=True, type="primary", key="cohort_analysis"):
        st.switch_page("pages/1__Когортный_анализ.py")

with col2:
    st.markdown("""
    <div style="text-align: center; padding: 20px; border: 2px solid #e0e0e0; border-radius: 10px; background: #f8f9fa;">
        <h2>🔄 Цикл жизни клиента</h2>
        <p>Анализ жизненного цикла клиента на продукте</p>
        <p style="color: #999; font-size: 0.9em;">Скоро</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔄 Цикл жизни клиента", use_container_width=True, key="lifecycle"):
        st.switch_page("pages/2_🔄_Цикл_жизни_клиента.py")

with col3:
    st.markdown("""
    <div style="text-align: center; padding: 20px; border: 2px solid #e0e0e0; border-radius: 10px; background: #f8f9fa;">
        <h2>📈 Другие инструменты</h2>
        <p>Дополнительные аналитические инструменты</p>
        <p style="color: #999; font-size: 0.9em;">Скоро</p>
    </div>
    """, unsafe_allow_html=True)
    st.button("📈 Другие инструменты", use_container_width=True, disabled=True, key="other")

st.markdown("---")
st.info("💡 Используйте боковое меню для быстрой навигации между инструментами")
