#!/usr/env/bin python
# -*- coding: utf-8 -*-

import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver

from uuid import uuid4


class ShoppingCart(object):
    totalInventory = 10
    callbacks = []
    carts = {}

    def register(self, callback):
        self.callbacks.append(callback)

    def unregister(self, callback):
        self.callbacks.remove(callback)

    def moveItemToCart(self, session):
        if session in self.carts:
            return
        self.carts[session] = True
        self.notifyCallbacks()

    def removeItemFromCart(self, session):
        if session not in self.carts:
            return
        del (self.carts[session])
        self.notifyCallbacks()

    def notifyCallbacks(self):
        for callback in self.callbacks:
            callback(self.getInventoryCount())

    def getInventoryCount(self):
        return self.totalInventory - len(self.carts)


class DetailHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        session = uuid4()
        count = self.application.shoppingCart.getInventoryCount()
        self.render(
            'index.html',
            session=session,
            count=count,
        )


class CartHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        action = self.get_argument('action')
        session = self.get_argument('session')
        if not session:
            self.set_status(400)
            return

        if action == 'add':
            self.application.shoppingCart.moveItemToCart(session)
        elif action == 'remove':
            self.application.shoppingCart.removeItemFromCart(session)
        else:
            self.set_status(400)


class StatusHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.application.shoppingCart.register(self.async_callback(self.on_message))

    def on_message(self, count):
        self.write('{"inventoryCount":"%d"}' % count)
        self.finish()


