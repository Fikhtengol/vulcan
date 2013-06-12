
import sys


def stripComment(line):
	idx = line.find("#")
	if idx != -1:
		return line[0:idx]
	else:
		return line


def stripWhiteSpace(line):
	return line.strip()


def matchSection(line):
	line = stripWhiteSpace(stripComment(line))
	if line[0] == '[' and line[-1] == ']':
		sectionName = stripWhiteSpace(line[1:-1])
		return True, sectionName
	else:
		return False, None


def matchVariable(line):
	line = stripWhiteSpace(stripComment(line))
	idx = line.find("=")
	if idx != -1:
		key = stripWhiteSpace(line[0:idx])
		value = stripWhiteSpace(line[idx + 1:])
		return True, key, value
	else:
		return False, None, None


class ConfigError(Exception):
	def __init__(self, args): 
		self.msg = args


class Config(object):
	DEF_SECTION_NAME = ""

	def __init__(self, fileInstance):
		self.sections = { Config.DEF_SECTION_NAME : {} }
		self.defaultSection = Config.DEF_SECTION_NAME
		self.__parseFile(fileInstance)

	# section operations
	def getSectionNames(self):
		"""Returns a list of section names"""
		return self.sections.keys()


	def getDefaultSection(self):
		"""Returns the default section name"""
		return self.defaultSection


	def setDefaultSection(self, sectionName):
		"""Sets the default section name. If the section does not exist ConfigError exception
		is raised"""

		if self.hasSection(sectionName):
			self.defaultSection = sectionName
		else:
			raise ConfigError, "Invalid section: " + sectionName


	def hasSection(self, sectionName):
		"""Returns True iff a section with sectionName exists, otherwise returns False"""
		return self.sections.has_key(sectionName)


	# variable operations
	def hasKey(self, key, sectionName = None):
		"""Returns True iff key exists in given section. If sectionName is not specified uses
		the default section. If the section does not exist ConfigError exception is raised"""

		if sectionName is None:
			sectionName = self.defaultSection

		if self.hasSection(sectionName):
			return self.sections[sectionName].has_key(key)
		else:
			raise ConfigError, "Invalid section: " + sectionName

	def getKeys(self, sectionName = None):
		"""Returns the list of all keys of the given section. If sectionName is not
		specified uses the default section. If the section does not exist ConfigError
		exception is raised"""

		if sectionName is None:
			sectionName = self.defaultSection

		if self.hasSection(sectionName):
			return self.sections[sectionName].keys()
		else:
			raise ConfigError, "Invalid section: " + sectionName


	def getValue(self, key, defaultValue = "", sectionName = None):
		"""Returns the value of key in a given section. If the key does not exist
		defaultValue is returned. If sectionName is not specified the default section
		is used. If sectionName does not exist, ConfigError exception is raised"""

		if sectionName is None:
			sectionName = self.defaultSection
		if self.hasSection(sectionName):
			if self.sections[sectionName].has_key(key):
				return self.sections[sectionName][key]
			else:
				return defaultValue
		else:
			raise ConfigError, "Invalid section: " + sectionName


	def getBoolValue(self, key, defaultValue = "", sectionName = None):
		"""Returns the value of key in a given section. If the key does not exist
		defaultValue is returned. If sectionName is not specified the default section
		is used. If sectionName does not exist, ConfigError exception is raised"""

		value = self.getValue(key, defaultValue, sectionName).lower()
		if value == "true" or value == "1" or value == "yes":
			return True
		elif value == "false" or value == "0" or value == "no":
			return False
		else:
			raise ConfigError, "Value %s cannot be interpreted as boolean" % value


	def iterateVariables(self, sectionName = None):
		"""Return and iterator that produces (key, value) pairs for all variables
		is sectionName. If sectionName is not specified, the default section is
		used. If sectionName does not exist. ConfigError exception is raised"""

		if sectionName is None:
			sectionName = self.defaultSection

		if self.hasSection(sectionName):
			return self.sections[sectionName].iteritems()
		else:
			raise ConfigError, "Invalid section: " + sectionName

	# private
	def __parseFile(self, f):
		currentSection = ""

		for lineNum, line in enumerate(f):
			line = stripWhiteSpace(stripComment(line))

			if len(line) == 0:
				continue

			isVariable, key, value = matchVariable(line)
			if isVariable:
				self.sections[currentSection][key] = value
				continue

			isSection, sectionName = matchSection(line)
			if isSection:
                                if sectionName in self.sections:
                                        raise ConfigError, "duplicate sections: %s" %(sectionName,)
				self.sections[sectionName] = {}
				currentSection = sectionName
				continue

			raise ConfigError, "Invalid syntax on line #%d: %s" % (lineNum, line)
		f.close()


def usage(cmd):
	print "Usage: %s config_path"
	sys.exit(1)

if __name__ == "__main__":
	if len(sys.argv) == 1:
		usage(sys.argv[0])

        f = open(sys.argv[1], "r")
	config = Config(f)
	for sectionName in config.getSectionNames():
		config.setDefaultSection(sectionName)
		print "Section: '%s'" % sectionName
		for key in config.getKeys(sectionName):
			print "\t '%s' = '%s'" % (key, config.getValue(key))
