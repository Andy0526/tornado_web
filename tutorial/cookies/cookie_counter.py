#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver

from tornado.options import define, options


def make_parser():
    define('port', type=int, default=8000, help='run the given port')


class MainHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        cookie = self.get_secure_cookie('count')
        count = int(cookie) + 1 if cookie else 1
        countString = "1 time" if count == 1 else "%d times" % count
        # self.set_secure_cookie('count', str(count))
        # httponly和secure属性可以防范用户自修改cookie
        self.set_cookie('count', str(count), httponly=True, secure=True)
        self.write(
            '<html><head><title>Cookie Counter</title></head>'
            '<body><h1>You’ve viewed this page %s times.</h1>' % countString +
            '</body></html>'
        )


if __name__ == '__main__':
    make_parser()
    tornado.options.parse_command_line()
    settings = {
        'cookie_secret': "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        "xsrf_cookies": True,

    }
    application = tornado.web.Application(
        [
            (r'/', MainHandler),
        ], **settings
    )
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
