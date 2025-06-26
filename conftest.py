import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selene.support.shared import browser
from dotenv import load_dotenv
from utils import attach

@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()

@pytest.fixture(scope="function", autouse=True)
def setup_browser():
    options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": "128.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.set_capability("selenoid:options", selenoid_capabilities["selenoid:options"])
    options.set_capability("browserName", selenoid_capabilities["browserName"])
    options.set_capability("browserVersion", selenoid_capabilities["browserVersion"])

    remote_url = f"https://{os.getenv('LOGIN')}:{os.getenv('PASSWORD')}@selenoid.autotests.cloud/wd/hub"

    driver = webdriver.Remote(
        command_executor=remote_url,
        options=options
    )

    browser.config.driver = driver
    browser.config.base_url = "https://demoqa.com"
    browser.config.timeout = 10

    yield

    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_video(browser)

    browser.quit()
