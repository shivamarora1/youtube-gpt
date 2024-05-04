from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.FirefoxOptions()
driver = webdriver.Remote(command_executor="http://127.0.0.1:4444/wd/hub", options=options)

driver.get("https://youtube-ai-gpt.streamlit.app/")

title = driver.title
print(title)

wait = WebDriverWait(driver, timeout=200)

wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
print("iFrame located")

driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))
print("iFrame switched...")

wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//input[@aria-label='query']")))

print("elements rendered...")

input_query = driver.find_element(By.XPATH, "//input[@aria-label='query']")
input_btn = driver.find_element(By.XPATH, "//p[text()='Search']")

input_query.send_keys("Story of mother who wants to kill his son")
input_btn.click()

print("button clicked")

wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='stImage']")))

images = driver.find_elements(By.XPATH,"//div[@data-testid='stImage']")

print(len(images))

assert len(images) >= 10

driver.quit()
