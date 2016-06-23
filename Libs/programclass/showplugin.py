#! /usr/bin/python3.4
# -*- coding: utf-8 -*-
#
# showplugin.py
#

import os


class ShowPlugin(object):
    '''Выводит на экран список установленных плагинов.'''

    def show_plugins(self):
        def select_plugin(*args):
            '''Вызывается при клике на имя плагина из списка.'''

            def activate_plugin(*args):
                '''Вызывается при клике на кнопки выбора
                'Подключить/Отключить' плагин.'''

                def save_activate_plugin(*args):
                    answer = args[0]

                    if answer == self.core.string_lang_yes:
                        manifest = \
                            self.Manifest('{}/Libs/Plugins/{}/manifest.txt'.format(
                                self.directory, name_plugin))
                        manifest['app-version-max'] = app_version
                        manifest.save('{}/Libs/Plugins/{}/manifest.txt'.format(
                            self.directory, name_plugin))
                    elif answer == self.core.string_lang_no:
                        return

                    list_activate_plugins.append(name_plugin)
                    open('{}/Libs/Plugins/plugins_list.list'.format(
                        self.directory), 'w').write(str(list_activate_plugins))

                    if answer == 'Warning':
                        text = '{}\n\n{}'.format(
                            self.core.string_lang_plugin.format(
                               name_plugin),
                            self.core.string_lang_plugin_warning.format(
                               name_plugin, app_version_min, app_version))
                    else:
                        text = self.core.string_lang_plugin_activate.format(
                            name_plugin)
                    self.KDialog(title=self.name_program,
                                 base_font_size=self.window_text_size).show(
                        text=text)

                answer = args[0]

                if answer == self.core.string_lang_plugin_enable:
                    app_version_min = \
                        self.started_plugins[name_plugin]['app-version-min']
                    app_version_max = \
                        self.started_plugins[name_plugin]['app-version-max']
                    app_version = \
                        self.started_plugins[name_plugin]['app-version']

                    if app_version_min > app_version:
                        save_activate_plugin('Warning')
                        return

                    if app_version > app_version_max:
                        window = \
                            self.KDialog(base_font_size=self.window_text_size,
                                         answer_callback=save_activate_plugin)
                        window.show(
                            text=self.core.string_lang_plugin_warning.format(
                                name_plugin, app_version_min, app_version),
                            text_button_ok=self.core.string_lang_yes,
                            text_button_no=self.core.string_lang_no,
                            param='query')
                        return
                    else:
                        save_activate_plugin('Ok')
                elif answer == self.core.string_lang_plugin_switch_off:
                    list_activate_plugins.remove(name_plugin)
                    open('{}/Libs/Plugins/plugins_list.list'.format(
                        self.directory), 'w').write(str(list_activate_plugins))

            name_plugin = args[0].id

            if not os.path.exists('{}/Libs/Plugins/{}/README.rst'.format(
                    self.directory, name_plugin)):
                info_plugin = \
                    '[color=ffffff]{} [color=#ff7f32]\'{}\'[/color]\n' \
                    '=======================\n\n' \
                    '[color=#ffffff]Version [color=#2fbfe0]{}\n\n' \
                    '[color=#ffffff]Author `{} <{}>`_' \
                    ''.format(
                        self.core.string_lang_plugin[:-1], name_plugin,
                        self.started_plugins[name_plugin]['plugin-version'],
                        self.started_plugins[name_plugin]['plugin-author'],
                        self.started_plugins[name_plugin]['plugin-mail'])
            else:
                info_plugin = open('{}/Libs/Plugins/{}/README.rst'.format(
                    self.directory, name_plugin)).read()

            window = \
                self.KDialog(title=self.name_program,
                             base_font_size=self.window_text_size,
                             answer_callback=activate_plugin)
            window.show(text=info_plugin, text_button_ok=switch_text,
                        text_button_cancel=self.core.string_lang_cancel,
                        param='query', auto_dismiss=True)

        list_all_plugins = []
        list_activate_plugins = eval(
            open('{}/Libs/Plugins/plugins_list.list'.format(
                self.directory)).read())

        for plugin in os.listdir('{}/Libs/Plugins'.format(self.directory)):
            if not os.path.isdir('{}/Libs/Plugins/{}'.format(
                    self.directory, plugin)):
                continue

            if plugin in list_activate_plugins:
                image = '{}/Libs/uix/kdialog/data/button_ok.png'.format(
                    self.directory)
                switch_text = self.core.string_lang_plugin_switch_off
            else:
                image = '{}/Libs/uix/kdialog/data/button_cancel.png'.format(
                    self.directory)
                switch_text = self.core.string_lang_plugin_enable

            list_all_plugins.append([plugin, image])

        if not len(list_all_plugins):
            self.KDialog(title=self.name_program,
                         base_font_size=self.window_text_size).show(
                text=self.core.string_lang_not_install_plugin)
            return

        scroll_plugin = \
            self.BDialog(title=self.core.string_lang_plugin,
                         events_callback=select_plugin,
                         button_list=list_all_plugins, hint_x=1.6)
        scroll_plugin.show()
