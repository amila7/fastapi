from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{settings.database_username}:"
    f"{settings.database_password}@"
    f"{settings.database_hostname}:"
    f"{settings.database_port}/"
    f"{settings.database_name}"
)


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#this how to connect the postgress sql use psycopg liobratry but now we dont want the psycopg because now we connectinbg use this us4 sql achemy


# import psycopg2
# from psycopg2.extras import RealDictCursor

# while True:
#     try:
#         conn = psycopg2.connect(host="localhost",database="fastapi",user="postgres",password="123456",cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("connected to the database")
#         break
#     except Exception as e:
#         print(e)