from selenium import webdriver
from lib.scraper import Scraper
from lib.database import MyDatabase
import time

class Crawler:
    def __init__(self):
        pass

    def run(self, debug=False, delay=4):
        scraper = Scraper()
        database = MyDatabase()

        driver = webdriver.Chrome()
        driver.get("https://www.amazon.com/s?k=watches")
        watch_list = scraper.get_watches(html=driver.page_source)

        if debug:
            for index, watch in enumerate(watch_list):
                print(index)
                for key, value in watch.items():
                    print(f"{key} = {value}")
                print("*" * 30)

        product_info_list  = database.add_watches(watch_list=watch_list)
        print("products saved in database")

        #time.sleep(delay)
        #product_driver = webdriver.Chrome()

        for product_info in product_info_list:
            print(product_info)
            '''
            product_url = watch["product_url"]

            if product_url == "None":
                continue
            print(f"Getting reviews from {product_url}")
            product_driver.get(product_url)
            time.sleep(delay)

            review_list = scraper.get_reviews(html=product_driver.page_source)

            if debug:
                for index, watch in enumerate(review_list):
                    print(index)
                    for key, value in watch.items():
                        print(f"{key} = {value}")
                    print("*" * 30)

            '''


            


if __name__ == "__main__":
    crawler = Crawler()
    crawler.run()
