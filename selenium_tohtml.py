from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import time



def init_chrome_driver(chrome_driver_path=r'C:\Users\zjin6\chromedriver.exe', headless=True):
    # Create a Service object with the path to ChromeDriver
    service = Service(chrome_driver_path)

    # Initialize Chrome options
    options = webdriver.ChromeOptions()

    # Set headless option if required
    if headless:
        options.add_argument('--headless')
        print('Setting Chrome WebDriver to headless mode.')

    # Add other options as needed
    # options.add_argument('--disable-gpu')  # Example for disabling GPU hardware acceleration

    # Initialize the Chrome WebDriver with the specified service and options
    driver = webdriver.Chrome(service=service, options=options)
    print('Chrome Browser is loaded... ')

    return driver


def url2html(driver, url, path_folder=r'C:\Users\zjin6\Downloads\url2html'):

    try:
        driver.get(url)
        print('loading webpage ... ')
    except Exception as e:
        print(e)
        return None
        
    now = datetime.now()
    load_time = now.strftime('%Y-%m-%d %H%M')
    suffix = '.mhtml'
    path_file = path_folder + '\\' + load_time + suffix
    print('file path = ' + path_file)  
    
    with open(path_file, "w", encoding='utf-8') as f:
        f.write(driver.page_source)
    print(suffix[1:].upper() + ' is saved.')
    return f


if __name__ == '__main__':
    driver = init_chrome_driver()
    url = 'https://bpms.chongqing.ford.com:8081/newPage/PProject/ECC_TrackingForAll'
    url2html(driver, url)

    
    # When you're done, make sure to quit the driver to close the browser
    driver.quit()
    


















    