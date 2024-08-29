from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import configs
from pages.base_page import BasePage



class HomePage(BasePage):
    # LOCATORS

    _you_may_be_interested_list = "//div[@class='H8Ch1']//div[@class='COaKTb']"
    _result_button = "div.result #reset" # can be >, <, =
    _weighing_list = "ol li" # list of all weighings
    _reset_button = "//button[text()='Reset']"
    _weigh_button = "//button[text()='Weigh']"


    def put_bars_to_bowl(self, bowl, bars_list):
        for i in range(0, len(bars_list)):
            element = WebDriverWait(self.driver, 40).until(
                EC.presence_of_element_located((By.ID, f"{bowl}_{i}")))
            element.click()
            element.send_keys(f"{bars_list[i]}")

    def click_weigh_button(self):
        weigh_button = WebDriverWait(self.driver, 40).until((
            EC.presence_of_element_located((By.XPATH, self._weigh_button))
        ))
        weigh_button.click()
        sleep(3)

    def click_reset_button(self):
        reset_button = WebDriverWait(self.driver, 40).until((
            EC.presence_of_element_located((By.XPATH, self._reset_button))
        ))
        reset_button.click()
        sleep(3)

    def click_bar(self, bar_number):
        element = WebDriverWait(self.driver, 40).until(
                EC.presence_of_element_located((By.ID, f"coin_{bar_number}")))
        element.click()
        # sleep(2)

    def result_button(self):
        element = WebDriverWait(self.driver, 40).until((
            EC.presence_of_element_located((By.CSS_SELECTOR, self._result_button))
        ))
        return element.text

    def pop_up_positive(self):
        alert = self.driver.switch_to.alert
        if alert.text == "Yay! You find it!":
            print(f"Alert message: {alert.text}")
            alert.accept()
            return True
        else:
            alert.dismiss()
            return False

    def pop_up_negative(self):
        alert = self.driver.switch_to.alert
        if alert.text == "Oops! Try Again!":
            alert.accept()
            return True
        else:
            alert.dismiss()
            return False

    def list_of_weighing_made(self):
        list_of_weighing_made = WebDriverWait(self.driver, 40).until((
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, self._weighing_list))
        ))
        weighing_made_text = [l.text for l in list_of_weighing_made]
        return weighing_made_text, len(weighing_made_text)


    def select_half_tuple(self, tuple_num):
        tuple_length = len(tuple_num)
        half_tuple = int(tuple_length / 2)
        left = tuple_num[:half_tuple]
        right = tuple_num[half_tuple:]
        self.put_bars_to_bowl("left", left)
        self.put_bars_to_bowl("right", right)
        self.click_weigh_button()
        if self.result_button() == "=":
            configs.final_bar = 8
        else:
            tuple_num = right if self.result_button() == ">" else left
            self.click_reset_button()
            if tuple_length > 2:
                self.select_half_tuple(tuple_num)
            else:
                configs.final_bar = tuple_num[0]
