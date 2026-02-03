"""
Конфигурация и константы приложения
"""

# Настройки страницы Streamlit
PAGE_CONFIG = {
    'page_title': 'Когортный анализ',
    'page_icon': '📊',
    'layout': 'wide'
}

# Ожидаемые названия столбцов
EXPECTED_COLUMNS = {
    'Год-месяц': 'Год-месяц',
    'Год-Неделя': 'Год-Неделя',
    'Год-неделя': 'Год-неделя',
    'Год-Месяц': 'Год-Месяц',
    'Код клиента': 'Код клиента'
}

# Словарь месяцев для парсинга
MONTHS_DICT = {
    'янв': 1, 'январь': 1,
    'фев': 2, 'февраль': 2,
    'мар': 3, 'март': 3,
    'апр': 4, 'апрель': 4,
    'май': 5, 'май': 5,
    'июн': 6, 'июнь': 6,
    'июл': 7, 'июль': 7,
    'авг': 8, 'август': 8,
    'сен': 9, 'сентябрь': 9,
    'окт': 10, 'октябрь': 10,
    'ноя': 11, 'ноябрь': 11,
    'дек': 12, 'декабрь': 12
}

# Пути к шрифтам для PDF
WINDOWS_FONTS = [
    r'C:\Windows\Fonts\arial.ttf',
    r'C:\Windows\Fonts\calibri.ttf',
    r'C:\Windows\Fonts\comic.ttf',
    r'C:\Windows\Fonts\cour.ttf',
]

LINUX_FONTS = [
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
    '/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf',
    '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/TTF/DejaVuSans.ttf',
]

# Пути к изображениям шаблонов
TEMPLATE_IMAGE_PATHS = [
    'Qlik.png',
    'qlik_template.png',
    'qlik_template.jpg',
    'qlik_template.jpeg',
    'шаблон_qlik.png',
    'шаблон_qlik.jpg',
    'шаблон_qlik.jpeg',
]

CATEGORIES_TEMPLATE_IMAGE_PATHS = [
    'qlik_template_categories.png',
    'qlik_template_categories.jpg',
    'qlik_template_categories.jpeg',
    'шаблон_qlik_категории.png',
    'шаблон_qlik_категории.jpg',
    'шаблон_qlik_категории.jpeg',
    'churn_categories_template.png',
    'churn_categories_template.jpg',
    'churn_categories_template.jpeg'
]

