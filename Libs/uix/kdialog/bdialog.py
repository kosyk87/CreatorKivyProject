#! /usr/bin/python3.4
# -*- coding: utf-8 -*-
#
# bdialog.py
#

from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.properties import ListProperty, NumericProperty

try:
    from . dialog import Dialog
    from . dialog import SettingSpacer
except (ValueError, SystemError):
    from dialog import Dialog
    from dialog import SettingSpacer


__version__ = '1.0.0'


class BDialog(Dialog):
    button_list = ListProperty([])
    '''[['name_button', 'path_to_image', ...], ]

    :attr:` button_list` is a :class:`~kivy.properties.ListProperty`
    and defaults to [].
    '''

    height_button = NumericProperty(40)
    '''Высота кнопки.

    :attr:` height_button` is a :class:`~kivy.properties.NumericProperty`
    and defaults to 40.
    '''

    def __init__(self, **kvargs):
        super(BDialog, self).__init__(size_hint_x=None, size_hint_y=None,
                                      **kvargs)
        box_buttons = GridLayout(cols=1, padding=5, spacing=5, size_hint_y=None)
        box_buttons.bind(minimum_height=box_buttons.setter('height'))
        scroll = ScrollView()

        # Фон для текста сообщения - (canvas GridLayout).
        with box_buttons.canvas:
            Color(0.0, 0.0, 0.0)
            self.canvas_for_box_content = \
                Rectangle(pos=(5, 5), size=(box_buttons.width,
                                            box_buttons.height))
            box_buttons.bind(size=self._update_canvas_size,
                             pos=self._update_canvas_size)

        for list_button in self.button_list:
            if not list_button[1]:
                image = 'atlas://data/images/defaulttheme/button'
            else:
                image = list_button[1]

            button = Button(text=list_button[0], size_hint_y=None,
                            height=self.dp(self.height_button),
                            background_normal=image, id=list_button[0])
            if callable(self.events_callback):
                button.bind(on_press=self.events_callback,
                            on_release=self.dismiss)
            box_buttons.add_widget(button)

        scroll.add_widget(box_buttons)
        self.content = scroll
        self.width = self.dp(int(Window.size[0] // self.hint_x))

    def show(self):
        self.open()

    def _update_canvas_size(self, instance, value):
        '''Вызывается при изменении размера экрана приложения.

        type instance: instance <kivy.uix.gridlayout.GridLayout object'>;

        type value: list;
        param value: текущий размер instance;

        '''

        self.canvas_for_box_content.pos = instance.pos
        self.canvas_for_box_content.size = instance.size

        # Установка высоты окна Popup.
        self.height = self.dp(self.canvas_for_box_content.size[1] + 70)
        self.width = self.dp(int(Window.size[0] // self.hint_x))

        if self.height > Window.size[1]:
            self.height = self.dp(Window.size[1] - 10)


if __name__ in ('__main__', '__android__'):
    from kivy.uix.boxlayout import BoxLayout
    from kivy.base import runTouchApp


    class Test(BoxLayout):
        def __init__(self, **kvargs):
            super(Test, self).__init__(**kvargs)

            self.add_widget(
                Button(text='Press me!', on_release=self.show_dialog)
            )

        def on_press(self, instance_button):
            print(instance_button.id)

        def show_dialog(self, *args):
            button_list = []
            for i in range(50):
                button_list.append(
                    ['Text{0:3d}'.format(i),
                     '{}/data/button_ok.png'.format(Dialog.root)]
                )

            BDialog(
                events_callback=self.on_press, button_list=button_list,
                hint_x=1.8, title='Пример окна BDialog').show()


    runTouchApp(Test())
