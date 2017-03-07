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
import configparser

from AudioConfig import audiocfg

def validVarChar(char) :
	return (char.isalpha() or char == '_')

class botcfg:
	path = None
	token = None
	bootmsg = None
	audioconfig = None
	masters = []
	bootmsgChats = []
	methods = []

	# Deprecated and will be replaced with configparser module
	def __init__(self, configPath) :
		self.path = configPath

		cfg = configparser.ConfigParser()
		cfg.read(configPath)

		if cfg.has_option('META', 'TOKEN') :
			self.token = cfg['META']['TOKEN']
		else :
			raise Exception(configPath + ": No token defined in bot configuration")
		
		self.masters = [int(user_id) for user_id in (cfg['USERS']['MASTERS'].split() if cfg.has_option('USERS', 'MASTERS') else None)]
		
		self.bootmsg      = cfg['BOOT']['BOOT_MSG']               if cfg.has_option('BOOT', 'BOOT_MSG')       else None
		self.bootmsgChats = cfg['BOOT']['BOOT_MSG_CHATS'].split() if cfg.has_option('BOOT', 'BOOT_MSG_CHATS') else None

		self.audioconfig = audiocfg(cfg['MEDIA']['AUDIO_SECTIONS'].split()) if cfg.has_option('MEDIA', 'AUDIO_SECTIONS') else None

		self.methods = cfg['METHODS']['SUPPORTED_METHODS'].split() if cfg.has_option('METHODS', 'SUPPORTED_METHODS') else None
	
	def includesMethod(self, method_name) :
		return method_name in self.methods

	def exportBot(self) :
		return telegram.Bot(self.token)
