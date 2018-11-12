# ORM mapper
from sqlalchemy.ext.declarative import declarative_base

# Import data types here

BASE = declarative_base()


# Custom declarative base
class CUSTOMBASE(BASE):
    __abstract__ = True
    
    def to_dict(self):
        """
	This method populates a dictionary with the attributes : values.
	"""
        tmp = {}
        for i in self.__table__.columns:
            tmp[i.name] = getattr(self, i.name)
        return tmp


# Tables
class TABLE_NAME(CUSTOMBASE):
    __tablename__ = 'TABLE_NAME'
    
    # Columns here

