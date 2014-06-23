#-*- coding: UTF-8 -*-

# Theory of computation hw4 103.6.21
# 陳亭宇 F74002272
# Function:
#	which road in a city has house trading records spread in #max_distinct_month
# Method:
#	if met new road than call newAddr(), save road name, price, year
#	else save max price, min price, # of records
#	output: road name, max price, min price

import json
import urllib2
import sys
import re
import unicodedata
reload(sys)
sys.setdefaultencoding('UTF-8')

url = raw_input(u"url:")

response = urllib2.urlopen(url)
data = json.load(response)
key1 = u"土地區段位置或建物區門牌"
key2 = u"交易年月"
key3 = u"總價元"

addr = []

class Addr:
	def __init__(self, road, price):
		self.road = road
		self.maxP = price
		self.minP = price
		self.total = 1
		self.iyear = 1
		self.year = []

def getRoad(i):
	road = data[i].get(key1)
	iroad = road.find(u"大道")
	if iroad == -1:
		iroad = road.find(u"路")
		if iroad == -1:
			iroad = road.find(u"街")
			if (iroad == -1):
				iroad = road.find(u"巷")

	if iroad != -1:
		return data[i].get(key1)[:iroad+1]
	else:
		return ""

def findRoad(index, road):
	i = 0
	while i < index:
		if re.search(road, addr[i].road) > 0:
			return i
		i += 1
	return -1

def findYear(curI, year):
	i = 0
	while i < addr[curI].iyear:
		if year == addr[curI].year[i]:
			return
		i += 1
	addr[curI].year.append(year)
	addr[curI].iyear += 1
	addr[curI].total += 1

def newAddr(index, road, year, price):
	addr.append(Addr(road, price))
	addr[index].year.append(year)
	index = index + 1
	return index

def output(index):
	i = 0
	totalList = []
	while i < index:
		totalList.append(addr[i].total)
		i += 1

	totalList.sort()
	maxTotal = totalList[index-1]
	line = 0
	i = 0
	while i < index:
		if addr[i].total == maxTotal:
			line += 1
		i += 1
	i = 0
	l = 0
	print "\"",
	while i < index:
		if addr[i].total == maxTotal:
			if l < line-1:
				print u"\b%s, 最高成交價:%d, 最低成交價:%d" %(unicodedata.normalize('NFKD', addr[i].road), addr[i].maxP, addr[i].minP)
				l += 1
			else:
				print u"%s, 最高成交價:%d, 最低成交價:%d\"" %(unicodedata.normalize('NFKD', addr[i].road), addr[i].maxP, addr[i].minP)
		i += 1

def main(index):
	idata = 0
	while idata < len(data):
		j = 0
		year = dict(data[idata]).get(key2)
		price = dict(data[idata]).get(key3)
		# first data
		if index == 0:
			# found road
			road = getRoad(idata)
			if road != "":
				index = newAddr(index, road, year, price)
		else:
			# found road
			road = getRoad(idata)
			if road != "":
				# find match road
				curAddrIndex = findRoad(index, road)
				if curAddrIndex != -1:
					if price > addr[curAddrIndex].maxP:
						addr[curAddrIndex].maxP = price
					elif price < addr[curAddrIndex].minP:
						addr[curAddrIndex].minP = price

					findYear(curAddrIndex, year)
				# no match road
				else:
					index = newAddr(index, road, year, price)
		idata += 1
	output(index)
main(0)
