import os
import shutil
import time
from pathlib import Path

import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome, ChromeOptions, ActionChains, Keys
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
        # self.destination_path = destination_path
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

        prefs = {"profile.default_content_settings.popups": 0,
                 "download.default_directory": os.getcwd() + '/temporary',
                 "directory_upgrade": True}
        browser_options.add_experimental_option('prefs', prefs)

        self.driver = Chrome(service=service, options=browser_options, )
        # self.driver = Chrome(options=browser_options,)

    def placer_google_translate_parser(self, filename):
        self.open_site()
        self.load_pic(filename)
        # self.download_pic(filename, self.destination_path)
        # self.screenshot_translation(filename, destination_path)
        self._wait_and_choose_element('//span[contains(text(), "Download translation")]', by=By.XPATH).click()
        self.download_pic(filename)

    def open_site(self):
        self.driver.get(self.BASE_URL.format(tl=self.tl))
        self._wait_and_choose_element(
            '//span[contains(text(),"Images")]',
            by=By.XPATH,
        ).click()

    def load_pic(self, filename):
        # pic_path = os.path.abspath(os.path.dirname(__file__)) + f'/Input/{filename}'
        self._wait_and_choose_element('.r83qMb [class="D7BEKc"] input').send_keys(
            filename
        )
        # time.sleep(10)

    def download_pic(self, filename):
        time.sleep(2)
        # Путь к папке, где находится файл
        source_path = os.getcwd() + '/temporary'
        # Имя файла, который вы хотите переименовать и переместить
        old_filename = filename  # Замените на реальное имя файла
        old = old_filename.split('.')
        # Новое имя файла
        new_filename = f'{old[0]}-EN.{old[1]}'  # Замените на новое имя файла
        # Полные пути к исходному файлу и файлу в целевой папке
        # old_path = os.path.join(source_path, old_filename)
        print(source_path+old_filename.split('/')[-1], new_filename)
        new_path = os.path.join(source_path, new_filename)
        # Переименование файла
        while True:
            try:
                os.rename(source_path + '/' + old_filename.split('/')[-1], new_filename)
                break
            except FileNotFoundError:
                continue
        # if os.path.exists(os.path.join(self.destination_path, new_filename)):
        #     os.remove(os.path.join(self.destination_path, new_filename))
        #
        # shutil.move(new_path,  self.destination_path)

    def screenshot_translation(self, filename, destination_path):
        filename = filename.split('.')
        src = self._wait_and_choose_element('.dQBt [class="CMhTbb tyW0pd"] img').get_attribute('src')
        self.driver.get(src)
        # time.sleep(2)
        self._wait_and_choose_element(
            'img'
        ).screenshot(str(Path(destination_path, f'{filename[0]}-{self.tl.upper()}.{filename[-1]}')))

    def _wait_and_choose_element(self, selector: str, by: By = By.CSS_SELECTOR, timeout: int = 20) -> WebElement:
        condition = EC.presence_of_element_located((by, selector))
        element = WebDriverWait(self.driver, timeout).until(condition)
        return element

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()


if __name__ == '__main__':
    folder_path = '/home/ernest/work/google_translate/Input/input.jpg'
    destination_path = 'Output'
    # file_path = os.path.join(folder_path, filename)
    print(os.path.isfile(folder_path))
    if os.path.isfile(folder_path):
        filename_format = folder_path.split('.')[1]
        if filename_format in ('png', 'jpg', 'jpeg'):
            print(folder_path)
            with PicGoogleTranslateParser() as placer:
                placer.placer_google_translate_parser(folder_path)
        else:
            print('Not supported format file')
