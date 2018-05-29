import csv
import sys
EATING = 1
EXCERCISE = -1

class Activity:
	def __init__(self, type, id, time, index):
		self.type = type
		self.id = id
		self.time = time
		self.index = index
	def __repr__(self):
		return repr((self.type, self.id, self.time, self.index))

class GlycationDB:
	def __init__(self, foodDB, excerciseDB):
		self.ActivityDB = dict()
		self.FoodDB = dict()
		self.ExcerciseDB = dict()
		
		self.__parseActivityFile(foodDB, EATING, self.FoodDB)
		self.__parseActivityFile(excerciseDB, EXCERCISE, self.ExcerciseDB)
		
	
	def addActivity(self, activityType, time, activityId):
		# Not sure if multiple activities can be done at the same exact time. i.e. eating
		# multiple foods or eating while exercising
		if activityType == EATING:
			if activityId in self.FoodDB:
				activity = self.FoodDB[activityId]
				self.ActivityDB[time] = Activity(activityType, activityId, time, activity.index)
			else:
				print("ERROR: Unrecognized food id of " + str(activityId))
		elif activityType == EXCERCISE:
			if activityId in self.ExcerciseDB:
				activity = self.FoodDB[activityId]
				self.ActivityDB[time] = Activity(activityType, activityId, time, -1*activity.index)
			else:
				print("ERROR: Unrecognized excercise id of " + str(activityId))

	
	def produceGlycationChart(self, fileName):
		# For the moment, I think having minute resolution for the chart works fairly
		# well, specifically since there are only 1440 minutes during the day
		glycolMonitor = list()
		glycolLevel = 80
		result = dict()
		glycation = 0
		for x in range(60*24):
			# Check if there are still time remaining to process the food or excercise.
			# If no excercise or eating took place within the last 1-2 hours, slowly
			# go back to the standard glycemic index
			if len(glycolMonitor) == 0:
				if glycolLevel > 80:
					glycolLevel -= 1
				elif glycolLevel < 80:
					glycolLevel += 1
				
				# Fix for percision errors
				if abs(glycolLevel-80) < 1:
					glycolLevel = 80
		
			# Check the time for each activity, if the time limit ends, we remove the
			# remove the rate changes for said limit
			newList = []
			for track in glycolMonitor:	
				cnt, rate = track
				glycolLevel += rate
				track = (cnt - 1, rate)
				if track[0] > 0:
					newList.append(track)
					
			glycolMonitor = newList
			
			# Record the glycemic index for this time
			if round(glycolLevel) >= 150:
				glycation += 1
			
			if glycolLevel < 0:
				glycolLevel = 0
			result[x] = glycolLevel

			# Keep track for activity we do during this time
			if x in self.ActivityDB:
				activity = self.ActivityDB[x]
				if (activity.type == EATING):
					rate = activity.index/120
					timeCnt = 120
					glycolMonitor.append((timeCnt, rate))
				else:
					rate = activity.index/60
					timeCnt = 60
					glycolMonitor.append((timeCnt, rate))

		#Write a csv file with time as the x axis and glycemic level as y access
		self.__writeChart(fileName, result)
		print ("Glycation found to be: " + str(glycation))
		s = input('--> ')  
	
	def __writeChart(self, fileName, result):
		file = open(fileName,'w') 
		for time, value in result.items():
			file.write(str(time) + "," +str(value) + '\n')
			
	def __parseActivityFile(self, fileName, activityType, dataBase):
		first = True
		with open(fileName, newline='') as csvfile:
			reader = csv.reader(csvfile, quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL)
			for row in reader:
				if first:
					first = False
					continue
				dataBase[int(row[0])] = Activity(activityType, int(row[0]), row[1].encode('utf-8'), int(row[2])*activityType)

	
if __name__ == "__main__":
	gDB = GlycationDB("FoodDB.csv", "ExcerciseDB.csv")
	gDB.addActivity(EATING, 100, 61)
	gDB.addActivity(EXCERCISE, 150, 4)
	
	gDB.addActivity(EATING, 400, 61)
	gDB.addActivity(EXCERCISE, 820, 2)
	gDB.addActivity(EXCERCISE, 850, 4)
	gDB.addActivity(EATING, 1220, 11)
	
	gDB.produceGlycationChart("Test.csv")
	