import os
import pytest
from dotenv import load_dotenv
from selene import browser
from selenium.webdriver import ChromeOptions
from selenium import webdriver

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
    options.set_capability('selenoid:options', selenoid_capabilities["selenoid:options"])
    options.set_capability('browserName', selenoid_capabilities["browserName"])
    options.set_capability('browserVersion', selenoid_capabilities["browserVersion"])
    options.set_capability('goog:loggingPrefs', selenoid_capabilities["goog:loggingPrefs"])

    login = os.getenv('LOGIN')
    password = os.getenv('PASSWORD')
    url = os.getenv('URL')

    browser.config.driver = webdriver.Remote(
        command_executor=f'https://{login}:{password}@{url}/wd/hub',
        options=options
    )
    browser.config.window_width = 1920
    browser.config.window_height = 1080

    yield

    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_video(browser)
    browser.quit()
