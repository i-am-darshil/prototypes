import random
import threading

from sqlalchemy import Column, String, Integer, create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base


Base = declarative_base()
class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(6), nullable=False)

class Seat(Base):
    __tablename__="seats"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(6), nullable=False)
    assigned_to = Column(Integer, unique=True)


DB_URL = "mysql+pymysql://root:@localhost:4306/my_org_dev"
engine = create_engine(DB_URL)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)

def get_random_name(size=6):
    name = ""
    for _ in range(size):
        name += chr(ord("A") + random.randint(0, 26))
    return name

session = Session()

def main(session):
    try:
        for i in range(120):
            seat = Seat(name = chr(ord('A') + i // 12) + f"-{i % 12}")
            session.add(seat)
            user = User(name=get_random_name())
            session.add(user)
        session.commit()

        # Pessimistic locking due to "FOR UPDATE SKIP LOCKED"
        def allocate_seat(user_id):
            session = Session()
            empty_seat_query = text("SELECT id from seats where assigned_to is NULL limit 1 FOR UPDATE SKIP LOCKED")
            empty_seat_id = session.execute(empty_seat_query).fetchall()[0][0]
            allocate_seat_query = text("UPDATE seats set assigned_to = :user_id where id = :empty_seat_id")
            session.execute(allocate_seat_query, {"user_id": user_id, "empty_seat_id": empty_seat_id})
            session.commit()
            session.close()

        # Simulate multiple requests via multiple threads
        requests = [threading.Thread(target=allocate_seat, args=(user_id,)) for user_id in range(120)]

        for r in requests:
            r.start()

        for r in requests:
            r.join()

        query = text("SELECT * from seats")
        seats = session.execute(query).fetchall()
        for seat in seats:
            seat_id, seat_name, seat_assigned_to = seat
            print(f"seat_id: {seat_id}, seat_name: {seat_name}, seat_assigned_to: {seat_assigned_to}")
    finally:
        session.execute(text("DROP table users"))
        session.execute(text("DROP table seats"))
        session.commit()

main(session)