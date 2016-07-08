# -*- coding: utf-8 -*-
#
# example.py
#

import time

import kivy

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.base import runTouchApp
from kivy.logger import PY2

from adialog import ADialog
from bdialog import BDialog
from fdialog import FDialog
from cdialog import CDialog
from pdialog import PDialog
from kdialog import KDialog
from dialog import Dialog


class TestPDialog:
        cancel_flag = True

        def complete(self):
            '''Функция вызывается после окончания цикла прогресса.'''

            KDialog(title='Info').show(text='Complete!')

        def retrieve_callback(self, *args):
            '''Функция вызывается во время цикла прогресса.'''

            tick = args[1]  # метод _tick класса PDialog
            complete = args[2]  # метод self.complete
            args = args[0]  # аргументы, переданные в метод show

            for i in range(1, 101):
                if self.cancel_flag:
                    tick(i, 100)
                    time.sleep(.05)
                else:
                    self.cancel_flag = True
                    break
            complete()

        def download_cancel(self, *args):
            '''Функция вызывается после прерывания цикла прогресса.'''

            self.cancel_flag = False
            self.progress_load.dismiss()

        def show(self, *args):
            self.progress_load = PDialog(
                title='Пример окна PDialog',
                retrieve_callback=self.retrieve_callback,
                events_callback=self.download_cancel, complete=self.complete
            )
            self.progress_load.show()


class TestFDialog:
        def select(self, *args):
            self.file_manager.dismiss()

            try:
                print(args[1][0])
            except IndexError:
                print(self.file_manager.select_folder)

        def show(self, *args):
            self.file_manager = \
                FDialog(events_callback=self.select, size_hint=(.5, .9),
                        filter='folder', title='Пример окна FDialog')


class TestCDialog:
        def select(self, *args):
            print(args[0])

        def show(self, *args):
            CDialog(
                title='Пример окна CDialog', events_callback=self.select,
                size_hint=(.8, .97)
            )


class TestBDialog:
        def on_press(self, instance_button):
            print(instance_button.id)

        def show(self, *args):
            button_list = []
            for i in range(50):
                button_list.append(
                    ['Text{0:3d}'.format(i),
                     '{}/data/button_ok.png'.format(Dialog.root)]
                )

            return BDialog(
                events_callback=self.on_press, button_list=button_list,
                hint_x=1.8, title='Пример окна BDialog').show()


class TestADialog:
        def events_callback(self, instance_label, text_link):
            print(text_link)

        def about_dismiss(self, *args):
            print('Dialog dismiss')

        def show(self):
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

            return ADialog(
                on_dismiss=self.about_dismiss,
                events_callback=self.events_callback,
                logo_program=logo_program, info_program=info_program,
                name_program=name_program, title='Пример окна ADialog'
            )


class Test(GridLayout):
    def __init__(self, **kwargs):
        super(Test, self).__init__(cols=2, spacing=5, padding=5)

        for text in ['Demo `info`', 'Demo `query`', 'Demo `text`',
                     'Demo `logpass`', 'Demo `rst`', 'Demo `loaddialog`',
                     'Demo `check`', 'Demo `ADialog`', 'Demo `BDialog`',
                     'Demo `FDialog`', 'Demo `CDialog`', 'Demo `PDialog`']:
            self.add_widget(Button(text=text, on_press=self.on_click))

    def on_click(self, *args):
        text = args[0].text

        # ----------------------------logpass-----------------------------
        if text == 'Demo `logpass`':
            window = KDialog(answer_callback=self.answer_callback,
                             title='Пример окна с параметром `logpass`')
            window.show(text='Your [color=#2fa7d4ff] Login [/color]:',
                        text_button_ok='OK', text_button_no='NO',
                        text_button_cancel='CANCEL', param='logpass',
                        password=True)
        # -----------------------------info-------------------------------
        elif text == 'Demo `info`':
            KDialog(title='Пример окна с параметром `info`').show(
                text='This string [color=#2fa7d4ff] Info!')
        # ----------------------------query-------------------------------
        elif text == 'Demo `query`':
            window = KDialog(answer_callback=self.answer_callback,
                             title='Пример окна с параметром `query`')
            window.show(text=kivy.__doc__, param='query', text_button_ok='OK',
                        text_button_no='NO')
        # ----------------------------text--------------------------------
        elif text == 'Demo `text`':
            window = KDialog(answer_callback=self.answer_callback,
                             title='Пример окна с параметром `text`')
            window.show(text='Input [color=#2fa7d4ff] Text [/color]:',
                        text_button_ok='OK', text_button_no='NO', param='text')
        # ----------------------------rst---------------------------------
        elif text == 'Demo `rst`':
            window = KDialog(answer_callback=self.answer_callback,
                             title='Пример окна с параметром `rst`')
            window.show(text=kivy.__doc__, rst=True, text_button_ok='OK',
                        text_button_no='NO')
        # ------------------------loaddialog------------------------------
        elif text == 'Demo `loaddialog`':
            window = KDialog(title='Пример окна с параметром `loaddialog`')
            window.show(text='Loading [color=#2fa7d4ff] Page...',
                        param='loaddialog')
        # --------------------------check---------------------------------
        elif text == 'Demo `check`':
            window = KDialog(title='Пример окна с параметром `check`',
                             answer_callback=self.answer_callback)
            window.show(text='Нажмите `OK...`', param='query', check=True,
                        check_text='Больше не показывать', text_button_ok='OK')
        # -------------------------ADialog---------------------------------
        elif text == 'Demo `ADialog`':
            TestADialog().show()
        # -------------------------BDialog---------------------------------
        elif text == 'Demo `BDialog`':
            TestBDialog().show()
        # -------------------------CDialog---------------------------------
        elif text == 'Demo `CDialog`':
            TestCDialog().show()
        # -------------------------FDialog---------------------------------
        elif text == 'Demo `FDialog`':
            TestFDialog().show()
        # -------------------------PDialog---------------------------------
        elif text == 'Demo `PDialog`':
            TestPDialog().show()

    def answer_callback(self, answer):
        if isinstance(answer, tuple):
            if isinstance(answer[1], bool):
                login, password = answer
                password = {1: 'True', 0: 'False'}[password]
                log = 'Press'
                pasw = 'Check'
            else:
                if ''.join(answer) == '':
                    return
                login, password = answer
                log = 'Login'
                pasw = 'Password'
            if not PY2:
                answer = '[color=#2fa7d4ff]{}[/color] - {}\n' \
                         '[color=#2fa7d4ff]{}[/color] - {}'.format(
                    log, login if login != '' else 'None', pasw, password
                    if password != '' else 'None')
            else:
                answer = u'[color=#2fa7d4ff]{}[/color] - {}\n' \
                         u'[color=#2fa7d4ff]{}[/color] - {}'.format(
                    log, login if login != '' else 'None', pasw, password
                    if password != '' else 'None')
        if answer != '':
            window = KDialog()
            window.show(text=answer)


runTouchApp(Test())
