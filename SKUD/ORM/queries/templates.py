
def query_for_table(table: str, cols: list[str], interval: tuple[int, int], order_column: str, desc: bool):
    '''Формирует запрос для таблицы `table` для столбцов `cols`, который берет записи, отсортированные по order_column 
    в порядке убывания, если `dirction` - true, иначе в порядке возрастания.
    Записи и берутся начиная с `interval[0]` по `interval[1]`. Последний столбец у всех записей - ее номер.'''
    return f'''SELECT {','.join(cols)}, 
                      ROW_NUMBER() OVER (ORDER BY {order_column}) 
                            BETWEEN 0 AND 100 AS RowNum 
                                FROM {table} ORDER BY {order_column} {'DESC' if desc else ''};'''

# def join_query(table: str, join_table: str, join_columns: tuple[str, str]):
#     query = f'''SELECT {str(rows)[1:-1]} FROM {table}'''
#     for table in tables:
#         query += f'''SELECT {str(rows)[1:-1]} FROM {table}'''
#     return

def condition_query(table: str, cols: list[str], condition: str):
    return f"SELECT {','.join(cols)} FROM {table} WHERE {condition}"

def sort_query(table: str):
    pass
