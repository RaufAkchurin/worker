from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Worker(Base):
    __tablename__ = 'worker'

    id = Column(Integer, primary_key=True)
    name = Column(String(10))
    surname = Column(String(10))
    password = Column(Integer)

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

class CategorySub(Base):
    __tablename__ = 'categorysub'

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    name = Column(String(255))

    category = relationship('Category', back_populates='categorysub')

class WorkType(Base):
    __tablename__ = 'worktype'

    id = Column(Integer, primary_key=True)
    sub_category_id = Column(Integer, ForeignKey('categorysub.id'))
    name = Column(String(255))
    value = Column(Integer)

    sub_category = relationship('CategorySub', back_populates='worktype')

class Object(Base):
    __tablename__ = 'object'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    workers_id = Column(Integer, ForeignKey('worker.id'))
    price_for_worker = Column(Integer)
    price_for_customer = Column(Integer)
    work_type_id = Column(Integer, ForeignKey('worktype.id'))
    work_scope = Column(Integer)

    workers = relationship('Worker', back_populates='object')
    work_type = relationship('WorkType', back_populates='object')

class Shift(Base):
    __tablename__ = 'shift'

    id = Column(Integer, primary_key=True)
    object_id = Column(Integer, ForeignKey('object.id'))
    worker_id = Column(Integer, ForeignKey('worker.id'))
    date = Column(String(255))
    work_type_id = Column(Integer, ForeignKey('worktype.id'))
    value = Column(Integer)

    object = relationship('Object', back_populates='shift')
    worker = relationship('Worker', back_populates='shift')
    work_type = relationship('WorkType', back_populates='shift')

# Здесь вы можете указать свой DSN (Data Source Name) для вашей базы данных
# Пример: 'postgresql://user:password@localhost/dbname'
engine = create_engine("postgresql://worker_app:worker_app@localhost/worker_app")

Base.metadata.create_all(engine)
