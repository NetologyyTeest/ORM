import psycopg2
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from models import create_tables, Publisher, Book, Shop, Stock, Sale

DSN = 'postgresql://postgres:postgres@localhost:5432/netology_bd'
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

def main():

    publisher_name = input("Введите имя или идентификатор издателя: ")

    publisher = session.query(Publisher).filter_by(name=publisher_name).first()

    if publisher is None:
        print("Издатель не найден.")
        return

    books = session.query(Book).filter_by(id_publisher=publisher.id).all()

    if len(books) == 0:
        print("У данного издателя нет книг.")
        return

    for book in books:
        sales = (
            session.query(Book.title, Shop.name, Sale.price, Sale.data_sale)
            .join(Stock)
            .join(Sale)
            .join(Shop)
            .filter(Stock.id_book == book.id)
            .order_by(Sale.data_sale.desc())
            .all()
        )

        if len(sales) > 0:
            for sale in sales:
                book_title, shop_name, price, data_sale = sale
                data_sale_str = datetime.strftime(data_sale, "%d-%m-%Y")
                print(f"{book_title} | {shop_name} | {price} | {data_sale_str}")
        else:
            print(f"Для книги {book.title} нет фактов покупки.")

session.close()


if __name__ == "__main__":
    main()