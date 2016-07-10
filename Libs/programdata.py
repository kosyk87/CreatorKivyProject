#! /usr/bin/python3.4
#
# programdata.py
#

import os
import sys
import traceback

from kivy.config import ConfigParser


__version__ = '0.0.1'

select_locale = {'Русский': 'russian', 'English': 'english'}
prog_path = os.path.split(os.path.abspath(sys.argv[0]))[0]

# Если файл настроек отсутствует.
if not os.path.exists('{}/program.ini'.format(prog_path)) \
        or open('{}/program.ini'.format(prog_path)).read() == '':
    language = 'russian'
    theme = 'default'
else:
    config = ConfigParser()
    config.read('{}/program.ini'.format(prog_path))
    theme = config.get('Theme', 'theme')
    language = select_locale[config.get('General', 'language')]
    # языковая локализация

# -----------------------УСТАНОВКА ЦВЕТОВОЙ ТЕМЫ---------------------------
config_theme = ConfigParser()
config_theme.read("{}/Data/Themes/{theme}/{theme}.ini".format(
    prog_path, theme=theme))

color_action_bar = eval(config_theme.get("color", "color_action_bar"))
color_body_program = eval(config_theme.get("color", "color_body_program"))
separator_color = eval(config_theme.get("color", "separator_color"))
theme_text_color = config_theme.get("color", "text_color")
theme_text_color_action_item = config_theme.get("color", "text_color_action_item")
theme_key_text_color = config_theme.get("color", "key_text_color")
theme_link_color = config_theme.get("color", "link_color")

try:  # устанавливаем языковую локализацию
    exec(open('{}/Data/Language/{}.txt'.format(
        prog_path, language), encoding='utf-8-sig').read().replace(
            "#key_text_color", theme_key_text_color).replace(
            "#text_color", theme_text_color).replace(
            "#link_color", theme_link_color))
except Exception:
    raise Exception(traceback.format_exc())

dict_language = {
    string_lang_on_russian: "russian",
    string_lang_on_english: "english"
}
