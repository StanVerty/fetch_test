from datetime import datetime
from pytz import timezone
import pytz


class Screenshots:

    def __init__(self, driver, class_name=None, func_name=None):
        self.driver = driver
        self.classname = class_name
        self.funcname = func_name

    def time(self):
        date_pst = datetime.now(pytz.utc).astimezone(timezone('US/Pacific'))
        now = date_pst.strftime('%Y-%m-%d_%H-%M-%S')
        return now

    def take_screenshot(self):
        """
        Takes screenshot of the current open web page
        """

        file_name = self.classname + "_" + self.funcname + "_" + self.time() + ".png"
        screenshot_directory = "./screenshots/"
        destination_file = screenshot_directory + file_name

        try:
            self.driver.save_screenshot(destination_file)
            print("Screenshot saved to directory --> " + destination_file)
            return destination_file
        except NotADirectoryError:
            print("Not a directory issue")
