import datetime
from json import loads
from sqlalchemy import Column, Date, Integer, String, create_engine, select
from sqlalchemy.orm import declarative_base, Session
from datetime import date, timedelta
from sqlalchemy.dialects.mysql import JSON
from dotenv import load_dotenv

from app.providers.functions import pdf_generator
load_dotenv()
import os

'''
Função para criar pdf e pptx automaticamente caso o Heroku tenha apagado.
'''


Base = declarative_base()

class Worksheet_Content(Base):
    __tablename__ = 'worksheet_content'
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    title = Column(String(255), nullable=False)
    company = Column(String(255))
    person = Column(String(255))
    content = Column(JSON, nullable=False)
    creation_date = Column(Date, nullable=False)
    image_id = Column(String(255), nullable=False, unique=True)

    def __init__(self, title, company, person, content, creation_date, image_id):
        self.title = title
        self.company = company
        self.person = person
        self.content = content
        self.creation_date = creation_date
        self.image_id = image_id

engine = create_engine(os.environ['SQLALCHEMY_DATABASE_URI'], echo=True, future=True)
session = Session(engine)

antique = select(Worksheet_Content)
result = session.scalars(antique).all()
for item in result:
    book_pdf = f'app/static/media/pdf/{item.image_id}.pdf'
    book_pptx = f'app/static/media/pptx/{item.image_id}.pptx'
    capa = {'nome': item.title, 'cliente': item.company, 'pessoa': item.person}
    if not os.path.exists(book_pdf) or not os.path.exists(book_pptx):
        print(f'{datetime.datetime.now()} - Gerando PDF e PPTX para o book {item.title}')
        generator = pdf_generator(capa, loads(item.content), item.image_id)
        print(f'{datetime.datetime.now()} - {generator}')