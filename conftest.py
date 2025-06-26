import os
import pytest
from dotenv import load_dotenv
from selene import browser
from selenium.webdriver import ChromeOptions, Remote
from utils import attach


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='function', autouse=True)
def setup_browser():
    options = ChromeOptions()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": "128.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True,
            "enableLog": True
        },
        "goog:loggingPrefs": {"browser": "ALL"}
    }

    for key, value in selenoid_capabilities.items():
        options.set_capability(key, value)

    login = os.getenv('LOGIN')
    password = os.getenv('PASSWORD')
    url = os.getenv('URL')

    print(f"[DEBUG] login={login}, password={password}, url={url}")

    # Вот это важно
    browser.config.driver = Remote(
        command_executor=f'https://{login}:{password}@{url}/wd/hub',
        options=options
    )
    browser.config.base_url = 'https://demoqa.com'
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.config.timeout = 6.0

    yield

    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_video(browser)
    browser.quit()
