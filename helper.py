from seleniumbase import Driver

def get_selenium_base_uc_driver():
    drv = Driver(uc=True, incognito=True)
    drv.maximize_window()
    return drv