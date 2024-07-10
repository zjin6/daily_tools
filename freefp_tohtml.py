from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Specify the correct path to your ChromeDriver executable
chrome_driver_path = r'C:\Users\zjin6\chromedriver.exe'

# Create a Service object with the path to ChromeDriver
service = Service(chrome_driver_path)

# If you have Chrome options you want to use, initialize them here
options = webdriver.ChromeOptions()
# Add any options you need
# options.add_argument('--headless')  # Example for headless mode

# Initialize the Chrome WebDriver with the specified service and options
driver = webdriver.Chrome(service=service, options=options)

# Now you can interact with the Chrome browser using the 'driver' object
# For example, open a webpage:
driver.get('https://www.bing.com')

# When you're done, make sure to quit the driver to close the browser
# driver.quit()



from datetime import datetime
import time


print('setting chrome webdriver headless ... ')
# options = webdriver.ChromeOptions()
options.add_argument("--headless")


while True:
    now = datetime.now()
    
    print('\n')
    print(now.strftime('%Y-%m-%d %H:%M  '))
    print('loading chrome and webpage ... ')
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get('https://github.com/freefq/free')
    except Exception as e:
        print(e)
        driver.close()
        time.sleep(60 * 1)
        continue
        
    path_folder = r'C:\Users\zjin6\Downloads\freefp'
    date = now.strftime('%Y-%m-%d')
    hour = (now.hour - now.hour % 4)    
    suffix = '.html'
    path_file = path_folder + '\\' + date + f' {hour:02d}' + suffix
    print('file path = ' + path_file)  
    
    with open(path_file, "w", encoding='utf-8') as f:
        f.write(driver.page_source)
    print(suffix[1:].upper() + ' is saved.')
            
    driver.close()
    time_sleep = 3600 * 2 - (datetime.now() - now).total_seconds()
    print('sleeping 2 hours ... ', flush=True)
    time.sleep(time_sleep)
    

    


















    