Аппроксимация
=============

Базовые аппроксиматоры
----------------------

.. autoclass:: miptlabs.approximators.Polynomial
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: miptlabs.approximators.Functional
    :members:
    :undoc-members:
    :show-inheritance:

Специальные аппроксиматоры
--------------------------

.. autoclass:: miptlabs.approximators.Linear
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: miptlabs.approximators.Exponential
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: miptlabs.approximators.Logarithmic
    :members:
    :undoc-members:
    :show-inheritance:

Экспериментальные аппроксиматоры
--------------------------------

.. autoclass:: miptlabs.approximators.Lowess
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: miptlabs.approximators.Fourier
    :members:
    :undoc-members:
    :show-inheritance:

Собственный аппроксиматор
-------------------------

.. autoclass:: miptlabs.approximators.base.Approximator
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: miptlabs.approximators.base.MultiLinearMixin
    :members:
    :undoc-members:
    :show-inheritance:

Использование
-------------

Аппроксиматоры можно использовать сами по себе

.. code:: python

    from miptlabs.approximators import Approximator


    apr = Approximator()

    # x, y - какой-то набор данных
    x_, y_ = apr.approximate(x, y)

`x_`, `y_` - аппроксимирующая кривая

Для некоторых аппроксиматоров определен метод label(), который генерирует аппроксимирующую формулу.

.. code:: python

    label = apr.label()

Так же аппросиматоры можно использовать совместно с рисованием графика

.. code:: python

    from miptlabs.approximators import Approximator
    from miptlabs.plotter import pretty_plot


    apr = Approximator()

    pretty_plot(x, y, approximator=apr)

Из apr так же можно вытащить label


Во всех аппроксиматорах есть атрибуты koefs и sigmas

В koefs записываются подогнанные коэффициенты, а в sigmas - стандартные отклонения этих коэффициентов.

Почти все аппроксиматоры умеют считать sigmas, кроме Lowess и Fourier.