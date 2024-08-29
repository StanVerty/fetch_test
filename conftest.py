import pytest
from pytest import fixture
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from sys import platform


def pytest_addoption(parser):
    parser.addoption("--headless", action="store", default="false", help="true,false")
    parser.addoption("--run_from", action="store", default="local", help="local, docker")
    group = parser.getgroup('custom_exit_code')
    group.addoption("--suppress-exit_codes", action='store_true', default=False,
                    help="Suppress all the exit codes except for 0")


SCOPE = "session"

@fixture(scope=SCOPE, autouse=True)
def headless(request):
    return request.config.getoption("--headless").lower()

@fixture(scope=SCOPE, autouse=True)
def run_from(request):
    return request.config.getoption("--run_from").lower()

@fixture(scope=SCOPE)
def driver(headless, run_from):
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--incognito")
    # if headless:
    #     chrome_options.add_argument('--headless')
    if run_from == "local":
        print("Running local")
        chrome_driver = 'chromedriver.exe' if platform == 'win32' else 'chromedriver'
        service = webdriver.ChromeService(executable_path=f'./drivers/{chrome_driver}')
        driver = webdriver.Chrome(options=chrome_options, service=service)
        print(driver)
    else:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--disable-setuid-sandbox")
        driver = webdriver.Chrome(options=chrome_options)


    driver.maximize_window()

    yield driver
    driver.close()
    driver.quit()

default_html_path = './reports/report'

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    if not config.option.htmlpath:
        config.option.htmlpath = default_html_path + '.html'
        # config.option.htmlpath = default_html_path + datetime.now().strftime("%d-%b-%Y_%H-%M-%S")+'.html'

@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    from pytest import ExitCode as ec
    failed_exit_codes = [ec.NO_TESTS_COLLECTED, ec.TESTS_FAILED, ec.USAGE_ERROR, ec.INTERNAL_ERROR, ec.INTERRUPTED]
    ok = ec.OK

    if session.config.getoption('--suppress-exit_codes'):
        if exitstatus in failed_exit_codes:
            session.exitstatus = ok
