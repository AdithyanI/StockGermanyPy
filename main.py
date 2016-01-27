"""
This function gives out the performance for the last 5 years for a set of urls.
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
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
    """
    This is the main function where all the cool stuff happens.
    """
    results = PrettyTable(["Stock", "1day", "1week", "1month", "3month",
                           "1year", "3years", "5years"])
    results.align["City name"] = "l"  # Left align city names
    results.padding_width = 1  # One space between column edges and contents
    # (default)
    days = [1, 7, 30, 90, 356, 3 * 356, 5 * 356]
    years = [i / 356.0 for i in days]
    stocks = {'Comstage DAX': 'https://www.maxblue.de/maerkte-analysen/boersen'
                              '-kurse/fonds-detailseite.charts.html?ID_NOTATIO'
                              'N=24379520',
              'Comstage MSCI World': 'https://www.maxblue.de/maerkte-analysen/'
                                     'boersen-kurse/fonds-detailseite.charts.h'
                                     'tml?ID_NOTATION=26312020',
              'Comstage MSCI EM': 'https://www.maxblue.de/maerkte-analysen/boe'
                                  'rsen-kurse/fonds-detailseite.charts.html?ID'
                                  '_NOTATION=52432566'}
    for name in stocks:
        results.add_row([name] + extract_performance(stocks[name], years))
    print results


def extract_performance(url, years):
    """
    For a given url, this function extracts the performance for the last 5 yrs.
    :param years:
    :param url:
    """
    performance = ['-'] * 7
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    # This one day difference is slightly a tricky thing to extract.
    value = soup.findAll("div", "col-xs-6")[7].span.contents[0]
    performance[0] = colorify(navigable_string_to_float(value.split('/')[1]))
    tmp = soup.findAll("td", "idms_right")[0:6]
    for idx, element in enumerate(tmp):
        if element.span is not None:
            if idx > 0:
                value = yearly_performance(
                        navigable_string_to_float(element.span.contents[0]),
                        years[idx + 1])
            else:
                value = navigable_string_to_float(element.span.contents[0])
        performance[idx + 1] = colorify(value)
    # First extract the corresponding "td" class element.
    # Second extract the span child element of the corresponding element.
    # Third extract the contents, if there are contents.
    # Convert the extracted navigable_string_to_float

    return performance


def navigable_string_to_float(nvstr):
    """
    Convert a navigablestring, that is how things are usually stored in html
    pages, into a float.
    :param nvstr:
    """
    string = str(unicode(nvstr)).strip()
    frmtdstring = string.strip('%').replace(',', '.')
    flt = float(frmtdstring)
    return flt


def yearly_performance(value, years):
    """
    Convert a net performance into yearly performance.
    :param value:
    :param years:
    """
    yearly = ((1 + value / 100) ** (1.0 / years) - 1) * 100
    return round(yearly, 2)


def colorify(value):
    """
    Make it red or green according to the value.
    :param value:
    """
    if value > 0:
        color = "0;32m"  # green color
    else:
        color = "0;31m"  # red color
    return "\033[" + color + str(value) + "\033[0m"


if __name__ == '__main__':
    print "The main file is being executed"
    main()
else:
    print "The main file is being imported as a module"
