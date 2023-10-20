# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
from bs4 import BeautifulSoup

# Define a class for scraping MercadoLibre


class MercadoLibreScraper:
    # Initialize the scraper with a URL
    def __init__(self, url):
        self.url = url

    # Define the scraping method
    def scrape(self):
        # Get the page content using requests library
        response = requests.get(self.url)
        text = response.text

        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(text, "html.parser")

        # Select the product elements on the page using CSS selectors
        product_elements = soup.select(".ui-search-result__content-wrapper")

        # Initialize an empty list to store the products
        products = []

        # Loop through each product element and extract the title and price
        for element in product_elements:
            title = element.select_one(".ui-search-item__title").get_text()
            price = element.select_one(
                ".andes-money-amount__fraction").get_text()

            # Append the product title and price (converted to int) to the products list
            products.append((title, int(price.replace('.', ''))))

        # Sort the products by price in ascending order
        products.sort(key=lambda x: x[1])

        # Write the products to a text file
        with open('products.txt', 'w') as f:
            for product in products:
                f.write(f"{product[0].strip()} \nPrice: {product[1]}\n\n")

# Define a class for automating browser actions with Selenium


class BrowserAutomator:
    # Initialize the browser automator with Chrome options
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("detach", True)
        self.browser = webdriver.Chrome(options=self.options)
        self.browser.implicitly_wait(10)

    # Define a method for navigating to a URL
    def navigate(self, url):
        self.browser.get(url)

    # Define a method for clicking a link by its ID
    def click_link_by_id(self, id):
        link = self.browser.find_element(By.ID, id)
        link.click()

    # Define a method for clicking a link by its partial link text
    def click_link_by_plt(self, plt):
        plt = self.browser.find_element(By.PARTIAL_LINK_TEXT, plt)
        plt.click()


# Create an instance of MercadoLibreScraper and scrape the page at the given URL
scraper = MercadoLibreScraper("https://home.mercadolibre.com.ni/computacion")
scraper.scrape()

# Create an instance of BrowserAutomator and navigate to a page, then click a link by its ID, and navigate to another page by clicking a link by its partial link text
automator = BrowserAutomator()
automator.navigate("https://mercadolibre.com")
automator.click_link_by_id("NI")
automator.click_link_by_plt("Computación")
