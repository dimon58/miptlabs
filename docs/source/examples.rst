Примеры выполнения лабораторных работ
=====================================

Измерение магнитного поля соленоида
-----------------------------------

Импортируем нужные библиотеки

.. code:: python

    import miptlabs
    import numpy as np
    import pandas as pd

    from miptlabs.plotter import pretty_plot
    from matplotlib.patches import *

Переписываем таблицу измерений

.. code:: python

    # Измерения для соленоида из 10 плоских магнитов
    data4_2 = pd.DataFrame({
        # Номер магнита
        'n': list(range(1, 20)),

        # Координата на оси соленоида
        'xx': [14.3, 13.6, 12.8, 12.0, 11.2, 10.5, 9.7, 9.0, 8.2, 7.4, 6.7, 5.9, 5.1, 4.3, 3.6, 2.8, 2.0, 1.3, 0.5],

        # Индукция поля
        'B': [14.9, 25.6, 50.3, 127.4, 340, 577.8, 671.2, 691.2, 705.4, 703.5, 685.1, 682.4, 662.1, 580.1, 320.9, 113.5, 47.9, 24.1, 13.8],
    })

    # Пересчет координат
    data4_2['x'] = data4_2['xx'][0] - data4_2['xx']


    R = 1 # радиус соленоида
    L = round(11.2 - 3.9, 1) # длинна соленоида


Эту таблицу сразу можно конвертировать в latex

.. code:: python

    print(miptlabs.latex.tables.gen_from_dataframe(data4_1,
                caption='Зависимость поля диполя от координаты'))

.. code::

    \begin{table}[H]
        \begin{center}
            \begin{tabular}{|c|c|c|c|}
                \hline
                n & xx, см & B, мТл & x, см\\
                \hline
                1 & 14.3 & 14.9 & 0.0\\
                ...
                \hline
            \end{tabular}
        \end{center}
        \caption{Зависимость поля соленоида от координаты}
    \end{table}

Получается такая таблица. Нужно только сделать нужные вам названия столбцов.

Теперь определяем функцию, которой булем аппроксимировать

Это теоретическая формула

.. math::

    B = a \cdot \left( \frac{x}{\sqrt{R^2 + x^2}} + \frac{L - x}{\sqrt{R^2 + (L - x)^2}} \right)

.. code:: python

    # Константа для пересчета координат. Новое начала будет у края соленоида
    offset = round(data4_2['xx'][0] - 11.2, 1)

    # Теоретическая формула для индукции магнитного поля конечного соленоида на его оси
    def dir_cos(l, a):
        l = l - offset
        return a * (l / np.sqrt(R * R + l * l) + (L - l) / np.sqrt(R * R + np.square(L - l)))

Начинаем строить график

.. code:: python

    # Отмечаем измеренные точки
    ax = pretty_plot(data4_2['x'], data4_2['B'], line=False)

Сама аппроксимация

.. code:: python

    apr4_2 = miptlabs.approximators.Functional(dir_cos)
    x_, y_ = data4_2['x'].to_numpy(), data4_2['B'].to_numpy()
    x_, y_ = apr4_2.approximate(x_, y_)
    a = apr4_2.koefs[0]
    legend = rf'$B = {round(a)} \cdot \left( \frac{{x - {offset}}}{{\sqrt{{{R**2} + (x - {offset})^2}}}} + \frac{{{L} - (x - {offset})}}{{\sqrt{{{R**2} + ({L**2} - (x - {offset})^2}}}} \right)$'

Из аппроксиматора можно вытащить значения параметра a, который скорее всего понадобиться в лабораторной еще где-то

.. code:: python

    a = apr4_2.koefs[0]


Атрибут approximator у функции pretty_plot не использовался, так как нужна была легенда.

Теперь строим аппроксимирующую кривую

.. code:: python

    pretty_plot(x_, y_, axes=ax, line=True, points=False, legend=legend, legend_loc='lower center')

И, наконец, отметим область, на которой располагался соленоид.
Результат выполнения функции pretty_plot является экземпляр класса Axes из matplotlib,
поэтому к нему применимо всё из matplotlib.

.. code:: python

    # магнит
    pretty_plot([data4_2['xx'][0] - 3.9]*10, np.linspace(-5, 720, 10), axes=ax, color='red', line=True, points=False)
    pretty_plot([data4_2['xx'][0] - 11.2]*10, np.linspace(-5, 720, 10), axes=ax, color='red', line=True, points=False,
               xlabel='x, см', ylabel='B, мТл'
               )

    rect = Rectangle((data4_2['xx'][0] - 11.2, -5), L, 725, facecolor=(0.1, 0.2, 0.5, 0.1))
    ax.add_patch(rect)

Получается такой график

.. figure:: _static/images/B_x_solenoid.png
       :align: center
       :alt: Результат

В конце нужно сохранить график, для вставки в latex

.. code:: python

    ax.figure.savefig('image_name')