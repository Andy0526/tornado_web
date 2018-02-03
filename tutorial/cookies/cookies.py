#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver

from tornado.options import define, options


def make_parser():
    define('port', type=int, default=8000, help='run the given port')


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('username')


class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        self.set_secure_cookie('username', self.get_argument('username'))
        self.redirect('/')


class WelcomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('index.html', user=self.current_user)


class LogoutHandler(BaseHandler):
    def get(self):
        if self.get_argument('logout', None):
            self.clear_cookie('username')
            self.redirect('/')


if __name__ == '__main__':
    make_parser()
    tornado.options.parse_command_line()
    settings = {
        'template_path': os.path.join(os.path.dirname(__file__, 'templates')),
        'cookie_secret': "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        'xsrf_cookies': True,
        'login_url': '/login',
    }
    application = tornado.web.Application([
        (r'/', WelcomeHandler),
        (r'/login', LoginHandler),
        (r'/logout', LogoutHandler)
    ], **settings)
    httpserver = tornado.httpserver.HTTPServer(application)
    httpserver.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
