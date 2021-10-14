from numpy import linspace
from scipy.interpolate import interp1d


class Interpolator:
    """
    Базовый класс интерполятора
    """

    def __init__(self, points=100):
        self.points = points

    def interpolate(self, x, y):
        pass


class Quadratic(Interpolator):
    """
    Квдратичный интерполятор
    """

    def gen_x_axis(self, start, end):
        """
        Генерирует набор точек по оси абсцисс
        :param start:
        :param end:
        :return:
        """
        return linspace(start, end, self.points)

    def interpolate(self, x, y):
        """
        Производит квадратическую интерполяцию, подробнее в `документации numpy`_

        .. _`документации numpy`: https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp1d.html

        :param x: координаты по оси x
        :param y: координаты по оси y

        :return: набор координат по оси x и набор координат по оси y после интерполяции
        """
        points = interp1d(x, y, kind='quadratic')
        x = linspace(min(x), max(x), self.points)
        y = points(x)

        return x, y
