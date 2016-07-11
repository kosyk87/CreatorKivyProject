# -*- coding: utf-8 -*-
#
# customsettings.py
#

import os

from kivy.uix.settings import (
    SettingOptions, SettingNumeric, SettingPath, SettingString
)
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty, ObjectProperty, ListProperty
from kivy.lang import Builder

from Libs.uix.kdialog import Dialog, KDialog, BDialog, FDialog


title_item = '''
<SettingSidebarLabel>:
    canvas.before:
        Color:
            rgba: [{background_sections}, int(self.selected)]
        Rectangle:
            pos: self.pos
            size: self.size

<SettingTitle>:
    color: {color_text_title}
    canvas.before:
        Color:
            rgba: {background_color_title}
        Rectangle:
            source: '{background_image_title}'
            pos: self.x, self.y + 2
            size: self.width, self.height - 2
        Color:
            rgba: {separator_color}
        Rectangle:
            pos: self.x, self.y - 2
            size: self.width, 1

<SettingItem>:
    canvas:
        Color:
            rgba: {background_color_item}
        Rectangle:
            source: '{background_image_item}'
            pos: self.x, self.y + 1
            size: self.size
        Color:
            rgba: {separator_color}
        Rectangle:
            pos: self.x, self.y - 2
            size: self.width, 1'''


class CustomSettings(Dialog):
    '''Кастомные диалоговые окна для экрана настроек.'''

    text_input = StringProperty('Enter value')
    '''Подпись окна для ввода значений.

    :attr: `text_input` is a :class:`~kivy.properties.StringProperty`
    and defaults to 'Enter value'.
    '''

    settings_obj = ObjectProperty(None)
    '''Интерфейс настроек.

    :attr: `settings_obj` is a :class:`~kivy.uix.settings.SettingsWithSidebar`
    and defaults to :class:`~kivy.uix.settings.SettingsWithSidebar`.
    '''

    background_sections = ListProperty([47 / 255., 167 / 255., 212 / 255., 1])
    '''Фоновый цвет активного раздела настроек.

    :attr: `background_sections` is a :class:`~kivy.properties.ListProperty`
    and defaults to [47 / 255., 167 / 255., 212 / 255., 1].
    '''

    button_close_background_down = StringProperty('')
    '''Фоновое изображение активной кнопки закрытия экрана настроек.

    :attr: `background_image_title` is a :class:`~kivy.properties.StringProperty`
    and defaults to ''.
    '''

    color_text_title = ListProperty([.9, .9, .9, 1])
    '''Цвет текста описания пункта настроек.

    :attr: `color_text_title` is a :class:`~kivy.properties.ListProperty`
    and defaults to [.9, .9, .9, 1].
    '''

    background_image_title = StringProperty('')
    '''Фоновое изображение описания пункта настроек.

    :attr: `background_image_title` is a :class:`~kivy.properties.StringProperty`
    and defaults to ''.
    '''

    background_color_title = ListProperty([.15, .15, .15, .5])
    '''Цвет описания пункта настроек.

    :attr: `background_color_title` is a :class:`~kivy.properties.ListProperty`
    and defaults to [.15, .15, .15, .5].
    '''

    background_image_item = StringProperty('')
    '''Фоновое изображение пункта настроек.

    :attr: `background_image_item` is a :class:`~kivy.properties.StringProperty`
    and defaults to ''.
    '''

    background_color_item = ListProperty(
        [47 / 255., 167 / 255., 212 / 255., 0]
    )
    '''Цвет пункта настроек.

    :attr: `background_color_item` is a :class:`~kivy.properties.ListProperty`
    and defaults to [47 / 255., 167 / 255., 212 / 255., 0].
    '''

    background_color = ListProperty([1, 1, 1, 0])
    '''Фоновый цвет настроек.

    :attr: `background_color_item` is a :class:`~kivy.properties.ListProperty`
    and defaults to [1, 1, 1, 0].
    '''

    separator_color = ListProperty(
        [0.12156862745098039, 0.8901960784313725, 0.2, 0.011764705882352941]
    )

    def __init__(self, **kvargs):
        super(CustomSettings, self).__init__(**kvargs)
        Builder.load_string(
            title_item.format(
                background_color_title=self.background_color_title,
                background_image_title=self.background_image_title,
                background_color_item=self.background_color_item,
                background_image_item=self.background_image_item,
                background_sections=', '.join(
                    [str(value) for value in self.background_sections[:-1]]),
                separator_color=self.separator_color,
                color_text_title=self.color_text_title
            )
        )

        SettingOptions._create_popup = self.options_popup
        SettingNumeric._create_popup = self.input_popup
        SettingString._create_popup = self.input_popup
        SettingPath._create_popup = self.path_popup

        # Цвет статической и фон нажатой кнопки закрытия экрана настроек.
        button_close = self.settings_obj.children[0].children[1].ids.button
        button_close.background_color = [
            value + .5 for value in self.background_color_title]
        button_close.background_down = self.button_close_background_down

        with self.settings_obj.canvas.before:
            Color(rgba=self.background_color)
            canvas_settings = Rectangle(
                pos=(0, 0), size=(
                    self.settings_obj.width, self.settings_obj.height
                )
            )

            def on_settings_pos(instance, value):
                canvas_settings.pos = value

            def on_settings_size(instance, value):
                canvas_settings.size = value

            self.settings_obj.bind(size=on_settings_size, pos=on_settings_pos)

    def options_popup(self, options_instance):
        def on_select(button_instance):
            options_instance.value = button_instance.id

        options_list = []
        for options in options_instance.options:
            button_image = '{}/data/button_ok.png'.format(BDialog.root) \
                if options == options_instance.value \
                else '{}/data/shadows/button_ok.png'.format(BDialog.root)
            options_list.append([options, button_image])

        BDialog(events_callback=on_select, button_list=options_list,
                hint_x=1.2, title=options_instance.title).show()

    def input_popup(self, input_instance):
        def on_select(result_value):
            if result_value == '':
                return
            input_instance.value = result_value

        dialog = KDialog(answer_callback=on_select,
                         title=input_instance.title,
                         separator_color=self.separator_color).show(
            text=self.text_input, text_button_ok='OK', param='text'
        )
        dialog.input_dialog.text = input_instance.value

    def path_popup(self, path_instance):
        def on_select(*args):
            file_manager.dismiss()

            if mask == 'folder':
                path_instance.value = file_manager.select_folder
            else:
                path_instance.value = args[1][0]

        if os.path.isfile(path_instance.value):
            mask = 'file'
            path = os.path.split(path_instance.value)[0]
        else:
            mask = 'folder'
            path = path_instance.value

        file_manager = FDialog(
            events_callback=on_select, size_hint=(.9, .9), filter=mask,
            title=path_instance.title, path=path
        )
