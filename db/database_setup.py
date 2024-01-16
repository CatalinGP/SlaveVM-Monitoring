from sqlalchemy import create_engine, Column, Integer, JSON, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///vm_statuss.db', echo=True)
Base = declarative_base()

class VMStatus(Base):
    __tablename__ = 'vm_status'
    id = Column(Integer, primary_key=True)
    status_data = Column(JSON)
    vm_name = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
