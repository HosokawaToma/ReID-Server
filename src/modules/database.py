from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class ModuleDatabase:
    def __init__(self):
        self._engine = create_engine("sqlite:///./src/.db")
        self._Session = sessionmaker(bind=self._engine)
        self._session = self._Session()

    def add(self, model):
        self._session.add(model)

    def commit(self):
        self._session.commit()

    def __del__(self):
        self._session.close()
