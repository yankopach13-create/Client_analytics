"""
Модуль для UI компонентов и форматирования
"""
import pandas as pd


def color_gradient(val, min_val, max_val, mean_val, is_diagonal=False):
    """Применяет четкий градиент от красного (минимум) через желтый (среднее) к зеленому (максимум).
    
    Если is_diagonal=True, возвращает белый фон без цвета.
    
    Args:
        val: значение для форматирования
        min_val: минимальное значение
        max_val: максимальное значение
        mean_val: среднее значение
        is_diagonal: флаг диагонального элемента
        
    Returns:
        str: CSS стиль для ячейки
    """
    # Диагональные значения (сама когорта) - без цвета, жирный шрифт, по центру
    if is_diagonal:
        return 'background-color: white; color: black; font-weight: bold; text-align: center'
    
    if pd.isna(val) or val == 0:
        return 'background-color: white; color: black; text-align: center'
    
    # Если значение меньше или равно среднему - градиент от красного к желтому
    if val <= mean_val:
        # Градиент от красного (255,0,0) к желтому (255,255,0)
        if mean_val == min_val:
            ratio = 1.0  # Все значения равны минимуму, делаем желтым
        else:
            ratio = (val - min_val) / (mean_val - min_val)
            ratio = max(0, min(1, ratio))  # Ограничиваем от 0 до 1
        
        # Красный -> Желтый: R=255 постоянный, G растет от 0 до 255, B=0 постоянный
        r = 255
        g = int(255 * ratio)  # от 0 до 255
        b = 0
    else:
        # Градиент от желтого (255,255,0) к зеленому (0,255,0)
        if max_val == mean_val:
            ratio = 1.0  # Все значения равны среднему, делаем зеленым
        else:
            ratio = (val - mean_val) / (max_val - mean_val)
            ratio = max(0, min(1, ratio))  # Ограничиваем от 0 до 1
        
        # Желтый -> Зеленый: R убывает от 255 до 0, G=255 постоянный, B=0 постоянный
        r = int(255 * (1 - ratio))  # от 255 до 0
        g = 255
        b = 0
    
    # Всегда используем чёрный цвет текста и выравнивание по центру
    return f'background-color: rgb({r},{g},{b}); color: black; text-align: center'


def apply_matrix_color_gradient(df, hide_zeros=False, horizontal_dynamics=False, hide_before_diagonal=False):
    """Применяет цветовое форматирование к матрице.
    
    Диагональные значения (сама когорта) отображаются без цвета, жирным шрифтом.
    
    Args:
        df: DataFrame для форматирования
        hide_zeros: если True, нулевые значения скрываются (пустая строка)
        horizontal_dynamics: если True, градиент рассчитывается по каждой строке отдельно
        hide_before_diagonal: если True, скрываются все значения до диагонали (для горизонтальной динамики)
        
    Returns:
        Styler: отформатированный DataFrame
    """
    # Получаем индексы периодов для определения порядка
    period_indices = {period: idx for idx, period in enumerate(df.index)}
    
    # Если нужно скрывать нули или значения до диагонали, заменяем значения на пустую строку перед форматированием
    df_display = df.copy()
    if hide_zeros or hide_before_diagonal:
        for row_name in df_display.index:
            row_idx = period_indices.get(row_name, 0)
            for col_name in df_display.columns:
                col_idx = period_indices.get(col_name, 0)
                is_diagonal = (row_name == col_name)
                
                # Скрываем значения до диагонали (если период меньше когорты)
                if hide_before_diagonal and not is_diagonal and col_idx < row_idx:
                    df_display.loc[row_name, col_name] = ''
                # Скрываем нулевые значения
                elif hide_zeros and not is_diagonal and (pd.isna(df_display.loc[row_name, col_name]) or df_display.loc[row_name, col_name] == 0):
                    df_display.loc[row_name, col_name] = ''
    
    # Применяем форматирование с учетом позиции (диагональные значения без цвета)
    def format_with_diagonal(x):
        """Применяет форматирование с учетом диагонали"""
        result = pd.DataFrame(index=x.index, columns=x.columns, dtype=object)
        
        # Получаем индексы для определения порядка в функции форматирования
        period_indices_format = {period: idx for idx, period in enumerate(x.index)}
        
        for row_name in x.index:
            row_idx_format = period_indices_format.get(row_name, 0)
            
            # Для горизонтальной динамики рассчитываем min/max/mean для каждой строки отдельно
            if horizontal_dynamics:
                row_values = []
                for col_name in x.columns:
                    col_idx_format = period_indices_format.get(col_name, 0)
                    # Учитываем только значения после диагонали (если hide_before_diagonal включен) или все недиагональные
                    if row_name != col_name and (not hide_before_diagonal or col_idx_format >= row_idx_format):
                        val = x.loc[row_name, col_name]
                        val_for_calc = 0 if (val == '' or pd.isna(val)) else val
                        if val_for_calc != 0:
                            row_values.append(val_for_calc)
                
                if row_values:
                    row_min = min(row_values)
                    row_max = max(row_values)
                    row_mean = sum(row_values) / len(row_values)
                else:
                    row_min = 0
                    row_max = 0
                    row_mean = 0
            else:
                # Глобальный расчет для всей таблицы (исключая диагональ)
                non_diagonal_values = []
                for r_name in x.index:
                    for c_name in x.columns:
                        if r_name != c_name:
                            val = x.loc[r_name, c_name]
                            # Преобразуем значение в число, если это строка с процентом
                            if isinstance(val, str):
                                # Пытаемся извлечь число из строки типа "45.7%"
                                try:
                                    val_for_calc = float(val.replace('%', '').strip())
                                except (ValueError, AttributeError):
                                    val_for_calc = 0
                            else:
                                val_for_calc = 0 if (val == '' or pd.isna(val)) else float(val)
                            
                            if val_for_calc != 0:
                                non_diagonal_values.append(val_for_calc)
                
                if non_diagonal_values:
                    row_min = min(non_diagonal_values)
                    row_max = max(non_diagonal_values)
                    row_mean = sum(non_diagonal_values) / len(non_diagonal_values)
                else:
                    row_min = 0
                    row_max = 0
                    row_mean = 0
            
            for col_name in x.columns:
                val = x.loc[row_name, col_name]
                is_diagonal = (row_name == col_name)
                
                # Если значение пустое (скрытое), применяем прозрачный стиль
                col_idx_display = period_indices.get(col_name, 0)
                row_idx_display = period_indices.get(row_name, 0)
                
                is_hidden = (
                    (hide_zeros and not is_diagonal and (val == '' or pd.isna(val) or val == 0)) or
                    (hide_before_diagonal and not is_diagonal and col_idx_display < row_idx_display)
                )
                
                if is_hidden:
                    result.loc[row_name, col_name] = 'background-color: white; color: white; text-align: center'
                else:
                    # Преобразуем значение для расчета цвета
                    # Если значение - строка с процентом, извлекаем число
                    if isinstance(val, str) and '%' in val:
                        try:
                            val_for_color = float(val.replace('%', '').strip())
                        except (ValueError, AttributeError):
                            val_for_color = 0
                    else:
                        val_for_color = 0 if (val == '' or pd.isna(val)) else float(val) if not isinstance(val, str) else 0
                    
                    gradient_style = color_gradient(val_for_color, row_min, row_max, row_mean, is_diagonal)
                    # Добавляем выравнивание по центру (если еще не добавлено)
                    if 'text-align' not in gradient_style:
                        gradient_style += '; text-align: center'
                    result.loc[row_name, col_name] = gradient_style
        return result
    
    styled_df = df_display.style.apply(format_with_diagonal, axis=None)
    
    return styled_df

