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
            else:
                product_url = "None"
            
            watch_list.append(
                {
                    "brand" : brand,
                    "model" : model,
                    "price" : price,
                    "specifications" : specifications,
                    "category" : category,
                    "image_url" : image_url,
                    "product_url" : product_url

                }

            )

        return watch_list
    
    def get_reviews(self, html):
        parser = BeautifulSoup(html, 'html.parser')
        reviews = parser.find_all('div', {'class': 'review'})
        review_list = []
    
        for review in reviews:
            rating = float(review.find('span', {'class': 'a-icon-alt'}).text.split()[0]) if review.find('span', {'class': 'a-icon-alt'}) else "None"
            review_text = review.find('div', class_='a-expander-content reviewText review-text-content a-expander-partial-collapse-content').text.strip() if review.find('div', class_='a-expander-content reviewText review-text-content a-expander-partial-collapse-content') else "None"
            reviewer_name = review.find('span', {'class': 'a-profile-name'}).text.strip() if review.find('span', {'class': 'a-profile-name'}) else "None"
            review_date = review.find('span', {'class': 'a-size-base a-color-secondary review-date'}).text.strip() if review.find('span', {'class': 'a-size-base a-color-secondary review-date'}) else "None"
            review_list.append(
                {
                    "rating" : rating,
                    "text" : review_text,
                    "reviewer_name" : reviewer_name,
                    "review_date" : review_date,
                }

            )

        return review_list

                


