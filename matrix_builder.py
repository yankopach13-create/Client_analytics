"""
Модуль для построения различных матриц когортного анализа
"""
import pandas as pd
from utils import parse_period


def build_cohort_matrix(df, year_month_col, client_col, value_type='clients'):
    """Строит когортную матрицу по периоду "Год-месяц".
    
    Args:
        df: DataFrame с данными
        year_month_col: название столбца с годом-месяцем
        client_col: название столбца с кодом клиента
        value_type: тип значений в матрице ('clients' - уникальные клиенты, 'count' - количество записей)
        
    Returns:
        tuple: (matrix_intersection, sorted_periods) - матрица пересечений и отсортированный список периодов
    """
    # Получаем уникальные периоды и сортируем их
    unique_periods = df[year_month_col].dropna().unique()
    
    # Сортируем периоды по году и номеру периода (месяц или неделя)
    periods_with_sort = [(period, parse_period(str(period).strip())) for period in unique_periods]
    
    # Сортируем: сначала по году, потом по типу (месяцы сначала), потом по номеру
    # Периоды с (0, 0, 0) будут в начале, поэтому фильтруем их
    valid_periods = [(p, parsed) for p, parsed in periods_with_sort if parsed != (0, 0, 0)]
    invalid_periods = [p for p, parsed in periods_with_sort if parsed == (0, 0, 0)]
    
    if valid_periods:
        valid_periods.sort(key=lambda x: (x[1][0], x[1][2], x[1][1]))  # (year, type, number)
        sorted_periods = [period[0] for period in valid_periods]
        
        # Добавляем нераспознанные периоды в конец (если есть)
        if invalid_periods:
            sorted_periods.extend(sorted(invalid_periods))
    else:
        # Если все периоды не распознаны, используем просто сортировку по строке
        sorted_periods = sorted([str(p) for p in unique_periods])
    
    # Оптимизация: предварительно группируем данные по периодам
    # Создаем словарь: период -> множество клиентов
    period_clients = {}
    for period in sorted_periods:
        period_data = df[df[year_month_col] == period]
        if value_type == 'clients':
            period_clients[period] = set(period_data[client_col].dropna().unique())
        else:
            # Для count просто сохраняем количество
            period_clients[period] = len(period_data)
    
    # Создаем матрицу пересечений клиентов
    matrix_intersection = pd.DataFrame(
        index=sorted_periods,
        columns=sorted_periods,
        dtype=int
    )
    
    # Заполняем матрицу используя предварительно вычисленные множества
    for row_period in sorted_periods:
        for col_period in sorted_periods:
            if row_period == col_period:
                # Диагональ - клиенты в этом периоде
                if value_type == 'clients':
                    matrix_intersection.loc[row_period, col_period] = len(period_clients[row_period])
                else:
                    matrix_intersection.loc[row_period, col_period] = period_clients[row_period]
            else:
                # Пересечение клиентов между двумя периодами
                if value_type == 'clients':
                    clients_row = period_clients[row_period]
                    clients_col = period_clients[col_period]
                    intersection = len(clients_row & clients_col)
                    matrix_intersection.loc[row_period, col_period] = intersection
                else:
                    # Для count это не имеет смысла, но оставляем для совместимости
                    matrix_intersection.loc[row_period, col_period] = 0
    
    return matrix_intersection, sorted_periods


def build_accumulation_matrix(df, year_month_col, client_col, sorted_periods):
    """Строит матрицу накопления возврата клиентов.
    
    Накопление идет только с периода СЛЕДУЮЩЕГО за периодом когорты (без самого периода когорты).
    
    Args:
        df: DataFrame с данными
        year_month_col: название столбца с годом-месяцем
        client_col: название столбца с кодом клиента
        sorted_periods: отсортированный список периодов
        
    Returns:
        pd.DataFrame: матрица накопления уникальных клиентов
    """
    matrix_accumulation = pd.DataFrame(
        index=sorted_periods,
        columns=sorted_periods,
        dtype=int
    )
    
    # Оптимизация: предварительно создаем словарь период -> множество клиентов
    period_clients_dict = {}
    for period in sorted_periods:
        period_data = df[df[year_month_col] == period]
        period_clients_dict[period] = set(period_data[client_col].dropna().unique())
    
    # Получаем индекс каждого периода для определения порядка
    period_indices = {period: idx for idx, period in enumerate(sorted_periods)}
    
    for row_period in sorted_periods:
        row_idx = period_indices[row_period]
        
        # Получаем множество клиентов этой когорты (в первом периоде когорты)
        cohort_clients = period_clients_dict[row_period]
        
        # Предварительно вычисляем накопление для всех последующих периодов
        accumulated_clients_by_period = {}
        current_accumulated = set()
        
        for col_idx in range(row_idx, len(sorted_periods)):
            col_period = sorted_periods[col_idx]
            
            if col_idx == row_idx:
                # Диагональ - клиенты в первом периоде когорты
                matrix_accumulation.loc[row_period, col_period] = len(cohort_clients)
                accumulated_clients_by_period[col_period] = set(cohort_clients)
            elif col_idx > row_idx:
                # Добавляем клиентов из текущего периода к накопленным
                period_clients = period_clients_dict[col_period]
                cohort_period_clients = period_clients & cohort_clients
                current_accumulated.update(cohort_period_clients)
                accumulated_clients_by_period[col_period] = set(current_accumulated)
                matrix_accumulation.loc[row_period, col_period] = len(current_accumulated)
        
        # Заполняем нулями периоды до начала когорты
        for col_idx in range(row_idx):
            col_period = sorted_periods[col_idx]
            matrix_accumulation.loc[row_period, col_period] = 0
    
    return matrix_accumulation


def build_accumulation_percent_matrix(accumulation_matrix, cohort_matrix):
    """Строит матрицу накопления возврата в процентах.
    
    Доля накопления количества клиентов от количества клиентов в когорте.
    
    Args:
        accumulation_matrix: матрица накопления (абсолютные значения)
        cohort_matrix: исходная когортная матрица (для получения количества клиентов в когорте)
        
    Returns:
        pd.DataFrame: матрица в процентах
    """
    matrix_percent = pd.DataFrame(
        index=accumulation_matrix.index,
        columns=accumulation_matrix.columns,
        dtype=float
    )
    
    # Получаем индексы периодов для определения порядка
    period_indices = {period: idx for idx, period in enumerate(accumulation_matrix.index)}
    
    for row_period in accumulation_matrix.index:
        row_idx = period_indices.get(row_period, 0)
        
        # Количество клиентов в когорте (диагональ)
        cohort_size = cohort_matrix.loc[row_period, row_period]
        
        for col_period in accumulation_matrix.columns:
            col_idx = period_indices.get(col_period, 0)
            
            if col_idx < row_idx:
                # До диагонали = 0
                matrix_percent.loc[row_period, col_period] = 0.0
            elif col_idx == row_idx:
                # Диагональ = 100% (все клиенты когорты)
                matrix_percent.loc[row_period, col_period] = 100.0
            else:
                # После диагонали = процент от размера когорты
                if cohort_size > 0:
                    accumulated = accumulation_matrix.loc[row_period, col_period]
                    percent = (accumulated / cohort_size) * 100
                    matrix_percent.loc[row_period, col_period] = percent
                else:
                    matrix_percent.loc[row_period, col_period] = 0.0
    
    return matrix_percent


def build_inflow_matrix(accumulation_percent_matrix):
    """Строит матрицу притока возврата в процентах.
    
    Показывает прирост уникальных клиентов когорты между периодами.
    
    Args:
        accumulation_percent_matrix: матрица накопления в процентах
        
    Returns:
        pd.DataFrame: матрица притока в процентах
    """
    inflow_matrix = pd.DataFrame(
        index=accumulation_percent_matrix.index,
        columns=accumulation_percent_matrix.columns,
        dtype=float
    )
    
    # Получаем индексы периодов для определения порядка
    period_indices = {period: idx for idx, period in enumerate(accumulation_percent_matrix.index)}
    
    for row_period in accumulation_percent_matrix.index:
        row_idx = period_indices.get(row_period, 0)
        
        for col_period in accumulation_percent_matrix.columns:
            col_idx = period_indices.get(col_period, 0)
            
            # Диагональ = 0%
            if row_idx == col_idx:
                inflow_matrix.loc[row_period, col_period] = 0.0
            elif col_idx < row_idx:
                # До диагонали = 0
                inflow_matrix.loc[row_period, col_period] = 0.0
            else:
                # Первый столбец после диагонали = значение из матрицы накопления
                if col_idx == row_idx + 1:
                    inflow_matrix.loc[row_period, col_period] = accumulation_percent_matrix.loc[row_period, col_period]
                else:
                    # Остальные столбцы = разница между текущим и предыдущим значением
                    current_val = accumulation_percent_matrix.loc[row_period, col_period]
                    # Находим предыдущий период
                    prev_period = accumulation_percent_matrix.columns[col_idx - 1]
                    prev_val = accumulation_percent_matrix.loc[row_period, prev_period]
                    inflow_matrix.loc[row_period, col_period] = current_val - prev_val
    
    return inflow_matrix



