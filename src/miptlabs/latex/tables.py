from typing import List

from pandas import DataFrame


def _gen_vertical_table(df, caption, header, line_names, index, index_start):
    col_count = len(df.columns)

    cols = ''.join(['c|' for i in range(col_count)])

    # -------------begin-------------
    index_col = ''
    if index:
        index_col = 'c|'

    header_col = ''
    if header:
        header_col = f'\t\t\t\\hline\n' \
                     f'\t\t\t\\multicolumn{{{col_count}}}{{|c|}}{{{header}}}\\\\\n'

    table_begin = f'\\begin{{table}}[H]\n' \
                  f'\t\\begin{{center}}\n' \
                  f'\t\t\\begin{{tabular}}{{|{index_col}{cols}}}\n' \
                  f'{header_col}' \
                  f'\t\t\t\\hline\n'

    # -------------body-------------
    if line_names:
        body = ' & '.join(line_names)

    else:
        body = ' & '.join(df.columns)

    body += '\\\\\n\t\t\t\\hline\n'

    if index:
        body = '\t\t\tN & ' + body
    else:
        body = '\t\t\t' + body

    if index:
        for num, i in enumerate(df.values):
            body += f'\t\t\t{num + index_start} & ' + ' & '.join([str(elem) for elem in i]) + '\\\\\n\t\t\t\\hline\n'

    else:
        for num, i in enumerate(df.values):
            body += '\t\t\t' + ' & '.join([str(elem) for elem in i]) + '\\\\\n\t\t\t\\hline\n'

    # -------------caption-------------
    caption_text = ''
    if caption is not None:
        caption_text = f'\t\\caption{{{caption}}}\n'

    # -------------end-------------
    table_end = f'\t\t\\end{{tabular}}\n' \
                f'\t\\end{{center}}\n' \
                f'{caption_text}' \
                f'\\end{{table}}'

    return f'{table_begin}{body}{table_end}'


def _gen_horizontal_table(df, caption, header, line_names, index, index_start):
    # -------------begin-------------
    cols = len(df.index) + 1  # +1, так как сбоку заголовок

    header_col = ''
    if header:
        header_col = f'\t\t\t\\hline\n' \
                     f'\t\t\t\\multicolumn{{{cols}}}{{|c|}}{{{header}}}\\\\\n'

    table_begin = f'\\begin{{table}}[H]\n' \
                  f'\t\\begin{{center}}\n' \
                  f'\t\t\\begin{{tabular}}{{|{"c|" * cols}}}\n' \
                  f'{header_col}' \
                  f'\t\t\t\\hline\n'

    # -------------body-------------

    body = ""

    if index:
        body += '\t\t\t& ' + ' & '.join(
            [str(i) for i in range(index_start, cols + index_start - 1)]) + ' \\\\\n\t\t\t\\hline\n'

    for num, row in enumerate(df):
        line_names_element = row

        if line_names:
            line_names_element = line_names[num]

        body += f'\t\t\t{line_names_element} & ' + ' & '.join([str(i) for i in df[row]]) + ' \\\\\n\t\t\t\\hline\n'

    # -------------caption-------------
    caption_text = ''
    if caption is not None:
        caption_text = f'\t\\caption{{{caption}}}\n'

    # -------------end-------------
    table_end = f'\t\t\\end{{tabular}}\n' \
                f'\t\\end{{center}}\n' \
                f'{caption_text}' \
                f'\\end{{table}}'

    return f'{table_begin}{body}{table_end}'


def gen_from_dataframe(df: DataFrame,
                       caption: str = None, header: List[str] = None, line_names: List[str] = None,
                       index: bool = False, index_start: int = 1, horizontal: bool = False) -> str:
    """
    Генерирует таблицу latex из DataFame.
    Нужно лишь дописать свой заголовок таблицы (хотя можно оставить сгенерированный)

    По умолчанию в заголовке находятся имена столбцов из pandas.

    :param df: dataframe из pandas
    :param caption: название таблицы
    :param header: заголовок таблицы, располагается сверху всех строк и размером со все столбцы
    :param line_names: названий столбцов/строк в таблице
    :param index: нужна ли индексация
    :param index_start: начала индексации, по умолчанию 1
    :param horizontal: нужно ли строить горизонтальную таблицу

    :return: строку, содержащую таблицу latex, которую можно вставить в редактор
    """
    if horizontal:
        return _gen_horizontal_table(df, caption, header, line_names, index, index_start)

    else:
        return _gen_vertical_table(df, caption, header, line_names, index, index_start)
