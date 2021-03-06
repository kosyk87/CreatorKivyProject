# -*- coding: utf-8 -*-
#
# dialog.py
#

import os

from kivy import metrics
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.properties import (
    ObjectProperty, NumericProperty, StringProperty, DictProperty,
    ListProperty)


root = os.path.split(__file__)[0]
if root == '':
    root = os.getcwd()


def _pass(*args):
    pass


class SettingSpacer(Widget):
    pass


class ImageButton(ButtonBehavior, Image):
    pass


class Dialog(Popup):
    '''Базоывй класс.'''

    retrieve_callback = ObjectProperty(_pass)
    '''Пользовательская функция, вызываемая при работе прогресса.

    :attr:`retrieve_callback` is a :class:`~kivy.properties.ObjectProperty`
    and defaults to pass.
    '''

    events_callback = ObjectProperty(_pass)
    '''Пользовательская функция обработки событий окна.

    :attr:`events_callback` is a :class:`~kivy.properties.ObjectProperty`
    and defaults to pass.
    '''

    answer_callback = ObjectProperty(_pass)
    '''Встроеная функция обработки событий окна.

    :attr:`answer_callback` is a :class:`~kivy.properties.ObjectProperty`
    and defaults to pass.
    '''

    progress_callback = ObjectProperty(None)
    '''Функция, вызываемая при старте окна прогресса.

    :attr:`progress_callback` is a :class:`~kivy.properties.ObjectProperty`
    and defaults to None.
    '''

    background = StringProperty('{}/data/decorator.png'.format(root))
    '''Декоратор окна.

    :attr:`background` is a :class:`~kivy.properties.StringProperty`
    and defaults to 'data/decorator.png'.
    '''

    text_input = StringProperty('{}/data/text_input.png'.format(root))
    '''Декоратор поля ввода.

    :attr:`text_input` is a :class:`~kivy.properties.StringProperty`
    and defaults to 'data/text_input.png'.
    '''

    checkbox_down = StringProperty('{}/data/checkbox_down.png'.format(root))
    '''Активный чекбокс.

    :attr:`checkbox_down` is a :class:`~kivy.properties.StringProperty`
    and defaults to 'data/checkbox_down.png'.
    '''

    checkbox_normal = StringProperty(
        '{}/data/checkbox_normal.png'.format(root)
    )
    '''Не активный чекбокс.

    :attr:`checkbox_normal` is a :class:`~kivy.properties.StringProperty`
    and defaults to 'data/checkbox_normal.png'.
    '''

    background_image_buttons = DictProperty(
        {0: '{}/data/button_ok.png'.format(root),
         1: '{}/data/button_no.png'.format(root),
         2: '{}/data/button_cancel.png'.format(root)}
    )

    background_image_shadows = DictProperty(
        {0: '{}/data/shadows/button_ok.png'.format(root),
         1: '{}/data/shadows/button_no.png'.format(root),
         2: '{}/data/shadows/button_cancel.png'.format(root)}
    )

    hint_x = NumericProperty(1)
    '''Ширина окна.

    Чем больше значение, тем меньше окно.

    :attr:` hint_x` is a :class:`~kivy.properties.NumericProperty`
    and defaults to 1.
    '''

    base_font_size = NumericProperty(15)
    '''Размер шрифта.

    :attr:`base_font_size` is a :class:`~kivy.properties.NumericProperty`
    and defaults to 15.
    '''

    base_font_name = StringProperty('DroidSans')
    '''Имя шрифта.

    :attr:`base_font_name` is a :class:`~kivy.properties.StringProperty`
    and defaults to 'DroidSans'.
    '''

    underline_color = StringProperty('#2fa7d4ff')
    '''Линия заголовка в RstDocument.

    :attr:`underline_color` is a :class:`~kivy.properties.StringProperty`
    and defaults to '#2fa7d4ff'.
    '''

    separator_color = ListProperty([1.0, 1.0, 1.0, 1.0])
    '''Цвет линии сепаратора окна.

    :attr:`separator_color` is a :class:`~kivy.properties.ListProperty`
    and defaults to [1.0, 1.0, 1.0, 1.0].
    '''

    dp = ObjectProperty(metrics.dp)
    sp = ObjectProperty(metrics.sp)
    root = root

    def __init__(self, **kvargs):
        super(Dialog, self).__init__(**kvargs)
