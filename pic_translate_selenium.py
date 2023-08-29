import os
import time
from pathlib import Path

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class PicGoogleTranslateParser:
    if not os.path.exists('output'):
        os.makedirs('output')

    output = f'{Path.cwd()}/output'


    BASE_URL = 'https://translate.google.com/?hl=en&tab=TT&sl=auto&tl={tl}&op=images'

    def __init__(self):
        service = Service(ChromeDriverManager().install())
        browser_options = ChromeOptions()
        service_args = [
            # '--headless=True'
            '--start-maximized',
            '--no-sandbox',
            '--disable-web-security',
            '--disable-blink-features=AutomationControlled',
            '--allow-running-insecure-content',
            '--hide-scrollbars',
            '--disable-setuid-sandbox',
            '--profile-directory=Default',
            '--ignore-ssl-errors=true',
            '--disable-dev-shm-usage',
        ]
        for arg in service_args:
            browser_options.add_argument(arg)
        browser_options.add_experimental_option(
            'excludeSwitches', ['enable-automation']
        )
        browser_options.add_experimental_option('prefs', {
            'profile.default_content_setting_values.notifications': 2,
            'profile.default_content_settings.popups': 0
        })
        browser_options.add_experimental_option('useAutomationExtension', False)

        self.driver = Chrome( service=service, options=browser_options,)

    def placer_google_translate_parser(self):
        self.open_site()
        self.load_pic()
        self.screenshot_translation()

    def open_site(self):
        self.driver.get(self.BASE_URL.format(tl='ru'))
        self._wait_and_choose_element(
            '//span[contains(text(),"Images")]',
            by=By.XPATH,
        ).click()

    def load_pic(self):
        pic_path = os.path.abspath(os.path.dirname(__file__)) + '/images/input.jpg'
        self._wait_and_choose_element('.r83qMb [class="D7BEKc"] input').send_keys(
            pic_path
        )
        time.sleep(10)

    def screenshot_translation(self):
        p = f'{Path.cwd()}/output'
        src = self._wait_and_choose_element('.dQBt [class="CMhTbb tyW0pd"] img').get_attribute('src')
        self.driver.get(src)
        time.sleep(4)
        self._wait_and_choose_element(
            'img'
        ).screenshot(str(Path(p, f'pic_translation.png')))

    def _wait_and_choose_element(self, selector: str, by: By = By.CSS_SELECTOR, timeout: int = 10) -> WebElement:
        condition = EC.presence_of_element_located((by, selector))
        element = WebDriverWait(self.driver, timeout).until(condition)
        return element

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()


if __name__ == '__main__':
    with PicGoogleTranslateParser() as placer:
        placer.placer_google_translate_parser()
