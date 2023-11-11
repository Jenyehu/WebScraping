# Import necessary libraries
# Importar las bibliotecas necesarias
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
from bs4 import BeautifulSoup

# Define a class for scraping MercadoLibre
# Definir una clase para hacer scraping en MercadoLibre


class MercadoLibreScraper:
    # Initialize the scraper with a URL
    # Inicializar el scraper con una URL
    def __init__(self, url):
        self.url = url

    # Define a function to convert USD to NIO
    # Definir una función para convertir USD a NIO
    def convert_usd_to_nio(self, price_in_usd):
        return round(price_in_usd * 36.2)

    # Define the scraping method
    # Definir el método de scraping
    def scrape(self):
        # Get the page content using requests library
        # Obtener el contenido de la página usando la biblioteca requests
        response = requests.get(self.url)
        text = response.text

        # Parse the page content with BeautifulSoup
        # Analizar el contenido de la página con BeautifulSoup
        soup = BeautifulSoup(text, "html.parser")

        # Select the product elements on the page using CSS selectors
        # Seleccionar los elementos del producto en la página usando selectores CSS
        product_elements = soup.select(".ui-search-result__content-wrapper")

        # Initialize an empty list to store the products
        # Inicializar una lista vacía para almacenar los productos
        products = []

        # Loop through each product element and extract the title and price
        # Recorrer cada elemento del producto y extraer el título y el precio
        for element in product_elements:
            title = element.select_one(".ui-search-item__title").get_text()
            money_symbol = element.select_one(
                ".andes-money-amount__currency-symbol").get_text()
            price = element.select_one(
                ".andes-money-amount__fraction").get_text()

            # Convert the price to int
            # Convertir el precio a int
            price = int(price.replace('.', ''))

            # If the money symbol is USD, convert the price to NIO and store both prices
            # Si el símbolo de dinero es USD, convertir el precio a NIO y almacenar ambos precios
            if money_symbol == 'U$S':
                price_nio = self.convert_usd_to_nio(price)
                products.append((title, money_symbol, price, 'C$', price_nio))
            else:
                products.append((title, money_symbol, price))

        # Sort the products by NIO price in ascending order
        # Ordenar los productos por precio NIO en orden ascendente
        products.sort(key=lambda x: x[4] if len(x) == 5 else x[2])

        # Write the products to a text file
        # Escribir los productos en un archivo de texto
        with open('products.txt', 'w') as f:
            for product in products:
                if len(product) == 5:
                    f.write(f"{product[0].strip()} \nPrice: {product[1]} {
                            product[2]} ({product[3]} {product[4]})\n\n")
                else:
                    f.write(f"{product[0].strip()} \nPrice: {
                            product[1]} {product[2]}\n\n")

# Define a class for automating browser actions with Selenium
# Definir una clase para automatizar acciones del navegador con Selenium


class BrowserAutomator:
    # Initialize the browser automator with Chrome options
    # Inicializar el automatizador del navegador con opciones de Chrome
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("detach", True)
        self.browser = webdriver.Chrome(options=self.options)
        self.browser.implicitly_wait(10)

    # Define a method for navigating to a URL
    # Definir un método para navegar a una URL
    def navigate(self, url):
        self.browser.get(url)

    # Define a method for clicking a link by its ID
    # Definir un método para hacer clic en un enlace por su ID
    def click_link_by_id(self, id):
        link = self.browser.find_element(By.ID, id)
        link.click()

    # Define a method for clicking a link by its partial link text
    # Definir un método para hacer clic en un enlace por su texto de enlace parcial
    def click_link_by_plt(self, plt):
        plt = self.browser.find_element(By.PARTIAL_LINK_TEXT, plt)
        plt.click()


# Create an instance of MercadoLibreScraper and scrape the page at the given URL
# Crear una instancia de MercadoLibreScraper y hacer scraping en la página de la URL dada
scraper = MercadoLibreScraper("https://home.mercadolibre.com.ni/computacion")
scraper.scrape()

# Create an instance of BrowserAutomator and navigate to a page, then click a link by its ID, and navigate to another page by clicking a link by its partial link text
# Crear una instancia de BrowserAutomator y navegar a una página, luego hacer clic en un enlace por su ID, y navegar a otra página haciendo clic en un enlace por su texto de enlace parcial
automator = BrowserAutomator()
automator.navigate("https://mercadolibre.com")
automator.click_link_by_id("NI")
automator.click_link_by_plt("Computación")
