import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from setting import Base
from setting import ENGINE

class Problem(Base):
    """
    ユーザモデル
    """
    __tablename__ = "problems"
    id = Column('id', Integer, primary_key = True)
    #problem = Column('problem', String(100))
    problem = Column('problem', String(100))
    problemURL = Column('url', String(200))
    participant = Column('participant', String(100))
    contest = Column('contest', String(100))
    contestID = Column('contestID', Integer)
    start_time = Column('start_time', DateTime)
    end_time = Column('end_time', DateTime)
    ac_time = Column('ac_time', String(100))
    penalty = Column('penalty', Integer)
    last_updated = Column('last_updated', DateTime)

def main(args):
    """
    メイン関数
    """
    Base.metadata.create_all(bind=ENGINE)

if __name__ == "__main__":
    main(sys.argv)