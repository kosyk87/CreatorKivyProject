# -*- coding: utf-8 -*-
#
# custom_windows_settings.py
#

import os

from kivy.uix.settings import (
    SettingOptions, SettingNumeric, SettingPath, SettingString
)
from kivy.properties import StringProperty

from Libs.uix.kdialog import Dialog, KDialog, BDialog, FDialog


class CustomWindowsSettings(Dialog):
    '''Кастомные диалоговые окна для экрана настроек.'''

    text_input = StringProperty('Enter value')

    def __init__(self, **kvargs):
        super(CustomWindowsSettings, self).__init__(**kvargs)

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
