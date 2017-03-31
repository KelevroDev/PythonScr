def getFile2(FolderPath):
	path = FolderPath
	global WeeklySeconds
	global DailySeconds
	global FilePassDaily
	global FilePassWeekly
	global counter
	global dayFile
	global weekFile
	global name3File
	global line
	global folderNameW
	#folderNameW = ""
	global folderNameD
	#folderNameD = ""
	line = ""
	name3File = ""
	maxTime = 0
	ext3File = ""
	counter = 0
	fileList = os.listdir(path)
	counter = 0
	for folder in fileList:
		if folder != "Thumbs.db":
			counter = counter + 1
			timeM = os.path.getctime(path + folder)
			if maxTime < time:
				maxTime = timeM
				name3File = folder
				#print ("name3File - " + name3File)
				timeM = os.path.getctime(path + name3File)
				if path == pathToDaily:
					if timeM == 0:
						print ("File size = NULL")
					else :
						DailySeconds = timeM
				if path == pathToWeekly:
					if timeM == 0:
						print ("File size = NULL")
					else :
						WeeklySeconds = timeM
					########################################
				for file in name3File:
					fileList = os.listdir(path + name3File)
					########################################
				for line in fileList:
					if line.endswith('.ext3'):
						if path == pathToDaily:
							FilePassDaily = path + name3File + "\\" + line
							folderNameD = name3File
							dayFile = line
						if path == pathToWeekly:
							weekFile = line
							FilePassWeekly = path + name3File + "\\" + line
							folderNameW = name3File
		else:
			print ("It's a file " + str(name3File) + "*********************************")