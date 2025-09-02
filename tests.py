import pytest
from main import BooksCollector
from conftest import collector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self, collector):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.get_books_genre()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()

    def test_add_new_book_add_one_book_valid_value(self, collector):
        collector.add_new_book('451 градус по фаренгейту')
        assert len(collector.get_books_genre()) == 1

    @pytest.mark.parametrize('invalid_value', ['123456789012345678901234567890123456789012', '12345678901234567890123456789012345678901', ''])
    def test_add_new_book_add_one_book_invalid_value(self, invalid_value, collector):
        collector.add_new_book(invalid_value)
        assert len(collector.get_books_genre()) == 0

    def test_add_new_book_add_two_same_books(self, collector):
        same_name = 'Над пропастью во ржи'
        collector.add_new_book(same_name)
        collector.add_new_book(same_name)
        assert len(collector.get_books_genre()) != 2

    def test_set_book_genre_valid_value_genre_in_collection(self, collector):
        book_name = 'Пикник на обочине'
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, 'Фантастика')
        assert collector.books_genre[book_name] == 'Фантастика'

    def test_set_book_genre_invalid_value_genre_not_in_collection(self, collector):
        book_name = 'Пикник на обочине'
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, 'Научная фантастика')
        assert collector.books_genre[book_name] != 'Научная фантастика'

    @pytest.mark.parametrize('book_name, book_genre', [['Пикник на обочине', 'Фантастика'], ['451 градус по Фаренгейту', 'Ужасы'],['12 Стульев', 'Комедии']])
    def test_get_book_genre_valid_value_book_in_collection(self, book_name, book_genre, collector):
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, book_genre)
        assert collector.get_book_genre(book_name) == book_genre

    def test_get_book_genre_invalid_value_genre_not_set_to_book(self, collector):
        collector.add_new_book('Пикник на обочине')
        assert collector.get_book_genre('Пикник на обочине') == ''

    def test_get_books_with_specific_genre_book_is_in_collection(self, collector):
        book_name = ['Пикник на обочине', '451 градус по Фаренгейту', 'Понедельник начинается в субботу']
        book_genre = ['Фантастика', 'Ужасы', 'Фантастика']
        for i in range(len(book_name)):
            collector.add_new_book(book_name[i])
            collector.set_book_genre(book_name[i], book_genre[i])
        fantasy_books = collector.get_books_with_specific_genre('Фантастика')
        assert len(fantasy_books) == 2
        assert 'Пикник на обочине' in fantasy_books
        assert 'Понедельник начинается в субботу' in fantasy_books

    def test_get_books_genre_not_empty_collection(self):
        collector = BooksCollector()
        book_name = ['Пикник на обочине', '451 градус по Фаренгейту', 'Понедельник начинается в субботу']
        book_genre = ['Фантастика', 'Ужасы', 'Фантастика']
        for i in range(len(book_name)):
            collector.add_new_book(book_name[i])
            collector.set_book_genre(book_name[i], book_genre[i])
        assert len(collector.get_books_genre()) == 3
        assert book_name[i] in collector.get_books_genre()

    def test_get_books_genre_empty_collection(self):
        collector = BooksCollector()
        assert len(collector.get_books_genre()) == 0

    @pytest.mark.parametrize('book_name, book_genre', [['Колобок', 'Фантастика'],['Кошкин дом', 'Комедии']])
    def test_get_books_for_children_valid_value_book_is_for_children_by_genre(self, book_name, book_genre):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, book_genre)
        books_for_children = collector.get_books_for_children()
        assert book_name in books_for_children

    def test_get_books_for_children_invalid_value_book_age_rating_in_collection(self):
        collector = BooksCollector()
        book_name = ['Кошкин дом', 'Колобок', 'По щучьему велению']
        book_genre = ['Фантастика', 'Ужасы', 'Фантастика']
        for i in range(len(book_name)):
            collector.add_new_book(book_name[i])
            collector.set_book_genre(book_name[i], book_genre[i])
        books_for_children = collector.get_books_for_children()
        assert 'Колобок' not in books_for_children

    @pytest.mark.parametrize('book_name, book_genre',
                             [['Пикник на обочине', 'Фантастика'], ['451 градус по Фаренгейту', 'Ужасы'],
                              ['12 Стульев', 'Комедии']])
    def test_add_book_in_favorites_valid_value_book_added_in_collection(self, book_name, book_genre):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, book_genre)
        collector.add_book_in_favorites(book_name)
        assert book_name in collector.favorites

    @pytest.mark.parametrize('book_name', ['Пикник на обочине', '451 градус по Фаренгейту', '12 Стульев'])
    def test_add_book_in_favorites_valid_value_book_without_genre_added_in_collection(self, book_name):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        assert book_name in collector.favorites

    def test_add_book_in_favorites_invalid_value_add_two_same_books(self):
        collector = BooksCollector()
        same_book = 'Пикник на обочине'
        collector.add_new_book(same_book)
        collector.add_book_in_favorites(same_book)
        collector.add_book_in_favorites(same_book)
        assert len(collector.favorites) != 2

    @pytest.mark.parametrize('book_name, book_genre',
                             [['Пикник на обочине', 'Фантастика'], ['451 градус по Фаренгейту', 'Ужасы'],
                              ['12 Стульев', 'Комедии']])
    def test_delete_book_from_favorites_valid_value_book_in_collection(self, book_name, book_genre):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, book_genre)
        collector.add_book_in_favorites(book_name)
        collector.delete_book_from_favorites(book_name)
        assert book_name not in collector.favorites

    def test_get_list_of_favorites_books(self):
        collector = BooksCollector()
        book_name = ['Пикник на обочине', '451 градус по Фаренгейту', 'Понедельник начинается в субботу']
        book_genre = ['Фантастика', 'Ужасы', 'Фантастика']
        for i in range(len(book_name)):
            collector.add_new_book(book_name[i])
            collector.set_book_genre(book_name[i], book_genre[i])
            collector.add_book_in_favorites(book_name[i])
        assert len(collector.get_list_of_favorites_books()) == len(collector.favorites)
        assert book_name[i] in collector.get_list_of_favorites_books()
        