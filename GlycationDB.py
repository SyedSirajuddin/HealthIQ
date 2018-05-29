import csv
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
		self.ActivityDB = dict()
	
	def addActivity(self, activity):
		# Not sure if multiple activities can be done at the same exact time. i.e. eating
		# multiple foods or eating while exercising
		self.ActivityDB[activity.time] = activity
	
	def produceGlycationChart(self, fileName):
		# For the moment, I think having minute resolution for the chart works fairly
		# well, specifically since there are only 1440 minutes during the day
		glycolMonitor = list()
		glycolLevel = 80
		result = dict()
		for x in range(60*24):
			# Check if there are still time remaining to process the food or excercise.
			# If no excercise or eating took place within the last 1-2 hours, slowly
			# go back to the standard glycemic index
			if len(glycolMonitor) == 0:
				if glycolLevel > 80:
					glycolLevel -= 1
				elif glycolLevel < 80:
					glycolLevel += 1
		
			# Check the time for each activity, if the time limit ends, we remove the
			# remove the rate changes for said limit
			newList = []
			for track in glycolMonitor:	
				cnt, rate = track
				glycolLevel += rate
				track = (cnt - 1, rate)
				if track[0] > 0:
					newList.append(track)
				#else:
					#glycolMonitor.remove(track)
					#continue
			glycolMonitor = newList
			
			# Record the glycemic index for this time
			result[x] = glycolLevel
			
			# Keep track for activity we do during this time
			if x in self.ActivityDB:
				activity = self.ActivityDB[x]
				if (activity.type == 1):
					rate = activity.index/120
					timeCnt = 120
					glycolMonitor.append((timeCnt, rate))
				else:
					rate = activity.index/60
					timeCnt = 60
					glycolMonitor.append((timeCnt, rate))

		#Write a csv file with time as the x axis and glycemic level as y access
		self.__writeChart(fileName, result)
		s = input('--> ')  
	
	def __writeChart(self, fileName, result):
		#with open(fileName, 'wb') as csvfile:
		#	writer = csv.writer(csvfile, delimiter=' ',
		#							quotechar='|', quoting=csv.QUOTE_MINIMAL)
		file = open(fileName,'w') 
		for time, value in result.items():
			#writer.writerow([str(time), str(value)])
			file.write(str(time) + "," +str(value) + '\n')
			print (str(time) + " " +  str(value))

	#def __parseActivityFile(self, fileName, activityType):
	#	with open(fileName, 'rb') as csvfile:
	#		data = csv.reader(csvfile, quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL):
	#		for row in data:
	
if __name__ == "__main__":
	gDB = GlycationDB("Eating", "Excercise")
# type, id, time, index
	lunch = Activity(1, 1, 400, 60)
	gDB.addActivity(lunch)
	dinner = Activity(1, 1, 1320, 60)
	gDB.addActivity(dinner)
	
	gDB.produceGlycationChart("Test.csv")
	