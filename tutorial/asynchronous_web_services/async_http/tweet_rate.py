#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:lewsan
import json
import time
import urllib
import datetime
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
import tornado.httpclient

from tornado.options import define, options


def make_parser():
    define('port', type=int, default=8000, help='run the given port')


class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        query = self.get_argument('q')
        client = tornado.httpclient.HTTPClient()
        response = client.fetch("http://search.twitter.com/search.json?" + urllib.urlencode(
            {"q": query.encode('utf8'), "result_type": "recent", "rpp": 100}))
        body = json.loads(response.body)
        result_count = len(body['results'])
        now = datetime.datetime.utcnow()
        raw_oldest_tweet_at = body['results'][-1]['created_at']
        oldest_tweet_at = datetime.datetime.strptime(raw_oldest_tweet_at,
                                                     "%a, %d %b %Y %H:%M:%S +0000")
        seconds_diff = time.mktime(now.timetuple()) - \
                       time.mktime(oldest_tweet_at.timetuple())
        tweets_per_second = float(result_count) / seconds_diff
        self.write("""
<div style="text-align: center">
	<div style="font-size: 72px">%s</div>
	<div style="font-size: 144px">%.02f</div>
	<div style="font-size: 24px">tweets per second</div>
</div>""" % (query, tweets_per_second))


if __name__ == '__main__':
    make_parser()
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
        (r"/", IndexHandler),
    ])
    server = tornado.httpserver.HTTPServer(app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
