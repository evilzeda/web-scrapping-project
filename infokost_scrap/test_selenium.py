from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

# Path to the Microsoft Edge WebDriver executable
edge_driver_path = './msedgedriver.exe'

# Configure options for the Edge WebDriver
options = Options()
options.add_argument("--headless")
options.add_argument("--start-maximized")  # Maximize the browser window
options.add_argument("--inprivate")  # Open an in-private browsing session

# Create a new Edge WebDriver instance
service = Service(edge_driver_path)
driver = webdriver.Edge(service=service, options=options)

# Open a website
driver.get('https://www.example.com')

# Find an element and interact with it
element = driver.find_element(By.ID, 'element-id')
element.click()

# Perform other actions as needed

# Close the browser
driver.quit()