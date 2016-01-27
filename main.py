#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#  
#  Copyright 2016 Adithyan Ilangovan <adithyan.i4internet@gmail.comy>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
from BeautifulSoup import BeautifulSoup
import urllib2
from prettytable import PrettyTable

def main():
	x = PrettyTable(["Stock", "1day", "1week", "1month", "3month", "1year", "3years", "5years"])
	x.align["City name"] = "l" # Left align city names
	x.padding_width = 1 # One space between column edges and contents (default)
	stocks = {'Comstage DAX' : 'https://www.maxblue.de/maerkte-analysen/boersen-kurse/fonds-detailseite.charts.html?ID_NOTATION=24379520',
			  'Comstage MSCI World' : 'https://www.maxblue.de/maerkte-analysen/boersen-kurse/fonds-detailseite.charts.html?ID_NOTATION=26312020',
			  'Comstage MSCI EM' : 'https://www.maxblue.de/maerkte-analysen/boersen-kurse/fonds-detailseite.charts.html?ID_NOTATION=52432566'}	
#	stocks = {'Comstage MSCI EM' : '\033[94m https://www.maxblue.de/maerkte-analysen/boersen-kurse/fonds-detailseite.charts.html?ID_NOTATION=52432566'}	
	for name in stocks:
		x.add_row([name] + extractPerformance(stocks[name]))
	print x

def extractPerformance(url):
	performance = ['-'] * 7
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page.read())
	# This one day difference is slightly a tricky thing to extract.
	value = soup.findAll("div", "col-xs-6")[7].span.contents[0]	
	performance[0] = (navigableStringToFloat(value.split('/')[1]))
	tmp = soup.findAll("td", "idms_right")[0:6]
	for idx, h in enumerate(tmp):
		if h.span is not None:
			if idx == 4: 
				performance[idx+1] = yearlyPerformance(navigableStringToFloat(h.span.contents[0]),3)
			elif idx == 5:
				performance[idx+1] = yearlyPerformance(navigableStringToFloat(h.span.contents[0]),5)
			else:
				performance[idx+1] = navigableStringToFloat(h.span.contents[0])	 
	# First extract the corresponding "td" class element.
	# Second extract the span child element of the corresponding element.
	# Third extract the contents, if there are contents.
	# Convert the extracted navigableStringToFloat
	return performance

def navigableStringToFloat(nvStr):
	string = str(unicode(nvStr)).strip()
	frmtdString = string.strip('%').replace(',','.')
	flt = float(frmtdString)
	return flt
	
def yearlyPerformance(value,years):
	yearly = ((1+value/100)**(1.0/years)-1)*100
	return round(yearly,2)

if __name__ == '__main__':
	print "The main file is being executed"
	main()
else:
	print "The main file is being imported as a module"
