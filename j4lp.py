#!/usr/bin/env python

import config
import daemon
import ssp
import tornado.httpclient
import tornado.ioloop
import tornado.web

import os
import sys
import cStringIO

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('home.html')

class SSPHandler(tornado.web.RequestHandler):
	def get(self):
		out = cStringIO.StringIO()
		ssp.ssp(out)
		report = out.getvalue()
		self.render('ssp.html', report=report)

if __name__ == '__main__':
	tornado.web.Application(
		handlers=[
			(r'/', MainHandler),
			(r'/ssp', SSPHandler),
		],
		template_path=os.path.join(os.path.dirname(__file__), 'templates'),
		debug=config.web.debug,
	).listen(config.web.port)
	if len(sys.argv) == 2 and sys.argv[1] == '-d':
		daemon.daemonize()
	print('listening on :%d' % config.web.port)
	tornado.ioloop.IOLoop.instance().start()
