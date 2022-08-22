from db import engine
from db.models import Base


def drop_tables():
    return Base.metadata.drop_all(engine)


if __name__ == "__main__":
    drop_tables()
