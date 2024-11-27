import unittest
import os
from json import load
from src.library import Library


class TestLibrary(unittest.TestCase):
    def setUp(self) -> None:
        """Создаёт тестовую библиотеку перед каждым тестом."""
        self.test_file = "test_library.json"
        self.library = Library()
        self.library.books = []

    def tearDown(self) -> None:
        """Удаляет тестовый файл после тестов."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_book(self) -> None:
        """Проверяет добавление книги."""
        self.library.add_book("1984", "Джордж Оруэлл", 1949)
        self.assertEqual(len(self.library.books), 1)
        book = self.library.books[0]
        self.assertEqual(book.title, "1984")
        self.assertEqual(book.author, "Джордж Оруэлл")
        self.assertEqual(book.year, 1949)
        self.assertEqual(book.status, "в наличии")

    def test_delete_book(self) -> None:
        """Проверяет удаление книги."""
        self.library.add_book("1984", "Джордж Оруэлл", 1949)
        book_id = self.library.books[0].id
        self.library.del_book(book_id)
        self.assertEqual(len(self.library.books), 0)

    def test_delete_nonexistent_book(self) -> None:
        """Проверяет удаление несуществующей книги."""
        initial_count = len(self.library.books)
        self.library.del_book("nonexistent-id")
        self.assertEqual(len(self.library.books), initial_count)

    def test_search_books_by_title(self) -> None:
        """Проверяет поиск книги по названию."""
        self.library.add_book("1984", "Джордж Оруэлл", 1949)
        self.library.add_book("Мастер и Маргарита", "Михаил Булгаков", 1966)

        result = [book.to_dict() for book in self.library.books if "1984".lower() in book.title.lower()]
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "1984")

    def test_search_books_by_author(self) -> None:
        """Проверяет поиск книги по автору."""
        self.library.add_book("1984", "Джордж Оруэлл", 1949)
        self.library.add_book("Мастер и Маргарита", "Михаил Булгаков", 1966)

        result = [book.to_dict() for book in self.library.books if "Булгаков".lower() in book.author.lower()]
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["author"], "Михаил Булгаков")

    def test_search_books_by_year(self) -> None:
        """Проверяет поиск книги по году издания."""
        self.library.add_book("1984", "Джордж Оруэлл", 1949)
        self.library.add_book("Мастер и Маргарита", "Михаил Булгаков", 1966)

        result = [book.to_dict() for book in self.library.books if 1966 == book.year]
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["author"], "Михаил Булгаков")

    def test_update_status(self) -> None:
        """Проверяет обновление статуса книги."""
        self.library.add_book("1984", "Джордж Оруэлл", 1949)
        book_id = self.library.books[0].id

        self.library.update_status(book_id, "выдана")
        self.assertEqual(self.library.books[0].status, "выдана")

        self.library.update_status(book_id, "в наличии")
        self.assertEqual(self.library.books[0].status, "в наличии")

    def test_update_status_invalid(self) -> None:
        """Проверяет попытку обновления статуса на недопустимый."""
        self.library.add_book("1984", "Джордж Оруэлл", 1949)
        book_id = self.library.books[0].id

        self.library.update_status(book_id, "утеряна")
        self.assertEqual(self.library.books[0].status, "в наличии")

    def test_display_books(self) -> None:
        """Проверяет вывод всех книг."""
        self.library.add_book("1984", "Джордж Оруэлл", 1949)
        self.library.add_book("Мастер и Маргарита", "Михаил Булгаков", 1966)

        books = [book.to_dict() for book in self.library.books]
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0]["title"], "1984")
        self.assertEqual(books[1]["title"], "Мастер и Маргарита")

    def test_load_books(self) -> None:
        """Проверяет загрузку книг из файла."""
        self.library.add_book("1984", "Джордж Оруэлл", 1949)
        self.library.save(self.test_file)

        new_library = Library()
        new_library.load(self.test_file)
        self.assertEqual(len(new_library.books), 1)
        self.assertEqual(new_library.books[0].title, "1984")

    def test_save_books(self) -> None:
        """Проверяет сохранение книг в файл."""
        self.library.add_book("1984", "Джордж Оруэлл", 1949)
        self.library.save(self.test_file)

        with open(self.test_file, "r", encoding="utf-8") as file:
            data = load(file)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["title"], "1984")


if __name__ == "__main__":
    unittest.main()
