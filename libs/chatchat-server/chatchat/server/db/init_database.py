from sqlalchemy import create_engine
from chatchat.server.db.base import Base
from chatchat.settings import BasicSettings

def init_database():
    settings = BasicSettings()
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_database()