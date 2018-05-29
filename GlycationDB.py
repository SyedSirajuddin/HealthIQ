EATING = 1
EXCERCISE = 2

class Activity:
	def __init__(self, type, id, time, index):
		self.type = type
		self.id = id
		self.time = time
		self.index = index
	def __repr__(self):
		return repr((self.type, self.id, self.time, self.index))

class GlycationDB:
	def __init__(self, excerciseIndexFile, foodIndexFile):
		#self.ActivityList = list()
		self.ActivityDB = dict()
	
	def addActivity(self, activity):
		#self.ActivityList.append(activity)
		self.ActivityDB[activity.time] = activity
	
	def produceGlycationChart(self, fileName):

	
	def __writeChart(self, fileName, result):

	def __parseActivityFile(self, fileName, activityType):
