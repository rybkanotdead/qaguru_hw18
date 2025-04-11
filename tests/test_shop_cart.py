from selene import browser, have
from allure import step
from api_shop.api import WebShopApi
from tests.conftest import BASE_URL

LOGIN = "ifoxspirit@yandex.ru"
PASSWORD = "qwerty12345"


def add_cookie(cookie):
    browser.open(BASE_URL)
    browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})


def test_adding_goods_to_the_cart():
    product_url = "/addproducttocart/catalog/31/1/1"
    cart_url = "/cart"

    with step("Api Добавление товара в корзину"):
        result = WebShopApi.send_request(product_url, method="POST")

    with step("Api Получение cookies"):
        cookie = result.cookies.get("Nop.customer")

    with step("Переход в корзину с помощью cookies"):
        add_cookie(cookie)
        browser.open(BASE_URL + cart_url)

    with step("WEB Проверка товара в корзине"):
        browser.element(".product-name").should(have.text("14.1-inch Laptop"))
        browser.element(".product-price.order-total").should(have.text("1590.00"))


def test_increase_quantity_goods_to_the_cart():
    product_url = "/addproducttocart/catalog/31/1/1"
    cart_url = "/cart"

    with step("Api Добавление товара в корзину"):
        result = WebShopApi.send_request(product_url, method="POST")

    with step("Api Получение cookies"):
        cookie = result.cookies.get("Nop.customer")

    with step("Api Увеличение количества товара в корзине"):
        WebShopApi.send_request(product_url, method="POST", cookies={"Nop.customer": cookie})

    with step("Переход в корзину с помощью cookies"):
        add_cookie(cookie)
        browser.open(BASE_URL + cart_url)

    with step("WEB Проверка увеличенного количества товара в корзине"):
        browser.element(".product-name").should(have.text("14.1-inch Laptop"))
        browser.element(".product-price.order-total").should(have.text("3180.00"))


def test_adding_several_goods_to_the_cart():
    first_product_url = "/addproducttocart/catalog/31/1/1"
    second_product_url = "/addproducttocart/details/72/1"
    cart_url = "/cart"

    with step("Api Добавление первого товара в корзину"):
        result = WebShopApi.send_request(first_product_url, method="POST")

    with step("Api Получение cookies"):
        cookie = result.cookies.get("Nop.customer")

    with step("Api Добавление второго товара в корзину"):
        WebShopApi.send_request(
            second_product_url,
            method="POST",
            data={
                "product_attribute_72_5_18": 3,
                "product_attribute_72_6_19": 54,
                "product_attribute_72_3_20": 57,
                "addtocart_72.EnteredQuantity": 1,
            },
            cookies={"Nop.customer": cookie},
        )

    with step("Переход в корзину с помощью cookis"):
        add_cookie(cookie)
        browser.open(BASE_URL + cart_url)

    with step("WEB Проверка добавленных товаров в корзине"):
        browser.element(".product-name").should(have.text("14.1-inch Laptop"))
        browser.all(".attributes").should(
            have.texts("Processor: 2X\nRAM: 2 GB\nHDD: 320 GB")
        )
        browser.element(".product-price.order-total").should(have.text("2390.00"))
