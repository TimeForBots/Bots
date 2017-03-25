# Audio file abstraction
class AudioFile :

	def __init__(self, section, name, fileID) :
		self.Name 	 = name		
		self.Section = section
		self.ID 	 = fileID

	Name    = None
	Section = None
	ID      = None

class AudioSection :

	Name  = None
	Files = []		# Pass audio() type

	def __init__(self, name, files = None) :
		self.Name = name

		if files :
			self.Files = files

	def add(self,  Name, ID) :
		self.Files.append(AudioFile(self.Name, Name, ID))

	def audio(self, identifier) :
		for file in self.Files :
			if type(identifier) == str and file.Name == identifier :
				return file
			elif type(identifier) == int and file.ID == identifier :
				return file

		return None

	def remove(self, identifier) :
		for file in self.Files :
			if type(identifier) == str and file.Name == identifier :
				self.Files.remove(file) # Remove list entry
				return True
			elif type(identifier) == int and file.ID == identifier :
				self.Files.remove(file)
				return True

		return False

	def strlist(self, prefix = '', suffix = ''):
		lst = ''
		
		if self.Files :
			lst = self.Name + '\n- - - -\n'

			for file in self.Files :
				lst += prefix + file.Name + suffix + '\n'

			lst = lst[0:-1]

		return lst

class AudioList :

	Sections = []

	def __init__(self, sectionlist = None) :
		if sectionlist :
			Sections = sectionlist

	def add(self, section) :
		self.Sections.append(section)

	def section(self, sectionName) :
		for section in self.Sections :
			if section.Name == sectionName :
				return section

		return None

	def strlist(self):
		lst = ''
		
		for section in self.Sections :
			sectionlist = section.strlist()

			if sectionlist :
				lst += sectionlist + '\n'
			else : return ''

		return lst

	def strlistSection(self, sectionName) :
		for section in self.Sections :
			if section.Name == sectionName :
				return section.strlist()

		return ''