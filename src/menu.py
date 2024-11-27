from library import Library


class Menu:
    """
    Класс, управлющий работой главного меню приложения.

    Атрибуты:
    ----------
    exit_flag : bool
        Флаг для остановки работы цикла.
    saved : bool
        Флаг для предупреждения при завершении работы пользователя о том, что библиотека не сохранена.

    Методы:
    -------
    __init__() -> None:
        Инициализирует новый объект меню устанавливает значения флагов exit_flag и saved в False.

    start() -> None:
        Запускает главное меню. Работает пока пользователь не выберет 0-ой вариант в консоли.
    """

    def __init__(self) -> None:
        """
        Инициализирует новый объект меню устанавливает значения флагов exit_flag и saved в False.
        """

        self.exit_flag: bool = False
        self.saved: bool = False

    def start(self) -> None:
        """
        Запускает главное меню. Работает пока пользователь не выберет 0-ой вариант в консоли.
        """

        while not self.exit_flag:
            print('0. Выход',
                  '1. Загрузить библиотеку',
                  '2. Сохранить библиотеку',
                  '3. Добавить в библиотеку книгу',
                  '4. Поиск книг',
                  '5. Удалить книгу из библиотеки',
                  '6. Отобразить все книги',
                  '7. Обновить статус книги',
                  sep='\n')
            match input():
                case '0':
                    if not self.saved:
                        print('Вы не сохранили библиотеку. Вы уверены, что хотите выйти?[y/n]')
                        if input() != 'y':
                            continue
                    self.exit_flag = True
                    print('Выход...')
                case '1':
                    filename = input('Введите имя файла, из которого хотите загрузить библиотеку: ')
                    Library().load(filename)
                case '2':
                    filename = input('Введите имя файла, в который хотели бы сохранить библиотеку: ')
                    Library().save(filename)
                    self.saved = True
                case '3':
                    title = input('Введите название книги: ')
                    author = input('Введите автора книги: ')
                    year = input('Введите год издания книги: ')
                    if not year.isdigit():
                        print('Год должен быть указан в виде числа')
                        continue
                    else:
                        Library().add_book(title, author, int(year))
                        self.saved = False

                case '4':
                    field = input('Введите характеристику, по которой будет вестись поиск (title/author/year): ')
                    if field not in ['title', 'author', 'year']:
                        print('Неверный ввод. Поиск может вестись по названию, автору или году издания книги.')
                        continue
                    else:
                        query = input('Введите запрос: ')
                        Library().search_books(field, query)

                case '5':
                    book_id = input('Введите ID книги, которую, хотите удалить: ')
                    Library().del_book(book_id)

                case '6':
                    Library().show_books()

                case '7':
                    book_id = input('Введите ID книги, статус которой хотите изменить: ')
                    new_status = input('Введите новый статус: ')
                    Library().update_status(book_id, new_status)

                case _:
                    print('Неверный ввод. Доступные варианты: 0-7')
