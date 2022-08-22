from sqlalchemy import select

from db import Session
from db.models import User


if __name__ == "__main__":
    with Session.begin() as session:
        result = session.execute(stmt := select(User, User.id).limit(2))
        print('result:', result)
        scalars = result.scalars().all()
        print('scalars:', scalars)
        # one = result.one()
        # print('one:', one)
        # scalar_one = result.scalar_one()
        # print('scalar_one:', scalar_one)
