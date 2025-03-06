import random
import threading
from typing import Any

from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, text, Result
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
DB_URL = "mysql+pymysql://root:@localhost:4306/my_org_dev"

engine = create_engine(DB_URL, pool_size=10)
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(6), nullable=False)

class Seat(Base):
    __tablename__ = "seats"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(6), nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"))
    version = Column(Integer, default=1, nullable=False)

Base.metadata.create_all(engine)

def get_random_name(size=6):
    name = ""
    for _ in range(size):
        name += chr(ord("A") + random.randint(0, 26))
    return name

session = Session()

def main(session):
    try:
        for i in range(1, 121):
            seat = Seat(name = chr(ord('A') + i // 12) + f"-{i % 12}")
            session.add(seat)
            user = User(name=get_random_name())
            session.add(user)
        session.commit()

        def allocate_seat(user_id):
            session = Session()
            empty_seat_query = text("SELECT id, version from seats where assigned_to is NULL limit 1")
            empty_seat_id, version = session.execute(empty_seat_query).first()
            allocate_seat_query = text("UPDATE seats set assigned_to = :user_id, version = :new_version where id = :empty_seat_id and version = :curr_version")
            result = session.execute(allocate_seat_query, {"user_id": user_id, "empty_seat_id": empty_seat_id, "curr_version": version, "new_version": version + 1})
            session.commit()
            session.close()

            # [Optimistic Lock] Retry as someone else might have booked the seat.
            if result.rowcount == 0:
                allocate_seat(user_id)

        # Simulate multiple requests via multiple threads
        requests = [threading.Thread(target=allocate_seat, args=(user_id,)) for user_id in range(1, 121)]

        for r in requests:
            r.start()

        for r in requests:
            r.join()

        query = text("SELECT * from seats")
        seats = session.execute(query).fetchall()
        for seat in seats:
            seat_id, seat_name, seat_assigned_to, version = seat
            print(f"seat_id: {seat_id}, seat_name: {seat_name}, seat_assigned_to: {seat_assigned_to}, version: {version}")
    finally:
        session.execute(text("DROP table seats"))
        session.execute(text("DROP table users"))
        session.commit()

main(session)


