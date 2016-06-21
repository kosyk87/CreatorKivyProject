#! /usr/bin/python2.7
# -*- coding: utf-8 -*-
#
# pdialog.py
#

import threading

try:
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.uix.button import Button
    from kivy.uix.widget import Widget
    from kivy.properties import (
        ObjectProperty, StringProperty, ListProperty, NumericProperty
    )
    try:
        from . dialog import Dialog
        from . progress import Progress
        from . dialog import SettingSpacer
    except (ValueError, SystemError):
        from dialog import Dialog
        from progress import Progress
        from dialog import SettingSpacer
except Exception as text_error:
    raise text_error


__version__ = '1.0.0'


class BDialog(Dialog):
    complete = ObjectProperty(None)
    '''Функция для обработки событий окна.

    :attr: `complete` is a :class:`~kivy.properties.ObjectProperty`
    and defaults to None'.
    '''

    text_already_loaded = StringProperty('Already loaded - {} byte')
    '''Текст текущего состояния прогресса.

    :attr: `text_already_loaded` is a :class:`~kivy.properties.StringProperty`
    and defaults to 'Already loaded - {} byte''.
    '''

    text_total_size = StringProperty('Total size - {} byte')
    '''Текст конечного состояния прогресса.

    :attr: `text_total_size` is a :class:`~kivy.properties.StringProperty`
    and defaults to 'Total size - {} byte''.
    '''

    progress_line_color = StringProperty('#ff7f32')
    '''Цвет линии прогресса.

    :attr: `progress_line_color` is a :class:`~kivy.properties.StringProperty`
    and defaults to '#ff7f32''.
    '''

    progress_border_color = StringProperty('#2fbfe0')
    '''Цвет рамки прогресса.

    :attr: `progress_border_color` is a :class:`~kivy.properties.StringProperty`
    and defaults to '#2fbfe0''.
    '''

    progress_line_height = NumericProperty(1)
    '''Ширира линии прогресса.

    :attr: `progress_line_height` is a :class:`~kivy.properties.NumericProperty`
    and defaults to 1'.
    '''

    text_button_cancel = StringProperty('Cancel')
    size_hint = ListProperty((.7, .5))

    def __init__(self, **kvargs):
        super(BDialog, self).__init__(**kvargs)

        self.box = BoxLayout(orientation='vertical')
        self.label_one = Label(text='', size_hint=(1, .1), markup=True)
        self.label_two = Label(text='', size_hint=(1, .1), markup=True)
        self.progress_load = Progress()
        self.button_cancel = Button(
            text='Cancel', on_press=self.events_callback, size_hint=(1, .1),
            background_normal=self.background_image_buttons[0]
        )

        self.label_one.bind(size=lambda *args: self._update_text_size(args))
        self.label_two.bind(size=lambda *args: self._update_text_size(args))

        self.box.add_widget(self.label_one)
        self.box.add_widget(self.label_two)
        self.box.add_widget(Widget(size_hint=(None, .02)))
        self.box.add_widget(SettingSpacer())
        self.box.add_widget(Widget(size_hint=(None, .02)))
        self.box.add_widget(self.progress_load)
        self.box.add_widget(Widget(size_hint=(None, .3)))
        self.box.add_widget(SettingSpacer())
        self.box.add_widget(Widget(size_hint=(None, .02)))
        self.box.add_widget(self.button_cancel)

        self.progress_load.min = 0
        self.progress_load.max = 100
        self.progress_load.bar_value = 0
        self.progress_load.height_widget = self.dp(self.progress_line_height)
        self.progress_load.color = self.progress_line_color
        self.progress_load.border_color = self.progress_border_color

    def show(self, *args):
        self.content = self.box
        self.open()

        if callable(self.complete):
            self._on_load = self.complete

        self.thread = \
            threading.Thread(target=self.retrieve_callback,
                             args=(args, self._tick, self._on_load,))
        self.thread.start()

    def _tick(self, value, total_size):
        '''
        Отрисовка прогресса загрузки.

        :type value: int;
        :param value: текущее колличество загруженного контента в байтах;

        :type total_size: int;
        :param total_size: общее колличество загруженного контента в байтах;

        '''

        value = (value * 100) // total_size
        self.progress_load.add_value_percent(value)

        self.label_one.text = self.text_already_loaded.format(value)
        self.label_two.text = self.text_total_size.format(total_size)

        if value == 100:
            self.dismiss()

    def _update_text_size(self, *args):
        label = args[0][0]
        width = args[0][1][0]

        label.text_size = (self.dp(width - 10), self.dp(20))

    def _on_load(self):
        pass


if __name__ in ('__main__', '__android__'):
    import time

    from kivy.base import runTouchApp

    from kdialog import KDialog


    class Test(BoxLayout):
        def __init__(self, **kvargs):
            super(Test, self).__init__(**kvargs)

            self.add_widget(
                Button(text='Press me!', on_release=self.show_progress)
            )
            self.cancel_flag = True

        def complete(self):
            '''Функция вызывается после окончания цикла прогресса.'''

            KDialog(title='Info').show(text='Complete!')

        def retrieve_callback(self, *args):
            '''Функция вызывается во время цикла прогресса.'''

            tick = args[1]  # метод _tick класса PDialog
            complete = args[2]  # метод self.complete
            args = args[0]  # аргументы, переданные в метод show

            for i in range(1, 101):
                assert(self.cancel_flag > 0)
                tick(i, 100)
                time.sleep(.05)

            complete()

        def download_cancel(self, *args):
            '''Функция вызывается после прерывания цикла прогресса.'''

            self.cancel_flag = False
            self.progress_load.dismiss()
            self.cancel_flag = True

        def show_progress(self, *args):
            self.progress_load = \
                BDialog(title='Пример окна PDialog',
                        retrieve_callback=self.retrieve_callback,
                        events_callback=self.download_cancel,
                        complete=self.complete)
            self.progress_load.show()


    runTouchApp(Test())
