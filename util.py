#  Copyright © 2020-2021 Ansh Gandhi
#
#  This file is part of NorCal Bot.
#
#  NorCal Bot is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  NorCal Bot is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with NorCal Bot.  If not, see <https://www.gnu.org/licenses/>.
#
#  Original Author: Ansh Gandhi
#  Original Source Code: <https://github.com/norcalbotftc/NorCalBot/>
#
#  EVERYTHING ABOVE THIS LINE MUST BE KEPT AS IS UNDER GNU GPL LICENSE RULES.

# Import
import base64
from bs4 import BeautifulSoup as soup
from dotenv import load_dotenv
import os
from pathlib import Path
import random
import requests
import urllib.request

# Read From .env
env_path = Path('.') / '.env'
load_dotenv(dotenv_path = env_path)

BOT_NAME = os.getenv('BOT_NAME')
BOT_ID = int(os.getenv('BOT_ID'))
ADMINS = os.getenv('ADMINS').split(',')
ADMIN_IDS = [int(id) for id in os.getenv('ADMIN_IDS').split(',')]
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
API_CREDENTIALS = os.getenv('API_CREDENTIALS')
TEST_GUILD = int(os.getenv('TEST_GUILD'))
TEST_CHANNEL = int(os.getenv('TEST_CHANNEL'))
DB_URL = os.getenv('DATABASE_URL')

# FIRST API
API_CODES = {'SCRIM': 'USCANSAQT1', 'GOOG': 'USCANSAQT2', 'FMT4': 'USCANFRQT4', 'DALY': 'USCANDCQT1', 'FMT1': 'USCANFRQT1', 'FMT2': 'USCANFRQT2', 'PIE': 'USCANSAQT3', 'SC': 'USCANFRQT3', 'GB': 'USCANGBQT1', 'CUP': 'USCANCUQT1', 'SJ1': 'USCANSJCT1', 'SAC': 'USCANSAQT4', 'SANM': 'USCANSMQT1', 'Regional': 'USCANSJCT'}
API_AUTH = {'Authorization': 'Basic ' + base64.b64encode(API_CREDENTIALS.encode('ascii')).decode('ascii')}

# Competition Data
COMP_NAMES = {'GOOG': 'Google', 'FMT4': 'Fremont #4', 'DALY': 'Daly City', 'FMT1': 'Fremont #1', 'FMT2': 'Fremont #2', 'PIE': 'Piedmont', 'SC': 'Santa Clara', 'GB': 'Granite Bay', 'CUP': 'Cupertino', 'SJ1': 'San Jose #1', 'SAC': 'Sacramento', 'SANM': 'San Mateo'}
COMP_DATES = {'GOOG': '12/5/20', 'FMT4': '2/13/21', 'DALY': '2/20/21', 'FMT1': '2/27/21', 'FMT2': '2/28/21', 'PIE': '3/14/21', 'SC': '3/20/21', 'GB': '3/21/21', 'CUP': '3/28/21', 'SJ1': '4/10/21', 'SAC': '4/17/21', 'SANM': '4/18/21'}

# FTC Stats API Regions
REGIONS = {'GLOBAL': 'global', 'AK': 'alaska', 'AZ': 'arizona', 'NORCAL': 'norcal', 'SOCAL': 'socal', 'CAL': 'california', 'CA': 'california', 'CT': 'connecticut', 'DE': 'delaware', 'FL': 'florida', 'GA': 'georgia', 'HI': 'hawaii', 'IA': 'iowa', 'IL': 'illinois', 'IN': 'indiana', 'LA': 'louisiana', 'MA': 'massachusetts', 'MD': 'maryland', 'MI': 'michigan', 'MN': 'minnesota', 'MO': 'missouri', 'MS': 'mississippi', 'NC': 'north carolina', 'NJ': 'new jersey', 'NV': 'nevada', 'OH': 'ohio', 'OK': 'oklahoma', 'OR': 'oregon', 'PA': 'pennsylvania', 'RI': 'rhode island', 'SC': 'south carolina', 'TX': 'texas', 'UT': 'utah', 'VA': 'virginia', 'VT': 'vermont', 'WI': 'wisconsin', 'AB': 'alberta', 'AUS': 'australia', 'BC': 'british columbia', 'MAD': 'military and diplomatic', 'RUS': 'russia'}

# Web Scraping User Agents
OS = ('Windows NT 10.0; Win64; x64', 'Windows NT 5.1', 'Windows NT 6.1; Win64; x64', 'Windows NT 6.1; WOW64', 'Windows NT 10.0; WOW64', 'Windows NT 10.0', 'X11; Linux x86_64')
WEBKIT = ('537.1', '537.36', '605.1.15')
CHROME = ('21.0.1180.83', '44.0.2403.157', '46.0.2490.71', '56.0.2924.76', '60.0.3112.90', '60.0.3112.113', '63.0.3239.132', '65.0.3325.181', '67.0.3396.99', '68.0.3440.106', '69.0.3497.100', '72.0.3626.121', '74.0.3729.131', '74.0.3729.157', '74.0.3729.169', '78.0.3904.108', '79.0.3945.88', '79.0.3945.117', '79.0.3945.130', '80.0.3987.132', '80.0.3987.163', '81.0.4044.138', '83.0.4103.116', '84.0.4147.105', '84.0.4147.135', '85.0.4183.83', '85.0.4183.102', '85.0.4183.121', '86.0.4240.16', '86.0.4240.111', '87.0.4280.40', '88.0.4298.4', '88.0.4324.146', '88.0.4324.150')
SAFARI = ('537.1', '537.36', '604.1')

# Bot Version
VERSION = '2021.4.1.15'

def get_html(url):
    """
    get_html(url): get HTML data from specified URL
    :param url: URL to take HTML from
    :return: HTML code
    """

    req = urllib.request.Request(url, headers = {'User-Agent': 'Mozilla/5.0 (' + random.choice(OS) + ') AppleWebKit/' + random.choice(WEBKIT) + ' (KHTML, like Gecko) Chrome/' + random.choice(CHROME) + ' Safari/' + random.choice(SAFARI)})
    return soup(urllib.request.urlopen(req).read(), 'html.parser').prettify()

def get_raw_html(url):
    """
    get_raw_html(url): get raw HTML data from specified URL
    :param url: URL to take HTML from
    :return: raw HTML code
    """

    return requests.get(url, headers = {'User-Agent': 'Mozilla/5.0 (' + random.choice(OS) + ') AppleWebKit/' + random.choice(WEBKIT) + ' (KHTML, like Gecko) Chrome/' + random.choice(CHROME) + ' Safari/' + random.choice(SAFARI)}).text

def first_request(url):
    """
    first_request(url): get data from FIRST API
    :param url: API endpoint
    :return: API data
    """

    return requests.get('https://ftc-api.firstinspires.org/v2.0/2020/' + url, headers = API_AUTH)
