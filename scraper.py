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
datadict = {'AjaxManager': 'esctl_20242569$ctlAssetManager$flwBrowseAssets$console$updConsolePanel|esctl_20242569$ctlAssetManager$flwBrowseAssets$console$paginationControl',
'EasySitePostBack': '', 'LinkState': '', 'PostbackAction': '', 'PostbackData': '', 'ScrollPos': '1431', '__ASYNCPOST': 'true', '__EVENTARGUMENT': '1', '__EVENTTARGET': 'esctl_20242569$ctlAssetManager$flwBrowseAssets$console$paginationControl',
'__EVENTVALIDATION': '/wEdABXBqwlJ0fM40ik8AyoZALD6Rww5ZtSA5diJbW2I/HREwEKMkDkEXVh/BozJJLZWmIJmZ3BDZPIC19uZp/PiF+75LWoQ3bQPxQZmxra1evH7kXYaIXBD9DWgLluI6zSsSbY42rd/vkmf9UUXmZ3CDBLAOX/G12jEMC/Tcm94u8rO4JK/Uc+TPhpkpSdGZC0jDmPqvD3ns0PYdvnc0DERQYSHYgtLRDO3IDOy1wVC5Jg4lsJfTQctkyI2vXf2rEcdTQq5cNTWwVoADv7aS41FQxItheDqUygEONgMkzQK5UXx6+RHr/MnmGMHQFwE9UPu1qwztcwdOlJIAQa1bX6DjX0dei2in64I7lLLlRgAzDLYuDhApZ2cCVTQiQJ6hjXOSSL6JCRp7T6PQmjN1AnbpU5rfebm+qWxvFnjAVTolseOqc7NJ6TJvlCk+xQgmXL824/AYvd2kuuq1WI6UX4BmKThzVAn8jbBNRhy+E83o64NLw==',
'__LASTFOCUS': '', '__VIEWSTATE': '/wEPZmRqNjs2tNXqh4Lvt46Eq6Emah7D3i8KU0s9y71iHC6Jzw==', '__VIEWSTATEGENERATOR': '090FE928', '__VIEWSTATEZIP': '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',
'esctl_20242569$ctlAssetManager$flwBrowseAssets$console$cKeywords$txtKeywords':'',
'esctl_20242569$ctlAssetManager$flwBrowseAssets$console$consoleMessagePanel$hfState':'',
'esctl_20242569$ctlAssetManager$flwBrowseAssets$console$resultsPerPageControl$ddlRecords':'84',
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
        if 'July2016' in csvYr:
            csvMth = '06'
            csvYr = '2016'
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
