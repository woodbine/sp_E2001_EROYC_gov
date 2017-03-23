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
datadict = {'AjaxManager': 'esctl_17747319$ctlAssetManager$flwBrowseAssets$console$updConsolePanel|esctl_17747319$ctlAssetManager$flwBrowseAssets$console$paginationControl',
'EasySitePostBack': '', 'LinkState': '', 'PostbackAction': '', 'PostbackData': '', 'ScrollPos': '1643', '__ASYNCPOST': 'true', '__EVENTARGUMENT': '1', '__EVENTTARGET': 'esctl_17747319$ctlAssetManager$flwBrowseAssets$console$paginationControl',
'__EVENTVALIDATION': '/wEdABnBqwlJ0fM40ik8AyoZALD6+CC+bNiOs8u5eKpfs4a2BCn1bqdQKha0Xx1QfFRcc683krVHOcs1tYhwj9y/in1ay4C5LHj5wgUXh0RsfTnsy10Vaart0NR4W0M440oziVzbHdMQ38l9VY8gYbK0zOCs+X9aYyb658RcYMMTQXQolORzbFBDwAH7LMOfFVZsd4sOit9/u1K1wlNAjxJtxw+fz0qs04/cAJBUaSTxFtaFfaMpw+TQXY43LQftyBFFR6sP8Cpd6WXUVZgEk7Q/B34IthmjkfwjxeHK9wB8V8uiopDK8vgHitDl1y0+CuFABhqCtI4b8Qu5swyjWo4ZRyttKir0EjHbwkyU5OoMwgo1Idjn7Iwn40N/Idv9d8qYncFJwTZ9jusuw14XUVqUy3oekyIf+0gCiPju+KJ5fmiqla6QbtkHMcZjwBw4/CZPdR4sSqHKbaDshiAIjt5juXWwa5kHoH5u/gQSlHL46nqUTUjv/aSSOv7nfqUqXN5bazhHpmyMfUCYMhWAWkix5NoBL983xvNcASc9KBh70t2KQUsZCAX+s6i1WwdbESEXVNs=',
'__LASTFOCUS': '', '__VIEWSTATE': '/wEPZmRqNjs2tNXqh4Lvt46Eq6Emah7D3i8KU0s9y71iHC6Jzw==', '__VIEWSTATEGENERATOR': '090FE928', '__VIEWSTATEZIP': '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',
'esctl_17747319$ctlAssetManager$flwBrowseAssets$console$cKeywords$txtKeywords':'',
'esctl_17747319$ctlAssetManager$flwBrowseAssets$console$consoleMessagePanel$hfState':'',
'esctl_17747319$ctlAssetManager$flwBrowseAssets$console$resultsPerPageControl$ddlRecords':'75',
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
