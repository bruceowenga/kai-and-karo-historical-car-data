from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller  # Import the chromedriver-autoinstaller library

def get_unique_id():
    # Automatically install and manage ChromeDriver
    chromedriver_autoinstaller.install()  # This will install the appropriate version of ChromeDriver

    # Configure Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    # Initialize ChromeDriver with Chrome options
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the website
    driver.get("https://www.kaiandkaro.com")

    # Simulate the action of clicking "Search" or navigating to the relevant page
    # You may need to inspect the website's HTML to identify the correct element and action
    search_button = driver.find_element(By.XPATH, "//div/form/div/button")  # Replace with the actual element ID
    search_button.click()

    # Wait for the page to load (you may need to adjust the waiting time)
    driver.implicitly_wait(5)  # Implicitly wait for up to 5 seconds for elements to appear

    # Use browser developer tools to inspect network requests
    # Locate the XHR (XMLHttpRequest) request that contains the URL you want
    # Extract the URL from the request headers
    network_requests = driver.execute_script("return performance.getEntriesByType('resource');")
    
    # Find the specific request you're interested in (it might have a unique pattern or keyword)
    desired_request = None
    for request in network_requests:
        if "_buildManifest" in request["name"]:
            desired_request = request
            break

    # Close the web browser
    driver.quit()

    if desired_request:
        # Extract the unique id from the URL
        url = desired_request["name"]
        unique_id = url.split("/")[-2]
        return unique_id
    else:
        return None

if __name__ == "__main__":
    get_unique_id()

