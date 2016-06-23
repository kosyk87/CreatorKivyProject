# -*- coding: utf-8 -*-

# Пример простого плагина. Добавляет кнопку в actionbar.


from kivy.clock import Clock
from kivy.uix.actionbar import ActionButton, ActionSeparator

from Libs.uix.kdialog import KDialog


def test_plugin(interval):
    action_view = app.start_screen.action_view
    item_button = \
        ActionButton(id='plugins', on_press=events_screen,
                     icon='{}/Libs/Plugins/TestPlugin/button.png'.format(
                         app.directory))
    action_view.add_widget(item_button, index=-1)
    action_view.add_widget(ActionSeparator(), index=-1)


def events_screen(button):
    KDialog(title='Plugin').show(
        text='[color=#ffffff]Привет, [color=#2fa7d4ff]{}!'.format(
            app.started_plugins['TestPlugin']['plugin-name']
    ))


Clock.schedule_once(test_plugin, 5)
