---

## Prerequisites

- Python (version 3.12.5)
- Docker (version 27.3.0)


## Installation

1. **Create and activate a virtual environment with Python 3.12.4**:
    ```bash
    python3.12 -m venv env
    source env/bin/activate   # On Windows use `env\Scripts\activate`
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Create Docker  Database**:
    ```bash
      docker run \
      --name my_postgres \
      -e POSTGRES_USER=myuser \
      -e POSTGRES_PASSWORD=mypassword \
      -e POSTGRES_DB=mydatabase \
      -v $(pwd)/pgdata:/var/lib/postgresql/data \
      -p 5432:5432 \
       postgres:16.2
    ```



5. **Create Table**:

    ```bash
        docker exec -it my_postgres psql -U myuser -d mydatabase
        CREATE TABLE watches ( id SERIAL PRIMARY KEY, brand VARCHAR(255), model           
        VARCHAR(255), price DECIMAL, specifications JSONB, image_url VARCHAR(255),category VARCHAR(255) ); 
        CREATE TABLE reviews ( id SERIAL PRIMARY KEY, watch_id INT REFERENCES watches(id), rating DECIMAL, review_text TEXT, reviewer_name VARCHAR(255), review_date DATE );
    ```

6. **Run The Crawler**:
    ```bash
    python main.py
    ```

7. **Run Fast API**:
    ```bash
    uvicorn server:app --reload
    ```



