from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.action_chains import ActionChains
import time
import pyautogui

driver = webdriver.Chrome()

# Prevents the web page from closing immediately: ===============
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
# ==============================================================

try:
    # Navigate to the web page: ====================================
    driver.get("http://localhost:3000")
    print("Web page title: ", driver.title)
    time.sleep(4) 
    # Zoom out
    for i in range(5):
        pyautogui.keyDown('ctrl')
        pyautogui.press('-')
        pyautogui.keyUp('ctrl')
        time.sleep(1) 
    # ===============================================================

    # login: ========================================================
    # find the username and password fields
    username = driver.find_element(By.ID,'formBasicUsername')
    password = driver.find_element(By.ID,'formBasicPassword')
    # enter username and password
    username.send_keys('Cat')
    password.send_keys('Murka1234')
    # submit the login form
    password.send_keys(Keys.RETURN)
    time.sleep(3)
    # ===============================================================

    # Navigate to the admins page to search for users: ==============
    expand_menu = driver.find_element(By.CLASS_NAME, "menu-bars")
    expand_menu.click()
    time.sleep(3)
    admin_link = driver.find_element(By.LINK_TEXT, "Administration")
    admin_link.click()
    time.sleep(3)
    select = Select(driver.find_element(By.CLASS_NAME, "theme-blue")).select_by_visible_text("User")
    time.sleep(3)
    search = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, '//*[@id="outlined-basic"]'))
    search.send_keys("er")
    search.send_keys(Keys.RETURN)
    time.sleep(10)
    search_results = []
    table = driver.find_element(By.TAG_NAME, "tbody")
    driver.execute_script("arguments[0].scrollIntoView();", table)
    # get the rows
    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        # Get the contents of the username column
        col = row.find_elements(By.TAG_NAME, "td")[2] 
        search_results.append(col.text)
    print(f"Username search results for 'er' are:\n{search_results}")
    time.sleep(3)
    # ===============================================================

    # # logout: =======================================================
    driver.back()
    time.sleep(2)
    logout = driver.find_element(By.XPATH, '//*[@id="root"]/html/div[1]/nav/div/div/span/form/button')
    logout.click()
    time.sleep(3)
    # # ===============================================================

except Exception as e:
    print(f"Test Failed! :/\nError: {e}.")
    driver.quit()

else:
    print("Test Passed! :)")
    driver.quit()
