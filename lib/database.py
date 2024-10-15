import psycopg2


class MyDatabase:
    def __init__(self):
        self.db = psycopg2.connect(
        dbname="mydatabase",       # The database name you used in Docker
        user="myuser",             # The user you set in Docker
        password="mypassword",     # The password you set in Docker
        host="localhost",          # Host where Docker exposes PostgreSQL (localhost)
        port="5432")                # Default PostgreSQL port

    def add_watches(self, watch_list):
        cursor = self.db.cursor()
        product_list = []

        for watch in watch_list:
            brand = watch["brand"].strip()
            model = watch["model"].strip()
            price = watch["price"].strip()
            specifications = watch["specifications"].strip()
            category = watch["category"].strip()
            image_url = watch["image_url"].strip()

            insert_query = """
        INSERT INTO watches (brand, model, price, specifications, category, image_url)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
          """
            cursor.execute(insert_query, (brand, model, price, specifications, category, image_url))
            watch_id = cursor.fetchone()[0]
            self.db.commit()

            if watch["product_url"] != "None":
                product_list.append(
                        {
                            "id" : watch_id,
                            "product_url" : watch["product_url"]

                        })


        cursor.close()
        return product_list





if __name__ == "__main__":
    database = MyDatabase()
