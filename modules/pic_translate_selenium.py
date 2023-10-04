import os
import shutil
import time
from pathlib import Path

from selenium.common import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class PicGoogleTranslateParser:
    if not os.path.exists('temporary'):
        os.makedirs('temporary')
    # shutil.rmtree(os.path.join(os.getcwd(), 'temporary'))
    tl = 'en'
    BASE_URL = 'https://translate.google.com/?hl=en&tab=TT&sl=auto&tl={tl}&op=images'

    def __init__(self):
        service = Service(ChromeDriverManager().install())
        browser_options = ChromeOptions()
        service_args = [
            # '--start-maximized',
            '--no-sandbox',
            '--disable-web-security',
            '--disable-blink-features=AutomationControlled',
            '--allow-running-insecure-content',
            '--hide-scrollbars',
            '--disable-setuid-sandbox',
            '--profile-directory=Default',
            '--ignore-ssl-errors=true',
            '--disable-dev-shm-usage',
            # '--headless=new',
        ]
        for arg in service_args:
            browser_options.add_argument(arg)
        # browser_options.add_experimental_option(
        #     'excludeSwitches', ['enable-automation']
        # )
        browser_options.add_experimental_option('prefs', {
            'profile.default_content_setting_values.notifications': 2,
            'profile.default_content_settings.popups': 0
        })
        browser_options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        browser_options.add_experimental_option('useAutomationExtension', False)
        browser_options.add_argument('--disable-blink-features=AutomationControlled')
        prefs = {"profile.default_content_settings.popups": 0,
                 "download.default_directory": os.path.join(os.getcwd(), 'temporary'),
                 "directory_upgrade": True}
        browser_options.add_experimental_option('prefs', prefs)

        self.driver = Chrome(service=service, options=browser_options)

    def placer_google_translate_parser(self, filename):
        self.open_site()
        self.load_pic(filename)
        self._wait_and_choose_element('//span[contains(text(), "Download translation")]', by=By.XPATH).click()
        self.download_pic(filename)

    def open_site(self):
        self.driver.get(self.BASE_URL.format(tl=self.tl))
        try:
            self._wait_and_choose_element('//span[contains(text(),"Accept all")]', by=By.XPATH, timeout=6).click()
        except (TimeoutException, IndexError):
            pass
        self._wait_and_choose_element('//span[contains(text(),"Images")]', by=By.XPATH, timeout=30).click()

    def load_pic(self, filename):
        self._wait_and_choose_element('.r83qMb [class="D7BEKc"] input').send_keys(filename)

    def download_pic(self, filename):
        time.sleep(2)
        # Путь к папке, где находится файл
        source_path = os.path.join(os.getcwd(), 'temporary')
        # Имя файла, который вы хотите переименовать и переместить
        old_filename = filename  # Замените на реальное имя файла
        path = Path(filename)
        old = path.name.split('.')
        # Новое имя файла
        new_filename = f'{".".join(old[:-1])}-EN.{old[-1]}'  # Замените на новое имя файла
        print(os.path.join(path.parent, new_filename))
        # Переименование файла
        while True:
            try:
                os.rename(os.path.join(source_path, os.path.basename(old_filename)), os.path.join(path.parent, new_filename))
                break
            except FileNotFoundError:
                continue
            except FileExistsError:
                os.remove(os.path.join(source_path, os.path.basename(old_filename)))
                print('The file cannot be created because it already exists:')
                break

    def _wait_and_choose_element(self, selector: str, by: By = By.CSS_SELECTOR, timeout: int = 20) -> WebElement:
        condition = EC.presence_of_element_located((by, selector))
        element = WebDriverWait(self.driver, timeout).until(condition)
        return element

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()


if __name__ == '__main__':
    folder_path = '/Input/input.jpg'
    destination_path = '../Output'
    print(os.path.isfile(folder_path))
    if os.path.isfile(folder_path):
        filename_format = folder_path.split('.')[1]
        if filename_format in ('png', 'jpg', 'jpeg'):
            with PicGoogleTranslateParser() as placer:
                placer.placer_google_translate_parser(folder_path)
        else:
            print('Not supported format file')
