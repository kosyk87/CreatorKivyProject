#! /usr/bin/python3.4
# -*- coding: utf-8 -*-
#
# cdialog.py
#

try:
    from kivy.uix.widget import Widget
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.colorpicker import ColorPicker
    from kivy.uix.button import Button
    from kivy.properties import StringProperty

    try:
        from . dialog import Dialog
        from . dialog import SettingSpacer
    except (ValueError, SystemError):
        from dialog import Dialog
        from dialog import SettingSpacer
except Exception as text_error:
    raise text_error


__version__ = '0.0.1'


class CDialog(Dialog):
    text_button_ok = StringProperty('OK')
    '''Текс кнопки выбора.

    :attr:`text_button_ok` is a :class:`~kivy.properties.StringProperty`
    and defaults to 'OK'.
    '''

    default_color = StringProperty('#ffffff00')
    '''Дефолтный цвет палитры.

    :attr:`default_color` is a :class:`~kivy.properties.StringProperty`
    and defaults to '#ffffff00'.
    '''

    def __init__(self, **kvargs):
        super(CDialog, self).__init__(**kvargs)

        box = BoxLayout(orientation='vertical')
        select_color = ColorPicker(hex_color=self.default_color)
        button_select = \
            Button(text=self.text_button_ok, size_hint=(1, .1),
                   background_normal=self.background_image_buttons[0])

        box.add_widget(select_color)
        box.add_widget(Widget(size_hint=(None, .02)))
        box.add_widget(SettingSpacer())
        box.add_widget(Widget(size_hint=(None, .02)))
        box.add_widget(button_select)

        button_select.bind(
            on_press=lambda color: self.events_callback(select_color.hex_color),
            on_release=lambda *args: self.dismiss()
        )
        self.content = box
        self.open()


if __name__ in ('__main__', '__android__'):
    from kivy.base import runTouchApp

    class Test(BoxLayout):
        def __init__(self, **kvargs):
            super(Test, self).__init__(**kvargs)

            self.add_widget(
                Button(text='Press me!', on_release=self.show_palette)
            )

        def select(self, *args):
            print(args[0])

        def show_palette(self, *args):
            CDialog(title='Пример окна CDialog', events_callback=self.select,
                    size_hint=(.8, .97))


    runTouchApp(Test())
