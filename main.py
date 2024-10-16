from lib.crawler import Crawler
import datetime as dt
import schedule
import time


def run_crawler():
    print("Running crawler")
    crawler = Crawler()
    crawler.run(debug=True)


if __name__ == "__main__":
    run_crawler()
    schedule.every(5).hours.do(run_crawler)

    while True:
        schedule.run_pending()
        time.sleep(1)

