import networkx as nx
import time
import re

class LocationSummary:
	'''Class that stores information and network statistics on each location in the foursquare data.'''
	def __init__(self,activity,network):
		self.activity = activity
		self.network = network
		G = nx.Graph()
		G.add_nodes_from(activity.users)
		G.add_edges_from(network)
		self.location = activity.location
		self.checkins = len(activity.checkins)
		self.degrees = sorted(G.degree().values())
		self.components = nx.connected_components(G)
		self.maxcomponent = 1
		for x in self.components:
			y = len(x)
			if y > self.maxcomponent:
				self.maxcomponent = y
		self.totalcomponents = len(self.components)
		self.totalnodes = len(activity.users)
		self.totaledges = len(network)
		if self.totalnodes > 1: 
			self.density = self.totaledges/float(self.totalnodes * (self.totalnodes - 1)/2) 
		else: 
			self.density = 0

def List_of_Location_Summaries(listoflists,edges):
	finallist = []
	y = List_of_Location_Activities(listoflists)
	for x in y:
		#print y[x]
		releventedges = []
		z = y[x].users
		for q in edges:
			a = q[0]
			b = q[1]
			#print a
			#print b
			if a in z and b in z:
				releventedges.append((a,b))
		t = LocationSummary(y[x],releventedges)
		finallist.append(t)
	return finallist

def List_of_Location_Activities(listoflists):
	LocationsList = List_of_Locations(listoflists)
	CheckinsList = List_of_Checkins(listoflists)
	LocationActivitiesList = {}
	for x in LocationsList:
		try:
			LocationActivitiesList[x] = Location_Activity(x)
		except:
			pass
	for a in CheckinsList:
		b = a.location
		c = LocationActivitiesList[b]
		c.addcheckin(a)
	return LocationActivitiesList

def List_of_Checkins(listoflists):
	'''Turns data into checkins using the Checkin class, and creates a giant list of them.'''
	finallist =[]
	for x in listoflists:
		y = Checkin(x)
		finallist.append(y)
	return finallist

def List_of_Locations(listoflists):
	locationinstances = []
	for x in listoflists:
		y = Checkin(x)
		z = y.location
		locationinstances.append(z) 
	locations = set(locationinstances)
	return locations

class Location_Activity:
	'''Class that stores all activity (Checkins, Users, etc.) associated with a given location'''
	def __init__(self,locationid):
		self.location = str(locationid)
		self.userinstances = []
		self.users = set(self.userinstances)
		self.numberofusers = len(self.users)
		self.checkins =[]
		self.numberofcheckins = len(self.checkins)

	def addcheckin(self,checkin):
		y = checkin.user
		z = (checkin.user,checkin.time)
		x = checkin.location
		if int(x) == int(self.location):
			self.userinstances.append(y)
			self.checkins.append(z)
			self.numberofcheckins = len(self.checkins)
			self.users = set(self.userinstances)
			self.numberofusers = len(self.users)

class Checkin:
	'''Class that stores details of one specific foursquare checkin. Helper class for function list_of_locations'''
	def __init__(self,string):
		newstring = re.sub(r'[\n]+',' ', string)
		listofcoords = newstring.split(',',4)
		self.user = listofcoords[0]
		self.coordinates = (listofcoords[1],listofcoords[2])
		self.time = listofcoords[3]
		self.location = int(listofcoords[4])

if __name__ == '__main__': 
	tic = time.time()
	checkins = (open('FoursquareCheckins.csv').readlines())[1:]
	networkedges = []
	for x in (open('FoursquareFriendship.csv').readlines())[1:]:
		y = re.sub(r'[\n]+','', x)
		z = y.split(',',2)
		if int(z[0]) < int(z[1]):
			networkedges.append(z)
	#print len(networkedges)
	#print len(checkins)
	#print networkedges[0:5]
	c = List_of_Location_Summaries(checkins,networkedges)
	print 'location' +'|' + 'checkins' + '|' + 'totalcomponents' + '|' + 'maxcomponent' + '|' + 'totalnodes' + '|' + 'totaledges' + '|' + 'density' + '|' + 'degrees' + '|' + 'components'
	for x in c:
		print str(x.location)+'|'+str(x.checkins)+'|'+str(x.totalcomponents)+'|'+str(x.maxcomponent)+'|'+str(x.totalnodes)+'|'+str(x.totaledges)+'|'+str(x.density)+'|'+ str(x.degrees)+ '|'+ str(x.components)
	#print time.time() - tic
