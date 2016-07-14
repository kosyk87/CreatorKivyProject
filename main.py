#! /usr/bin/python3.4
#
# main.py
#
# Точка входа в приложение. Запускает основной программный код program.py.
# В случае ошибки, выводит на экран окно с ее текстом.
#

import os
import sys
import shutil
import argparse

try:
    from kivy.logger import Logger
except Exception:
    import traceback
    raise(traceback.format_exc())

__version__ = '0.0.1'

if len(sys.argv) <= 1:
    Logger.warning('''
Используйте скрипт со строковыми аргументами:

'name' - Имя проекта
'path' - Директория проекта
'repo' - Адресс репозитория на GitHub
    ''')
    sys.exit(0)

prog_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
# sys.dont_write_bytecode = True

parser = argparse.ArgumentParser()
parser.add_argument('name', type=str, help='Имя проекта')
parser.add_argument('path', type=str, help='Директория проекта')
parser.add_argument('repo', type=str, help='Адресс репозитория на GitHub')

name_project = parser.parse_args().name
dir_project = parser.parse_args().path
repo_project = parser.parse_args().repo

full_path_to_project = '{}/{}'.format(dir_project, name_project)
dir_language = '{}/Data/Language'.format(full_path_to_project)
dir_settings = '{}/Data/Settings'.format(full_path_to_project)

if os.path.exists(full_path_to_project):
    Logger.error('Проект {} уже существует!'.format(name_project))
    sys.exit(0)

try:
    for directory in [full_path_to_project, dir_language, dir_settings]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            Logger.info('Создана директория проекта {} ...'.format(directory))
except FileNotFoundError:
    Logger.error('Указанная директория {} не существует!'.format(dir_project))
except PermissionError:
    Logger.error('У вас нет прав для создания проекта в директории {}!'.format(
        dir_project))

try:
    Logger.info('Создание точки входа main.py ...')
    open('{}/main.py'.format(full_path_to_project), 'w').write(
        open('{}/Data/Files/main'.format(prog_path)).read() % repo_project)

    Logger.info('Создание файла языковой локализации russian.txt ...')
    open('{}/russian.txt'.format(dir_language), 'w').write(open(
        '{}/Data/Files/russian'.format(prog_path)).read().format(
        NAME_PROJECT=name_project, REPOSITORY=repo_project, NAME_PLUGIN='{}',
        VERSION='{}'))

    Logger.info('Создание файла README.md ...')
    open('{}/README.md'.format(full_path_to_project), 'w').write(
        open('{}/Data/Files/README'.format(prog_path)).read().format(
            NAME_PROJECT=name_project))

    data = {
        '{}/program.py'.format(full_path_to_project):
            'Создание файла программного кода program.py ...',
        '{}/Data/Settings/general.json'.format(full_path_to_project):
            'Создание файла настроек general.json ...',
        '{}/Data/Settings/theme.json'.format(full_path_to_project):
            'Создание файла настроек theme.json ...'}
    for file in data.keys():
        Logger.info(data[file])
        open(file, 'w').write(open('{}/Data/Files/{}'.format(
            prog_path, os.path.splitext(os.path.split(file)[1])[0])).read())

    Logger.info('Копирование файлов проекта ...')
    for directory in ['{}/Libs', '{}/LICENSE', '{}/Data/Images',
                      '{}/Data/Themes']:
        shutil.copytree(directory.format(prog_path),
                        directory.format(full_path_to_project))

except FileNotFoundError as exc:
    Logger.error('Не могу найти файл проекта - ', exc)
    shutil.rmtree(full_path_to_project)
    sys.exit(0)
except Exception as exc:
    Logger.error('Неизвестная ошибка - ', exc)
    shutil.rmtree(full_path_to_project)
    sys.exit(0)

Logger.info('')
Logger.info('Проект {} успешно создан!'.format(name_project))
