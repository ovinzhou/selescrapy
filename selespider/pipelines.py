# -*- coding: utf-8 -*-
import pymysql


class SelespiderPipeline(object):
    def __init__(self):
        self.db = pymysql.connect(host='localhost', port=3306, user='root', passwd='mysql',
                                  db='movie_db', charset="utf8")
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):

        values = (
            item['name'],
            item['url'],
            item['image_url'],
            item['price'],
        )

        execute_sql = 'INSERT INTO amazon_data (com_name, url, image_url, price) VALUES (%s,%s,%s,%s)'
        self.cursor.execute(execute_sql, values)
        self.db.commit()
        yield item

    # def insert_db(self, tx, item):
    #     values = (
    #         item['upc'],
    #         item['name'],
    #         item['price'],
    #         item['review_rating'],
    #         item['review_num'],
    #         item['stock'],
    #     )
    #     sql = 'INSERT INTO books VALUES (%s,%s,%s,%s,%s,%s)'
    #     tx.execute(sql, values)

    def next_item(self, item, spider):
        print('-'*50)
        return item
