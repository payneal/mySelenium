import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # NOQA
from selenium.webdriver.chrome.options import Options  # NOQA
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

# --------------------------------------------------------------


class MySeleniumDriver:

    def __init__(self):
        # address being used
        self.host = 'http://127.0.0.1:5000/'
        # chrom driver based on machine running on
        self.ChromeDriver = 'Tests/webDrivers/chromedriver_linux64'
        self.__setDriverOptions()

    # helpers ___________________________________________________
    def __setDriverOptions(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument('--disable-logging')
        self.chrome_options.add_argument("--use-fake-ui-for-media-stream")
        os.environ["webdriver.chrome.driver"] = self.ChromeDriver

    def __setWait(self, time):
        return WebDriverWait(self.driver, time)
    # ------------------------------------------------------------

    def getDriver(self):
        driver = webdriver.\
            Chrome(self.ChromeDriver, chrome_options=self.chrome_options)
        driver.get(self.host)
        # driver.maximize_window()
        driver.implicitly_wait(2)
        self.driver = driver
        return driver

    def killDriver(self):
        self.driver.close()

    def waitForElementToShowBasedOnID(self, time, elementID, expectedValue):
        wait = self.__setWait(time)
        wait.until(
            EC.text_to_be_present_in_element(
                (By.ID, elementID), expectedValue))

    def grabAllTextOptionsInDropdownByXpath(self, theXpath):
        dropDown = Select(self.driver.find_element_by_xpath(theXpath)).options
        options = []
        for val in dropDown:
            options.append(val.text)
        return options

    def grabFirstSelectedOptionInDropDownByXpath(self, theXpath):
        return Select(self.driver.find_element_by_xpath(theXpath)).\
            first_selected_option.text

    def waitTillClickAble(self, time, elementId):
        wait = self.__setWait(time)
        return wait.until(
            EC.element_to_be_clickable(
                (By.ID, elementId)))

    def selectValueInDropDown(self, selectXpath, attributeValue):
        el = self.driver.find_element_by_xpath(selectXpath)
        for option in el.find_elements_by_tag_name('option'):
            if option.get_attribute('value') == attributeValue:
                option.click()

    def verifySelectedValueInDropDown(self, selectedXpath, expectedValue):
        selectedOption = self.grabFirstSelectedOptionInDropDownByXpath(
                selectedXpath)
        assert selectedOption in expectedValue
# ----------------------------------------------------------------
