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

# Author 			: Patrick Pedersen <ctx.xda@gmail.com>
# Last updated 		: 14:00 8/4/2017 CEST
# Descriptiption	: Bot configuration parser/reader

import os
import re
import telegram
import configparser
import Audio

from re import findall
from Binder import bind

def validVarChar(char) :
	return (char.isalpha() or char == '_')

def toAudiolist(config) :
	if type(config) == configparser.ConfigParser :
		cfg = config
	else :
		cfg = configparser.ConfigParser()
		cfg.read(config)

	audiolist = Audio.AudioList()

	for section in cfg.sections() :
		sectionEntry = Audio.AudioSection(section)
		for option in cfg.options(section) :
			sectionEntry.add(option, cfg[section][option])

		audiolist.add(sectionEntry)

	return audiolist

def toAudiocfg(audiolist, config) :
	if type(config) == configparser.ConfigParser() :
		cfg = config
	else :
		cfg = configparser.ConfigParser()
		cfg.read(config)

	# Start with section and option removal (Sections and options that do not appear in the audio list)
	for section in cfg.sections() :
		if not audiolist.section(section) :
			cfg.remove_section(section)

		else :
			for option in cfg.options(section) :
				if not audiolist.section(section).audio(option) :
					cfg.remove_option(section, option)

	# Proceed by adding missing sections or options
	for section in audiolist.Sections :

		# Ensure that section actually exists in first place
		if not cfg.has_section(section.Name) :
			cfg.add_section(section.Name)

		for file in section.Files :
			cfg.set(section.Name, file.Name, file.ID)

	return cfg

class botcfg:

	# Main configuration
	maincfgPath = None
	maincfg     = None
	execPath    = None
	token       = None
	bootmsg     = None

	masters       = []
	bootmsgChats  = []
	methods       = []
	binds 		  = []

	# Audio configuration
	audiocfgPath = None
	audiocfg     = None
	audiolist    = Audio.AudioList()

	# Timed configuration
	timedcfg  = None

	#Audio configuration

	def __init__(self, maincfgPath, audiocfgPath, schedcfgPath) :

		# Load main configuration (MUST BE PRESENT)
		self.maincfgPath = maincfgPath
		self.maincfg = configparser.ConfigParser()
		self.maincfg.read(maincfgPath)

		if self.maincfg.has_option('META', 'TOKEN') :
			self.token = self.maincfg['META']['TOKEN']
		else :
			raise Exception(mainself.maincfg + ": No token defined in bot configuration")
		
		self.execPath = self.maincfg['META']['EXEC_PATH'] if self.maincfg.has_option('META', 'EXEC_PATH') else None
		self.masters = [int(user_id) for user_id in (self.maincfg['USERS']['MASTERS'].split() if self.maincfg.has_option('USERS', 'MASTERS') else None)]
		
		self.bootmsg      = self.maincfg['BOOT']['BOOT_MSG']               if self.maincfg.has_option('BOOT', 'BOOT_MSG')       else None
		self.bootmsgChats = self.maincfg['BOOT']['BOOT_MSG_CHATS'].split() if self.maincfg.has_option('BOOT', 'BOOT_MSG_CHATS') else None

		self.methods = self.maincfg['COMMANDS']['SUPPORTED_METHODS'].split() if self.maincfg.has_option('COMMANDS', 'SUPPORTED_METHODS') else None

		if self.maincfg.has_option('COMMANDS', 'PERMA_BINDS') :
			for binds in findall('".+?"', self.maincfg['COMMANDS']['PERMA_BINDS']) :
				self.binds.append(bind(binds[2:binds.find('/', 2)].strip(), binds[binds.find('/', 2) + 1:-1].strip()))
	
		if audiocfgPath :
			self.audiocfgPath = audiocfgPath
			self.audiocfg = configparser.ConfigParser()
			self.audiocfg.read(audiocfgPath)

			self.audiolist = toAudiolist(self.audiocfg)

		if schedcfgPath :
			self.schedcfg = configparser.ConfigParser()
			self.schedcfg = configparser.ConfigParser()

	def includesMethod(self, method_name) :
		return method_name in self.methods

	def exportBot(self) :
		return telegram.Bot(self.token)
