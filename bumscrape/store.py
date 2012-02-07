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
                `listing_id` int auto_increment,

                `url` varchar(512) not null,
                `spider` varchar(64) not null,
                `visited` timestamp default current_timestamp,

                `title` varchar(255) not null,
                `price` int null default null,
                `num_tickets` int null default null,
                `posted` timestamp null,

                primary key (`listing_id`)
            ) engine=InnoDB""")

        cursor.execute("""
            create table if not exists `crawls` (
                `spider` varchar(64) not null,
                `crawls` int not null default '0',
                `last_crawled` timestamp not null default current_timestamp,
                primary key ( `crawler` )
            ) engine = InnoDB""")

        cursor.close()

    def log_crawl(self, spider_name):
        cursor = self.conn.cursor()
        cursor.execute("""
            insert into `crawls` (`spider`, `crawls`) values (%s, 1)
                on duplicate key update `crawls` = `crawls` + 1, last_crawled = now()""",
            (spider_name,))

    def add_item(self, item, spider_name):
        cursor = self.conn.cursor()

        cursor.execute("""
            insert into `listings` (
                `url`, `spider`, `title`, `price`, `num_tickets`, `posted`
            ) values (%s, %s, %s, %s, %s, %s)""",
            (item['url'], spider_name, item.get('title'), item.get('price'), item.get('num_tickets'), item.get('posted')),)
