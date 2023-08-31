import os
from pathlib import Path

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class PicGoogleTranslateParser:
    # if not os.path.exists('Output'):
    #     os.makedirs('Output')
    output = f'{Path.cwd()}/Output'
    tl = 'en'
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

        self.driver = Chrome(service=service, options=browser_options,)
        # self.driver = Chrome(options=browser_options,)

    def placer_google_translate_parser(self, filename):
        self.open_site()
        self.load_pic(filename)
        self.screenshot_translation(filename)

    def open_site(self):
        self.driver.get(self.BASE_URL.format(tl=self.tl))
        self._wait_and_choose_element(
            '//span[contains(text(),"Images")]',
            by=By.XPATH,
        ).click()

    def load_pic(self, filename):
        pic_path = os.path.abspath(os.path.dirname(__file__)) + f'/Input/{filename}'
        self._wait_and_choose_element('.r83qMb [class="D7BEKc"] input').send_keys(
            pic_path
        )
        # time.sleep(10)

    def screenshot_translation(self, filename):
        filename = filename.split('.')
        src = self._wait_and_choose_element('.dQBt [class="CMhTbb tyW0pd"] img').get_attribute('src')
        self.driver.get(src)
        # time.sleep(2)
        self._wait_and_choose_element(
            'img'
        ).screenshot(str(Path(self.output, f'{filename[0]}-{self.tl.upper()}.{filename[-1]}')))

    def _wait_and_choose_element(self, selector: str, by: By = By.CSS_SELECTOR, timeout: int = 20) -> WebElement:
        condition = EC.presence_of_element_located((by, selector))
        element = WebDriverWait(self.driver, timeout).until(condition)
        return element

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()


if __name__ == '__main__':
    folder_path = 'Input'
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            filename_format = filename.split('.')[1]
            if filename_format in ('png', 'jpg', 'jpeg'):
                print(filename)
                with PicGoogleTranslateParser() as placer:
                    placer.placer_google_translate_parser(filename)

            else:
                print('Not supported format file')

