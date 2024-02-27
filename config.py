from dotenv import dotenv_values

config = dotenv_values(".env")

db_url = config["DATABASE_URL"]