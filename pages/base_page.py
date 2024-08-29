from utils.screenshots import Screenshots


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def take_screenshot(self, class_name, function_name):
        return Screenshots(self.driver, class_name, function_name).take_screenshot()

    def get_url(self, url):
        self.driver.get(url)
