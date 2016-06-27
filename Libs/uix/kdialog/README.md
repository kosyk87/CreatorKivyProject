kdialog
--------
`Библиотека для работы с диалоговыми окнами`

ЯЗЫК ПРОГРАММИРОВАНИЯ
----------------------
`Python 2.7 +`

ЗАВИСИМОСТИ
------------
`Фреймворк Kivy и сопутствующие библиотеки`

УСТАНОВКА
----------
Скачайте (https://github.com/HeaTTheatR/kdialog.git) и распакуйте архив
в любую удобную дирекорию

ЗАПУСК ПРИМЕРОВ
----------------

```python
python [`'kdialog.py', 'adialog.py', 'cdialog.py', 'fdialog.py', 'bdialog', 'pdialog'`]
```

ВЕРСИЯ
-------
`Version 1.0.0`

ЛИЦЕНЗИЯ
--------
`MIT LICENSE`

ДОКУМЕНТАЦИЯ
-------------

kdialog
-------
`Библиотека для вывода диаолговых окон.`

`Луганская Народная Республика`, 11:27 16.06.16.

**version** `'1.0.0'`

**Автор** `Иванов Юрий aka HeaTTheatR`

**Email** `gorodage@gmail.com`

Библиотека предоставляет для работы следующие классы:

  **KDialog** - `класс для работы с диалоговыми окнами;`
 
  **ADialog** - `класс для работы с окном 'О программе';`
 
  **BDialog** - `класс для работы со списком кнопок;`
 
  **FDialog** - `класс для работы с файловым менеджером;`
 
  **CDialog** - `класс для работы с окном выбора цвета;`
 
  **PDialog** - `класс для работы с прогресс баром;`

Все классы имееют одного родителя,который наследуется от
:class:` ~kivy.uix.popup.Popup`. Поэтому при создании экземпляра любого из
вышеперечисленных классов, вы можете передавать и использовать все атрибуты
виджета Popup.

Импорт модуля в проект
----------------------

```python
from kdialog import class_module
```

Описание класса KDialog
------------------------

Создает окна следующих типов:

  **info** - `окно без кнопок выбора;`
 
  **query** - `окно с кнопками выбора;`
 
  **text** - `окно для ввода текста;`
 
  **logpass** - `окно для ввода логина и пароля с двойным полем ввода;`
 
  **loaddialog** - `окно прогресса;`

Пример окна с параметром 'info'
-------------------------------

```python
    KDialog().show(text='Твой текст!', param='info')
```

или

```python
    KDialog().show(text='Твой текст!')
```

![ScreenShot](https://raw.githubusercontent.com/HeaTTheatR/KDialog/master/data/screenshots/info.png)

Параметр **'info'** используется по умолчанию, поэтому при использовании
данного типа окна его указывать не обязательно.

Пример окна с параметром 'query'
--------------------------------

Для управления контролем событий окна, передайте параметру **answer_callback**
при создании экземпляра класса функцию-обработчик. Вы можете использовать
три управляющие кнопки **text_button_ok, text_button_no, text_button_cancel**:

```python
    def dialog_show(self, *args):
        def dialog_answer_handler(answer):
            print(answer)

        KDialog(answer_callback=dialog_answer_handler).show(
            text_button_ok='Yes', text_button_no='No',
            text=__doc__, param='query')
```

Также для всех типов окон вы можете указать функцию, которая будет вызвана
при закрытии окна, передав ее в параметр **dismiss_callback**:

```python
    def dialog_show(self, *args):
        def dialog_answer_handler(answer):
            print(answer)

        def dialog_dismiss_handler(*args):
            print('Window dismiss!')

        KDialog(answer_callback=dialog_answer_handler,
                dismiss_callback=dialog_dismiss_handler).show(
            text_button_ok='Yes', text_button_no='No',
            text=__doc__, param='query')
```

![ScreenShot](https://raw.githubusercontent.com/HeaTTheatR/KDialog/master/data/screenshots/query.png)

Вы можете использовать виждет RstDocument для вывода текстовой информации.
Укажите дополнительный параметр **rst=True** при вызове окна:

```python
    KDialog(answer_callback=dialog_answer_handler,
            dismiss_callback=dialog_dismiss_handler).show(
        text_button_ok='Yes', text_button_no='No',
        text=__doc__, param='query', rst=True)
```

![ScreenShot](https://raw.githubusercontent.com/HeaTTheatR/KDialog/master/data/screenshots/rst.png)

Пример окна с параметром 'text'
--------------------------------

```python
        def show_dialog(self, *args):
            def edit_status(answer):
                print(answer)

            KDialog(answer_callback=edit_status).show(
                text_button_ok='Yes', param='text')
```

![ScreenShot](https://raw.githubusercontent.com/HeaTTheatR/KDialog/master/data/screenshots/text.png)

Пример окна с параметром 'logpass'
----------------------------------

```python
        def show_dialog(self, *args):
            def set_login_password(data):
                """
                type data: list
                param data: ['login', 'password']

                """

                if ''.join(answer) == '':
                    return

                login, password = answer
                print('login -', login, 'password -', password)

            KDialog(answer_callback=set_login_password).show(
                text_button_ok='Yes', param='logpass', password=True)
```

![ScreenShot](https://raw.githubusercontent.com/HeaTTheatR/KDialog/master/data/screenshots/logpass.png)

Обратите внимание, что если не указывать в параметре **password**
значение **True** - вводимый текст не будет скрываться звездочками.

Пример окна с параметром 'loaddialog'
-------------------------------------

```python
        def show_dialog(self, *args):
            def connection_to_server(*args):
                import urllib

                page = urllib.urlopen('http://python.org')
                print('Page loading')
                progress.dismiss()

            KDialog(progress_callback=connection_to_server).show(
                param='loaddialog')
```

![ScreenShot](https://raw.githubusercontent.com/HeaTTheatR/KDialog/master/data/screenshots/loaddialog.png)

Описание класса ADialog
------------------------
Для использования класса вам нужно передать при его инициализации три
параметра:

  **name_program** - `имя программы;`
 
  **info_program** - `список визуализируемой информации;`
 
  **logo_program** - `путь к иконке логотипа программы;`
 

Пример использования
---------------------

```python
        def events_callback(self, instance_label, text_link):
            print(text_link)

        def about_dismiss(self, *args):
            print('Dialog dismiss')

        def build(self):
            return Button(text='Press Me', on_press=self.show)

        def show(self, *args):
            name_program = '[color=#ff7f32][size=22]HeaTDV4A[/size] ' \
                           '[size=16][color=#2fbfe0]blue-[color=#ff7f32]' \
                           'orange [/size][color=#ffffffff]version 0.0.1'
            logo_program = 'data/logo/kivy-icon-24.png'
            info_program = [
                '',

                '[color=#ffffffff]Мобильный клиент сайта [color=#2fbfe0]'
                '[ref=www.dimonvideo.ru]dimonvideo.ru[/ref]',

                '',

                '[b][color=#ffffffff]Автор - [/b][color=#ff7f32]Иванов Юрий '
                '[color=#ffffffff]aka [color=#2fbfe0][ref=http://dimonvideo.ru'
                '/smart/0/name/HeaTTheatR]HeaTTheatR[/ref]',

                '[b][color=#ffffffff]Система плагинов - [/b][color=#ff7f32]'
                'Виталий [color=#ffffffff]aka [color=#2fbfe0][ref=http://'
                'dimonvideo.ru/smart/0/name/Virtuos86]Virtuos86[/ref]',

                '[b][color=#ffffffff]Серверная часть - [/b][color=#ff7f32]'
                'Дмитрий [color=#ffffffff]aka [color=#2fbfe0][ref=http://'
                'dimonvideo.ru/smart/0/name/dimy44]dimy44[/ref]',

                '',

                '[b][color=#ffffffff]E-mail - [/b][color=#2fbfe0]'
                '[ref=gorodage@gmail.com]gorodage@gmail.com[/ref]',

                '[b][color=#ffffffff]Исходный код - [/b]'
                '[ref=https://github.com/HeaTTheatR/HeaTDV4A.git]'
                '[color=#2fbfe0]github.com[/ref]',

                '[color=#ff7f32]P.S',

                '',

                '[color=#ffffffff]Программа написана на языке '
                'программирования [ref=www.python.org][color=#2fbfe0]Python '
                '[/ref][color=#ffffffff]с использованием фреймворка '
                '[ref=www.kivy.org][color=#2fbfe0]Kivy[/ref]',

                '[color=#ff7f32]P.P.S',

                '',

                '[i][color=#ffffffff]Хотите добиться успеха - приложите все '
                'силы для создания наилучшего продукта. А если он не принесет '
                'вам успеха, значит, так тому и быть.[/i]',

                '[i]Успеха достигает тот, '
                'кто обеспечивает качество и удовлетворяет потребности.[/i]',

                '',

                '[color=#ff7f32]Linus TORVALDS [color=#ffffffff]and '
                '[color=#ff7f32]David DIAMOND.',

                '[color=#ffffffff] "JUST FOR  FUN. THE  STORY OF AN ACCIDENTAL '
                'REVOLUTIONARY."'
            ]

            ADialog(dismiss_callback=self.about_dismiss,
                    events_callback=self.events_callback,
                    logo_program=logo_program, info_program=info_program,
                    name_program=name_program)
```

![ScreenShot](https://raw.githubusercontent.com/HeaTTheatR/KDialog/master/data/screenshots/about.png)

Обратите внимание, что в списке **info_program** пустые строчки ('') при
выводе окна на экран будут заменены на разделительные линии.

`Окно ADialog не снабжается управляющими кнопками.`

Описание класса FDialog
------------------------
Предоставляет два режима - выбор директорий и выбор файлов. По умолчанию
используется режим выбора файлов. Для перехода в режим выбора директории
передайте при инициализации класса параметру **filter** значение **'folder'**.

Пример использования
---------------------

```python
        def select(self, *args):
            self.file_manager.dismiss()

            try:
                print(args[1][0])
            except IndexError:
                print(self.file_manager.select_folder)

        def show_manager(self, *args):
            self.file_manager = \
                FDialog(events_callback=self.select, size_hint=(.5, .9),
                        filter='folder')
            return self.file_manager
```

![ScreenShot](https://raw.githubusercontent.com/HeaTTheatR/KDialog/master/data/screenshots/fdialog.png)

Описание класса CDialog
------------------------
Предоставляет окно для выбора цвета.

Пример использования
---------------------

```python
        def select(self, *args):
            print(args[0])

        def show_palette(self, *args):
            self.select_color = \
                CDialog(events_callback=self.select, size_hint=(.8, .97))
```

![ScreenShot](https://raw.githubusercontent.com/HeaTTheatR/KDialog/master/data/screenshots/cdialog.png)

При инициализации класса вы можете передать параметру **default_color**
значение цвета по умолчанию в hex формате.

Декораторы и кнопки
--------------------
Для использования пользовательского фона окон и кнопок при 
инициализации класса передайте параметрам **background** и 
**background_image_buttons** свои значения. Для фона окна это строка - путь 
к изображению декоратора. По умолчанию это

```python
    'data/decorator.png'
```

Для фона кнопок используйте словарь. По умолчанию это -
 
```python
    background_image_buttons = (
        {0: 'data/button_ok.png', 1: 'data/button_no.png', 2: 'data/button_cancel.png'}
    )
```

Описание класса BDialog
------------------------
Предоставляет список кнопок.

Пример использования
---------------------
Передайте при инициализации класса BDialog параметру button_list список вида 
['Текст кнопки', 'путь к фону кнопки', ...]:

```python
        def on_press(self, instance_button):
            print(instance_button.id)

        def show_dialog(self, *args):
            button_list = []
            for i in range(50):
                button_list.append(
                    ['Text{0:3d}'.format(i),
                     '{}/data/button_ok.png'.format(root)]
                )

            BDialog(
                events_callback=self.on_press, button_list=button_list,
                hint_x=1.8, title='Пример окна BDialog').show()
```

![ScreenShot](https://raw.githubusercontent.com/HeaTTheatR/KDialog/master/data/screenshots/bdialog.png)

Описание класса PDialog
------------------------
Предоставляет простой прогресс бар.

Пример использования
---------------------

```python
        def complete(self):
            '''Функция вызывается после окончания цикла прогресса.'''

            KDialog(title='Info').show(text='Complete!')

        def retrieve_callback(self, *args):
            '''Функция вызывается во время цикла прогресса.'''

            tick = args[1]  # метод _tick класса PDialog
            complete = args[2]  # метод self.complete
            args = args[0]  # аргументы, переданные в метод show

            for i in range(1, 101):
                assert(self.cancel_flag > 0)
                tick(i, 100)
                time.sleep(.1)

            complete()

        def download_cancel(self, *args):
            '''Функция вызывается после прерывания цикла прогресса.'''

            self.cancel_flag = False
            self.progress_load.dismiss()
            self.cancel_flag = True

        def show_progress(self, *args):
            self.progress_load = \
                BDialog(title='Пример окна PDialog',
                        retrieve_callback=self.retrieve_callback,
                        events_callback=self.download_cancel,
                        complete=self.complete)
            self.progress_load.show()
```

![ScreenShot](https://raw.githubusercontent.com/HeaTTheatR/KDialog/master/data/screenshots/pdialog.png)

Пример окна с параметром 'check'
-------------------------------------

Для того, чтобы в окно был добавлен чекбокс, укажите параметр **check=True**
и подпишите его - **check_text='Больше не показывать'**.

```python
    def dialog_show(self, *args):
        def dialog_answer_handler(answer):
            print(answer)

        KDialog(title='Пример окна с параметром `check`',
                answer_callback=dialog_answer_handler).show(
            text='Нажмите `OK...`', check_text='Больше не показывать',
            param='query', text_button_ok='OK', check=True,
            auto_dismiss=True)
```

![ScreenShot](https://raw.githubusercontent.com/HeaTTheatR/KDialog/master/data/screenshots/check.png)

КОНТАКТЫ
---------
**Email**: `gorodage@gmail.com`

[Аккаунт на Хабре](https://habrahabr.ru/users/heattheatr/)

[Аккаунт ВКОНТАКТЕ](https://vk.com/heattheatr)
