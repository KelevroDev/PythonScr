import sys
import re

def main (arg1):
	print ('File to be analysed: ' + arg1)
	print ()

	sbcat = open(arg1, 'r')

	#for line in sbcat:
		#line = line.replace("a00e".decode("hex"), "") 
		# print(line)

	#regexp for api name, e.g. "SharedData.DSharedData 0.5"
	p_api = re.compile('([a-zA-Z_]+).([a-zA-Z_]+) ([0-9]{1,2}).([0-9]{1,2})')

	list1 = []
	list2 = []
	mismatches = []
	exceptions = []


	for line in sbcat:
		line = line.replace("a00e".decode("hex"), "")
		print (line)
		m = p_api.search(line)
		if m:
			api = re.split(' ', m.group())
			list1.append(api)
			list2.append(api)


	for api1 in list1:
		i = 0

		for api2 in list2:
			if(api1[0] == api2[0]):
				i = i+1 
				if (api1[1] != api2[1]):
					mismatches.append(api1)

		if (i == 1):
			exceptions.append(api1)

	print ("----------API with version mismatches")
	printlist (mismatches)

#	print ()

#	print ("----------API without pairs")
#	printlist (exceptions)

	sbcat.close()
	return mismatches


def printlist(apilist):
	for api in apilist:
		print (api[0] + ' ' + api[1])


if __name__ == "__main__":
    main(sys.argv[1])