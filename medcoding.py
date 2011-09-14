#!/usr/bin/env python

import sys
import irclib
import urllib2
import random
import json

class Shorty(irclib.SimpleIRCClient) :
	def __init__(self, server, nick, chan, len=40) :
		self.len = len
		irclib.SimpleIRCClient.__init__(self)
		self.connect(server, 6667, nick)
		self.connection.join(chan)
	
	def on_join(self, c, e) :
		pass

	def on_pubmsg(self, c, e) :
		nick = e.source().split("!")[0]
		chan = e.target()
		txt = e.arguments()[0]
		words = txt.split(' ')
		if words[0] == '!med' :
			search = words[1]
			try :
				codes = json.loads(urllib2.urlopen("http://graphicsweb.wsj.com/documents/MEDICALCODES0911/data.php?sort=code&term=%s&dir=asc&startIndex=0&results=500" % search).read())["codes"]
				if not codes :
					msg = "He's dead jim"
				else :
					random.shuffle(codes)
					code = codes[0]
					msg = ': '.join(code.values())
			except RuntimeError :
				msg = "I died jim"

			self.connection.privmsg(chan, msg)

if __name__ == '__main__' :
	try :
		try :
			s = Shorty(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]))
		except IndexError :
			s = Shorty(sys.argv[1], sys.argv[2], sys.argv[3])
	except IndexError :
		print 'usage: python medcoding.py server nick channel [minlen]\n\n\texample:\n\tpython shorty.py irc.example.com shortbot \#hackers 40\n\n(Escape of # character is needed in most shells.)'
		sys.exit(1)
	s.start();
