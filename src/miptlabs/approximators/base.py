"""
Модуль содержаший базовые апроксиматоры
"""

from warnings import warn

import numpy as np
import scipy.fftpack
import scipy.optimize

from ..utils import round_to_n, format_monoid


class Approximator:
    """
    Базовый класс апроксиматор.
    Классы нужны, чтобы сохранять разные данные, во время апроксимации. Напрмер коэффициенты, ошибки.
    Для некоторых позволяют гененрировать формулу в латехе
    """

    def __init__(self, points=100, left_offset=5, right_offset=5):
        """
        :param points: количество точек, которые будут на выходе
        :param left_offset: отступ от левой гриницы диапозона
        :param right_offset: отступ от правой гриницы диапозона
        """
        self.left_offset = left_offset / 100
        self.right_offset = right_offset / 100
        self.points = points
        self.meta = []

        # Данные
        self._x = np.array([])
        self._y = np.array([])
        self._xerr = np.array([])
        self._yerr = np.array([])

        # Коэффициенты апроксимации
        self.koefs = np.array([])
        # Стандартное отклонение параметров
        self.sigmas = np.array([])

        # Наиболее правдоподобная функция
        self._function = None

    def _gen_x_axis_with_offset(self, start, end):
        """
        Генерирует набор точек по оси абсцисс в заданом диапозоне с учетом отступов.
        Функция нужна для внутрених нужд
        :param start: начало диапозона
        :param end: конец диапозона
        :return:
        """

        delta = end - start

        return np.linspace(start - delta * self.left_offset, end + delta * self.right_offset, self.points)

    def gen_x_axis(self, start, end):
        """
        Генерирует набор точек по оси абсцисс в заданом диапозоне
        :param start: начало диапозона
        :param end: конец диапозона
        :return:
        """
        return np.linspace(start, end, self.points)

    def _prepare_before_approximation(self, x, y, xerr, yerr):
        xerr = np.ones_like(x) * xerr

        if not isinstance(yerr, np.ndarray):
            yerr = np.ones_like(y) * yerr

        self._x = np.array(x)
        self._y = np.array(y)
        self._xerr = xerr
        self._yerr = yerr

        return self._x, self._y, self._xerr, self._yerr

    def approximate(self, x, y, xerr=0, yerr=0):
        """
        Функция апроксимации
        :param x: набор параметров оси x
        :param y: набор параметров оси y
        :param xerr: погрешность параметров оси x
        :param yerr: погрешность параметров оси y
        :return: набор точек на кривой апроксимации
        """
        self._x = np.array(x)
        self._y = np.array(y)
        self._xerr = xerr
        self._yerr = yerr

        return x, y

    def get_function(self):
        """Возвращает полученную функцию"""
        return self._function

    def label(self, xvar='x', yvar='y'):
        """
        Генерирует формулу для латеха
        :param xvar: буква перемонной по оси x
        :param yvar: буква перемонной по оси y
        :return: сгенерированную формулу
        """
        return f'[{self.__class__.__name__}] function with params: {self.meta}'

    def calc_hi_square(self):
        if not self._yerr.all():
            return None

        return np.sum(np.square((self._y - self.get_function()(self._x)) / self._yerr))

    def calc_quality_of_approximation(self):
        if not self._yerr.all():
            return None

        return self.calc_hi_square() / (len(self._x) - len(self.koefs))

    def is_approximation_good(self):
        if not self._yerr.all():
            return 'У ваших измерений по вертикальной оси нет погрешности, ' \
                   'поэтому невозможно пользоваться методом хи-квадрат'

        if len(self._x) - len(self.koefs) <= 0:
            return 'Слишком мало точек для аппроксимации, воспользуйтесь интерполяцией'

        quality_of_approximation = self.calc_quality_of_approximation()

        if 0 < quality_of_approximation <= 0.5:
            return f'Качество ваших измерений составляется {round(quality_of_approximation, 2)} <= 0.5.\n' \
                   f'Это слишком мало, скорее всего это свидетельствуют о завышенных погрешностях.'

        if 0.5 < quality_of_approximation < 2:
            return f'Качество ваших измерений составляется {round(quality_of_approximation, 2)} ~ 1.\n' \
                   f'Это хороший результат. Ваша теоретическая модель хорошо сходится с экспериментом.'

        if 2 <= quality_of_approximation:
            return f'Качество ваших измерений составляется {round(quality_of_approximation, 2)} >= 2.\n' \
                   f'Это слишком много. Это свидетельствуют либо о плохом соответствии \n' \
                   f'теории и результатов измерений, либо о заниженных погрешностях.'


class MultiLinearMixin:
    """
    Добавляет возможность получить функции,
    которая считает значения между двумя точками на прямой в результирующей аппроксимации

    Полезно для аппроксиматоров, которые только двигают точки, например Lowess
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._res_x = None
        self._res_y = None

    def get_function(self):

        def scalar_func(x):
            # При выходе за область определения возбуждаем исключение
            if x < np.min(self._x) or x > np.max(self._x):
                raise AttributeError(
                    f'Значение {x=} выходит за область определения [{np.min(self._x)}, {np.max(self._x)}]')

            # Если есть значение в точке
            idx = np.where(np.isclose(self._x, x))[0]

            if len(idx) != 0:
                return self._res_y[idx[0]]

            # Ищем значение на прямой между двумя ближайшими по оси x точками
            upper_bound = np.where(self._x > x)[0][0]
            # lower_bound = np.where(self._x < x)[0][-1]
            lower_bound = upper_bound - 1

            x1 = self._res_x[lower_bound]
            x2 = self._res_x[upper_bound]

            y1 = self._res_y[lower_bound]
            y2 = self._res_y[upper_bound]

            k = (y2 - y1) / (x2 - x1)
            return k * x + y1 - k * x1

        def vector_func(x):
            # При выходе за область определения возбуждаем исключение
            if np.any(x < np.min(self._x)) or np.any(x > np.max(self._x)):
                raise AttributeError(
                    f'Одна из координат {x=} выходит за область определения [{np.min(self._x)}, {np.max(self._x)}]')

            return np.array([scalar_func(_x_comp) for _x_comp in x])

        def inner(x):
            if isinstance(x, np.ndarray):
                return vector_func(x)

            else:
                return scalar_func(x)

        return inner


class Polynomial(Approximator):
    """
    Апроксимация с помощью полинома
    Получаемая функция
    """

    def __init__(self, deg=1, points=100, left_offset=5, right_offset=5):
        """
        :param deg: степень апроскимируещего полинома
        :param points: количество точек, которые будут на выходе
        :param left_offset: отступ от левой гриницы диапозона
        :param right_offset: отступ от правой гриницы диапозона
        """
        super(Polynomial, self).__init__(points, left_offset, right_offset)
        self.deg = deg

    def approximate(self, x, y, xerr=0, yerr=0):

        x, y, xerr, yerr = self._prepare_before_approximation(x, y, xerr, yerr)

        result = np.polyfit(x, y, deg=self.deg, cov=True)

        popt = result[0]
        pcov = result[-1]

        self.meta = self.meta = {
            'popt': popt,
            'pcov': pcov
        }
        self.koefs = popt
        self.sigmas = np.sqrt(np.diag(pcov))

        self._function = np.poly1d(popt)

        poly = np.poly1d(popt)
        xs = self._gen_x_axis_with_offset(min(x), max(x))

        return xs, poly(xs)

    def label(self, xvar='x', yvar='y'):

        # если степень равна 0, то возвращаем эту константу
        if self.deg == 0:
            return f'${yvar} = {format_monoid(self.koefs[0], True)}$'

        # списисок моноидов
        monoids = []

        # форматируем коэффициент при каждой степени, кроме первой и нулевой
        for i in range(self.deg - 1):
            monoid = f'{format_monoid(self.koefs[i])}{xvar}^{{{self.deg - i}}}'
            monoids.append(monoid)

        # форматируем коэффициент при первой степени
        monoids.append(f'{format_monoid(self.koefs[self.deg - 1])}{xvar}')

        # форматируем коэффициент при нулевой степени
        monoids.append(f'{format_monoid(self.koefs[self.deg])}')

        # объединяем в один полином
        res = ''.join(monoids)

        # убираем плюс при максимальной степени
        # FIXME неоптимизированный костыль с копирование строк
        if self.koefs[0] >= 0:
            res = res[1:]

        return f"${yvar} = {res}$"


class Functional(Approximator):

    def __init__(self, function, points=100, left_offset=5, right_offset=5):
        """
        :param function: функция для апроксимации
        Должна быть в виде f(x, *params), где x - переменная, params - параметры для подгона. например
            def exp(x, a, b, c):
                return a * np.exp(b * x) + c
        У этой функции будут определяться параметры a, b, c
        :param points: количество точек, которые будут на выходе
        :param left_offset: отступ от левой гриницы диапозона
        :param right_offset: отступ от правой гриницы диапозона
        """
        super(Functional, self).__init__(points, left_offset, right_offset)
        self._function_for_fit = function

    def approximate(self, x, y, xerr=0, yerr=0):

        x, y, xerr, yerr = self._prepare_before_approximation(x, y, xerr, yerr)

        # пытаемся аппроксимировать. если у scipy не получается, то оно выбрасывает исключение RuntimeError
        try:
            popt, pcov = scipy.optimize.curve_fit(
                f=self._function_for_fit, xdata=x, ydata=y, sigma=yerr)
            perr = np.sqrt(np.diag(pcov))

            self.meta = {
                'popt': popt,
                'pcov': pcov
            }

            self.koefs = popt
            self.sigmas = perr

            def fff(*params):
                def inner(xx):
                    return self._function_for_fit(xx, *params)

                return inner

            self._function = fff(*self.koefs)

            xs = self._gen_x_axis_with_offset(min(x), max(x))
            ys = self._function_for_fit(xs, *self.koefs)
            return xs, ys

        except RuntimeError:
            # Если вызывается исключение, то возвращаем исходные данные
            warn(f"Точки плохо подходят под апроксимацию выбранной функцией {self._function.__name__}")
            return x, y

    def label(self, xvar='x', yvar='y'):
        try:
            return f'function with params: {[round_to_n(param, 3) for param in self.koefs]}'
        except IndexError:
            return f'Функция {self._function.__name__}, которая плохо подходит'
