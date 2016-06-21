#! /usr/bin/python3.4
#
# programdata.py
#

import os
import sys
import traceback

try:
    from kivy.config import ConfigParser
except Exception as text_error:
    raise text_error


__version__ = '0.0.1'

select_locale = {'Русский': 'russian', 'English': 'english'}
prog_path = os.path.split(os.path.abspath(sys.argv[0]))[0]

# Если файл настроек отсутствует.
if not os.path.exists('{}/program.ini'.format(prog_path)) \
        or open('{}/program.ini'.format(prog_path)).read() == '':
    language = 'russian'
    theme = 'blue_orange'
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

theme_background_screen = eval(config_theme.get("color", "background_screen"))
theme_background_window = eval(config_theme.get("color", "background_window"))
theme_text_color = config_theme.get("color", "text_color")
theme_key_text_color = config_theme.get("color", "key_text_color")
theme_link_color = config_theme.get("color", "link_color")
theme_separator_color_window = eval(config_theme.get("color", "separator_color_window"))
theme_underline_color_title = config_theme.get("color", "underline_color_title")

theme_decorator_window = "Data/Themes/{}/{}".format(theme, config_theme.get(
    "resource", "decorator_window"))
theme_check_normal = "Data/Themes/{}/{}".format(theme, config_theme.get(
    "resource", "check_normal"))
theme_check_down = "Data/Themes/{}/{}".format(theme, config_theme.get(
    "resource", "check_down"))

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
