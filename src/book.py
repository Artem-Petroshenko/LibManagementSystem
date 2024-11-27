from uuid import uuid4


class Book:
    """
    Класс, представляющий книгу в библиотеке.

    Атрибуты:
    ----------
    id : str
        Уникальный идентификатор книги.
    title : str
        Название книги.
    author : str
        Автор книги.
    year : int
        Год издания книги.
    status : str
        Статус книги (в наличии или выдана).

    Методы:
    -------
    __init__(title: str, author: str, year: int) -> None:
        Инициализирует новый объект книги с уникальным id и статусом "в наличии".

    to_dict() -> dict:
        Преобразует объект книги в словарь для сохранения в JSON.

    from_dict(cls, data: dict) -> 'Book':
        Статический метод класса. Создаёт объект книги из данных в виде словаря.
    """

    def __init__(self, title: str, author: str, year: int, status: str = 'в наличии') -> None:
        """
        Инициализирует новый объект книги с уникальным id и статусом "в наличии".

        Параметры:
        ----------
        title : str
            Название книги.
        author : str
            Автор книги.
        year : int
            Год издания книги.
        """

        self.id: str = str(uuid4())
        self.title: str = title
        self.author: str = author
        self.year: int = year
        self.status: str = status

    def to_dict(self) -> dict:
        """
        Преобразует объект книги в словарь.

        Возвращает:
        ---------
        dict
            Словарь, представляющий объект книги.
        """

        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status,
        }

    @staticmethod
    def from_dict(data) -> 'Book':
        """
        Статический метод класса. Создаёт объект книги из словаря.

        Параметры:
        ----------
        data : dict
            Данные книги в виде словаря.

        Возвращает:
        ---------
        Book
            Новый объект книги, созданный из словаря.
        """

        book = Book(data['title'], data['author'], data['year'])
        book.id = data['id']
        book.status = data['status']
        return book
