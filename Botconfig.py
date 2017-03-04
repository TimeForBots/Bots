
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
# Last updated  : 18:30 3/3/2017 CEST
# Descriptiption	: Bot configuration parser/reader

import telegram
from array import array

def validVarChar(char) :
	return (char.isalpha() or char == '_')

class botcfg:
	token = None
	methods = []
	methodPackages = [] 

	def __init__(self, configPath) :
		with open(configPath, 'r') as config :
			configBuffer = config.read() 
	
			i      = 0 # Char iterator

			while i < len(configBuffer) and i != -1 :
			
				# Check if comment
				if configBuffer[i] == '#' :
					i = configBuffer.find('\n', i)
				else :
					toggle = 0 # Toggles between abc/non-abc chars and varname start/end elements
					varnamePosition = [None] * 2 

					# I'm having a hard time explaining this part to others
					# TODO: Replace with for
					while True :
						while i <  len(configBuffer) and configBuffer[i] != '=' and validVarChar(configBuffer[i]) == toggle : i += 1
						if    i >= len(configBuffer) or configBuffer[i] == '=' : break

						varnamePosition[toggle] = i 
						toggle = not toggle

					# Get Var name
					_var = configBuffer[varnamePosition[0]:varnamePosition[1]]
					_def = configBuffer[i + 1:configBuffer.find(';', i)]

					if _var == "BOT_TOKEN" :
						self.token = _def.strip()

					elif _var == "SUPPORTED_METHODS" :
						for method in _def.split() :
							self.methods.append(method)

					i = configBuffer.find(';', i)

	def includesMethod(self, method_name) :
		return method_name in self.methods
			
	def exportBot(self) :
		return telegram.Bot(self.token)
