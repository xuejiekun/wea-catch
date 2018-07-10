# -*- coding:utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class BaseORM:

    def __init__(self, database, echo=False, autocommit=True):
        self.engine = create_engine(database, echo=echo)
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession(autocommit=autocommit)

    def close(self):
        self.session.close()

    def commit(self):
        self.session.commit()
