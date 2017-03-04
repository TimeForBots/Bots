
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Author 		: Patrick Pedersen <ctx.xda@gmail.com>
# Last updated 		: 17:54 3/4/2017 CEST
# Descriptiption	: Bot configuration parser/reader

import os
import re
import telegram
from array import array

def validVarChar(char) :
	return (char.isalpha() or char == '_')

class botcfg:
	path = None
	token = None
	bootmsg = None
	bootmsgChats = []
	methods = []
	methodPackages = []

	def __init__(self, configPath) :
		self.path = configPath
		with open(configPath, 'r') as config :
			configBuffer = config.read()

			i      = 0 # Char iterator

			while i < len(configBuffer) and i != -1 :

				toggle = 0 # Toggles between abc/non-abc chars and varname start/end elements
				varnamePosition = [None] * 2

				# I'm having a hard time explaining this part to others
				# TODO: Replace with for
				while True :

					while i < len(configBuffer) and configBuffer[i] != '#' and configBuffer[i] != '=' and validVarChar(configBuffer[i]) == toggle :
						i += 1

					if i >= len(configBuffer) or configBuffer[i] == '=' :
						break

					if configBuffer[i] == '#' :
						i = configBuffer.find("\n", i)


					varnamePosition[toggle] = i
					toggle = not toggle

				# Get Var name
				_var = configBuffer[varnamePosition[0]:varnamePosition[1]]
				_def = configBuffer[i + 1:configBuffer.find(';', i)]

				if _var == "BOT_TOKEN" :
					self.token = _def.strip()

				elif _var == "BOOT_MSG" :
					try:
						self.bootmsg = re.findall(r'"([^"]*)"', _def)[0]
					except IndexError:
						raise Exception(os.path.basename(self.path) + ": Quotation marks missing on BOOT_MSG definition")

				elif _var == "BOOT_MSG_CHATS" :
					for chat_id in _def.split() :
						self.bootmsgChats.append(chat_id)

				elif _var == "SUPPORTED_METHODS" :
					for method in _def.split() :
						self.methods.append(method)

				i = configBuffer.find(';', i)

	def includesMethod(self, method_name) :
		return method_name in self.methods

	def exportBot(self) :
		return telegram.Bot(self.token)
