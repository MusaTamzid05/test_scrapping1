from bs4 import BeautifulSoup

class Scraper:
    def __init__(self):
        pass

    def get_watches(self, html):
        soup = BeautifulSoup(html, "html.parser")

        watches = soup.select('div.s-result-item')
        watch_list = []

        for watch in watches:
            #brand = watch.select_one('span.a-size-medium').text if watch.select_one('span.a-size-medium') else 'None'
            model = watch.select_one('h2 span').text if watch.select_one('h2 span') else 'None'
            brand = model.split()[0] if model != "None" else "None"
            price = watch.select_one('span.a-price-whole').text if watch.select_one('span.a-price-whole') else 'None'
            specifications = "Material: XYZ, Water resistance: 50m"  # Scrape actual specs or hardcode for now
            category = "Men's Watch"  # Scrape the category
            image_url = watch.select_one('img.s-image')['src'] if watch.select_one('img.s-image') else 'None'
            product_url = watch.select_one('a.a-link-normal')['href'] if watch.select_one('a.a-link-normal') else 'None'

            if product_url:
                product_url = f"https://www.amazon.com/{product_url}"
            
            watch_list.append(
                {
                    "brand" : brand,
                    "model" : model,
                    "price" : price,
                    "specification" : specifications,
                    "category" : category,
                    "image_url" : image_url,
                    "product_url" : product_url

                }

            )

        return watch_list

                



