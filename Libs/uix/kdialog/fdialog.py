# -*- coding: utf-8 -*-
#
# fdialog.py
#

import os

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.properties import StringProperty

try:
    from . dialog import Dialog
    from . dialog import SettingSpacer
except (ValueError, SystemError):
    from dialog import Dialog
    from dialog import SettingSpacer


class FDialog(Dialog):
    text_button_ok = StringProperty('OK')
    '''Текс кнопки выбора.

    :attr:`text_button_ok` is a :class:`~kivy.properties.StringProperty`
    and defaults to 'OK'.
    '''

    filter = StringProperty('files')
    '''Тип диалога выбора - files/folder.

    :attr:`filter` is a :class:`~kivy.properties.StringProperty`
    and defaults to 'files'.
    '''

    path = StringProperty('.')
    '''Путь открытия менеджера по умолчанию.

    :attr:`path` is a :class:`~kivy.properties.StringProperty`
    and defaults to '.'.
    '''

    def __init__(self, **kvargs):
        super(FDialog, self).__init__(**kvargs)

        box = BoxLayout(orientation='vertical', spacing=10)
        fdialog = FileChooserListView(path=self.path)
        fdialog.bind(selection=self.events_callback)
        box.add_widget(fdialog)

        if self.filter == 'folder':
            box.add_widget(SettingSpacer())
            box.add_widget(
                Button(text=self.text_button_ok, size_hint=(1, .1),
                       background_normal=self.background_image_buttons[0],
                       background_down=self.background_image_shadows[0],
                       on_press=self.events_callback)
            )
            fdialog.filters = [self.is_dir]
        elif self.filter == 'files':
            fdialog.filters = [self.is_file]

        self.content = box
        self.open()

    def is_dir(self, directory, filename):
        self.select_folder = directory
        return os.path.isdir(os.path.join(directory, filename))

    def is_file(self, directory, filename):
        return os.path.isfile(os.path.join(directory, filename))
