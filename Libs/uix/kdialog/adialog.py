# -*- coding: utf-8 -*-
#
# adialog.py
#

from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty

try:
    from . dialog import Dialog
    from . dialog import SettingSpacer
    from . dialog import ImageButton
except(ValueError, SystemError):
    from dialog import Dialog
    from dialog import SettingSpacer
    from dialog import ImageButton


class ADialog(Dialog):
    logo_program = StringProperty('data/logo/kivy-icon-24.png')
    '''Логотип приложения.

    :attr:` logo_program` is a :class:`~kivy.properties.StringProperty`
    and defaults to 'data/logo/kivy-icon-24.png'.
    '''

    name_program = StringProperty('Kivy 1.9.2')
    '''Название приложения.

    :attr:` name_program` is a :class:`~kivy.properties.StringProperty`
    and defaults to 'Kivy 1.9.2'.
    '''

    user_size_hint = ListProperty((.95, .85))
    '''Размер окна

    :attr: `user_size_hint` is a :class:`~kivy.properties.ListProperty`
    and defaults to [.95, .85].
    '''

    info_program = ListProperty([])

    Builder.load_file('{}/kv/adialog.kv'.format(Dialog.root))

    def __init__(self, **kvargs):
        super(ADialog, self).__init__(**kvargs)

        content = self.ids.content
        box_content = self.ids.box_content
        height, avatar_size_hint = (self.dp(60), (.05, .9))

        self.ids.logo.size_hint = avatar_size_hint
        self.ids.box_logo_and_title.height = height

        # Текстовая информация.
        for info_string in self.info_program:
            if info_string == '':
                content.add_widget(SettingSpacer())
                continue

            info_string = \
                Label(text=info_string, size_hint_y=None,
                      font_size=self.dp(self.base_font_size), markup=True,
                      on_ref_press=self.events_callback)
            info_string.bind(size=lambda *args: self._update_label_size(args))
            content.add_widget(info_string)

        self.content = box_content
        self.size_hint = (self.user_size_hint[0], self.user_size_hint[1])
        self.open()

    def _update_label_size(self, *args):
        label = args[0][0]

        if label.id == 'name_program':
            if not self.flag:
                label.height = self.dp(52)
        else:
            label.height = self.dp(label.texture_size[1] - 8)

        label.text_size = (self.dp(label.width - 30), None)
        label.texture_update()
