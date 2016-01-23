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
	stocks = {'Comstage MSCI World': 'https://www.boerse-stuttgart.de/en/stock-exchange/securities-and-markets/exchange-traded-products/exchange-traded-funds/factsheet/?ID_NOTATION=26562449',
			  'Comstage DAX': 'https://www.boerse-stuttgart.de/en/stock-exchange/securities-and-markets/exchange-traded-products/exchange-traded-funds/factsheet/?ID_NOTATION=24526432'}	
	for name in stocks:
		x.add_row([name] + extractPerformance(stocks[name]))
	print x

def extractPerformance(url):
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page.read())
	# This one day difference is slightly a tricky thing to extract.
	values02 = [h2.contents[1] for h2 in soup.findAll('td', {'class': 'left down'})]	
	soupForValue0 = BeautifulSoup(''.join(values02[1]))
	values0 = navigableStringToFloat(soupForValue0)
	# Extracting other is fairly easy.
	values1 = [navigableStringToFloat(h2.string) for h2 in soup.findAll("td", "right  down")]	
	values2 = [navigableStringToFloat(h2.string) for h2 in soup.findAll("td", "right  up")]	
	values3 = [navigableStringToFloat(h2.string) for h2 in soup.findAll("td", "right last up")]
	performance = [values0,values1[0],values1[1],values1[2],values1[3],yearlyPerformance(values2[0],3),yearlyPerformance(values3[0],5)] 
	print yearlyPerformance(values2[0],3)
	print yearlyPerformance(values3[0],5)
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
