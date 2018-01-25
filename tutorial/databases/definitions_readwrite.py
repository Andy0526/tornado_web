#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:lewsan
import pymongo
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver

from tornado.options import define, options

from tutorial.databases.config import MONGO_SERVER


def make_parser():
    define('port', type=int, default=8000, help='run the given port')


class WordHandler(tornado.web.RequestHandler):
    def get(self, word):
        coll = self.application.db.words
        word_doc = coll.find_one({"word": word})
        if word_doc:
            del word_doc["_id"]
            self.write(word_doc)
        else:
            self.set_status(404)

    def post(self, word):
        definition = self.get_argument('definition')
        coll = self.application.db.words
        word_doc = coll.find_one({'word': word})
        if word_doc:
            word_doc['definition'] = definition
            coll.save(word_doc)
        else:
            word_doc = {
                'word': word,
                'definition': definition
            }
            coll.insert(word_doc)
        del word_doc['_id']
        self.write(word_doc)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/(\w+)", WordHandler),
        ]
        conn = pymongo.MongoClient(MONGO_SERVER['host'], MONGO_SERVER['port'])
        self.db = conn[MONGO_SERVER['database']]
        tornado.web.Application.__init__(self, handlers)


if __name__ == '__main__':
    make_parser()
    options.parse_command_line()
    server = tornado.httpserver.HTTPServer(Application())
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
