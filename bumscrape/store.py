#!/usr/bin/env python

import MySQLdb

class Store(object):
    """Class which takes care of storing item listings in MySQL"""
    def __init__(self, settings):
        self.settings = settings

    def connect(self):
        self.conn = MySQLdb.connect(
            host=self.settings['MYSQL_HOST'],
            user=self.settings['MYSQL_USER'],
            passwd=self.settings['MYSQL_PASSWD'],
            db=self.settings['MYSQL_DB'])

    def disconnect(self):
        self.conn.close()

    def create_db(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            create table if not exists `listings` (
                `id` int auto_increment,
                `url` varchar(512) not null,
                `last_seen` timestamp default current_timestamp,
                unique index (`url`),
                primary key (`id`)
            ) engine=InnoDB""")
        cursor.execute("""
            create table if not exists `visits` (
                `listing_id` int not null,
                `title` varchar(255) not null,
                `price` int null default null,
                `num_tickets` int null default null,
                `posted` timestamp null,
                `seen` timestamp default current_timestamp,
                foreign key (`listing_id`) references `listings`(`id`)
            ) engine=InnoDB""")
        cursor.close()

    def add_item(self, item):
        cursor = self.conn.cursor()
        self._insert(cursor, item)
        cursor.execute("select `id` from `listings` where `url`=%s",
                       (item['url'],))
        row = cursor.fetchone()
        if row is not None:
            self._add_visit(cursor, row[0], item)
        cursor.close()
        self.conn.commit()

    def _insert(self, cursor, item):
        cursor.execute("""
            insert into `listings` (`url`) values(%s)
                on duplicate key update `last_seen` = now()""",
            (item['url'],))

    def _add_visit(self, cursor, listing_id, item):
        cursor.execute("""
            insert into `visits` (
                `listing_id`, `title`, `price`, `num_tickets`
            ) values (%s, %s, %s, %s)""",
            (listing_id, item.get('title'),
             item.get('price'), item.get('num_tickets')))
