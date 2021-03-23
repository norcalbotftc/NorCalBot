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
BOT_ID = int(os.getenv('BOT_ID'))
ADMINS = os.getenv('ADMINS').split(',')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
API_CREDENTIALS = os.getenv('API_CREDENTIALS')
TEST_GUILD = int(os.getenv('TEST_GUILD'))
TEST_CHANNEL = int(os.getenv('TEST_CHANNEL'))

# Commands
COMMANDS = ('help', 'about', 'ping', 'version', 'moo', 'monke', 'laff', 'joos', 'bts', 'osas', 'kwaza', 'bigshaq', 'asznee', 'frydae', 'wednesdae', 'beteor', 'leek', 'sad', 'comrade', 'veriguds', 'veribads', 'sus', 'setcounters', 'stats', 'tlookup', 'clookup', 'comps', 'advancement', 'qual', 'fairplay', 'rankings', 'awards', 'scores', 'dscores', 'topteams', 'highscores', 'sourcecode', 'resources', 'dm', 'special')
HELP_COMMANDS = ('$' + COMMANDS[0], '$' + COMMANDS[1], '$' + COMMANDS[2], '$' + COMMANDS[3], '$' + COMMANDS[23], '$' + COMMANDS[24] + ' [team number]', '$' + COMMANDS[25] + ' [competition id]', '$' + COMMANDS[26], '$' + COMMANDS[27], '$' + COMMANDS[28], '$' + COMMANDS[29], '$' + COMMANDS[30] + ' [competition id]', '$' + COMMANDS[31] + ' [competition id]', '$' + COMMANDS[32] + ' [competition id] [team number]', '$' + COMMANDS[33] + ' [competition id] [team number]', '$' + COMMANDS[34] + ' [region]*', '$' + COMMANDS[35] + ' [region]*', '$' + COMMANDS[36], '$' + COMMANDS[37], '$' + COMMANDS[38])
HELP_MESSAGES = ('Shows this help message', 'Shows credits', 'To make sure the bot is running', 'Shows bot version', 'Shows the counters for each command', 'Shows the competitions for the registered team', 'Shows the registered teams for the specified competition', 'Shows all of the competition codes', 'Shows the advancement order for the specified competition', 'Shows a list of all teams qualified to NorCal Regionals', 'Shows a list of all of the fair play teams', 'Shows the rankings at a competition', 'Shows the award winners at a competition', 'Shows a team\'s scores at a competition', 'Shows a detailed breakdown of a team\'s scores at a competition', 'Shows top 15 teams in specified region', 'Shows top 10 scores in specified region', 'Shows the source code for this bot', 'Shows links for FTC resources', 'Start DM with User')
NUM_COMMANDS = len(COMMANDS)

# FIRST API
API_CODES = {'SCRIM': 'USCANSAQT1', 'GOOG': 'USCANSAQT2', 'FMT4': 'USCANFRQT4', 'DALY': 'USCANDCQT1', 'FMT1': 'USCANFRQT1', 'FMT2': 'USCANFRQT2', 'SJ2': 'USCANSJQT2', 'PIE': 'USCANSAQT3', 'SC': 'USCANFRQT3', 'GB': 'USCANGBQT1', 'CUP': 'USCANCUQT1', 'SJ1': 'USCANSJCT1', 'SAC': 'USCANSAQT4', 'SANM': 'USCANSMQT1', 'Regional': 'USCANSJCT'}
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
teams = {524: ['GOOG', 'DALY', 'PIE', 'Boss Bots'], 596: ['N/A', 'N/A', 'N/A', 'SpectreBots'], 669: ['N/A', 'N/A', 'N/A', 'Milpitas Xtreme Robotics'], 3470: ['DALY', 'SAC', 'N/A', 'The Patriots'], 3873: ['N/A', 'N/A', 'N/A', 'Scotbotics'], 4345: ['FMT1', 'FMT4', 'N/A', 'Aragon Robotics'], 4475: ['SANM', 'N/A', 'N/A', 'Purple Reign'], 4950: ['SAC', 'N/A', 'N/A', 'Tino 49ers'], 4998: ['FMT1', 'N/A', 'N/A', 'SPQR - Sen?tus Populusque R?boticus'], 5206: ['CUP', 'SANM', 'N/A', 'The Knights of Ni'], 5214: ['N/A', 'N/A', 'N/A', 'QLS Tech Support'], 5773: ['FMT2', 'CUP', 'N/A', 'Ink and Metal'], 6038: ['SAC', 'N/A', 'N/A', 'Tino Techformers'], 6165: ['GOOG', 'FMT4', 'N/A', 'MSET CuttleFish'], 6949: ['FMT1', 'SC', 'N/A', 'Einstein Eagles'], 7128: ['SAC', 'N/A', 'N/A', '28 Karat'], 7303: ['FMT1', 'GB', 'N/A', 'RoboAvatars'], 7316: ['SANM', 'N/A', 'N/A', 'Iron Panthers'], 7390: ['FMT1', 'CUP', 'N/A', 'MSET JellyFish'], 7593: ['N/A', 'N/A', 'N/A', 'TigerBots'], 7610: ['SANM', 'N/A', 'N/A', 'Tino Frontier'], 7641: ['DALY', 'GB', 'N/A', 'MSET BettaFish'], 7854: ['GOOG', 'FMT1', 'N/A', 'MidKnight Madness'], 8367: ['FMT1', 'SC', 'N/A', 'ACME Robotics'], 8375: ['GOOG', 'DALY', 'N/A', 'Vulcan Robotics'], 8381: ['DALY', 'SC', 'N/A', 'M'], 8404: ['DALY', 'FMT2', 'DROPPED', 'Quixilver'], 8872: ['FMT1', 'GB', 'N/A', 'Robopocalypse'], 9578: ['SJ1', 'N/A', 'N/A', 'Purple Pi'], 9614: ['FMT4', 'SAC', 'N/A', 'Hyperion'], 9656: ['FMT4', 'N/A', 'N/A', 'Omega'], 9657: ['DROPPED', 'DALY', 'SC', 'Athena Robotics'], 9784: ['GOOG', 'DALY', 'N/A', 'Dry Ice'], 10023: ['N/A', 'N/A', 'N/A', 'GatorBots'], 10163: ['N/A', 'N/A', 'N/A', 'Axes of Revolution'], 11039: ['GOOG', 'FMT1', 'N/A', 'Innov8rz'], 11099: ['N/A', 'N/A', 'N/A', 'Tacobots'], 11201: ['FMT2', 'GB', 'N/A', 'Piedmont Pioneers'], 11311: ['GB', 'SJ1', 'N/A', 'Paragon'], 11466: ['SANM', 'N/A', 'N/A', 'Tinosaurus'], 11467: ['SANM', 'N/A', 'N/A', 'Audacious Pioneers'], 11475: ['FMT2', 'CUP', 'N/A', 'Teravoltz'], 11575: ['FMT2', 'CUP', 'N/A', 'Robust Robots'], 11689: ['PIE', 'SJ1', 'N/A', 'We Love Pi'], 12516: ['N/A', 'N/A', 'N/A', 'TBD'], 12628: ['N/A', 'N/A', 'N/A', 'Fremont Hawk'], 12635: ['GOOG', 'N/A', 'N/A', 'Kuriosity Robotics'], 12804: ['SAC', 'N/A', 'N/A', 'LED'], 12869: ['FMT1', 'PIE', 'N/A', 'Voyager 6+'], 12962: ['GOOG', 'FMT2', 'N/A', 'Zenith'], 13035: ['SC', 'N/A', 'N/A', 'Boundless Robotics'], 13050: ['PIE', 'CUP', 'N/A', 'SharkBytes'], 13180: ['FMT4', 'SC', 'N/A', 'Roverdrive'], 13217: ['FMT2', 'SANM', 'N/A', 'AstroBruins'], 13218: ['SC', 'N/A', 'N/A', 'Taro'], 13223: ['GOOG', 'SAC', 'N/A', 'Endgame'], 13274: ['DALY', 'SJ1', 'N/A', 'Longhorn Robotics'], 13345: ['GOOG', 'DALY', 'GB', 'Polaris'], 13356: ['FMT4', 'FMT1', 'N/A', 'RoboForce'], 13380: ['FMT1', 'SANM', 'N/A', 'Quantum Stinger'], 14078: ['SANM', 'SJ1', 'N/A', 'Mechanical Lemons'], 14162: ['GOOG', 'FMT1', 'N/A', 'Bots&amp;Bytes'], 14214: ['FMT1', 'PIE', 'N/A', 'NvyUs'], 14259: ['DALY', 'SAC', 'N/A', 'TURB? V8'], 14298: ['SAC', 'N/A', 'N/A', 'Lincoln Robotics'], 14300: ['FMT1', 'SC', 'N/A', 'Animatronics'], 14318: ['GOOG', 'PIE', 'N/A', 'BioBots'], 14341: ['DROPPED', 'FMT2', 'N/A', 'Hypercube Robotics'], 14473: ['FMT4', 'SAC', 'N/A', 'Future'], 14502: ['FMT1', 'N/A', 'N/A', 'Chocolate Cyborgs'], 14504: ['DALY', 'CUP', 'N/A', 'SerenityNow!'], 14525: ['GOOG', 'SANM', 'N/A', 'TerraBats'], 14663: ['DALY', 'PIE', 'N/A', 'Killabytez'], 14784: ['GOOG', 'SJ1', 'N/A', 'Robotic Rampage'], 14969: ['GOOG', 'FMT2', 'N/A', 'Vortex'], 15068: ['SC', 'N/A', 'N/A', 'Blood Type Zeta'], 15385: ['GOOG', 'DALY', 'N/A', 'MidKnight Mayhem'], 15453: ['SAC', 'N/A', 'N/A', 'RaiderBots'], 16026: ['FMT2', 'GB', 'N/A', 'Alphabots'], 16177: ['FMT1', 'CUP', 'N/A', 'Acmatic'], 16194: ['SC', 'N/A', 'N/A', 'Roses &amp; Rivets'], 16197: ['CUP', 'SC', 'N/A', 'SWARM'], 16236: ['SC', 'CUP', 'N/A', 'Juice'], 16247: ['N/A', 'N/A', 'N/A', 'Thor Bots'], 16278: ['SJ1', 'N/A', 'N/A', 'Wookie Patrol'], 16306: ['GB', 'SANM', 'N/A', 'Incognito'], 16481: ['SANM', 'N/A', 'N/A', 'Robo racers'], 16532: ['N/A', 'N/A', 'N/A', 'Sparkbots'], 16533: ['N/A', 'N/A', 'N/A', 'Infernobots'], 16535: ['FMT2', 'CUP', 'N/A', 'LEGIT'], 16561: ['N/A', 'N/A', 'N/A', 'Navigators'], 16594: ['FMT2', 'SANM', 'N/A', 'Hyper Geek Turtles'], 16656: ['DALY', 'CUP', 'N/A', 'Thunderbots'], 16688: ['N/A', 'N/A', 'N/A', 'Wolfbotics'], 16689: ['N/A', 'N/A', 'N/A', 'Team Yantra'], 16778: ['FMT1', 'N/A', 'N/A', 'Cyber Wizards'], 16898: ['PIE', 'N/A', 'N/A', 'Poseidon'], 16944: ['FMT2', 'N/A', 'N/A', 'FM493RS'], 17099: ['DALY', 'FMT1', 'SC', 'NaH Robotics'], 17390: ['FMT4', 'N/A', 'N/A', 'TechnoG.O.A.Ts'], 17488: ['N/A', 'N/A', 'N/A', 'Firebotics'], 17571: ['DROPPED', 'CUP', 'N/A', 'Quantum Leapers'], 17759: ['FMT2', 'N/A', 'N/A', 'Mind'], 18023: ['N/A', 'N/A', 'N/A', 'South Tahoe Vikings Robotics'], 18096: ['GOOG', 'N/A', 'N/A', 'PizzaBots1'], 18133: ['FMT2', 'N/A', 'N/A', 'CyberCats'], 18134: ['GB', 'SJ1', 'N/A', 'Arkatron'], 18143: ['SANM', 'N/A', 'N/A', 'Brainy Probotics'], 18203: ['N/A', 'N/A', 'N/A', 'MCII'], 18219: ['GB', 'N/A', 'N/A', 'Primitive Data'], 18223: ['N/A', 'N/A', 'N/A', 'EmberBots'], 18233: ['SJ1', 'N/A', 'N/A', 'M.E.R.C.Y.B.'], 18247: ['DALY', 'N/A', 'N/A', 'Gilded Gears'], 18254: ['GOOG', 'FMT1', 'PIE', 'The Inzain Bots'], 18271: ['N/A', 'N/A', 'N/A', 'BPC RoBawks'], 18272: ['DALY', 'CUP', 'SC', 'Sigma'], 18307: ['SC', 'FMT4', 'N/A', 'Robo Stars'], 18309: ['FMT2', 'CUP', 'N/A', 'Dream Machines'], 18311: ['FMT4', 'SC', 'N/A', 'Icon Maniacs'], 18320: ['N/A', 'N/A', 'N/A', 'Plus Ultra 3'], 18321: ['N/A', 'N/A', 'N/A', 'Plus Ultra'], 18322: ['N/A', 'N/A', 'N/A', 'Plus Ultra 5'], 18323: ['N/A', 'N/A', 'N/A', 'Plus Ultra 4'], 18324: ['N/A', 'N/A', 'N/A', 'Plus Ultra 2'], 18325: ['N/A', 'N/A', 'N/A', 'Plus Ultra 6'], 18326: ['N/A', 'N/A', 'N/A', 'Tech-DREAMS FTC'], 18337: ['N/A', 'N/A', 'N/A', 'Artisans'], 18340: ['GB', 'N/A', 'N/A', 'Polaris Robotics'], 18343: ['N/A', 'N/A', 'N/A', 'Chartwell FTC 3'], 18344: ['N/A', 'N/A', 'N/A', 'Chartwell FTC 2'], 18345: ['N/A', 'N/A', 'N/A', 'Chartwell FTC 1'], 18346: ['FMT2', 'CUP', 'N/A', 'AA Batteries'], 18371: ['N/A', 'N/A', 'N/A', 'Wolf Pack'], 18373: ['SANM', 'N/A', 'N/A', 'Blizzard Robotics'], 18412: ['SJ1', 'N/A', 'N/A', 'OtterPups'], 18413: ['SJ1', 'N/A', 'N/A', 'SealPups'], 18451: ['SAC', 'N/A', 'N/A', 'Bots of Thunder'], 18466: ['N/A', 'N/A', 'N/A', 'Mastermindz'], 18481: ['N/A', 'N/A', 'N/A', 'CAF Robotics'], 18490: ['SANM', 'N/A', 'N/A', 'Green Machine'], 18504: ['GB', 'SAC', 'N/A', 'MAGIC BOTS'], 18510: ['N/A', 'N/A', 'N/A', 'MH Plus Ultra'], 18513: ['DALY', 'SAC', 'N/A', 'Gear Toes'], 18536: ['N/A', 'N/A', 'N/A', 'Robodores FTC'], 18563: ['N/A', 'N/A', 'N/A', 'Landslide'], 18564: ['DALY', 'PIE', 'FMT2', 'Techbots'], 18569: ['FMT2', 'SJ1', 'N/A', 'Seal Team Schicks'], 18604: ['N/A', 'N/A', 'N/A', 'Robo R0ckstars'], 18712: ['N/A', 'N/A', 'N/A', 'Impact Robotics'], 18715: ['GB', 'SJ1', 'N/A', 'Artemis'], 18726: ['PIE', 'SJ1', 'N/A', 'Ninjabots'], 18729: ['FMT2', 'N/A', 'N/A', 'TeamFirst-FTC'], 18756: ['SAC', 'N/A', 'N/A', 'FTC Horner Team 4'], 18767: ['SJ1', 'SAC', 'N/A', 'The Techarinos'], 18786: ['FMT1', 'GB', 'N/A', 'Liverbots'], 18788: ['N/A', 'N/A', 'N/A', 'ZeusTech'], 18837: ['N/A', 'N/A', 'N/A', 'Kronos'], 18897: ['PIE', 'N/A', 'N/A', 'Raider Robotics'], 17252: ['SJ1', 'N/A', 'N/A', 'HT7']}
comps = {'DALY': [524, 3470, 7641, 8375, 8381, 8404, 9657, 9784, 13274, 13345, 14259, 14504, 14663, 15385, 16656, 17099, 18247, 18272, 18513, 18564], 'GOOG': [524, 6165, 7854, 8375, 9784, 11039, 12635, 12962, 13223, 13345, 14162, 14318, 14525, 14784, 14969, 15385, 18096, 18254], 'SJ1': [9578, 11311, 11689, 13274, 14078, 14784, 16278, 18134, 18233, 18412, 18413, 18569, 18715, 18726, 18767, 17252], 'FMT1': [4345, 4998, 6949, 7303, 7390, 7854, 8367, 8872, 11039, 12869, 13356, 13380, 14162, 14214, 14300, 14502, 16177, 16778, 17099, 18254, 18786], 'SC': [6949, 8367, 8381, 9657, 13035, 13180, 13218, 14300, 15068, 16194, 16197, 16236, 17099, 18272, 18307, 18311], 'CUP': [5206, 5773, 7390, 11475, 11575, 13050, 14504, 16177, 16197, 16236, 16535, 16656, 17571, 18272, 18309, 18346], 'FMT2': [5773, 8404, 11201, 11475, 11575, 12962, 13217, 14341, 14969, 16026, 16535, 16594, 16944, 17759, 18133, 18309, 18346, 18564, 18569, 18729], 'PIE': [524, 11689, 12869, 13050, 14214, 14318, 14663, 16898, 18254, 18564, 18726, 18897], 'GB': [7303, 7641, 8872, 11201, 11311, 13345, 16026, 16306, 18134, 18219, 18340, 18504, 18715, 18786], 'SAC': [3470, 4950, 6038, 7128, 9614, 12804, 13223, 14259, 14298, 14473, 15453, 18451, 18504, 18513, 18756, 18767], 'SANM': [4475, 5206, 7316, 7610, 11466, 11467, 13217, 13380, 14078, 14525, 16306, 16481, 16594, 18143, 18373, 18490], 'FMT4': [4345, 6165, 9614, 9656, 13180, 13356, 14473, 17390, 18307, 18311]}
fairplay = [524, 4345, 4950, 4998, 5206, 5773, 6038, 6165, 6448, 6949, 7083, 7128, 7303, 7316, 7390, 7610, 7641, 7854, 8300, 8367, 8375, 8381, 8404, 8872, 9614, 9656, 9768, 9784, 11039, 11201, 11311, 11466, 11467, 11575, 11689, 12635, 12869, 13107, 13180, 13217, 13218, 13345, 13356, 13380, 14300, 14318, 14341, 14374, 14473, 14504, 14525, 14663, 14969, 15385, 16026, 16072, 16177, 16197, 16236, 16306, 16309, 16532, 16533, 16535, 16594, 16944, 17759, 18183, 18190, 18219, 18223, 18254, 18272, 18309, 18340, 18373, 18466, 18513, 18564]
advancement = {'GOOG': [14525, 12635, 6165, 8375, '', 11039, 11039, 9784, 13223, 18254, 9784, 13345, 12635, 18254, 8375, 14318, '', 14162, '', 7854], 'FMT4': [6165, 13356, 9656, 13180, 4345, 14473, 9656, 17390, 14473, 18311, 13356, 9614, 4345, 9614, 18307, '', 6165, '', 13180, ''], 'DALY': [8375, 9784, 8381, 8404, 8404, 13345, 8381, 14504, 8404, 14259, 7641, 17099, 9784, 18272, 14259, 18564, 13345, 14663, 9657, 18513], 'FMT1': [11039, 7303, 14300, 13356, 7390, 18254, 14300, 4345, 7854, 14162, 7390, 13380, 7303, 13380, 13356, 12869, 8872, 17099, 8367, 16778], 'FMT2': [14341, 17759, 13217, 5773, 8404, 16535, 11475, 11201, 13217, 18346, 14969, 11575, 8404, 5773, 11575, 16944, 16944, 18564, 14341, 18729], 'PIE': [12869, 18254, 14663, 16898, 11689, 14214, 524, 14318, 14318, 18564, 11689, 18726, 14214, 16898, 14663, '', 13050, '', 13050, ''], 'SC': [], 'GB': [], 'CUP': [], 'SJ1': [], 'SAC': [], 'SANM': []}
qualified = {'GOOG': [14525, 12635, 6165], 'FMT4': [13356], 'DALY': [8375, 9784, 8381], 'FMT1': [11039, 7303, 14300, 7390], 'FMT2': [14341, 17759, 13217], 'PIE': [12869, 18254], 'SC': [], 'GB': [], 'CUP': [], 'SJ1': [], 'SAC': [], 'SANM': []}
slots = ['Inspire, 1st', 'Next Rank', 'Inspire, 2nd', 'Next Rank', 'Inspire, 3rd', 'Next Rank', 'Think, 1st', 'Next Rank', 'Connect, 1st', 'Next Rank', 'Innovate, 1st', 'Next Rank', 'Control, 1st', 'Motivate, 1st', 'Design, 1st', 'Next Rank', 'Think, 2nd', 'Next Rank', 'Connect, 2nd', 'Next Rank']
qual = [6165, 7303, 7390, 8375, 8381, 9784, 11039, 12635, 12869, 13217, 13356, 14300, 14341, 14525, 17759, 18254]

# Initialize Bot
VERSION = '2021.3.23.5'
loop_counter = 0
client = discord.Client()

def get_html(url):
    req = urllib.request.Request(url, headers = {'User-Agent': 'Mozilla/5.0 (' + random.choice(OS) + ') AppleWebKit/' + random.choice(WEBKIT) + ' (KHTML, like Gecko) Chrome/' + random.choice(CHROME) + ' Safari/' + random.choice(SAFARI)})
    return soup(urllib.request.urlopen(req).read(), 'html.parser').prettify()

def get_raw_html(url):
    return requests.get(url, headers = {'User-Agent': 'Mozilla/5.0 (' + random.choice(OS) + ') AppleWebKit/' + random.choice(WEBKIT) + ' (KHTML, like Gecko) Chrome/' + random.choice(CHROME) + ' Safari/' + random.choice(SAFARI)}).text

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

        if loop_counter % 3 == 0:
            html_code = get_html('https://www.norcalftc.org/norcal-ftc-team-list-new/')
            numList = re.compile('mn-1">\s*?(\S*?)\s*?</td>', re.DOTALL).findall(html_code)

            global teams
            global comps
            global fairplay
            global advancement
            global qualified
            global slots
            global qual

            for team in numList:
                if int(team) <= 50000:
                    # print(team)
                    teams[int(team)] = lookup_data(team)
                    await asyncio.sleep(random.randint(3, 8))

            # print(teams)

            allQT = []
            for team in teams:
                allQT.append(teams[team][0])
                allQT.append(teams[team][1])
                allQT.append(teams[team][2])

            allQT = list(set(allQT))
            allQT.remove('N/A')
            allQT.remove('DROPPED')
            comps = {}
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

            html_code = get_raw_html('https://www.norcalftc.org/2020-advancement-summary/')
            headers = re.compile('th class=\"c.*?>(.*?)</th', re.DOTALL).findall(html_code)
            while '&nbsp;' in headers:
                headers.remove('&nbsp;')
            headers.pop(0)
            num_comps = len(headers)

            advancement = {}
            qualified = {}
            for comp in headers:
                advancement[comp] = []
                qualified[comp] = []

            data = re.compile('td class=\"c.*?>(.*?)</td', re.DOTALL).findall(html_code)
            while data[0].find('I') == -1:
                data.pop(0)
            num_rows = 20
            num_cols = len(data) // num_rows

            slots = []
            qual = []
            for i in range(num_rows):
                slots.append(' '.join([word[0].capitalize() + word[1:] for word in data[num_cols * i].split(' ')]))
                row = data[num_cols * i + 2: num_cols * i + num_comps + 2]

                for j in range(num_comps):
                    team = row[j]
                    key = list(advancement.keys())[j]
                    if team[:1] == '<':
                        if team[2] == 't':
                            team = int(re.compile('\D*(\d*)\D*', re.DOTALL).findall(team)[0])
                            qualified[key].append(team)
                            qual.append(team)
                        else:
                            team = int(re.compile('\D*(\d*)\D*', re.DOTALL).findall(team)[0])
                        advancement[key].append(team)
                    else:
                        advancement[key].append(int(team) if team != '' else '')

                    if advancement[key].count('') == num_rows:
                        advancement[key] = []

            qual.sort()

            # print(advancement)
            # print(qualified)
            # print(slots)
            # print(qual)

            requests.patch("https://dynamic.jackcrane.rocks/api/ftcstats/fetch.php")

        loop_counter += 1
        await asyncio.sleep(7200)

async def log(command, text, guild):
    counter[COMMANDS[command]] += 1
    await client.get_guild(TEST_GUILD).get_channel(TEST_CHANNEL).send('(' + guild + ') ' + text)

@client.event
async def on_ready():
    await client.get_guild(TEST_GUILD).get_channel(TEST_CHANNEL).send('I Just Woke Up!')
    await client.change_presence(activity = discord.Game(name = '$help | ' + str(len(client.guilds)) + ' guilds'))

@client.event
async def on_message_edit(before, after):
    await on_message(after)

@client.event
async def on_message(message):
    """
    on_message(message): main bot code, reacts to user messages
    :param message: user message
    """

    # Save Command
    command = message.content.lower()
    author = message.author
    guild = message.guild.name if message.guild is not None else (author.mention if author in ADMINS else author.name)

    # Run If Bot Did Not Send Command
    if str(author) != BOT_NAME:
        global counter
        global fairplay

        # help
        if '$' + COMMANDS[0] in command:
            await log(0, command, guild)
            help = discord.Embed(title = 'NorCal Bot Help', description = 'A list of commands for NorCal Bot')
            for index in range(len(HELP_COMMANDS)):
                help.add_field(name = HELP_COMMANDS[index], value = HELP_MESSAGES[index])
            help.set_footer(text = '* optional field')
            await message.channel.send(content = None, embed = help)

        # about
        elif '$' + COMMANDS[1] in command:
            await log(1, command, guild)
            await message.channel.send('I was made by Ansh Gandhi and Jonathan Ma from FTC Team 7303 RoboAvatars.\nHere is my source code: https://github.com/norcalbotftc/NorCalBot.\nPlease support them by downloading the RoboAvatars Ultimate Goal Scoring app here: https://tinyurl.com/UltimateGoalRA.')

        # ping
        elif '$' + COMMANDS[2] in command:
            await log(2, command, guild)
            pong = await message.channel.send('Pong!')
            time = (pong.created_at - message.created_at).total_seconds()
            await pong.edit(content = 'Pong! Responded in ' + str(int(time * 1000)) + ' ms.')

        # version
        elif '$' + COMMANDS[3] in command:
            await log(3, command, guild)
            await message.channel.send(VERSION)

        # moo
        elif '$' + COMMANDS[4] in command:
            await log(4, command, guild)
            await message.channel.send('https://cdn.discordapp.com/attachments/736303564388827278/771527080088961064/unknown.png')

        # monke
        elif '$' + COMMANDS[5] in command:
            await log(5, command, guild)
            await message.channel.send('https://cdn.discordapp.com/attachments/771453190222512183/771586361375326218/unknown.png')

        # laff
        elif command.find('$' + COMMANDS[6]) == 0:
            await log(6, command, guild)
            name = command.upper().split(' ')[1:]
            if len(name) == 0:
                await message.channel.send('I LAFF U')
            else:
                name = ' '.join(name)
                if str(BOT_ID) in name or 'NORCAL' in name or 'BOT' in name:
                    await message.channel.send('Y U LAFF ME?? I LAFF U ' + author.mention)
                else:
                    await message.channel.send('I LAFF AT ' + name)

        # joos
        elif '$' + COMMANDS[7] in command:
            await log(7, command, guild)
            await message.channel.send('JOOOOOOOOOS')

        # bts
        elif '$' + COMMANDS[8] in command:
            await log(8, command, guild)
            await message.channel.send('https://cdn.discordapp.com/attachments/225450307654647808/770722462207967272/bts.png')

        # osas
        elif '$' + COMMANDS[9] in command:
            await log(9, command, guild)
            await message.channel.send('https://cdn.discordapp.com/attachments/698281158663733311/771914826804232192/unknown.png')

        # kwaza
        elif '$' + COMMANDS[10] in command:
            await log(10, command, guild)
            await message.channel.send('https://cdn.discordapp.com/attachments/699668920335859732/823976109959676004/unknown.png')

        # bigshaq
        elif '$' + COMMANDS[11] in command:
            await log(11, command, guild)
            await message.channel.send('https://cdn.discordapp.com/attachments/698281158663733311/771915056459808788/unknown.png')

        # asznee
        elif '$' + COMMANDS[12] in command:
            await log(12, command, guild)
            await message.channel.send('https://cdn.discordapp.com/attachments/698281158663733311/771915212684001320/unknown.png')

        # frydae
        elif '$' + COMMANDS[13] in command:
            await log(13, command, guild)
            await message.channel.send('https://cdn.discordapp.com/attachments/698281158663733311/774069046735142932/unknown.png')

        # wednesdae
        elif '$' + COMMANDS[14] in command:
            await log(14, command, guild)
            await message.channel.send('https://cdn.discordapp.com/attachments/699668920335859732/780676203580882944/flat750x075f-pad750x1000f8f8f8.u2.jpg')

        # beteor
        elif '$' + COMMANDS[15] in command:
            await log(15, command, guild)
            await message.channel.send('https://media.discordapp.net/attachments/743291565631602691/753110344523841557/beteor.jpg?width=500&height=250')

        # leek
        elif '$' + COMMANDS[16] in command:
            await log(16, command, guild)
            await message.channel.send('https://cdn.discordapp.com/attachments/699668920335859732/783229118816583700/unknown.png')

        # sad
        elif '$' + COMMANDS[17] in command:
            await log(17, command, guild)
            await message.channel.send('https://tenor.com/view/sad-down-gif-5337069')

        # comrade
        elif '$' + COMMANDS[18] in command:
            await log(18, command, guild)
            await message.channel.send('https://tenor.com/view/commie-communism-commie-lizard-lizard-lizard-dancing-gif-19535820')

        # veriguds
        elif command.find('$' + COMMANDS[19]) == 0:
            await log(19, command, guild)
            lookup = command.split(' ')
            if lookup[0] != '$' + COMMANDS[19] or len(lookup) != 2:
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

        # veribads
        elif command.find('$' + COMMANDS[20]) == 0:
            await log(20, command, guild)
            lookup = command.split(' ')
            if lookup[0] != '$' + COMMANDS[20] or len(lookup) != 2:
                await message.channel.send(
                    'For reacting "VERIBADS" to a message, type "$veribads", a space, and then the message id or message link. The message must be in this channel.')
            else:
                try:
                    if len(lookup[1]) == 18:
                        number = int(lookup[1])
                    elif len(lookup[1].split('/')[-1]) == 18:
                        number = int(lookup[1].split('/')[-1])
                    else:
                        number = 0
                        await message.channel.send('For reacting "VERIBADS" to a message, type "$veribads", a space, and then the message id or message link. The message must be in this channel.')

                    if number != 0:
                        reactMessage = await message.channel.fetch_message(number)
                        await reactMessage.add_reaction('🇻')
                        await reactMessage.add_reaction('🇪')
                        await reactMessage.add_reaction('🇷')
                        await reactMessage.add_reaction('🇮')
                        await reactMessage.add_reaction('🇧')
                        await reactMessage.add_reaction('🇦')
                        await reactMessage.add_reaction('🇩')
                        await reactMessage.add_reaction('🇸')
                except:
                    await message.channel.send('For reacting "VERIBADS" to a message, type "$veribads", a space, and then the message id or message link. The message must be in this channel.')

        # sus
        elif '$' + COMMANDS[21] in command:
            await log(21, command, guild)
            await message.channel.send('https://cdn.discordapp.com/attachments/761658481328914482/817475965126180945/amogus.mp4')

        # setcounters
        elif command.find('$' + COMMANDS[22]) == 0 and str(author) in ADMINS:
            counters = list(map(lambda c: int(c), command.split(' ')[1:]))
            if len(counters) == NUM_COMMANDS:
                counter = {COMMANDS[index]: counters[index] for index in range(NUM_COMMANDS)}
                await log(22, command, guild)
                counter[COMMANDS[22]] = 0

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
        elif command == '$' + COMMANDS[23]:
            await log(23, command, guild)
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
        elif command.find('$' + COMMANDS[24]) == 0:
            await log(24, command, guild)
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
                    info.set_footer(text = 'Source: https://www.norcalftc.org/ftc-team-status/?ftcteam=' + str(number))
                    await message.channel.send(content = None, embed = info)
                except:
                    await message.channel.send('For looking up a team, type "$tlookup", a space, and then the team number.')

        # clookup
        elif command.find('$' + COMMANDS[25]) == 0:
            await log(25, command, guild)
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
                    info.set_footer(text = 'This data updates every 6 hours. Teams in fairplay are marked with "*".')
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
                            info.set_footer(text = 'This data updates every 6 hours. Teams in fairplay are marked with "*".')
                    if overflowcounter % 25 != 0 and overflowcounter != 0:
                        await message.channel.send(content = None, embed = info)
                except:
                    await message.channel.send('For looking up a competition, type "$clookup", a space, and then the competition ID.')

        # comps
        elif command == '$' + COMMANDS[26]:
            await log(26, command, guild)
            info = discord.Embed(title = 'Competitions', description = 'Shows Codes for NorCal Competitions')
            for comp in comps.keys():
                try:
                    info.add_field(name = comp, value = COMP_NAMES[comp] + ': ' + COMP_DATES[comp])
                except:
                    info.add_field(name = comp, value = comp)
            await message.channel.send(content = None, embed = info)

        # advancement
        elif command.find('$' + COMMANDS[27]) == 0:
            await log(27, command, guild)
            lookup = command.split(' ')
            if lookup[0] != '$advancement' or len(lookup) != 2:
                await message.channel.send('To look up a qualifier\'s advancing team order, type "$advancement", a space, and then the competition ID.')
            else:
                id = lookup[1].upper()
                if id not in advancement or len(advancement[id]) == 0:
                    await message.channel.send('The competition ID is invalid or the advancement data has not been published yet.')
                else:
                    info = discord.Embed(title = id + ' Qualifier Advancement', description = 'The teams that have advanced to NorCal Regionals are marked with a "*". Use $qual to see all of the qualifying teams.')
                    info.set_footer(text = 'Source: https://www.norcalftc.org/2020-advancement-summary/')

                    slot = 0
                    for team in advancement[id]:
                        if team != '':
                            info.add_field(name = str(slot + 1) + ') ' + slots[slot] + ('*' if team in qualified[id] else ''), value = str(team) + ' (' + teams[team][3] + ')')
                            slot += 1

                    await message.channel.send(content = None, embed = info)

        # qual
        elif command == '$' + COMMANDS[28]:
            await log(28, command, guild)
            info = discord.Embed(title = 'NorCal Regionals Qualifying Teams', description = 'This is a list of all of NorCal teams that have qualified for regionals. Teams in fairplay are marked with "*".')
            info.add_field(name = 'Number of Teams', value = str(len(qual)))

            fairplaycount = 0
            for team in qual:
                if team in fairplay:
                    fairplaycount += 1
            info.add_field(name = '% of Teams in Fair Play', value = str(int(fairplaycount / len(qual) * 100)))
            info.set_footer(text = 'Source: https://www.norcalftc.org/2020-advancement-summary/')
            overflowcounter = 2
            for index in range(len(qual)):
                team = qual[index]
                try:
                    info.add_field(name = str(team) + ('*' if team in fairplay else ''), value = teams[team][3])
                    overflowcounter += 1
                except:
                    pass
                if overflowcounter % 25 == 0 and overflowcounter != 0:
                    await message.channel.send(content = None, embed = info)
                    info = discord.Embed(title = 'NorCal Regionals Qualifying Teams (cont)', description = 'This is a list of all of NorCal teams that have qualified for regionals. Teams in fairplay are marked with "*".')
                    info.set_footer(text = 'Source: https://www.norcalftc.org/2020-advancement-summary/')
            if overflowcounter % 25 != 0 and overflowcounter != 0:
                await message.channel.send(content = None, embed = info)

        # fairplay
        elif command == '$' + COMMANDS[29]:
            await log(29, command, guild)
            info = discord.Embed(title = 'Fair Play Teams', description = 'A list of all of the fair play teams')
            info.add_field(name = 'Number of Fair Play Teams', value = str(len(fairplay)))
            info.add_field(name = '% of Teams in Fair Play', value = str(int(len(fairplay) / len(teams) * 100)))
            info.set_footer(text = 'Source: https://www.norcalftc.org/fair-play-team-list/')
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
                    info.set_footer(text = 'Source: https://www.norcalftc.org/fair-play-team-list/')
            if overflowcounter % 25 != 0 and overflowcounter != 0:
                await message.channel.send(content = None, embed = info)

        # rankings
        elif command.find('$' + COMMANDS[30]) == 0:
            await log(30, command, guild)
            lookup = command.split(' ')
            if lookup[0] != '$rankings' or len(lookup) != 2:
                await message.channel.send('For looking up competition rankings, type "$rankings", a space, and then the competition ID.')
            else:
                try:
                    id = lookup[1].upper()
                    code = API_CODES.get(id)
                    info = discord.Embed(title = 'Rankings for ' + id)
                    info.set_footer(text = 'Data from FIRST API: https://ftc-events.firstinspires.org/services/API')

                    apiInfo = first_request('rankings/' + code).json().get('Rankings')
                    if len(apiInfo) == 0:
                        await message.channel.send('FIRST API Error')
                    else:
                        for data in apiInfo:
                            info.add_field(name = str(data['rank']) + '. ' + str(data['teamNumber']) + ' (' + teams[data['teamNumber']][3] + ')', value = str(int(data['sortOrder1'])) + ' Ranking Pts\n' + str(int(data['sortOrder6'])) + ' Max Match Pts')
                        await message.channel.send(content = None, embed = info)
                except:
                    await message.channel.send('The competition ID is invalid or the rankings have not been published yet.')

        # awards
        elif command.find('$' + COMMANDS[31]) == 0:
            await log(31, command, guild)
            lookup = command.split(' ')
            if lookup[0] != '$awards' or len(lookup) != 2:
                await message.channel.send('For looking up competition awards, type "$awards", a space, and then the competition ID.')
            else:
                try:
                    id = lookup[1].upper()
                    code = API_CODES.get(id)
                    info = discord.Embed(title = 'Awards for ' + id)
                    info.set_footer(text = 'Data from FIRST API: https://ftc-events.firstinspires.org/services/API')

                    apiInfo = first_request('awards/' + code).json().get('awards')
                    if len(apiInfo) == 0:
                        await message.channel.send('FIRST API Error')
                    else:
                        for data in apiInfo:
                            info.add_field(name = data['name'], value = str(data['teamNumber']) + ' (' + teams[data['teamNumber']][3] + ')')

                        await message.channel.send(content = None, embed = info)
                except:
                    await message.channel.send('The competition ID is invalid or the awards have not been published yet.')

        # scores
        elif command.find('$' + COMMANDS[32]) == 0:
            await log(32, command, guild)
            lookup = command.split(' ')
            if lookup[0] != '$scores' or len(lookup) != 3:
                await message.channel.send('For looking up a team\'s scores, type "$scores", a space, the competition ID, a space, and the team number.')
            else:
                try:
                    id = lookup[1].upper()
                    team = lookup[2]
                    code = API_CODES.get(id)
                    info = discord.Embed(title = id + ' Scores for ' + teams[int(team)][3], description = 'Use $dscores for detailed score breakdown')
                    info.set_footer(text = 'Data from FIRST API: https://ftc-events.firstinspires.org/services/API')

                    apiInfo = first_request('scores/' + code + '/qual?teamnumber=' + team).json().get('MatchScores')
                    if len(apiInfo) == 0:
                        await message.channel.send('FIRST API Error')
                    else:
                        for data in apiInfo:
                            matchData = data.get('scores')
                            penalty = ' (penalties -' + str(matchData['penaltyPoints']) + ')' if matchData['penaltyPoints'] > 0 else ''
                            info.add_field(name = 'Match ' + str(data['matchNumber']), value = 'Total: ' + str(matchData['totalPoints']) + ' pts\nAuto: ' + str(matchData['autoPoints']) + ' pts\nTeleOp: ' + str(matchData['dcPoints'] + matchData['endgamePoints']) + ' points\n' + penalty)

                        await message.channel.send(content = None, embed = info)
                except:
                    await message.channel.send('The competition ID or team number is invalid or the scores have not been published yet.')

        # dscores
        elif command.find('$' + COMMANDS[33]) == 0:
            await log(33, command, guild)
            lookup = command.split(' ')
            if lookup[0] != '$dscores' or len(lookup) != 3:
                await message.channel.send('For looking up a team\'s detailed scores, type "$dscores", a space, the competition ID, a space, and the team number.')
            else:
                try:
                    id = lookup[1].upper()
                    team = lookup[2]
                    code = API_CODES.get(id)

                    info = discord.Embed(title = id + ' Scores for ' + teams[int(team)][3])
                    info.set_footer(text = 'Data from FIRST API: https://ftc-events.firstinspires.org/services/API')

                    apiInfo = first_request('scores/' + code + '/qual?teamnumber=' + team).json().get('MatchScores')
                    if len(apiInfo) == 0:
                        await message.channel.send('FIRST API Error')
                    else:
                        count = 0
                        for data in apiInfo:
                            matchData = data.get('scores')
                            penalty = ' (penalties -' + str(matchData['penaltyPoints']) + ')' if matchData['penaltyPoints'] > 0 else ''
                            info.add_field(name = 'Match ' + str(data['matchNumber']), value = 'Total: ' + str(matchData['totalPoints']) + ' pts' + penalty + '\nAuto: ' + str(matchData['autoPoints']) + ' pts\nTeleOp: ' + str(matchData['dcPoints'] + matchData['endgamePoints']) + ' pts', inline = False)

                            info.add_field(name = 'Auto Rings', value = 'High: ' + str(matchData['autoTowerHigh']) + '\nMid: ' + str(matchData['autoTowerMid']) + '\nLow: ' + str(matchData['autoTowerLow']))
                            info.add_field(name = 'Auto Powershots', value = str(matchData['autoPowerShotPoints'] // 15))
                            park = 'Yes' if matchData['navigated1'] else 'No'
                            info.add_field(name = 'Auto Wobble/Park', value = 'Delivered: ' + str(matchData['autoWobblePoints'] // 15) + '\nParked: ' + park)

                            info.add_field(name = 'TeleOp Rings', value = 'High: ' + str(matchData['dcTowerHigh']) + '\nMid: ' + str(matchData['dcTowerMid']) + '\nLow: ' + str(matchData['dcTowerLow']))
                            info.add_field(name = 'TeleOp Powershots', value = str(matchData['endPowerShotPoints'] // 15))
                            wobble = ['', '']
                            wobble[0] = 'Drop Zone' if matchData['wobbleEnd1'] == 2 else ('Start Line' if matchData['wobbleEnd1'] == 1 else 'N/A')
                            wobble[1] = 'Drop Zone' if matchData['wobbleEnd2'] == 2 else ('Start Line' if matchData['wobbleEnd2'] == 1 else 'N/A')
                            info.add_field(name = 'TeleOp Wobble', value = 'Delivered: ' + wobble[0] + ', ' + wobble[1] + '\nRings: ' + str(matchData['wobbleRingPoints'] // 5))

                            count += 1
                            if count % 2 == 0:
                                await message.channel.send(content = None, embed = info)
                                info = discord.Embed(title = id + ' Scores for ' + teams[int(team)][3] + ' (cont)')
                                info.set_footer(text = 'Data from FIRST API: https://ftc-events.firstinspires.org/services/API')
                except:
                    await message.channel.send('The competition ID or team number is invalid or the detailed scores have not been published yet.')

        # topteams
        elif command.find('$' + COMMANDS[34]) == 0:
            await log(34, command, guild)
            lookup = command.split(' ')
            ca = False
            if len(lookup) > 1:
                if lookup[1] in ['norcal', 'cal', 'ca']:
                    ca = True
                elif lookup[1] == 'global':
                    ca = False
                else:
                    await message.channel.send('Only Global and Cal Regions Supported')
                    return

            await message.channel.send('Looking up ' + ('Cal' if ca else 'Global') + ' Top Team Data')
            info = discord.Embed(title = 'California Top 15 Ranked Teams' if ca else 'Global Top 15 Ranked Teams')
            info.set_footer(text = 'Data from FTC Stats API: https://dynamic.jackcrane.rocks/api/ftcstats/docs.php')

            response2 = None
            if ca:
                payload = {'location': 'California'}
                payload2 = {'rank': '<= 250'}
                response2 = requests.post("https://dynamic.jackcrane.rocks/api/ftcstats/fetch.php", data = payload2).json().get('data')
            else:
                payload = {'rank': '<= 50'}
            response = requests.post("https://dynamic.jackcrane.rocks/api/ftcstats/fetch.php", data = payload).json().get('data')

            names = []
            for key in response.keys():
                if len(names) < 15:
                    data = response.get(key)
                    name = data.get('teamname')
                    if names.count(name) == 0:
                        rank = '-1'
                        if ca:
                            names2 = []
                            for key2 in response2.keys():
                                name2 = response2.get(key2).get('teamname')
                                if names2.count(name2) == 0:
                                    names2.append(name2)
                                if name == name2:
                                    rank = str(len(names2))
                                    break
                            if rank == '-1':
                                rank = '250+'

                        info.add_field(name = str(len(names) + 1) + ". " + data.get('teamname'), value = 'OPR: ' + str(data.get('opr')) + '\nMax score: ' + str(data.get('max_np_score')) + (('\nGlobal Rank: ' + rank) if ca else ''))
                        names.append(name)

            await message.channel.send(content = None, embed = info)

        # highscores
        elif command.find('$' + COMMANDS[35]) == 0:
            await log(35, command, guild)
            lookup = command.split(' ')
            ca = False
            if len(lookup) > 1:
                if lookup[1] in ['norcal', 'cal', 'ca']:
                    ca = True
                elif lookup[1] == 'global':
                    ca = False
                else:
                    await message.channel.send('Only Global and Cal Regions Supported')
                    return

            await message.channel.send('Looking up ' + ('Cal' if ca else 'Global') + ' High Score Data')
            info = discord.Embed(title = 'California Top 10 Scores' if ca else 'Global Top 10 Scores', description = 'Scores/Rings ([auto]/[teleop])')
            info.set_footer(text = 'Data from FTC Stats API: https://dynamic.jackcrane.rocks/api/ftcstats/docs.php')

            region = 'index'
            if ca:
                region = 'california'

            html = get_raw_html('http://www.ftcstats.org/2021/'+ region + '.html')
            data = re.compile('<td align="right" width="4%">(.*?)</td><td align="right" width="4%">(.*?)</td><td align="right" width="4%">(.*?)</td><td align="right" width="4%">(.*?)</td><td align="right" width="4%">(.*?)'
                              '</td><td align="right" width="4%">(.*?)</td><td align="right" width="4%">(.*?)</td><td><a href=.*?>(.*?)</a></td><td></td><td></td><td>(.*?)</td>', re.DOTALL).findall(html)

            count = 1
            for score in data:
                info.add_field(name = str(count) + ') ' + score[7], value = 'Score: ' + str(score[0]) + ' (' + str(score[1]) + '/' + str(int(score[2]) + int(score[3])) + ')' + '\nRings: ' + str(score[4]) + '/' + str(score[5]))
                count += 1

            await message.channel.send(content = None, embed = info)

        # sourcecode
        elif '$' + COMMANDS[36] in command:
            await log(36, command, guild)
            await message.channel.send('https://github.com/norcalbotftc/NorCalBot')

        # resources
        elif '$' + COMMANDS[37] in command:
            await log(37, command, guild)
            resources = discord.Embed(title = 'Game Manuals')
            resources.add_field(name = 'GM0', value = '[Game Manual 0](https://gm0.org/en/stable/)')
            resources.add_field(name = 'GM1 - Traditional', value = '[Game Manual 1 - Traditional](https://www.firstinspires.org/sites/default/files/uploads/resource_library/ftc/game-manual-part-1-traditional-events.pdf)')
            resources.add_field(name = 'GM1 - Remote', value = '[Game Manual 1 - Remote](https://www.firstinspires.org/sites/default/files/uploads/resource_library/ftc/game-manual-part-1-remote-events.pdf)')
            resources.add_field(name = 'GM2 - Traditional', value = '[Game Manual 2 - Traditional](https://www.firstinspires.org/sites/default/files/uploads/resource_library/ftc/game-manual-part-2-traditional-events.pdf)')
            resources.add_field(name = 'GM2 - Remote', value = '[Game Manual 2 - Remote](https://www.firstinspires.org/sites/default/files/uploads/resource_library/ftc/game-manual-part-2-remote-events.pdf)')
            resources.add_field(name = 'UG Scorer', value = '[Ultimate Goal Scorer App](http://roboavatars.weebly.com/ultimategoalscorer.html)')
            resources.add_field(name = 'OpenOdo', value = '[OpenOdometry](https://openodometry.weebly.com/)')
            await message.channel.send(content = None, embed = resources)

        # dm
        elif '$' + COMMANDS[38] in command:
            await log(38, command, guild)
            await message.channel.send('Starting DM with ' + author.mention)
            dm = await author.create_dm()
            await dm.send('You requested a DM! Here it is!')

# Run Bot
client.loop.create_task(update())
client.run(DISCORD_TOKEN)