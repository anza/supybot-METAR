###
# METAR supybot plugin
#
# written on Dec 2010 by louk
# published under 'do whatever you want'-license
###

from supybot.commands import *
import supybot.callbacks as callbacks
import subprocess, re

# this is the path to metar executable, you may need to change this
# NOTE: the old 'metar' from e.g. debian or ubuntu repos isn't suitable!
# use this: https://github.com/anza/metar/
metarpath = "/usr/bin/metar"

class METAR(callbacks.Plugin):
	def metar(self, irc, msg, args, reptype, station):
		# this is the help, you want to modify this
		"""[raw|basic|extended] <station code>
		retrieves current weather conditions for given METAR observation station. More help and Finnish station codes: http://may.fi/~antti/metar.txt)"""

		# we map wanted options with dict
		dict = { None:'b', 'basic':'b', 'raw':'r', 'extended':'e' }
		# and then get suitable option for wanted report type
		reptype = dict[reptype]

		# sanitize user input, allows only alphanumerical chars
		station = re.sub('[^\w]', '', station)
		# convert station to uppercase
		station = station.upper()

		# define command to execute with subprocess
		command = metarpath + ' -' + reptype + ' ' + station
		proc = subprocess.Popen(command,
					shell=True,
					stdout=subprocess.PIPE,
					)
		output = proc.communicate()[0]
		# we want to strip possible newlines and hyphens
		# from beginning and end
		output = output.strip('\n\'')

		# we get reply!
		irc.reply(output, prefixNick=False)

	# at last the wrapper..
	metar = wrap(metar, [optional(("literal", ("raw", "basic", "extended"), 'argument parse error')), 'something'])

Class = METAR
