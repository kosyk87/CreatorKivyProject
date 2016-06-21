#! /usr/bin/python3.4
# -*- coding: utf-8 -*-
#
# adialog.py
#

import os

try:
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.lang import Builder
    from kivy.properties import ListProperty, StringProperty

    try:
        from . dialog import Dialog
        from . dialog import SettingSpacer
        from . dialog import ImageButton
    except (ValueError, SystemError):
        from dialog import Dialog
        from dialog import SettingSpacer
        from dialog import ImageButton
except Exception as text_error:
    raise text_error


__version__ = '1.0.0'

root = os.path.split(__file__)[0]
if root == '':
    root = os.getcwd()


class ADialog(Dialog):
    logo_program = StringProperty('data/logo/kivy-icon-24.png')
    '''Логотип приложения.

    :attr:` logo_program` is a :class:`~kivy.properties.StringProperty`
    and defaults to 'data/logo/kivy-icon-24.png'.
    '''

    name_program = StringProperty('Kivy 1.9.2')
    '''Название приложения.

    :attr:` name_program` is a :class:`~kivy.properties.StringProperty`
    and defaults to 'Kivy 1.9.2'.
    '''

    user_size_hint = ListProperty((.95, .85))
    '''Размер окна

    :attr: `user_size_hint` is a :class:`~kivy.properties.ListProperty`
    and defaults to [.95, .85].
    '''

    info_program = ListProperty([])

    Builder.load_file('{}/kv/adialog.kv'.format(root))

    def __init__(self, **kvargs):
        super(ADialog, self).__init__(**kvargs)

        content = self.ids.content
        box_content = self.ids.box_content
        height, avatar_size_hint = (self.dp(60), (.05, .9))

        self.ids.logo.size_hint = avatar_size_hint
        self.ids.box_logo_and_title.height = height

        # Текстовая информация.
        for info_string in self.info_program:
            if info_string == '':
                content.add_widget(SettingSpacer())
                continue

            info_string = \
                Label(text=info_string, size_hint_y=None,
                      font_size=self.dp(self.base_font_size), markup=True,
                      on_ref_press=self.events_callback)
            info_string.bind(size=lambda *args: self._update_label_size(args))
            content.add_widget(info_string)

        self.content = box_content
        self.size_hint = (self.user_size_hint[0], self.user_size_hint[1])
        self.open()

    def _update_label_size(self, *args):
        label = args[0][0]

        if label.id == 'name_program':
            if not self.flag:
                label.height = self.dp(52)
        else:
            label.height = self.dp(label.texture_size[1] - 8)

        label.text_size = (self.dp(label.width - 30), None)
        label.texture_update()


if __name__ in ('__main__', '__android__'):
    from kivy.app import App
    from kivy.uix.button import Button


    class Test(App):
        def events_callback(self, instance_label, text_link):
            print(text_link)

        def about_dismiss(self, *args):
            print('Dialog dismiss')

        def build(self):
            return Button(text='Press Me', on_press=self.show)

        def show(self, *args):
            name_program = '[color=#ff7f32][size=22]HeaTDV4A[/size] ' \
                           '[size=16][color=#2fbfe0]blue-[color=#ff7f32]' \
                           'orange [/size][color=#ffffffff]version 0.0.1'
            logo_program = 'data/logo/kivy-icon-24.png'
            info_program = [
                '',

                '[color=#ffffffff]Мобильный клиент сайта [color=#2fbfe0]'
                '[ref=www.dimonvideo.ru]dimonvideo.ru[/ref]',

                '',

                '[b][color=#ffffffff]Автор - [/b][color=#ff7f32]Иванов Юрий '
                '[color=#ffffffff]aka [color=#2fbfe0][ref=http://dimonvideo.ru'
                '/smart/0/name/HeaTTheatR]HeaTTheatR[/ref]',

                '[b][color=#ffffffff]Система плагинов - [/b][color=#ff7f32]'
                'Виталий [color=#ffffffff]aka [color=#2fbfe0][ref=http://'
                'dimonvideo.ru/smart/0/name/Virtuos86]Virtuos86[/ref]',

                '[b][color=#ffffffff]Серверная часть - [/b][color=#ff7f32]'
                'Дмитрий [color=#ffffffff]aka [color=#2fbfe0][ref=http://'
                'dimonvideo.ru/smart/0/name/dimy44]dimy44[/ref]',

                '',

                '[b][color=#ffffffff]E-mail - [/b][color=#2fbfe0]'
                '[ref=gorodage@gmail.com]gorodage@gmail.com[/ref]',

                '[b][color=#ffffffff]Исходный код - [/b]'
                '[ref=https://github.com/HeaTTheatR/HeaTDV4A.git]'
                '[color=#2fbfe0]github.com[/ref]',

                '[color=#ff7f32]P.S',

                '',

                '[color=#ffffffff]Программа написана на языке '
                'программирования [ref=www.python.org][color=#2fbfe0]Python '
                '[/ref][color=#ffffffff]с использованием фреймворка '
                '[ref=www.kivy.org][color=#2fbfe0]Kivy[/ref]',

                '[color=#ff7f32]P.P.S',

                '',

                '[i][color=#ffffffff]Хотите добиться успеха - приложите все '
                'силы для создания наилучшего продукта. А если он не принесет '
                'вам успеха, значит, так тому и быть.[/i]',

                '[i]Успеха достигает тот, '
                'кто обеспечивает качество и удовлетворяет потребности.[/i]',

                '',

                '[color=#ff7f32]Linus TORVALDS [color=#ffffffff]and '
                '[color=#ff7f32]David DIAMOND.',

                '[color=#ffffffff] "JUST FOR  FUN. THE  STORY OF AN ACCIDENTAL '
                'REVOLUTIONARY."'
            ]

            ADialog(dismiss_callback=self.about_dismiss,
                    events_callback=self.events_callback,
                    logo_program=logo_program, info_program=info_program,
                    name_program=name_program, title='Пример окна ADialog')


    Test().run()
