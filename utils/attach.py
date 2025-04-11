import allure
from allure_commons.types import AttachmentType


# Скриншоты
def add_screenshot(browser):
    if not hasattr(browser, 'driver'):
        return
    png = browser.driver.get_screenshot_as_png()
    allure.attach(png, 'screenshot', AttachmentType.PNG, '.png')


# логи
def add_logs(browser):
    log = "".join(f'{text}\n' for text in browser.driver.get_log(log_type='browser'))
    allure.attach(log, 'browser_logs', AttachmentType.TEXT, '.log')


# html-код страницы
def add_html(browser):
    html = browser.driver.page_source
    allure.attach(html, 'page_source', AttachmentType.HTML, '.html')