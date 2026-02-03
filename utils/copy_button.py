"""Модуль для создания кнопки копирования в буфер обмена"""
import streamlit.components.v1 as components
import json
import re


def create_copy_button(text, button_label, key):
    """Создает кнопку для копирования текста в буфер обмена"""
    # Очищаем key от специальных символов для использования в JavaScript
    safe_key = re.sub(r'[^a-zA-Z0-9_]', '_', str(key))
    
    # Экранируем текст для безопасной вставки в JavaScript
    # Используем JSON для правильного экранирования
    text_json = json.dumps(text)
    
    html = f"""
    <div data-testid="stButton" style="width: 100%; margin: 5px 0;">
        <button id="copy_btn_{safe_key}" onclick="copyToClipboard_{safe_key}()" style="
            width: 100%;
            padding: 12px 16px;
            background: #f8f9fa !important;
            color: #333 !important;
            border: 2px solid #e0e0e0 !important;
            border-radius: 8px !important;
            cursor: pointer !important;
            font-weight: 400 !important;
            font-size: 0.85rem !important;
            line-height: 1.3 !important;
            text-align: center !important;
            min-height: 50px !important;
            height: auto !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            white-space: normal !important;
            word-wrap: break-word !important;
            overflow-wrap: break-word !important;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05) !important;
            transition: all 0.3s ease !important;
            margin: 0 !important;
            box-sizing: border-box !important;
            position: relative !important;
        " onmouseover="if (!this.classList.contains('copied')) {{ this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 8px rgba(0, 0, 0, 0.1)'; this.style.background='#ffffff'; this.style.borderColor='#d0d0d0'; }}" onmouseout="if (!this.classList.contains('copied')) {{ this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 4px rgba(0, 0, 0, 0.05)'; this.style.background='#f8f9fa'; this.style.borderColor='#e0e0e0'; }}" onmousedown="if (!this.classList.contains('copied')) {{ this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 4px rgba(0, 0, 0, 0.05)'; }}" onmouseup="if (!this.classList.contains('copied')) {{ this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 8px rgba(0, 0, 0, 0.1)'; }}">
            <div style="display: flex; align-items: center; justify-content: center; width: 100%;">
                <p id="copy_btn_text_{safe_key}" style="margin: 0; padding: 0; font-size: 0.85rem; font-weight: 400; line-height: 1.3; word-wrap: break-word; overflow-wrap: break-word; white-space: normal;">{button_label}</p>
            </div>
        </button>
        <style>
            @keyframes pulse {{
                0% {{ transform: scale(1); }}
                50% {{ transform: scale(1.05); }}
                100% {{ transform: scale(1); }}
            }}
        </style>
    </div>
    <script>
        const textToCopy_{safe_key} = {text_json};
        
        function copyToClipboard_{safe_key}() {{
            const text = textToCopy_{safe_key};
            const button = document.getElementById('copy_btn_{safe_key}');
            const buttonText = document.getElementById('copy_btn_text_{safe_key}');
            const originalText = buttonText.innerHTML;
            
            // Функция для показа успешного копирования
            function showSuccess() {{
                // Изменяем внешний вид кнопки
                button.classList.add('copied');
                button.style.background = 'linear-gradient(135deg, #4CAF50 0%, #45a049 100%)';
                button.style.borderColor = '#4CAF50';
                button.style.color = 'white';
                button.style.transform = 'scale(0.98)';
                buttonText.innerHTML = '✓ Скопировано!';
                
                // Возвращаем исходное состояние через 2.5 секунды
                setTimeout(function() {{
                    button.classList.remove('copied');
                    button.style.background = '#f8f9fa';
                    button.style.borderColor = '#e0e0e0';
                    button.style.color = '#333';
                    button.style.transform = 'translateY(0)';
                    buttonText.innerHTML = originalText;
                }}, 2500);
            }}
            
            // Пробуем использовать современный API
            if (navigator.clipboard && navigator.clipboard.writeText) {{
                navigator.clipboard.writeText(text).then(function() {{
                    showSuccess();
                }}).catch(function(err) {{
                    console.error('Clipboard API error:', err);
                    // Fallback на старый метод
                    fallbackCopy_{safe_key}(text, showSuccess);
                }});
            }} else {{
                // Fallback для старых браузеров
                fallbackCopy_{safe_key}(text, showSuccess);
            }}
        }}
        
        function fallbackCopy_{safe_key}(text, successCallback) {{
            const textarea = document.createElement('textarea');
            textarea.value = text;
            textarea.style.position = 'fixed';
            textarea.style.left = '-999999px';
            textarea.style.top = '-999999px';
            textarea.style.opacity = '0';
            document.body.appendChild(textarea);
            textarea.focus();
            textarea.select();
            
            try {{
                const successful = document.execCommand('copy');
                if (successful) {{
                    successCallback();
                }} else {{
                    alert('Не удалось скопировать. Пожалуйста, скопируйте вручную.');
                }}
            }} catch(err) {{
                console.error('Copy command error:', err);
                alert('Ошибка копирования: ' + err);
            }} finally {{
                document.body.removeChild(textarea);
            }}
        }}
    </script>
    """
    components.html(html, height=70)

