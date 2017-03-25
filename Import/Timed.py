from datetime import datetime
from abc import ABC, abstractmethod

def getDayTime(h, m) :
	return datetime.strptime(h + ':' + m, '%H:%M')

class schedual(ABC):
	
	def __init__(self, time, method) :
		self.time = time
		self.method = method

	time = None
	method = None

	@abstractmethod
	def expired() :
		pass # Abstract

class dailySchedual(schedual) :
	def expired(self) :
		return datetime.now().time() >= time