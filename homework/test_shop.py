"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    @pytest.mark.parametrize("quantity", (0, 999, 1000))
    def test_product_check_quantity(self, product, quantity):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(quantity) is True

    @pytest.mark.parametrize("quantity", [1001, 9999])
    def test_product_check_more_quantity(self, product, quantity):
        assert product.check_quantity(quantity) is False

    @pytest.mark.parametrize("quantity, expected", [
        (0, 1000),
        (999, 1),
        (1000, 0)
    ])
    def test_product_buy(self, product, quantity, expected):
        # TODO напишите проверки на метод buy
        product.buy(quantity)
        assert product.quantity == expected

    @pytest.mark.parametrize("quantity", [1001, 9999])
    def test_product_buy_more_than_available(self, product, quantity):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError, match = "Продуктов не хватает или некорректное значение"):
            product.buy(quantity)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product_in_cart(self, product, cart, buy_count=1):
        cart.add_product(product, buy_count)
        assert cart.products[product] == 1

    def test_add_existing_product_in_cart(self, product, cart):
        cart.add_product(product, 1)
        cart.add_product(product, 1)
        assert cart.products[product] == 2

    def test_add_product_with_zero_buy_count(self, product, cart, buy_count=0):
        with pytest.raises(ValueError, match = "Количество должно быть положительным числом"):
            cart.add_product(product, buy_count)

    def test_remove_product_from_cart(self, product, cart):
        cart.add_product(product, 3)
        cart.remove_product(product, 2)
        assert cart.products[product] == 1

    def test_remove_all_product(self, product, cart):
        cart.add_product(product, 3)
        cart.remove_product(product)
        assert product not in cart.products

    def test_add_and_remove_same_quantity_in_cart(self, product, cart):
        cart.add_product(product, 5)
        assert cart.products[product] == 5
        cart.remove_product(product, 5)
        assert product not in cart.products

    def test_remove_more_than_in_cart(self, product, cart):
        cart.add_product(product, 3)
        cart.remove_product(product, 5)
        assert product not in cart.products

    def test_remove_non_existing_product(self, product, cart):
        with pytest.raises(ValueError, match = f"Продукт {product.name} не найден в корзине."):
            cart.remove_product(product)

    def test_clear_cart(self, product, cart):
        cart.add_product(product, 5)
        cart.clear()
        assert len(cart.products) == 0

    def test_get_total_price(self, product, cart):
        cart.add_product(product, 2)
        assert cart.get_total_price() == product.price * 2

    def test_get_total_price_for_empty_cart(self, cart):
        assert cart.get_total_price() == 0

    def test_buy_cart(self, product, cart):
        cart.add_product(product, 2)
        cart.buy()
        assert product.quantity == 998

    def test_buy_cart_not_enough_quantity(self, product, cart):
        cart.add_product(product, 1001)
        with pytest.raises(ValueError, match = "Товара book не хватает на складе"):
            cart.buy()
