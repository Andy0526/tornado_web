# -*- coding: utf-8 -*-
import tornado.web
from datetime import datetime


class FeedListItem(tornado.web.UIModule):
    def render(self, staus_item):
        return self.render_string('entry.html', item=staus_item,
                                  format=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S+0000').strftime('%c'))
