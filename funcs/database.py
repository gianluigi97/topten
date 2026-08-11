from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

load_dotenv("/Users/gianluigimosti/WorkPlace/topten/key.env")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD") 
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DB = os.getenv("DB")



engine = create_engine(
    f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}",
    connect_args={"connect_timeout": 5}
)

print("Prima di connect")

with engine.connect() as conn:
    print("Connesso")
    print("Prima di SELECT")
    result = conn.execute(text("SELECT 1"))
    print("Dopo SELECT")
    print(result.fetchall())