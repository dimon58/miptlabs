import numpy as np
import scipy.fftpack
import scipy.optimize

from . import functions
from .base import Polynomial, Functional, Approximator, MultiLinearMixin
from ..utils import round_to_n, format_monoid


class Linear(Polynomial):
    """
    Аппроксимация с помощью прямой y=kx+b. Использует numpy.polyfit
    """

    def __init__(self, points=100, left_offset=5, right_offset=5, no_bias=False):
        """
        :param points: количество точек, которые будут на выходе
        :param left_offset: отступ  от правой границы диапазона
        :param right_offset: отступ, то свободного коэффициента нет, иначе есть
        :param no_bias: Если *True* от левой границы диапазона
        """
        super(Linear, self).__init__(1, points, left_offset, right_offset)
        self.no_bias = no_bias

        # Данные
        self.__k = None
        self.__b = None

    def approximate(self, x, y, xerr=0, yerr=0):

        x, y, xerr, yerr = self._prepare_before_approximation(x, y, xerr, yerr)

        if not self.no_bias:
            return super(Linear, self).approximate(x, y)

        else:
            # fixme: убрать дублирование кода
            popt, pcov = scipy.optimize.curve_fit(
                f=functions.line_for_fit, xdata=x, ydata=y, sigma=yerr)
            perr = np.sqrt(np.diag(pcov))

            self.meta = {
                'popt': popt,
                'pcov': pcov
            }

            self.koefs = popt
            self.sigmas = perr

            self._function = functions.line(popt[0])

            xs = self._gen_x_axis_with_offset(min(x), max(x))
            ys = self._function(xs)
            return xs, ys

    def label(self, xvar='x', yvar='y'):
        res = f'{format_monoid(self.koefs[0])}{xvar}'

        if not self.no_bias:
            res += format_monoid(self.koefs[1])

        # убираем плюс при максимальной степени
        # FIXME неоптимизированный костыль с копирование строк
        if self.koefs[0] >= 0:
            res = res[1:]

        return f"${yvar} = {res}$"

    def _brac_x(self):
        return self._x.mean()

    def _brac_y(self):
        return self._y.mean()

    def _brac_x2(self):
        return (self._x * self._x).mean()

    def _brac_y2(self):
        return (self._y * self._y).mean()

    def _brac_xy(self):
        return (self._x * self._y).mean()

    def _d_xy(self):
        return (self._x - self._x.mean()).mean() * (self._y - self._y.mean()).mean()

    def _d_xx(self):
        return np.square(self._x - self._x.mean()).mean()

    def _d_yy(self):
        return np.square(self._y - self._y.mean()).mean()

    def _k(self):
        self.__k = (self._brac_xy() - self._brac_x() * self._brac_y()) / (self._brac_x2() - self._brac_x() ** 2)
        return self.__k

    def _b(self):
        if self.__k is None:
            self._k()

        self.__b = self._brac_y() - self.__k * self._brac_x()
        return self.__b

    def _sigma_k(self):
        if self.__k is None:
            self._k()

        if len(self._x) == 2:
            return 0

        return np.sqrt(np.abs((self._d_yy() / self._d_xx() - self._k() ** 2) / (len(self._x) - 2)))

    def _sigma_b(self):
        if self.__b is None:
            self._b()

        return self._sigma_k() * np.sqrt(self._brac_x2())


class Exponential(Functional):
    """
    Экспоненциальный апроксиматор
    y = a*exp(bx)+c
    """

    def __init__(self, points=100, left_offset=5, right_offset=5):
        """
        :param points: количество точек, которые будут на выходе
        :param left_offset: отступ  от правой границы диапазона
        :param right_offset: отступ, то свободного коэффициента нет, иначе есть
        """
        super(Exponential, self).__init__(
            function=functions.exp_for_fit,
            points=points,
            left_offset=left_offset,
            right_offset=right_offset
        )

    def label(self, xvar='x', yvar='y'):
        try:
            return f'${yvar} = {format_monoid(round_to_n(self.koefs[0], 3), True)}' \
                   f'e^{{{round_to_n(self.koefs[1], 3)}{xvar}}} ' \
                   f'{format_monoid(round_to_n(self.koefs[2], 3))}$'
        except TypeError:
            return 'Экспонента, которая не смогла'


class Logarithmic(Functional):
    """
    Логарифмический апроксиматор
    y = a * ln(bx + c) + d
    """

    def __init__(self, points=100, left_offset=5, right_offset=5):
        """
        :param points: количество точек, которые будут на выходе
        :param left_offset: отступ  от правой границы диапазона
        :param right_offset: отступ, то свободного коэффициента нет, иначе есть
        """
        super(Logarithmic, self).__init__(
            function=functions.log_for_fit,
            points=points,
            left_offset=left_offset,
            right_offset=right_offset
        )

    def label(self, xvar='x', yvar='y'):

        try:

            return f'${format_monoid(round_to_n(self.koefs[0], 3), True)}\ln{{(' \
                   f'{format_monoid(round_to_n(self.koefs[1], 3), True)}x ' \
                   f'{format_monoid(round_to_n(self.koefs[2], 3))})}} ' \
                   f'{format_monoid(round_to_n(self.koefs[3], 3))}$'

        except IndexError:
            return 'Логарифм, который не смог'


class StupidApproximator(MultiLinearMixin, Approximator):
    """
    Аппроксиматор, который просто соединяет соседние точки прямой
    """
