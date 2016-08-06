# -*- coding: utf-8 -*-
#
# customsettings.py
#

import os

from kivy.uix.settings import (
    SettingOptions, SettingNumeric, SettingPath, SettingString,
    InterfaceWithNoMenu, Settings
)
from kivy.lang import Builder

from Libs.uix.kdialog import KDialog, BDialog, FDialog


TEXT_INPUT = 'Enter value'  # подпись окна для ввода значений
BACKGROUND_SECTIONS = [47 / 255., 167 / 255., 212 / 255., 1]  # фоновый цвет активного раздела настроек
COLOR_TEXT_INPUT = [.9, .9, .9, 1]  # цвет текста описания пункта настроек
BACKGROUND_IMAGE_TITLE = ''  # фоновое изображение описания пункта настроек
BACKGROUND_COLOR_TITLE = [.15, .15, .15, .5]  # цвет описания пункта настроек
BACKGROUND_IMAGE_ITEM = ''  # фоновое изображение пункта настроек
BACKGROUND_COLOR_ITEM = [47 / 255., 167 / 255., 212 / 255., 0]  # цвет пункта настроек
BACKGROUND_COLOR = [1, 1, 1, 0]  # фоновый цвет настроек
SEPARATOR_COLOR = [0.12156862745098039, 0.8901960784313725, 0.2, 0.011764705882352941]
SETTINGS_INTERFACE = InterfaceWithNoMenu

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


Builder.load_string("""
<-CustomSettings>:
    interface_cls: 'SettingsInterface'

    canvas:
        Color:
            rgba: 0, 0, 0, .9
        Rectangle:
            size: self.size
            pos: self.pos
""")


class SettingsInterface(SETTINGS_INTERFACE):
    pass


class CustomSettings(Settings):
    '''Кастомные диалоговые окна для экрана настроек.'''

    def __init__(self, **kvargs):
        super(CustomSettings, self).__init__(**kvargs)
        Builder.load_string(
            title_item.format(
                background_color_title=BACKGROUND_COLOR_TITLE,
                background_image_title=BACKGROUND_IMAGE_TITLE,
                background_color_item=BACKGROUND_COLOR_ITEM,
                background_image_item=BACKGROUND_IMAGE_ITEM,
                background_sections=', '.join(
                    [str(value) for value in BACKGROUND_SECTIONS[:-1]]),
                separator_color=SEPARATOR_COLOR,
                color_text_title=COLOR_TEXT_INPUT
            )
        )
        SettingOptions._create_popup = self.options_popup
        SettingNumeric._create_popup = self.input_popup
        SettingString._create_popup = self.input_popup
        SettingPath._create_popup = self.path_popup

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
                         separator_color=SEPARATOR_COLOR).show(
            text=TEXT_INPUT, text_button_ok='OK', param='text'
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
