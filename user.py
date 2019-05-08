import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from setting import Base
from setting import ENGINE

class User(Base):
    """
    ユーザモデル
    """
    __tablename__ = "users"
    id = Column('id', String(100), primary_key = True)
    password = Column('password', String(100))

def main(args):
    """
    メイン関数
    """
    Base.metadata.create_all(bind=ENGINE)

if __name__ == "__main__":
    main(sys.argv)