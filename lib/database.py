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

        for watch in watch_list:
            brand = watch["brand"]
            model = watch["model"]
            price = watch["price"]
            specifications = watch["specifications"]
            category = watch["category"]
            image_url = watch["image_url"]

            insert_query = """
        INSERT INTO watches (brand, model, price, specifications, category, image_url)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
          """
            cursor.execute(insert_query, (brand, model, price, specifications, category, image_url))
            watch_id = cursor.fetchone()[0]
            self.db.commit()

        cursor.close()





if __name__ == "__main__":
    database = MyDatabase()
