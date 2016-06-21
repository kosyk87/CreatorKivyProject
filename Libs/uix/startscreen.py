#! /usr/bin/python3.4
#
# startscreen.py
#
# Главный экран программы.
#
# Декабрь, 2015
# Луганск
# Автор сценария: Иванов Юрий aka HeaTTheatR
#
# Email: gleb.assert@mail.ru
# gorodage@gmail.com
#

import os
import sys

try:
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.actionbar import ActionButton, ActionGroup
    from kivy.lang import Builder
    from kivy.properties import (ObjectProperty, ListProperty, StringProperty,
                                 DictProperty)
except Exception as text_error:
    raise text_error


__version__ = '0.0.1'


class StartScreen(BoxLayout):
    events_callback = ObjectProperty(None)
    """Функция обработки сигналов экрана."""

    buttons_menu = ListProperty([])
    """Пути к иконкам для кнопок ActionBar."""

    name_buttons_menu = DictProperty({})
    """{'mail': 'Сообщения', ...}"""

    buttons_group = ListProperty([])
    """мена пунктов кнопок меню в ActionGroup."""

    previous = StringProperty('data/logo/kivy-icon-24.png')
    """Путь к иконке для ActionPrevious."""

    title_previous = StringProperty('My program')
    """Заголоок ActionBar."""

    title_image = StringProperty('data/logo/kivy-icon-24.png')
    """Путь к изображению для шапки програмы."""

    title_image_size = ListProperty((1, 2.5))
    """Размер изображения шапки програмы."""

    overflow_image = StringProperty(
        'atlas://data/images/defaulttheme/overflow')

    previous_image = StringProperty(
        'atlas://data/images/defaulttheme/previous_normal')
    """Путь к иконке для ActionOverflow."""

    Builder.load_file('{}/Libs/uix/kv/startscreen.kv'.format(
        os.path.split(os.path.abspath(sys.argv[0]))[0].split("/Libs/uix")[0]))

    def __init__(self, **kvargs):
        super().__init__(**kvargs)
        self.mobile_client_label = self.ids.mobile_client_label
        self.action_view = self.ids.action_view
        self.screen_manager = self.ids.screen_manager
        self.action_previous = self.ids.action_previous

        for item_name in self.buttons_group:  # кнопки спинера
            item_button = ActionButton(
                text=item_name, id=item_name, on_press=self.events_screen,
                on_release=lambda *args: self.ids.action_overflow._dropdown.select(
                    self.on_release_select_item_spinner()))
            self.ids.action_overflow.add_widget(item_button)

        for path_image in self.buttons_menu:  # кнопки меню
            name_image = os.path.split(path_image)[1].split('.')[0]
            text_name_button = self.name_buttons_menu[name_image]

            action_group = ActionGroup(text=text_name_button)
            #button_menu = \
            #    ActionButton(text=text_name_button, icon=path_image,
            #                 id=name_image, on_press=self.events_screen)
            button_menu = \
                ActionButton(icon=path_image, id=name_image, on_press=self.events_screen)
            action_group.add_widget(button_menu)
            self.ids.action_view.add_widget(action_group)

    def events_screen(self, button_menu):
        """
        Вызывается при нажатии кнопок меню программы.

        type button_menu: instance <class 'kivy.uix.button.Button'>;

        """

        if callable(self.events_callback):
            self.events_callback(button_menu)

    def on_release_select_item_spinner(self):
        """Вешается на release событие кнопок спиннера ActionBar.
        В противноном случае, список не будет автоматически скрываться."""

        pass

if __name__ in ('__main__', '__android__'):
    try:
        from Libs.uix.tests import startscreen
    except ImportError:
        from tests import startscreen

    startscreen.Test(StartScreen=StartScreen).run()
