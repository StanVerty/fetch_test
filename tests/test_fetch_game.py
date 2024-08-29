from pages.home_page import HomePage
import configs
import inspect


class TestFetchGame:

    def get_class_name(self):
        return self.__class__.__name__

    def test_find_fake_gold_bar(self, driver):
        this_function_name = inspect.currentframe().f_code.co_name
        hp = HomePage(driver)
        try:
            hp.get_url(configs.url)
            hp.select_half_tuple((0, 1, 2, 3, 4, 5, 6, 7))
            hp.click_bar(configs.final_bar)
            assert hp.pop_up_positive()
            print(f"Fake bar is: {configs.final_bar}")
            weighing_list, number_of_weighing = hp.list_of_weighing_made()
            print(f"This is list of weighing made: {weighing_list}")
            print(f"This is number of weghings: {number_of_weighing}")
        except AssertionError:
            hp.take_screenshot(self.get_class_name(), this_function_name)
            raise
