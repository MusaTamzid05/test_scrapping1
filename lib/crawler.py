from selenium import webdriver
from lib.scraper import Scraper

class Crawler:
    def __init__(self):
        pass

    def run(self):
        scraper = Scraper()

        driver = webdriver.Chrome()
        driver.get("https://www.amazon.com/s?k=watches")
        watch_list = scraper.get_watches(html=driver.page_source)

        for index, watch in enumerate(watch_list):
            print(index)
            for key, value in watch.items():
                print(f"{key} = {value}")
            print("*" * 30)

        breakpoint()
            


if __name__ == "__main__":
    crawler = Crawler()
    crawler.run()
