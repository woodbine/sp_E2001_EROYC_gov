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
datadict = {'AjaxManager': 'esctl_15378791$ctlAssetManager$flwBrowseAssets$console$updConsolePanel|esctl_15378791$ctlAssetManager$flwBrowseAssets$console$paginationControl',
'EasySitePostBack': '', 'LinkState': '', 'PostbackAction': '', 'PostbackData': '', 'ScrollPos': '1287', '__ASYNCPOST': 'true', '__EVENTARGUMENT': '1', '__EVENTTARGET': 'esctl_15378791$ctlAssetManager$flwBrowseAssets$console$paginationControl',
'__EVENTVALIDATION': '/wEdABnCOcOyQ53nETANBmt3sKUvTJwA/WrsVqWEA1Mxr5FAwaZXX3EwrMvhJSo7A13489hXjRiGnyH7cBbIvPLqGcEmeRmpoE2A5iwOc3/+V+7G1Xi/3l4mrQM9vxnj/XuxyItsur/TwAeJmRa+gQukeo5h4iaCYPi10oTbekUvkZT2SilTJad66qgm2Osm5LTEnAQXllq2v8ImVeLQ2AAKbbw1W10u5nq2AFcwnFLgmYGBOhlSWM/7G9A6iqsJPaoyh0zeNSlSthQmr5btlytdhzbi4LeV5RzbME9BKiR365wPV8v6E8Dbo+iTOuEC09RvTNY6OIRtrssEdRSXtHt2Q0vVCcjGC47WVUV5NOXOleZ5Nu4YnQ3iXf0Lk4kdqh3ZBL9NVuTg68wp2Qq+y9zspIxgns1yHtJXk+zhKClIH8bB/1UEdRz375IEpGU0Tj5pAbAsSqHKbaDshiAIjt5juXWwa5kHoH5u/gQSlHL46nqUTUjv/aSSOv7nfqUqXN5bazhHpmyMfUCYMhWAWkix5NoBIkjHueEyL7lJfA7WZHrrJ+z8M0b+rYItg5lxWzdZXeY=',
'__LASTFOCUS': '', '__VIEWSTATE': '/wEPZmTOhBo/81FZKUngvj7bGxUNDfMHLwKZGHAYK5vi+mXHkg==', '__VIEWSTATEGENERATOR': '7C0681A6', '__VIEWSTATEZIP': '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\
/b/DvkP',
'esctl_15378791$ctlAssetManager$flwBrowseAssets$console$cKeywords$txtKeywords':'',
'esctl_15378791$ctlAssetManager$flwBrowseAssets$console$consoleMessagePanel$hfState':'',
'esctl_15378791$ctlAssetManager$flwBrowseAssets$console$resultsPerPageControl$ddlRecords':'59',
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

