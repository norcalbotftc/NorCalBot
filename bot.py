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
#  Original Source Code: <https://github.com/anshgandhi4/NorCal-Bot/>
#
#  EVERYTHING ABOVE THIS LINE MUST BE KEPT AS IS UNDER GNU GPL LICENSE RULES.

# Import
import asyncio
import base64
from bs4 import BeautifulSoup as soup
import discord
from dotenv import load_dotenv
import os
from pathlib import Path
import random
import re
import requests
import urllib.request

# Sensitive Info
env_path = Path('.') / '.env'
load_dotenv(dotenv_path = env_path)

BOT_NAME = os.getenv('BOT_NAME')
ADMINS = os.getenv('ADMINS').split(',')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
API_CREDENTIALS = os.getenv('API_CREDENTIALS')
TEST_GUILD = int(os.getenv('TEST_GUILD'))
TEST_CHANNEL = int(os.getenv('TEST_CHANNEL'))

# Commands
COMMANDS = ('help', 'about', 'test', 'version', 'moo', 'monke', 'laff', 'joos', 'bts', 'osas', 'bigshaq', 'asznee', 'frydae', 'wednesdae', 'beteor', 'leek', 'sad', 'comrade', 'veriguds', 'setcounters', 'stats', 'tlookup', 'clookup', 'comps', 'fairplay', 'rankings', 'awards', 'scores', 'dscores', 'special')
HELP_COMMANDS = ('$' + COMMANDS[0], '$' + COMMANDS[1], '$' + COMMANDS[2], '$' + COMMANDS[3], '$' + COMMANDS[20], '$' + COMMANDS[21] + ' [team number]', '$' + COMMANDS[22] + ' [competition id]', '$' + COMMANDS[23], '$' + COMMANDS[24], '$' + COMMANDS[25] + ' [competition id]', '$' + COMMANDS[26] + ' [competition id]', '$' + COMMANDS[27] + ' [competition id] [team number]', '$' + COMMANDS[28] + ' [competition id] [team number]')
HELP_MESSAGES = ('Shows this help message', 'Shows credits', 'To make sure the bot is running', 'Shows bot version', 'Shows the counters for each command', 'Shows the competitions for the registered team', 'Shows the teams for the specified competition', 'Shows all of the competition codes', 'Shows a list of all of the fair play teams', 'Shows the rankings at a competition', 'Shows the award winnners at a competition', 'Shows a team\'s scores at a competition', 'Shows a detailed breakdown of a team\'s scores at a competition')
NUM_COMMANDS = len(COMMANDS)

# FIRST API
API_CODES = {'SCRIM': 'USCANSAQT1', 'GOOG': 'USCANSAQT2', 'FMT4': 'USCANSAQT14',  'DALY': 'USCANSAQT8', 'FMT1': 'USCANSAQT9', 'SJ2': 'USCANSAQT10', 'PIE': 'USCANSAQT3', 'SC': 'USCANSAQT11', 'GB': 'USCANSAQT12', 'SJ1': 'USCANSAQT7', 'SAC': 'USCANSAQT4', 'SANM': 'USCANSAQT6'}
API_AUTH = {'Authorization': 'Basic ' + base64.b64encode(API_CREDENTIALS.encode('ascii')).decode("ascii")}

# Competition Data
COMP_NAMES = {'GOOG': 'Google', 'FMT4': 'Fremont #4', 'DALY': 'Daly City', 'FMT1': 'Fremont #1', 'FMT2': 'Fremont #2', 'SJ2': 'San Jose #2', 'PIE': 'Piedmont', 'SC': 'Santa Clara', 'GB': 'Granite Bay', 'CUP': 'Cupertino', 'SJ1': 'San Jose #1', 'SAC': 'Sacramento', 'SANM': 'San Mateo'}
COMP_DATES = {'GOOG': '12/5/20', 'FMT4': '2/13/21', 'DALY': '2/20/21', 'FMT1': '2/27/21', 'FMT2': '2/28/21', 'SJ2': '3/13/21', 'PIE': '3/14/21', 'SC': '3/20/21', 'GB': '3/21/21', 'CUP': '3/28/21', 'SJ1': '4/10/21', 'SAC': '4/17/21', 'SANM': '4/18/21'}

# Web Scraping User Agent
OS = ('Windows NT 10.0; Win64; x64', 'Windows NT 5.1', 'Windows NT 6.1; Win64; x64', 'Windows NT 6.1; WOW64', 'Windows NT 10.0; WOW64', 'Windows NT 10.0', 'X11; Linux x86_64')
WEBKIT = ('537.1', '537.36', '605.1.15')
CHROME = ('21.0.1180.83', '44.0.2403.157', '46.0.2490.71', '56.0.2924.76', '60.0.3112.90', '60.0.3112.113', '63.0.3239.132', '65.0.3325.181', '67.0.3396.99', '68.0.3440.106', '69.0.3497.100', '72.0.3626.121', '74.0.3729.131', '74.0.3729.157', '74.0.3729.169', '78.0.3904.108', '79.0.3945.88', '79.0.3945.117', '79.0.3945.130', '80.0.3987.132', '80.0.3987.163', '81.0.4044.138', '83.0.4103.116', '84.0.4147.105', '84.0.4147.135', '85.0.4183.83', '85.0.4183.102', '85.0.4183.121', '86.0.4240.16', '86.0.4240.111', '87.0.4280.40', '88.0.4298.4', '88.0.4324.146', '88.0.4324.150')
SAFARI = ('537.1', '537.36', '604.1')

# Data
counter = {command: 0 for command in COMMANDS}
teams = {524: ['GOOG', 'DALY', 'N/A', 'Boss Bots'], 596: ['N/A', 'N/A', 'N/A', 'SpectreBots'], 669: ['N/A', 'N/A', 'N/A', 'Milpitas Xtreme Robotics'], 3470: ['DALY', 'N/A', 'N/A', 'The Patriots'], 3873: ['N/A', 'N/A', 'N/A', 'Scotbotics'], 4345: ['FMT1', 'FMT4', 'N/A', 'Aragon Robotics'], 4475: ['N/A', 'N/A', 'N/A', 'Purple Reign'], 4950: ['N/A', 'N/A', 'N/A', 'Tino 49ers'], 4998: ['FMT1', 'N/A', 'N/A', 'SPQR - Sen?tus Populusque R?boticus'], 5206: ['CUP', 'N/A', 'N/A', 'The Knights of Ni'], 5214: ['N/A', 'N/A', 'N/A', 'QLS Tech Support'], 5773: ['FMT2', 'N/A', 'N/A', 'Ink and Metal'], 6038: ['N/A', 'N/A', 'N/A', 'Tino Techformers'], 6165: ['GOOG', 'FMT4', 'N/A', 'MSET CuttleFish'], 6949: ['FMT1', 'SC', 'N/A', 'Einstein Eagles'], 7128: ['N/A', 'N/A', 'N/A', '28 Karat'], 7303: ['FMT1', 'N/A', 'N/A', 'RoboAvatars'], 7316: ['N/A', 'N/A', 'N/A', 'Iron Panthers'], 7390: ['FMT1', 'N/A', 'N/A', 'MSET JellyFish'], 7593: ['N/A', 'N/A', 'N/A', 'TigerBots'], 7610: ['N/A', 'N/A', 'N/A', 'Tino Frontier'], 7641: ['DALY', 'N/A', 'N/A', 'MSET BettaFish'], 7854: ['GOOG', 'FMT1', 'N/A', 'MidKnight Madness'], 8367: ['FMT1', 'N/A', 'N/A', 'ACME Robotics'], 8375: ['GOOG', 'DALY', 'N/A', 'Vulcan Robotics'], 8381: ['DALY', 'SC', 'N/A', 'M'], 8404: ['DALY', 'FMT2', 'N/A', 'Quixilver'], 8872: ['FMT1', 'N/A', 'N/A', 'Robopocalypse'], 9578: ['N/A', 'N/A', 'N/A', 'Purple Pi'], 9614: ['FMT4', 'N/A', 'N/A', 'Hyperion'], 9656: ['FMT4', 'N/A', 'N/A', 'Omega'], 9657: ['DROPPED', 'DALY', 'N/A', 'Athena Robotics'], 9784: ['GOOG', 'DALY', 'N/A', 'Dry Ice'], 10023: ['N/A', 'N/A', 'N/A', 'GatorBots'], 10163: ['N/A', 'N/A', 'N/A', 'Axes of Revolution'], 11039: ['GOOG', 'FMT1', 'N/A', 'Innov8rz'], 11099: ['N/A', 'N/A', 'N/A', 'Tacobots'], 11201: ['FMT2', 'GB', 'N/A', 'Piedmont Pioneers'], 11311: ['N/A', 'N/A', 'N/A', 'Paragon'], 11466: ['N/A', 'N/A', 'N/A', 'Tinosaurus'], 11467: ['N/A', 'N/A', 'N/A', 'Data Miners'], 11475: ['FMT2', 'N/A', 'N/A', 'Teravoltz'], 11575: ['FMT2', 'CUP', 'N/A', 'Robust Robots'], 11689: ['N/A', 'N/A', 'N/A', 'We Love Pi'], 12516: ['N/A', 'N/A', 'N/A', 'TBD'], 12628: ['N/A', 'N/A', 'N/A', 'Fremont Hawk'], 12635: ['GOOG', 'N/A', 'N/A', 'Kuriosity Robotics'], 12804: ['N/A', 'N/A', 'N/A', 'LED'], 12869: ['FMT1', 'N/A', 'N/A', 'Voyager 6+'], 12962: ['GOOG', 'FMT2', 'N/A', 'Zenith'], 13035: ['N/A', 'N/A', 'N/A', 'Boundless Robotics'], 13050: ['SJ2', 'N/A', 'N/A', 'SharkBytes'], 13180: ['FMT4', 'SC', 'N/A', 'Roverdrive'], 13217: ['FMT2', 'N/A', 'N/A', 'AstroBruins'], 13218: ['SC', 'N/A', 'N/A', 'Taro'], 13223: ['GOOG', 'N/A', 'N/A', 'Endgame'], 13274: ['DALY', 'N/A', 'N/A', 'Longhorn Robotics'], 13345: ['GOOG', 'DALY', 'N/A', 'Polaris'], 13356: ['FMT4', 'FMT1', 'N/A', 'RoboForce'], 13380: ['FMT1', 'N/A', 'N/A', 'Quantum Stinger'], 14078: ['N/A', 'N/A', 'N/A', 'Mechanical Lemons'], 14162: ['GOOG', 'FMT1', 'N/A', 'Bots&amp;Bytes'], 14214: ['FMT1', 'N/A', 'N/A', 'NvyUs'], 14259: ['DALY', 'N/A', 'N/A', 'TURB? V8'], 14298: ['N/A', 'N/A', 'N/A', 'Lincoln Robotics'], 14300: ['FMT1', 'N/A', 'N/A', 'Animatronics'], 14318: ['GOOG', 'DALY', 'N/A', 'BioBots'], 14341: ['DROPPED', 'FMT2', 'N/A', 'Hypercube Robotics'], 14473: ['FMT4', 'N/A', 'N/A', 'Future'], 14502: ['FMT1', 'N/A', 'N/A', 'Chocolate Cyborgs'], 14504: ['DALY', 'CUP', 'N/A', 'SerenityNow!'], 14525: ['GOOG', 'N/A', 'N/A', 'TerraBats'], 14663: ['DALY', 'FMT2', 'N/A', 'Killabytez'], 14784: ['GOOG', 'N/A', 'N/A', 'Robotic Rampage'], 14969: ['GOOG', 'FMT2', 'N/A', 'Vortex'], 15068: ['SC', 'N/A', 'N/A', 'Blood Type Zeta'], 15385: ['GOOG', 'DALY', 'N/A', 'MidKnight Mayhem'], 15453: ['N/A', 'N/A', 'N/A', 'RaiderBots'], 16026: ['FMT2', 'N/A', 'N/A', 'Alphabots'], 16177: ['FMT1', 'N/A', 'N/A', 'Acmatic'], 16194: ['N/A', 'N/A', 'N/A', 'Roses &amp; Rivets'], 16197: ['CUP', 'N/A', 'N/A', 'SWARM'], 16236: ['SC', 'N/A', 'N/A', 'Juice'], 16247: ['N/A', 'N/A', 'N/A', 'Thor Bots'], 16278: ['N/A', 'N/A', 'N/A', 'Wookie Patrol'], 16306: ['N/A', 'N/A', 'N/A', 'Incognito'], 16481: ['FMT1', 'N/A', 'N/A', 'Robo racers'], 16532: ['N/A', 'N/A', 'N/A', 'Sparkbots'], 16533: ['N/A', 'N/A', 'N/A', 'Infernobots'], 16535: ['FMT2', 'CUP', 'N/A', 'LEGIT'], 16561: ['N/A', 'N/A', 'N/A', 'Navigators'], 16594: ['FMT2', 'GB', 'N/A', 'Hyper Geek Turtles'], 16656: ['DALY', 'N/A', 'N/A', 'Thunderbots'], 16688: ['N/A', 'N/A', 'N/A', 'Wolfbotics'], 16689: ['N/A', 'N/A', 'N/A', 'Team Yantra'], 16778: ['FMT1', 'N/A', 'N/A', 'Cyber Wizards'], 16898: ['SJ2', 'N/A', 'N/A', 'Poseidon'], 16944: ['FMT2', 'N/A', 'N/A', 'FM493RS'], 17099: ['DALY', 'FMT1', 'N/A', 'NaH Robotics'], 17390: ['FMT4', 'N/A', 'N/A', 'TechnoG.O.A.Ts'], 17488: ['N/A', 'N/A', 'N/A', 'Firebotics'], 17571: ['DROPPED', 'N/A', 'N/A', 'Quantum Leapers'], 17759: ['FMT2', 'N/A', 'N/A', 'Mind'], 18023: ['N/A', 'N/A', 'N/A', 'South Tahoe Vikings Robotics'], 18096: ['GOOG', 'N/A', 'N/A', 'PizzaBots1'], 18133: ['FMT2', 'N/A', 'N/A', 'CyberCats'], 18134: ['GB', 'N/A', 'N/A', 'Arkatron'], 18143: ['N/A', 'N/A', 'N/A', 'Brainy Probotics'], 18203: ['N/A', 'N/A', 'N/A', 'MCII'], 18219: ['GB', 'N/A', 'N/A', 'Primitive Data'], 18223: ['N/A', 'N/A', 'N/A', 'EmberBots'], 18233: ['FMT1', 'N/A', 'N/A', 'M.E.R.C.Y.B.'], 18247: ['DALY', 'N/A', 'N/A', 'Gilded Gears'], 18254: ['GOOG', 'FMT1', 'N/A', 'The Inzain Bots'], 18271: ['N/A', 'N/A', 'N/A', 'BPC Robotics'], 18272: ['DALY', 'CUP', 'N/A', 'Sigma'], 18307: ['FMT2', 'FMT4', 'N/A', 'Robo Stars'], 18309: ['FMT2', 'N/A', 'N/A', 'Dream Machines'], 18311: ['FMT4', 'SC', 'N/A', 'Icon Maniacs'], 18320: ['N/A', 'N/A', 'N/A', 'Plus Ultra 3'], 18321: ['N/A', 'N/A', 'N/A', 'Plus Ultra'], 18322: ['N/A', 'N/A', 'N/A', 'Plus Ultra 5'], 18323: ['N/A', 'N/A', 'N/A', 'Plus Ultra 4'], 18324: ['N/A', 'N/A', 'N/A', 'Plus Ultra 2'], 18325: ['N/A', 'N/A', 'N/A', 'Plus Ultra 6'], 18326: ['N/A', 'N/A', 'N/A', 'Tech-DREAMS FTC'], 18337: ['N/A', 'N/A', 'N/A', 'Artisans'], 18340: ['GB', 'N/A', 'N/A', 'Polaris Robotics'], 18343: ['N/A', 'N/A', 'N/A', 'Chartwell FTC 3'], 18344: ['N/A', 'N/A', 'N/A', 'Chartwell FTC 2'], 18345: ['N/A', 'N/A', 'N/A', 'Chartwell FTC 1'], 18346: ['FMT2', 'N/A', 'N/A', 'AA Batteries'], 18371: ['N/A', 'N/A', 'N/A', 'Wolf Pack'], 18373: ['FMT2', 'N/A', 'N/A', 'Blizzard Robotics'], 18412: ['N/A', 'N/A', 'N/A', 'OtterPups'], 18413: ['N/A', 'N/A', 'N/A', 'SealPups'], 18451: ['N/A', 'N/A', 'N/A', 'Bots of Thunder'], 18466: ['N/A', 'N/A', 'N/A', 'Mastermindz'], 18481: ['N/A', 'N/A', 'N/A', 'CAF Robotics'], 18490: ['N/A', 'N/A', 'N/A', 'Green Machine'], 18504: ['GB', 'N/A', 'N/A', 'MAGIC BOTS'], 18510: ['N/A', 'N/A', 'N/A', 'MH Plus Ultra'], 18513: ['DALY', 'N/A', 'N/A', 'Gear Toes'], 18536: ['N/A', 'N/A', 'N/A', 'Robodores FTC'], 18563: ['N/A', 'N/A', 'N/A', 'Landslide'], 18564: ['DALY', 'N/A', 'N/A', 'Techbots'], 18569: ['FMT2', 'N/A', 'N/A', 'Seal Team Schicks'], 18604: ['N/A', 'N/A', 'N/A', 'Robo R0ckstars'], 18712: ['N/A', 'N/A', 'N/A', 'Impact Robotics'], 18715: ['N/A', 'N/A', 'N/A', 'Artemis'], 18726: ['PIE', 'N/A', 'N/A', 'Ninjabots'], 18729: ['FMT2', 'N/A', 'N/A', 'TeamFirst-FTC'], 18756: ['N/A', 'N/A', 'N/A', 'FTC Horner Team 4'], 18767: ['CUP', 'N/A', 'N/A', 'The Techarinos'], 18786: ['FMT1', 'N/A', 'N/A', 'Liverbots'], 18788: ['N/A', 'N/A', 'N/A', 'ZeusTech'], 18837: ['N/A', 'N/A', 'N/A', 'Kronos'], 18897: ['N/A', 'N/A', 'N/A', 'Raider Robotics']}
comps = {'DALY': [524, 3470, 7641, 8375, 8381, 8404, 9657, 9784, 13274, 13345, 14259, 14318, 14504, 14663, 15385, 16656, 17099, 18247, 18272, 18513, 18564], 'GB': [11201, 16594, 18134, 18219, 18340, 18504], 'SC': [6949, 8381, 13180, 13218, 15068, 16236, 18311], 'SJ2': [13050, 16898], 'FMT1': [4345, 4998, 6949, 7303, 7390, 7854, 8367, 8872, 11039, 12869, 13356, 13380, 14162, 14214, 14300, 14502, 16177, 16481, 16778, 17099, 18233, 18254, 18786], 'CUP': [5206, 11575, 14504, 16197, 16535, 18272, 18767], 'GOOG': [524, 6165, 7854, 8375, 9784, 11039, 12635, 12962, 13223, 13345, 14162, 14318, 14525, 14784, 14969, 15385, 18096, 18254], 'FMT4': [4345, 6165, 9614, 9656, 13180, 13356, 14473, 17390, 18307, 18311], 'FMT2': [5773, 8404, 11201, 11475, 11575, 12962, 13217, 14341, 14663, 14969, 16026, 16535, 16594, 16944, 17759, 18133, 18307, 18309, 18346, 18373, 18569, 18729], 'PIE': [18726]}
fairplay = [524, 4345, 4950, 4998, 5773, 6038, 6165, 6949, 7083, 7128, 7303, 7390, 7610, 7641, 7854, 8300, 8367, 8375, 8381, 8404, 8872, 9614, 9656, 9784, 11039, 11201, 11311, 11466, 11467, 11575, 11689, 12635, 12869, 13180, 13217, 13218, 13345, 13356, 13380, 14300, 14318, 14341, 14473, 14504, 14525, 14663, 14969, 15385, 16026, 16072, 16177, 16236, 16306, 16309, 16532, 16533, 16535, 16594, 16944, 17759, 18183, 18190, 18219, 18223, 18254, 18272, 18309, 18373, 18430, 18466, 18513, 18564]

# Initialize Bot
VERSION = '2021.2.11.1'
loop_counter = 0
client = discord.Client()

def get_html(url):
    req = urllib.request.Request(url, headers = {'User-Agent': 'Mozilla/5.0 (' + random.choice(OS) + ') AppleWebKit/' + random.choice(WEBKIT) + ' (KHTML, like Gecko) Chrome/' + random.choice(CHROME) + ' Safari/' + random.choice(SAFARI)})
    return soup(urllib.request.urlopen(req).read(), 'html.parser').prettify()

def first_request(url):
    return requests.get('https://ftc-api.firstinspires.org/v2.0/2020/' + url, headers = API_AUTH)

def lookup_data(number):
    """
    lookup_data(number): takes in team number and outputs qualifier codes
    :param number: (int) team number
    :return: (list) qualifier codes for all three qualifiers
    """

    html_code = get_html('https://www.norcalftc.org/ftc-team-status/?ftcteam=' + str(number))
    qt = re.compile('QT #\d.*?er">\s*?(\S*?)\s*?</td>', re.DOTALL).findall(html_code)
    name = re.compile('am Name.*?">\s*?(\S.*?)\s*?</td>', re.DOTALL).findall(html_code)[0]
    return [qt[0].upper() if len(qt) >= 1 else 'N/A', qt[1].upper() if len(qt) >= 2 else 'N/A', qt[2].upper() if len(qt) == 3 else 'N/A', name]

async def update():
    """
    update(): scrapes/saves registration/fairplay data for all teams every 24 hours
    """

    await client.wait_until_ready()
    while not client.is_closed():
        global loop_counter
        global counter

        stats = discord.Embed(title = 'NorCal Bot Command Counter', description = 'This runs every two hours.')
        stats.add_field(name = 'Total', value = sum(counter.values()))
        overflowcounter = 1
        STATS_CHANNEL = client.get_guild(TEST_GUILD).get_channel(TEST_CHANNEL)
        for index in range(NUM_COMMANDS):
            stats.add_field(name = '$' + COMMANDS[index], value = counter[COMMANDS[index]])
            overflowcounter += 1
            if overflowcounter % 25 == 0 and overflowcounter != 0:
                await STATS_CHANNEL.send(content = None, embed = stats)
                stats = discord.Embed(title = 'NorCal Bot Command Counter (cont)', description = 'This runs every two hours.')
        if overflowcounter % 25 != 0 and overflowcounter != 0:
            await STATS_CHANNEL.send(content = None, embed = stats)

        if loop_counter % 12 == 0:
            html_code = get_html('https://www.norcalftc.org/norcal-ftc-team-list-new/')
            numList = re.compile('mn-1">\s*?(\S*?)\s*?</td>', re.DOTALL).findall(html_code)[:-7]

            global teams
            global comps
            global fairplay

            for team in numList:
                # print(team)
                teams[int(team)] = lookup_data(team)
                await asyncio.sleep(random.randint(4, 10))

            # print(teams)

            allQT = []
            for team in teams:
                allQT.append(teams[team][0])
                allQT.append(teams[team][1])
                allQT.append(teams[team][2])

            allQT = list(set(allQT))
            allQT.remove('N/A')
            allQT.remove('DROPPED')
            for qt in allQT:
                temp = []
                for team in teams:
                    if qt in teams[team]:
                        temp.append(team)
                comps[qt] = temp

            # print(comps)

            html_code = get_html('https://www.norcalftc.org/fair-play-team-list/')
            fairplay = sorted(list(map(lambda n: int(n), re.compile('mn-1">\s*?(\S*?)\s*?</td>', re.DOTALL).findall(html_code))))

            # print(fairplay)

        loop_counter += 1
        await asyncio.sleep(7200)

@client.event
async def on_ready():
    await client.get_guild(TEST_GUILD).get_channel(TEST_CHANNEL).send('I Just Woke Up!')

@client.event
async def on_message(message):
    """
    on_message(message): main bot code, reacts to user messages
    :param message: user message
    """

    # Save Command
    command = message.content.lower()
    member = message.author

    # Run If Bot Did Not Send Command
    if str(member) != BOT_NAME:
        global counter
        global fairplay

        STATS_CHANNEL = client.get_guild(TEST_GUILD).get_channel(TEST_CHANNEL)

        # help
        if '$' + COMMANDS[0] in command:
            counter[COMMANDS[0]] += 1
            await STATS_CHANNEL.send(command)
            help = discord.Embed(title = 'NorCal Bot Help', description = 'A list of commands for NorCal Bot')
            for index in range(len(HELP_COMMANDS)):
                help.add_field(name = HELP_COMMANDS[index], value = HELP_MESSAGES[index])
            await message.channel.send(content = None, embed = help)

        # about
        elif '$' + COMMANDS[1] in command:
            counter[COMMANDS[1]] += 1
            await STATS_CHANNEL.send(command)
            await message.channel.send('I was made by Ansh Gandhi from FTC Team 7303 RoboAvatars.\nPlease support him by downloading the RoboAvatars Ultimate Goal Scoring app here: https://tinyurl.com/UltimateGoalRA.')

        # test
        elif '$' + COMMANDS[2] in command:
            counter[COMMANDS[2]] += 1
            await STATS_CHANNEL.send(command)
            await message.channel.send('I\'m Alive!')

        # version
        elif '$' + COMMANDS[3] in command:
            counter[COMMANDS[3]] += 1
            await STATS_CHANNEL.send(command)
            await message.channel.send(VERSION)

        # moo
        elif '$' + COMMANDS[4] in command:
            counter[COMMANDS[4]] += 1
            await STATS_CHANNEL.send(command)
            await message.channel.send('https://cdn.discordapp.com/attachments/736303564388827278/771527080088961064/unknown.png')

        # monke
        elif '$' + COMMANDS[5] in command:
            counter[COMMANDS[5]] += 1
            await STATS_CHANNEL.send(command)
            await message.channel.send('https://cdn.discordapp.com/attachments/771453190222512183/771586361375326218/unknown.png')

        # laff
        elif '$' + COMMANDS[6] in command:
            counter[COMMANDS[6]] += 1
            await STATS_CHANNEL.send(command)
            await message.channel.send('I LAFF AT U')

        # joos
        elif '$' + COMMANDS[7] in command:
            counter[COMMANDS[7]] += 1
            await STATS_CHANNEL.send(command)
            await message.channel.send('JOOOOOOOOOS')

        # bts
        elif '$' + COMMANDS[8] in command:
            counter[COMMANDS[8]] += 1
            await STATS_CHANNEL.send(command)
            await message.channel.send('https://cdn.discordapp.com/attachments/225450307654647808/770722462207967272/bts.png')

        # osas
        elif '$' + COMMANDS[9] in command:
            counter[COMMANDS[9]] += 1
            await STATS_CHANNEL.send(command)
            await message.channel.send('https://cdn.discordapp.com/attachments/698281158663733311/771914826804232192/unknown.png')

        # bigshaq
        elif '$' + COMMANDS[10] in command:
            counter[COMMANDS[10]] += 1
            await STATS_CHANNEL.send(command)
            await message.channel.send('https://cdn.discordapp.com/attachments/698281158663733311/771915056459808788/unknown.png')

        # asznee
        elif '$' + COMMANDS[11] in command:
            counter[COMMANDS[11]] += 1
            await STATS_CHANNEL.send(command)
            await message.channel.send('https://cdn.discordapp.com/attachments/698281158663733311/771915212684001320/unknown.png')

        # frydae
        elif '$' + COMMANDS[12] in command:
            counter[COMMANDS[12]] += 1
            await STATS_CHANNEL.send(command)
            await message.channel.send('https://cdn.discordapp.com/attachments/698281158663733311/774069046735142932/unknown.png')

        # wednesdae
        elif '$' + COMMANDS[13] in command:
            counter[COMMANDS[13]] += 1
            await STATS_CHANNEL.send(command)
            await message.channel.send('https://cdn.discordapp.com/attachments/699668920335859732/780676203580882944/flat750x075f-pad750x1000f8f8f8.u2.jpg')

        # beteor
        elif '$' + COMMANDS[14] in command:
            counter[COMMANDS[14]] += 1
            await STATS_CHANNEL.send(command)
            await message.channel.send('https://media.discordapp.net/attachments/743291565631602691/753110344523841557/beteor.jpg?width=500&height=250')

        # leek
        elif '$' + COMMANDS[15] in command:
            counter[COMMANDS[15]] += 1
            await STATS_CHANNEL.send(command)
            await message.channel.send('https://cdn.discordapp.com/attachments/699668920335859732/783229118816583700/unknown.png')

        # sad
        elif '$' + COMMANDS[16] in command:
            counter[COMMANDS[16]] += 1
            await STATS_CHANNEL.send(command)
            await message.channel.send('https://tenor.com/view/sad-down-gif-5337069')

        # comrade
        elif '$' + COMMANDS[17] in command:
            counter[COMMANDS[17]] += 1
            await STATS_CHANNEL.send(command)
            await message.channel.send('https://tenor.com/view/commie-communism-commie-lizard-lizard-lizard-dancing-gif-19535820')

        # veriguds
        elif command.find('$' + COMMANDS[18]) == 0:
            counter[COMMANDS[18]] += 1
            await STATS_CHANNEL.send(command)
            lookup = command.split(' ')
            if lookup[0] != '$veriguds' or len(lookup) != 2:
                await message.channel.send('For reacting "VERIGUDS" to a message, type "$veriguds", a space, and then the message id or message link. The message must be in this channel.')
            else:
                try:
                    if len(lookup[1]) == 18:
                        number = int(lookup[1])
                    elif len(lookup[1].split('/')[-1]) == 18:
                        number = int(lookup[1].split('/')[-1])
                    else:
                        number = 0
                        await message.channel.send('For reacting "VERIGUDS" to a message, type "$veriguds", a space, and then the message id or message link. The message must be in this channel.')

                    if number != 0:
                        reactMessage = await message.channel.fetch_message(number)
                        await reactMessage.add_reaction('🇻')
                        await reactMessage.add_reaction('🇪')
                        await reactMessage.add_reaction('🇷')
                        await reactMessage.add_reaction('🇮')
                        await reactMessage.add_reaction('🇬')
                        await reactMessage.add_reaction('🇺')
                        await reactMessage.add_reaction('🇩')
                        await reactMessage.add_reaction('🇸')
                except:
                    await message.channel.send('For reacting "VERIGUDS" to a message, type "$veriguds", a space, and then the message id or message link. The message must be in this channel.')

        # setcounters
        elif command.find('$' + COMMANDS[19]) == 0 and str(member) in ADMINS:
            counters = list(map(lambda c: int(c), command.split(' ')[1:]))
            if len(counters) == NUM_COMMANDS:
                counter = {COMMANDS[index]: counters[index] for index in range(NUM_COMMANDS)}
                counter[COMMANDS[19]] += 1
                await STATS_CHANNEL.send(command)

                stats = discord.Embed(title = 'NorCal Bot Command Set Counters', description = 'Counters have been reset')
                stats.add_field(name = 'Total', value = sum(counter.values()))
                overflowcounter = 1
                for index in range(NUM_COMMANDS):
                    stats.add_field(name = '$' + COMMANDS[index], value = counter[COMMANDS[index]])
                    overflowcounter += 1
                    if overflowcounter % 25 == 0 and overflowcounter != 0:
                        await message.channel.send(content = None, embed = stats)
                        stats = discord.Embed(title = 'NorCal Bot Command Set Counters (cont)', description = 'Counters have been reset')
                if overflowcounter % 25 != 0 and overflowcounter != 0:
                    await message.channel.send(content = None, embed = stats)
            else:
                await message.channel.send('Incorrect Number of Counters. You sent ' + str(len(counters)) + ' but ' + str(NUM_COMMANDS) + ' are needed.')

        # stats
        elif command == '$' + COMMANDS[20]:
            counter[COMMANDS[20]] += 1
            await STATS_CHANNEL.send(command)
            stats = discord.Embed(title = 'NorCal Bot Command Counter', description = 'Shows the number of times each command is used')
            stats.add_field(name = 'Total', value = sum(counter.values()))
            overflowcounter = 1
            for index in range(NUM_COMMANDS):
                stats.add_field(name = '$' + COMMANDS[index], value = counter[COMMANDS[index]])
                overflowcounter += 1
                if overflowcounter % 25 == 0 and overflowcounter != 0:
                    await message.channel.send(content = None, embed = stats)
                    stats = discord.Embed(title = 'NorCal Bot Command Counter (cont)', description = 'Shows the number of times each command is used')
            if overflowcounter % 25 != 0 and overflowcounter != 0:
                await message.channel.send(content = None, embed = stats)

        # tlookup
        elif command.find('$' + COMMANDS[21]) == 0:
            counter[COMMANDS[21]] += 1
            await STATS_CHANNEL.send(command)
            lookup = command.split(' ')
            if lookup[0] != '$tlookup' or len(lookup) != 2:
                await message.channel.send('For looking up a team, type "$tlookup", a space, and then the team number.')
            else:
                try:
                    number = int(lookup[1])
                    data = teams[number]
                    info = discord.Embed(title = str(number) + ' Qualifier Registration', description = 'Qualifier Registration for ' + data[3])
                    info.add_field(name = 'QT #1', value = data[0])
                    info.add_field(name = 'QT #2', value = data[1])
                    info.add_field(name = 'QT #3', value = data[2])
                    info.add_field(name = 'Fair Play', value = 'Yes' if number in fairplay else 'No')
                    info.set_footer(text = 'This data updates every 2 hours.')
                    await message.channel.send(content = None, embed = info)
                except:
                    await message.channel.send('For looking up a team, type "$tlookup", a space, and then the team number.')

        # clookup
        elif command.find('$' + COMMANDS[22]) == 0:
            counter[COMMANDS[22]] += 1
            await STATS_CHANNEL.send(command)
            lookup = command.split(' ')
            if lookup[0] != '$clookup' or len(lookup) != 2:
                await message.channel.send('For looking up a competition, type "$clookup", a space, and then the competition ID.')
            else:
                try:
                    id = lookup[1].upper()
                    data = comps[id]
                    fairplaycount = 0
                    for team in data:
                        if team in fairplay:
                            fairplaycount += 1
                    try:
                        description = 'Teams Registered for **' + COMP_NAMES[id] + '** Qualifier on **' + COMP_DATES[id] + '**'
                    except:
                        description = 'Teams Registered for ' + id + ' Qualifier'
                    info = discord.Embed(title = id + ' Qualifier Registration', description = description)
                    info.add_field(name = '# Teams', value = str(len(data)))
                    info.add_field(name = '% Teams in Fair Play', value = str(int(fairplaycount / len(data) * 100)))
                    info.set_footer(text = 'This data updates every 2 hours. Teams in fairplay are marked with "*".')
                    overflowcounter = 2
                    for team in data:
                        try:
                            info.add_field(name = str(team) + ('*' if team in fairplay else ''), value = teams[team][3])
                            overflowcounter += 1
                        except:
                            pass
                        if overflowcounter % 25 == 0 and overflowcounter != 0:
                            await message.channel.send(content = None, embed = info)
                            info = discord.Embed(title = id + ' Qualifier Registration (cont)', description = description)
                            info.set_footer(text = 'This data updates every 2 hours. Teams in fairplay are marked with "*".')
                    if overflowcounter % 25 != 0 and overflowcounter != 0:
                        await message.channel.send(content = None, embed = info)
                except:
                    await message.channel.send('For looking up a competition, type "$clookup", a space, and then the competition ID.')

        # comps
        elif command == '$' + COMMANDS[23]:
            counter[COMMANDS[23]] += 1
            await STATS_CHANNEL.send(command)
            info = discord.Embed(title = 'Competitions', description = 'Shows Codes for NorCal Competitions')
            for comp in comps.keys():
                try:
                    info.add_field(name = comp, value = COMP_NAMES[comp] + ': ' + COMP_DATES[comp])
                except:
                    info.add_field(name = comp, value = comp)
            await message.channel.send(content = None, embed = info)

        # fairplay
        elif command == '$' + COMMANDS[24]:
            counter[COMMANDS[24]] += 1
            await STATS_CHANNEL.send(command)
            info = discord.Embed(title = 'Fair Play Teams', description = 'A list of all of the fair play teams')
            info.add_field(name = 'Number of Fair Play Teams', value = str(len(fairplay)))
            info.add_field(name = '% of Teams in Fair Play', value = str(int(len(fairplay) / len(teams) * 100)))
            overflowcounter = 2
            for index in range(len(fairplay)):
                team = fairplay[index]
                try:
                    info.add_field(name = team, value = teams[team][3])
                    overflowcounter += 1
                except:
                    pass
                if overflowcounter % 25 == 0 and overflowcounter != 0:
                    await message.channel.send(content = None, embed = info)
                    info = discord.Embed(title = 'Fair Play Teams (cont)', description = 'A list of all of the fair play teams')
            if overflowcounter % 25 != 0 and overflowcounter != 0:
                await message.channel.send(content = None, embed = info)

        # rankings
        elif command.find('$' + COMMANDS[25]) == 0:
            counter[COMMANDS[25]] += 1
            await STATS_CHANNEL.send(command)
            lookup = command.split(' ')
            if lookup[0] != '$rankings' or len(lookup) != 2:
                await message.channel.send('For looking up competition rankings, type "$rankings", a space, and then the competition ID.')
            else:
                try:
                    id = lookup[1].upper()
                    code = API_CODES.get(id)
                    info = discord.Embed(title = 'Rankings for ' + id, description = '')

                    apiInfo = first_request('rankings/' + code).json().get('Rankings')
                    if len(apiInfo) == 0:
                        await message.channel.send('FIRST API Error')
                    else:
                        for dict in apiInfo:
                            info.add_field(name = str(dict['rank']) + '. ' + str(dict['teamNumber']) + ' (' + teams[dict['teamNumber']][3] + ')', value = str(int(dict['sortOrder1'])) + ' Ranking Pts\n' + str(int(dict['sortOrder6'])) + ' Max Match Pts')
                        await message.channel.send(content = None, embed = info)
                except:
                    await message.channel.send('The competition ID is invalid or the rankings have not been published yet.')

        # awards
        elif command.find('$' + COMMANDS[26]) == 0:
            counter[COMMANDS[26]] += 1
            await STATS_CHANNEL.send(command)
            lookup = command.split(' ')
            if lookup[0] != '$awards' or len(lookup) != 2:
                await message.channel.send('For looking up competition awards, type "$awards", a space, and then the competition ID.')
            else:
                try:
                    id = lookup[1].upper()
                    code = API_CODES.get(id)
                    info = discord.Embed(title = 'Awards for ' + id, description = '')

                    apiInfo = first_request('awards/' + code).json().get('awards')
                    if len(apiInfo) == 0:
                        await message.channel.send('FIRST API Error')
                    else:
                        for dict in apiInfo:
                            info.add_field(name = dict['name'], value = str(dict['teamNumber']) + ' (' + teams[dict['teamNumber']][3] + ')')

                        await message.channel.send(content = None, embed = info)
                except:
                    await message.channel.send('The competition ID is invalid or the awards have not been published yet.')

        # scores
        elif command.find('$' + COMMANDS[27]) == 0:
            counter[COMMANDS[27]] += 1
            await STATS_CHANNEL.send(command)
            lookup = command.split(' ')
            if lookup[0] != '$scores' or len(lookup) != 3:
                await message.channel.send('For looking up a team\'s scores, type "$scores", a space, the competition ID, a space, and the team number.')
            else:
                try:
                    id = lookup[1].upper()
                    team = lookup[2]
                    code = API_CODES.get(id)
                    info = discord.Embed(title = id + ' Scores for ' + teams[int(team)][3], description = '_Use $dscores for detailed score breakdown_')

                    apiInfo = first_request('scores/' + code + '/qual?teamnumber=' + team).json().get('MatchScores')
                    if len(apiInfo) == 0:
                        await message.channel.send('FIRST API Error')
                    else:
                        for dict in apiInfo:
                            data = dict.get('scores')
                            penalty = ' (penalties -' + str(data['penaltyPoints']) + ')' if data['penaltyPoints'] > 0 else ''
                            info.add_field(name = 'Match ' + str(dict['matchNumber']), value = 'Total: ' + str(data['totalPoints']) + ' pts\nAuto: ' + str(data['autoPoints']) + ' pts\nTeleOp: ' + str(data['dcPoints'] + data['endgamePoints']) + ' points\n' + penalty)

                        await message.channel.send(content = None, embed = info)
                except:
                    await message.channel.send('The competition ID or team number is invalid or the scores have not been published yet.')

        # dscores
        elif command.find('$' + COMMANDS[28]) == 0:
            counter[COMMANDS[28]] += 1
            await STATS_CHANNEL.send(command)
            lookup = command.split(' ')
            if lookup[0] != '$dscores' or len(lookup) != 3:
                await message.channel.send('For looking up a team\'s detailed scores, type "$dscores", a space, the competition ID, a space, and the team number.')
            else:
                try:
                    id = lookup[1].upper()
                    team = lookup[2]
                    code = API_CODES.get(id)

                    info = discord.Embed(title = id + ' Scores for ' + teams[int(team)][3], description = '')

                    apiInfo = first_request('scores/' + code + '/qual?teamnumber=' + team).json().get('MatchScores')
                    if len(apiInfo) == 0:
                        await message.channel.send('FIRST API Error')
                    else:
                        count = 0
                        for dict in apiInfo:
                            data = dict.get('scores')
                            penalty = ' (penalties -' + str(data['penaltyPoints']) + ')' if data['penaltyPoints'] > 0 else ''
                            info.add_field(name = 'Match ' + str(dict['matchNumber']), value = 'Total: ' + str(data['totalPoints']) + ' pts' + penalty + '\nAuto: ' + str(data['autoPoints']) + ' pts\nTeleOp: ' + str(data['dcPoints'] + data['endgamePoints']) + ' pts', inline = False)

                            info.add_field(name = 'Auto Rings', value = 'High: ' + str(data['autoTowerHigh']) + '\nMid: ' + str(data['autoTowerMid']) + '\nLow: ' + str(data['autoTowerLow']))
                            info.add_field(name = 'Auto Powershots', value = str(data['autoPowerShotPoints'] // 15))
                            park = 'Yes' if data['navigated1'] else 'No'
                            info.add_field(name = 'Auto Wobble/Park', value = 'Delivered: ' + str(data['autoWobblePoints'] // 15) + '\nParked: ' + park)

                            info.add_field(name = 'TeleOp Rings', value = 'High: ' + str(data['dcTowerHigh']) + '\nMid: ' + str(data['dcTowerMid']) + '\nLow: ' + str(data['dcTowerLow']))
                            info.add_field(name = 'TeleOp Powershots', value = str(data['endPowerShotPoints'] // 15))
                            wobble = ['', '']
                            wobble[0] = 'Drop Zone' if data['wobbleEnd1'] == 2 else ('Start Line' if data['wobbleEnd1'] == 1 else 'N/A')
                            wobble[1] = 'Drop Zone' if data['wobbleEnd2'] == 2 else ('Start Line' if data['wobbleEnd2'] == 1 else 'N/A')
                            info.add_field(name = 'TeleOp Wobble', value = 'Delivered: ' + wobble[0] + ', ' + wobble[1] + '\nRings: ' + str(data['wobbleRingPoints'] // 5))

                            count += 1
                            if count % 2 == 0:
                                await message.channel.send(content = None, embed = info)
                                info = discord.Embed(title = id + ' Scores for ' + teams[int(team)][3] + ' (cont)', description = '')
                except:
                    await message.channel.send('The competition ID or team number is invalid or the detailed scores have not been published yet.')

# Run Bot
client.loop.create_task(update())
client.run(DISCORD_TOKEN) #TODO: Suggestions, SQL