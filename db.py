from sqlalchemy import create_engine, Column, Integer, String, select, func
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = 'postgresql://postgres:postgres@postgres:5432/pysoa'

engine = create_engine(DATABASE_URL)

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)

Session = sessionmaker(bind=engine)
session = Session()

def verify_user(username, password):
    try:
        query = select(Users.password).where(Users.name == username)
        result = session.execute(query).fetchone()

        if result is not None:
            verify_query = select(Users).where(
                Users.name == username,
                Users.password == func.crypt(password, Users.password)
            )
            verify_result = session.execute(verify_query).fetchone()

            if verify_result:
                return True
            else:
                return False
        else:
            return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    finally:
        session.close()