###
# METAR supybot plugin
#
# written on Dec 2010 by louk
# published under 'do whatever you want'-license
###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import subprocess
import re


class METAR(callbacks.Plugin):
	def metar(self, irc, msg, args, reptype, station):
		"""[raw|basic|extended] <station code>
		retrieves current weather conditions for given METAR observation station. More help and Finnish station codes: http://may.fi/~antti/metar.txt)"""

		dict = { None:'b', 'basic':'b', 'raw':'r', 'extended':'e' }

		reptype = dict[reptype]

		station = station.upper()
		station = re.sub('[^\w]', '', station)

		command = 'metar' + ' -' + reptype + ' ' + station
		proc = subprocess.Popen(command,
					shell=True,
					stdout=subprocess.PIPE,
					)
		output = proc.communicate()[0]
		output = output.strip('\n\'')

		irc.reply(output, prefixNick=False)
	metar = wrap(metar, [optional(("literal", ("raw", "basic", "extended"), 'argument parse error')), 'something'])

Class = METAR
