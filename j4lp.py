#!/usr/bin/env python

import os
import sys

import daemon
import tornado.httpclient
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('home.html')

class SSPHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('ssp.html')

if __name__ == '__main__':
	tornado.web.Application(
		handlers=[
			(r'/', MainHandler),
			(r'/ssp', SSPHandler),
		],
		template_path=os.path.join(os.path.dirname(__file__), 'templates'),
		debug=True,
	).listen(8889)
	if len(sys.argv) == 2 and sys.argv[1] == '-d':
		daemon.daemonize()
	print('listening on :%d' % 8889)
	tornado.ioloop.IOLoop.instance().start()
