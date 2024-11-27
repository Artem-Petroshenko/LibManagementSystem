from json import load, dump, JSONDecodeError
from typing import Optional
from book import Book


class Library:
    """
    Singleton-класс для управления коллекцией книг в библиотеке.

    Атрибуты:
    ----------
    _instance : Optional['Library']
        Единственный экземпляр класса

    books : list
        Список всех книг в библиотеке.

    Методы:
    -------
    __new__(cls) -> 'Library':
        Создает экземпляр класса и возвращает его. При попытке создать еще один экземпляр будет возвращен уже созданный.

    __init__() -> None:
        Инициализирует объект библиотеки.

    load() -> None:
        Загружает библиотеку из файла в список books.

    save() -> None:
        Сохраняет библиотеку в файл JSON.

    add_book(title: str, author: str, year: int) -> None:
        Добавляет новую книгу в библиотеку.

    del_book(book_id: str) -> None:
        Удаляет книгу по id.

    search_books(field: str, query: str) -> List[Book]:
        Ищет книги по заданному полю (title, author, year).

    show_books() -> None:
        Отображает все книги в библиотеке.

    update_status(book_id: str, new_status: str) -> None:
        Изменяет статус книги по id.
    """

    _instance: Optional['Library'] = None

    def __new__(cls) -> 'Library':
        """
        Создает экземпляр класса и возвращает его. При попытке создать еще один экземпляр будет возвращен уже созданный.

        Параметры:
        -------
        cls : Type['Library']
            Текущий класс

        Возвращает:
        -------
        Optional['Library']
            Новый либо уже существующий объект библиотеки
        """

        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        """
        Инициализирует объект библиотеки.
        """

        if self._initialized:
            return
        self.books: list[Book] = list()
        self._initialized: bool = True

    def load(self, filename: str) -> None:
        """
        Загружает книги из файла в список books.
        """

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = load(f)
                self.books = [Book.from_dict(book) for book in data]
        except (FileNotFoundError, JSONDecodeError):
            print(f'Невозможно открыть или прочитать {filename}. Проверьте имя файла и/или что он не поврежден')

    def save(self, filename: str) -> None:
        """
        Сохраняет текущие книги в файл в формате JSON.
        """

        with open(filename, 'w', encoding='utf-8') as f:
            dump([book.to_dict() for book in self.books], f, ensure_ascii=False, indent='\t')

    def add_book(self, title: str, author: str, year: int) -> None:
        """
        Добавляет новую книгу в библиотеку с уникальным id и статусом "в наличии".

        Параметры:
        ----------
        title : str
            Название книги.
        author : str
            Автор книги.
        year : int
            Год издания книги.
        """

        new_book = Book(title, author, year)
        self.books.append(new_book)
        print(f'Новая книга добавлена: {new_book.title} (id: {new_book.id})')

    def del_book(self, book_id: str) -> None:
        """
        Удаляет книгу по id.

        Параметры:
        ----------
        book_id : int
            Уникальный идентификатор книги.
        """

        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                print(f'Книга {book.title} удалена')
                break
        else:
            print('Книга с таким ID не найдена. Проверьте, что введенный ID верен.')

    def search_books(self, field: str, query: str) -> None:
        """
        Ищет книги по заданному полю.

        Параметры:
        ----------
        field : str
            Поле для поиска, может быть 'title', 'author' или 'year'.
        query : str
            Строка для поиска.

        Возвращает:
        ---------
        list
            Список книг, удовлетворяющих запросу.
        """

        found_books = [
            book for book in self.books
            if query.lower() in str(getattr(book, field, "").lower())
        ]

        if found_books:
            print(f'Книг, найденных по запросу "{query}": {len(found_books)}')
            for book in found_books:
                print(book.to_dict())
        else:
            print(f'Книг по запросу "{query}" не найдено')

    def show_books(self) -> None:
        """
        Отображает все книги в библиотеке.
        """

        if not self.books:
            print('Библиотека пуста')
        else:
            print(f'Всего книг в бибилиотеке: {len(self.books)}')
            for book in self.books:
                print(book.to_dict())

    def update_status(self, book_id: str, new_status: str) -> None:
        """
        Изменяет статус книги по id.

        Параметры:
        ----------
        book_id : int
            Уникальный идентификатор книги.
        new_status : str
            Новый статус книги (должен быть "в наличии" или "выдана").
        """

        if new_status in ["в наличии", "выдана"]:
            for book in self.books:
                if book.id == book_id:
                    book.status = new_status
                    print(f'Статус книги {book.title} обновлён на "{new_status}".')
                    break
            else:
                print("Книга с таким ID не найдена.")
        else:
            print('Некорректный статус. Возможные варианты: "в наличии", "выдана".')
