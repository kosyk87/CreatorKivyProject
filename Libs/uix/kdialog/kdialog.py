# -*- coding: utf-8 -*-
#
# kdialog.py
#

from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
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


class KDialog(Dialog):
    Builder.load_file('{}/kv/kdialog.kv'.format(Dialog.root))

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

    def show(self, text='Your text message!', check_text='', hint_text='',
             rst=False, check=False, text_button_ok=None, text_button_no=None,
             text_button_cancel=None, image=None, param='info', password=False,
             auto_dismiss=True):
        '''
        :param hint_text: текст по умолчанию в поле ввода;
        :type hint_text: str;

        :param text: текст окна;
        :type text: str;

        :param check_text: текст чекбокса;
        :type check_text: str;

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

        :param check: использовать ли в окне чекбос;
        :type check: boolean;

        '''

        def create_button(name_button, background_image_normal,
                          background_image_down):
            self.box_buttons_select.add_widget(
                Button(text=name_button, id=name_button,
                       background_normal=background_image_normal,
                       background_down=background_image_down,
                       on_release=self._answer_user)
            )
            return True

        self.rst = rst
        self.check = check
        self.param = param
        button = None

        if not image:
            image = '{}/data/loading.gif'.format(self.root)
        if self.param not in [
                'info', 'query', 'logpass', 'text', 'loaddialog']:
            self.param = 'info'

        for i, name_button in enumerate(
                [text_button_ok, text_button_no, text_button_cancel]):
            if name_button:
                button = create_button(
                    name_button, self.background_image_buttons[i],
                    self.background_image_shadows[i]
                )

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
                        size=lambda *args: self._update_label_size(args)
                    )
                    self.box_content.add_widget(self.message)
            else:
                self.message = RstDocument(
                    text=text, size_hint_y=None, height=self.dp(400),
                    background_color=[1.0, 1.0, 1.0, 0.0]
                )
                self.box_content.add_widget(self.message)

        if self.param not in ['query', 'info', 'loaddialog']:
            param = self.param

            # FIXME: Виджет TextInput не реагирует на значения аргументов
            # 'tel', 'address', 'mail', 'datetime', 'number'.
            if self.param == 'logpass':
                param = 'text'
                hint_text = 'Password'

                self.input_dialog_double = \
                    TextInput(input_type=param, password=password,
                              size_hint_y=None, height=self.dp(40),
                              hint_text='Login', multiline=False,
                              background_normal=self.text_input,
                              background_active=self.text_input)
                self.input_dialog_double.bind(on_press=self._answer_user)
                self.box_root.add_widget(self.input_dialog_double)

            self.box_root.add_widget(Widget(size_hint=(None, .03)))
            self.input_dialog = \
                TextInput(input_type=param, password=password,
                          hint_text=hint_text, multiline=False,
                          size_hint_y=None, height=self.dp(40),
                          background_normal=self.text_input,
                          background_active=self.text_input)
            self.input_dialog.bind(on_press=self._answer_user)
            self.box_root.add_widget(self.input_dialog)

        if self.param == 'query':
            if check:
                box_check = BoxLayout(size_hint_y=None, height=self.dp(40))
                label_check = Label(
                    id='check', text=check_text, size_hint=(1, None),
                    font_size=self.sp(self.base_font_size),
                    font_name=self.base_font_name, markup=True, height=18
                )
                label_check.bind(
                    size=lambda *args: self._update_label_size(args)
                )
                self.checkbox = CheckBox(
                    active=False, size_hint_y=.5, size_hint_x=.1,
                    background_checkbox_normal=self.checkbox_normal,
                    background_checkbox_down=self.checkbox_down
                )

                box_check.add_widget(self.checkbox)
                box_check.add_widget(label_check)
                self.box_root.add_widget(box_check)

        if not button and self.param in ['query', 'text', 'logpass']:
            create_button(
                'OK', self.background_image_buttons[0],
                self.background_image_shadows[0]
            )
        if self.param in ['query', 'text', 'logpass']:
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
                    if self.param == 'query' and self.check:
                        h = self.dp(190)
                    else:
                        h = self.dp(150)
                    self.height = h if height < h else height
        else:
            if self.rst:
                self.height = self.dp(400)

        if self.height > Window.size[1]:
            self.height = self.dp(Window.size[1] - 10)

    def _update_label_size(self, *args):
        label = args[0][0]
        if label.id == 'check':
            pass
        else:
            label.height = label.texture_size[1]

        if self.param == 'loaddialog':
            label.text_size = (label.width - 30, 50)
        elif self.param == 'query' and self.check:
            label.text_size = (label.width, None)
        else:
            label.text_size = (label.width - 30, None)

        label.texture_update()

    def _answer_user(self, *args):
        '''Вызывается при нажатии управляющих кнопок.'''

        if self.param in ['text', 'tel', 'address', 'mail', 'password',
                          'datetime', 'number', 'logpass']:
            if self.param == 'logpass':
                self.answer_callback(
                    (self.input_dialog_double.text, self.input_dialog.text)
                )
            else:
                self.answer_callback(self.input_dialog.text)
        elif self.param == 'query':
            if self.param == 'query' and self.check:
                self.answer_callback((args[0].text, self.checkbox.active))
            else:
                self.answer_callback(args[0].text)
        self.dismiss()
