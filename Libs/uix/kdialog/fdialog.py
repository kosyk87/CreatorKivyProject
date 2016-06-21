#! /usr/bin/python3.4
# -*- coding: utf-8 -*-
#
# fdialog.py
#

import os

try:
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    from kivy.uix.widget import Widget
    from kivy.uix.filechooser import FileChooserListView
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

    def __init__(self, **kvargs):
        super(FDialog, self).__init__(**kvargs)

        box = BoxLayout(orientation='vertical', spacing=10)
        fdialog = FileChooserListView()
        fdialog.bind(selection=self.events_callback)
        box.add_widget(fdialog)

        if self.filter == 'folder':
            box.add_widget(SettingSpacer())
            box.add_widget(
                Button(text=self.text_button_ok, size_hint=(1, .1),
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


if __name__ in ('__main__', '__android__'):
    from kivy.base import runTouchApp

    class Test(BoxLayout):
        def __init__(self, **kvargs):
            super(Test, self).__init__(**kvargs)

            self.add_widget(
                Button(text='Press me!', on_release=self.show_manager)
            )

        def select(self, *args):
            self.file_manager.dismiss()

            try:
                print(args[1][0])
            except IndexError:
                print(self.file_manager.select_folder)

        def show_manager(self, *args):
            self.file_manager = \
                FDialog(events_callback=self.select, size_hint=(.5, .9))


    runTouchApp(Test())
