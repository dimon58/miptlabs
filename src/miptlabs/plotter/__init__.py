"""
Модуль отвечает за всё, что непосредственно относиться к рисованию графиков
"""
from .plotter import (
    NothingDrawError,
    pretty_plot, pretty_plot_many, show,
    savefig,
)

__all__ = ['NothingDrawError', 'pretty_plot', 'pretty_plot_many', 'show', 'savefig']
