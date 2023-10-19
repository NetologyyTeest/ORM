import psycopg2
import sqlalchemy
from sqlalchemy.orm import sessionmaker


from models import create_tables, Publisher, Book, Shop, Stock, Sale

DSN = 'postgresql://postgres:postgres@localhost:5432/netology_bd'
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

def get_shops(publisher_name):
    query = (
        session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)
        .select_from(Shop)
        .join(Stock)
        .join(Book)
        .join(Publisher)
        .join(Sale)
    )

    if publisher_name.isdigit():
        query = query.filter(Publisher.id == int(publisher_name)).all()
    else:
        query = query.filter(Publisher.name == publisher_name).all()

    if len(query) > 0:
        for book_title, shop_name, price, date_sale in query:
            date_sale_str = date_sale.strftime('%d-%m-%Y')
            print(f"{book_title: <40} | {shop_name: <10} | {price: <8} | {date_sale_str}")
    else:
        print(f"У данного издателя нет магазинов.")

session.close()

if __name__ == 'main':
    publisher_name = input("Введите имя или идентификатор издателя: ")
    get_shops(publisher_name)


