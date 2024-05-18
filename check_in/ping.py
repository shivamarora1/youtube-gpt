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

print("testing Done...")

driver.quit()
