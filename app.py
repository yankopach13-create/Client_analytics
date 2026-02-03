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
    <div style="text-align: center; padding: 20px; border: 2px solid #4CAF50; border-radius: 10px; background: #f1f8f4;">
        <h2>📊 Когортный анализ</h2>
        <p>Анализ возвращаемости и оттока клиентов</p>
        <p style="color: #4CAF50; font-weight: bold; margin-top: 10px;">✓ Доступен</p>
    </div>
    """, unsafe_allow_html=True)
    # Используем кнопку Streamlit для навигации
    if st.button("📊 Открыть когортный анализ", use_container_width=True, type="primary", key="cohort_nav"):
        # Используем правильный формат для Streamlit Pages
        try:
            # Формат: имя файла без расширения, с префиксом pages/
            st.switch_page("pages/1__Когортный_анализ")
        except Exception as e:
            # Если не работает, показываем сообщение
            st.error(f"Не удалось перейти на страницу: {str(e)}. Используйте боковое меню слева для навигации.")

with col2:
    st.markdown("""
    <div style="text-align: center; padding: 20px; border: 2px solid #e0e0e0; border-radius: 10px; background: #f8f9fa;">
        <h2>🔄 Цикл жизни клиента</h2>
        <p>Анализ жизненного цикла клиента на продукте</p>
        <p style="color: #999; font-size: 0.9em; margin-top: 10px;">🚧 В разработке</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="text-align: center; padding: 20px; border: 2px solid #e0e0e0; border-radius: 10px; background: #f8f9fa;">
        <h2>📈 Другие инструменты</h2>
        <p>Дополнительные аналитические инструменты</p>
        <p style="color: #999; font-size: 0.9em; margin-top: 10px;">🚧 В разработке</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.info("💡 Нажмите на карточку инструмента для перехода к нему")
