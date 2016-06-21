#! /usr/bin/python3.4
# -*- coding: utf-8 -*-
#
# kdialog.py
#

import os

try:
    from kivy.uix.widget import Widget
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    from kivy.uix.label import Label
    from kivy.uix.textinput import TextInput
    from kivy.uix.image import Image
    from kivy.uix.rst import RstDocument
    from kivy.core.window import Window
    from kivy.clock import Clock
    from kivy.lang import Builder

    try:
        from . dialog import Dialog
        from . dialog import SettingSpacer
    except (ValueError, SystemError):
        from dialog import Dialog
        from dialog import SettingSpacer
except Exception as text_error:
    raise text_error

__version__ = '1.0.0'

root = os.path.split(__file__)[0]
if root == '':
    root = os.getcwd()


class KDialog(Dialog):
    Builder.load_file('{}/kv/kdialog.kv'.format(root))

    def __init__(self, **kvargs):
        super(KDialog, self).__init__(**kvargs)

        self.param = None
        self.rst = None
        self.input_dialog_double = None

        # Бокс для кнопок 'Yes, No, Cancel'.
        self.box_buttons_select = \
            BoxLayout(size_hint_y=None, height=self.dp(40), spacing=5)
        self.scroll = self.ids.scroll
        self.box_root = self.ids.box_root
        self.box_content = self.ids.box_content
        self.box_content.bind(
            height=lambda *args: self._update_box_content_size(args)
        )

    def show(self, text='Your text message!', rst=False,
             text_button_ok=None, text_button_no=None, text_button_cancel=None,
             image=None, param='info', password=False, auto_dismiss=False):
        '''
        :param text: текст окна;
        :type text: str;

        :param text_button_ok: текст кнопки;
        :type text_button_ok: str;

        :param text_button_no:
        :type text_button_no: str;

        :param text_button_cancel:
        :type text_button_cancel: str;

        :param image: путь к иконке заргузки при параметре окна 'loaddialog';
        :type image: str;

        :param param: тип окна;
        :type param: str;

        :param password: скрывать ли вводимый текст звездочками
                         при параметре окна 'password';
        :type password: boolean;

        :param auto_dismiss: автоматически скрывать окно;
        :type auto_dismiss: boolean;

        :param rst: выводить текст на виджет RstDocument;
        :type rst: boolean;

        '''

        def create_button(name_button, background_image_button):
            self.box_buttons_select.add_widget(
                Button(text=name_button, id=name_button,
                       background_normal=background_image_button,
                       on_press=self._answer_user)
            )
            return True

        self.rst = rst
        self.param = param
        button = None
        if not image:
            image = '{}/data/loading.gif'.format(root)

        if self.param not in ['info', 'query', 'logpass', 'text',
                              'loaddialog']:
            self.param = 'info'

        if self.param == 'info':
            auto_dismiss = True
        else:
            for i, name_button in enumerate(
                    [text_button_ok, text_button_no, text_button_cancel]):
                if name_button:
                    button = create_button(name_button,
                                           self.background_image_buttons[i])

        if self.param == 'loaddialog':
            self.box_content.cols = 2
            self.message = \
                Label(size_hint_y=None, markup=True, text=text,
                      font_size=self.sp(self.base_font_size),
                      font_name=self.base_font_name, valign='middle')
            self.message.bind(size=lambda *args: self._update_label_size(args))
            self.box_content.add_widget(Image(source=image, size_hint_x=None))
            self.box_content.add_widget(self.message)
        else:
            if not rst:
                while text != '':
                    _text = text[:3500]
                    text = text[3500:]
                    # Текстовая информация.
                    self.message = \
                        Label(size_hint_y=None, markup=True, text=_text,
                              on_ref_press=self.answer_callback,
                              font_size=self.sp(self.base_font_size),
                              font_name=self.base_font_name)
                    self.message.bind(
                        size=lambda *args: self._update_label_size(args))
                    self.box_content.add_widget(self.message)
            else:
                self.message = \
                    RstDocument(text=text, size_hint_y=None, height=self.dp(400),
                                background_color=[1.0, 1.0, 1.0, 0.0])
                self.box_content.add_widget(self.message)

        if self.param != 'query' and self.param != 'info' and \
                self.param != 'loaddialog':
            if not button:
                create_button('Yes', 'button_ok')

            param = self.param
            hint_text = ''

            # FIXME: Виджет TextInput не реагирует на значения аргументов
            # 'tel', 'address', 'mail', 'datetime', 'number'.
            if self.param == 'logpass':
                hint_text = 'Password'
                param = 'text'

                self.input_dialog_double = \
                    TextInput(input_type=param, password=password,
                              size_hint_y=None, height=self.dp(40),
                              hint_text='Login', ultiline=False)
                self.input_dialog_double.bind(on_press=self._answer_user)
                self.box_root.add_widget(self.input_dialog_double)

            self.box_root.add_widget(Widget(size_hint=(None, .03)))
            self.input_dialog = \
                TextInput(input_type=param, password=password,
                          hint_text=hint_text, multiline=False,
                          size_hint_y=None, height=self.dp(40))
            self.input_dialog.bind(on_press=self._answer_user)
            self.box_root.add_widget(self.input_dialog)

        if not auto_dismiss or self.param == 'query':
            if self.param == 'loaddialog':
                pass
            else:
                self.box_root.add_widget(Widget(size_hint=(None, .03)))
                self.box_root.add_widget(SettingSpacer())
                self.box_root.add_widget(Widget(size_hint=(None, .03)))
                self.box_root.add_widget(self.box_buttons_select)

        self.auto_dismiss = auto_dismiss
        self._update_box_content_size()
        self.open()

        if self.param == 'loaddialog':
            if callable(self.progress_callback):
                Clock.schedule_once(self.progress_callback, 0)
        return self

    def _update_box_content_size(self, *args):
        if args != ():
            height = self.dp(args[0][1])
            if height != 0 and height is not None and height != self.dp(150):
                if self.param == 'logpass':
                    self.height = self.dp(210)
                elif self.param == 'text':
                    self.height = self.dp(170)
                else:
                    self.height = self.dp(150) if height < self.dp(150) else height
        else:
            if self.rst:
                self.height = self.dp(400)

        if self.height > Window.size[1]:
            self.height = self.dp(Window.size[1] - 10)

    def _update_label_size(self, *args):
        label = args[0][0]
        label.height = label.texture_size[1]

        if self.param == 'loaddialog':
            label.text_size = (label.width - 30, 50)
        else:
            label.text_size = (label.width - 30, None)

        label.texture_update()

    def _answer_user(self, *args):
        '''Вызывается при нажатии управляющих кнопок.'''

        if self.param in ['text', 'tel', 'address', 'mail', 'password',
                          'datetime', 'number', 'logpass']:
            if self.param == 'logpass':
                self.answer_callback(
                    [self.input_dialog_double.text, self.input_dialog.text])
            else:
                self.answer_callback(self.input_dialog.text)
        elif self.param == 'query':
            self.answer_callback(args[0].text)
        self.dismiss()


if __name__ in ('__main__', '__android__'):
    import kivy

    from kivy.uix.gridlayout import GridLayout
    from kivy.base import runTouchApp
    from kivy.logger import PY2


    class Test(GridLayout):
        def __init__(self, **kwargs):
            super(Test, self).__init__(cols=2, spacing=5, padding=5)

            for text in ['Demo `info`', 'Demo `query`', 'Demo `text`',
                         'Demo `logpass`', 'Demo `rst`', 'Demo `loaddialog`']:
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
                window.show(text=kivy.__doc__, param='query',
                            text_button_ok='OK',
                            text_button_no='NO')
            # ----------------------------text--------------------------------
            elif text == 'Demo `text`':
                window = KDialog(answer_callback=self.answer_callback,
                                 title='Пример окна с параметром `text`')
                window.show(text='Input [color=#2fa7d4ff] Text [/color]:',
                            text_button_ok='OK', text_button_no='NO',
                            param='text')
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
                            param='loaddialog', auto_dismiss=True)

        def answer_callback(self, answer):
            if isinstance(answer, list):
                if ''.join(answer) == '':
                    return

                login, password = answer
                if not PY2:
                    answer = \
                        '[color=#2fa7d4ff]Login[/color] - {}\n' \
                        '[color=#2fa7d4ff]Password[/color] - {}'.format(
                            login if login != '' else 'None',
                            password if password != '' else 'None')
                else:
                    answer = \
                        u'[color=#2fa7d4ff]Login[/color] - {}\n' \
                        u'[color=#2fa7d4ff]Password[/color] - {}'.format(
                            login if login != u'' else u'None',
                            password if password != u'' else u'None')
            if answer != '':
                window = KDialog()
                window.show(text=answer)


    runTouchApp(Test())
