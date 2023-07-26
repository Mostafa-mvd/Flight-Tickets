from selenium.webdriver import FirefoxOptions, Firefox
from selenium.webdriver.firefox.service import Service as FireFoxService
from webdriver_manager.firefox import GeckoDriverManager

#from seleniumrequests import Firefox


options = FirefoxOptions()

options.headless = True

driver = Firefox(
    service=FireFoxService(GeckoDriverManager().install()),
    options=options)

payload = {
            "tab": "airplane",
        }

#tickets_detail = driver.request('https://www.tcharter.ir/tickets/tickets/VEhSLU1IRC0xNDAyLzA2LzI1/')

tickets_detail = driver.request(
    'POST', 
    'https://www.tcharter.ir/tickets/tickets/VEhSLU1IRC0xNDAyLzA2LzI1/', 
    data=payload)

driver.quit()
driver.close()
