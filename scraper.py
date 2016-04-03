# -*- coding: utf-8 -*-

#### IMPORTS 1.0

import os
import re
import scraperwiki
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup


#### FUNCTIONS 1.0

def validateFilename(filename):
    filenameregex = '^[a-zA-Z0-9]+_[a-zA-Z0-9]+_[a-zA-Z0-9]+_[0-9][0-9][0-9][0-9]_[0-9QY][0-9]$'
    dateregex = '[0-9][0-9][0-9][0-9]_[0-9QY][0-9]'
    validName = (re.search(filenameregex, filename) != None)
    found = re.search(dateregex, filename)
    if not found:
        return False
    date = found.group(0)
    now = datetime.now()
    year, month = date[:4], date[5:7]
    validYear = (2000 <= int(year) <= now.year)
    if 'Q' in date:
        validMonth = (month in ['Q0', 'Q1', 'Q2', 'Q3', 'Q4'])
    elif 'Y' in date:
        validMonth = (month in ['Y1'])
    else:
        try:
            validMonth = datetime.strptime(date, "%Y_%m") < now
        except:
            return False
    if all([validName, validYear, validMonth]):
        return True


def validateURL(url):
    try:
        r = urllib2.urlopen(url)
        count = 1
        while r.getcode() == 500 and count < 4:
            print ("Attempt {0} - Status code: {1}. Retrying.".format(count, r.status_code))
            count += 1
            r = urllib2.urlopen(url)
        sourceFilename = r.headers.get('Content-Disposition')

        if sourceFilename:
            ext = os.path.splitext(sourceFilename)[1].replace('"', '').replace(';', '').replace(' ', '')
        else:
            ext = os.path.splitext(url)[1]
        validURL = r.getcode() == 200
        validFiletype = ext.lower() in ['.csv', '.xls', '.xlsx']
        return validURL, validFiletype
    except:
        print ("Error validating URL.")
        return False, False

def validate(filename, file_url):
    validFilename = validateFilename(filename)
    validURL, validFiletype = validateURL(file_url)
    if not validFilename:
        print filename, "*Error: Invalid filename*"
        print file_url
        return False
    if not validURL:
        print filename, "*Error: Invalid URL*"
        print file_url
        return False
    if not validFiletype:
        print filename, "*Error: Invalid filetype*"
        print file_url
        return False
    return True


def convert_mth_strings ( mth_string ):
    month_numbers = {'JAN': '01', 'FEB': '02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09','OCT':'10','NOV':'11','DEC':'12' }
    for k, v in month_numbers.items():
        mth_string = mth_string.replace(k, v)
    return mth_string


#### VARIABLES 1.0

entity_id = "E2001_EROYC_gov"
url = "http://www2.eastriding.gov.uk/council/governance-and-spending/budgets-and-spending/council-spending-and-salaries/"
errors = 0
data = []
user_agent = {'User-agent': 'Mozilla/5.0'}
datadict = {'AjaxManager': 'esctl_15712881$ctlAssetManager$flwBrowseAssets$console$updConsolePanel|esctl_15712881$ctlAssetManager$flwBrowseAssets$console$paginationControl',
'EasySitePostBack': '', 'LinkState': '', 'PostbackAction': '', 'PostbackData': '', 'ScrollPos': '1212', '__ASYNCPOST': 'true', '__EVENTARGUMENT': '1', '__EVENTTARGET': 'esctl_15712881$ctlAssetManager$flwBrowseAssets$console$resultsPerPageControl$ddlRecords',
'__EVENTVALIDATION': '/wEdABlPYYMJcTYbQOzU8gkAswXZVMAiGsPEIl/MzwaHO7JWCpwEbgEfDW02V4/lJAfe3nsdugdIdggJSxESK2ismjkk8On4AhAsNOSxclRIGdc2C1149VO8vozDppoCubfhmsCHNVn0eCMRQ7zdsB+Qd3IuMSSQsXVsKHKtDNQzrLlCCrrMNMTetg+iYqVYQpGkXVYgXLrjBkoTTL59WDhHIlb0yn8BSgGfMAK5r4XuO6LML93zO3qcyxBr1oQJjdIV4Vsm+yuabnVae4tCj5Hz0U2swRmDbf5N8sTgRoM7Rjes2MPVjcpusO42JQ1B4hq+wqQW/QyCo8wEQi2fgrgOea4x7OIqIZIvy9j5oZK8p5areJyJVpAn5Mnkxzcvo5Z9uZf5fxarF+F41BSGwQ1WZ9tUdHyGkoKgvz+SEjfYgs700jodKDwlCYSI49jSG3BpeEMsSqHKbaDshiAIjt5juXWwa5kHoH5u/gQSlHL46nqUTUjv/aSSOv7nfqUqXN5bazhHpmyMfUCYMhWAWkix5NoBpzJhbnBzaWbz9z3ZO/ECDXD/Q468YDca0jJi9HE/S4o=',
'__LASTFOCUS': '', '__VIEWSTATE': '/wEPZmSKJeMg9d+B0FsT4XD5g9e4eYueNsf1zKF8ivOqzQXS7A==', '__VIEWSTATEGENERATOR': '7C0681A6', '__VIEWSTATEZIP': '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',
'esctl_15712881$ctlAssetManager$flwBrowseAssets$console$cKeywords$txtKeywords':'',
'esctl_15712881$ctlAssetManager$flwBrowseAssets$console$consoleMessagePanel$hfState':'',
'esctl_15712881$ctlAssetManager$flwBrowseAssets$console$resultsPerPageControl$ddlRecords':'63',
}


#### READ HTML 1.2

import requests   # import requests for making post requests

html = requests.post(url, data= datadict, headers=user_agent)     # using requests for making post requests
soup = BeautifulSoup(html.text, 'lxml')

#### SCRAPE DATA


block = soup.find('div', 'clear grid-inner')
links = soup.findAll('a', href=True)
for link in links:
    csvfile = link.text.strip()
    if '500'  in csvfile:
        urls = link['href']
        code_url = urls[-8:-2]
        url = 'http://www2.eastriding.gov.uk/EasysiteWeb/getresource.axd?AssetID={}&type=full&servicetype=Attachment'.format(code_url)
        csvMth =csvfile.split(' ')[-2][:3]
        csvYr =csvfile.split(' ')[-1]
        csvMth = convert_mth_strings(csvMth.upper())
        data.append([csvYr, csvMth, url])

#### STORE DATA 1.0

for row in data:
    csvYr, csvMth, url = row
    filename = entity_id + "_" + csvYr + "_" + csvMth
    todays_date = str(datetime.now())
    file_url = url.strip()

    valid = validate(filename, file_url)

    if valid == True:
        scraperwiki.sqlite.save(unique_keys=['l'], data={"l": file_url, "f": filename, "d": todays_date })
        print filename
    else:
        errors += 1

if errors > 0:
    raise Exception("%d errors occurred during scrape." % errors)


#### EOF

