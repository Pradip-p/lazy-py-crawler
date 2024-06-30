import undetected_chromedriver as uc
options = uc.ChromeOptions()

options.headless = True
options.add_argument( '--headless' )
driver = uc.Chrome(options = options)
driver.get('https://distilnetworks.com')