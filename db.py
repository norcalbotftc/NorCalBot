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

import psycopg2
from psycopg2.extras import execute_values
from util import DB_URL

connection = cursor = None
teams = comps = advancement = qualified = counters = {}
fairplay = slots = regionals = []

def open():
    global connection, cursor

    connection = psycopg2.connect(DB_URL, sslmode = 'require')
    cursor = connection.cursor()

def close():
    global connection, cursor

    connection.commit()
    cursor.close()
    connection.close()

def reset():
    global cursor

    open()

    cursor.execute('CREATE TABLE teams (id serial NOT NULL PRIMARY KEY, number SMALLINT, info TEXT [])')
    cursor.execute('CREATE TABLE comps (id serial NOT NULL PRIMARY KEY, comp TEXT, teams SMALLINT [])')
    cursor.execute('CREATE TABLE advancement (id serial NOT NULL PRIMARY KEY, comp TEXT, teams SMALLINT [])')
    cursor.execute('CREATE TABLE qualified (id serial NOT NULL PRIMARY KEY, comp TEXT, teams SMALLINT [])')
    cursor.execute('CREATE TABLE data (id serial NOT NULL PRIMARY KEY, fairplay SMALLINT [], slots TEXT [], regionals SMALLINT [])')
    cursor.execute('CREATE TABLE counters (id serial NOT NULL PRIMARY KEY, command TEXT, count SMALLINT)')

    set(False)
    set_counters(False)

    close()

def set(standalone = True):
    global cursor, teams, comps, advancement, qualified, fairplay, slots, regionals, counters

    if standalone:
        open()

    cursor.execute('TRUNCATE TABLE teams')
    cursor.execute('TRUNCATE TABLE comps')
    cursor.execute('TRUNCATE TABLE advancement')
    cursor.execute('TRUNCATE TABLE qualified')
    cursor.execute('TRUNCATE TABLE data')

    execute_values(cursor, 'INSERT INTO teams (number, info) VALUES %s', ((item[0], list(item[1])) for item in teams.items()), template = '(%s, %s)', page_size = 200)
    execute_values(cursor, 'INSERT INTO comps (comp, teams) VALUES %s', ((item[0], list(item[1])) for item in comps.items()), template = '(%s, %s)')
    execute_values(cursor, 'INSERT INTO advancement (comp, teams) VALUES %s', ((item[0], list(item[1])) for item in advancement.items()), template = '(%s, %s)')
    execute_values(cursor, 'INSERT INTO qualified (comp, teams) VALUES %s', ((item[0], list(item[1])) for item in qualified.items()), template = '(%s, %s)')
    cursor.execute('INSERT INTO data (fairplay, slots, regionals) VALUES (%s, %s, %s)', (fairplay, slots, regionals))

    if standalone:
        close()

def set_counters(standalone = True):
    global cursor

    if standalone:
        open()

    cursor.execute('TRUNCATE TABLE counters')
    execute_values(cursor, 'INSERT INTO counters (command, count) VALUES %s', ((item[0], item[1]) for item in counters.items()), template = '(%s, %s)')

    if standalone:
        close()

def get(standalone = True):
    global cursor, teams, comps, advancement, qualified, fairplay, slots, regionals, counters

    if standalone:
        open()

    cursor.execute('SELECT number, info FROM teams')
    teams = {team[0]: team[1] for team in cursor.fetchall()}

    cursor.execute('SELECT comp, teams FROM comps')
    comps = {comp[0]: comp[1] for comp in cursor.fetchall()}

    cursor.execute('SELECT comp, teams FROM advancement')
    advancement = {comp[0]: comp[1] for comp in cursor.fetchall()}

    cursor.execute('SELECT comp, teams FROM qualified')
    qualified = {comp[0]: comp[1] for comp in cursor.fetchall()}

    cursor.execute('SELECT fairplay, slots, regionals FROM data')
    fairplay, slots, regionals = cursor.fetchone()

    cursor.execute('SELECT command, count FROM counters')
    counters = {command[0]: command[1] for command in cursor.fetchall()}

    if standalone:
        close()

def backup(bot_commands):
    global cursor, teams, comps, advancement, qualified, fairplay, slots, regionals, counters

    teams = {524: ['GOOG', 'DALY', 'PIE', 'Boss Bots'], 596: ['N/A', 'N/A', 'N/A', 'SpectreBots'], 669: ['N/A', 'N/A', 'N/A', 'Milpitas Xtreme Robotics'], 3470: ['DALY', 'SAC', 'N/A', 'The Patriots'], 3873: ['N/A', 'N/A', 'N/A', 'Scotbotics'], 4345: ['FMT1', 'FMT4', 'CUP', 'Aragon Robotics'], 4475: ['SANM', 'N/A', 'N/A', 'Purple Reign'], 4950: ['SAC', 'N/A', 'N/A', 'Tino 49ers'], 4998: ['FMT1', 'N/A', 'N/A', 'SPQR - Sen?tus Populusque R?boticus'], 5206: ['CUP', 'SANM', 'N/A', 'The Knights of Ni'], 5214: ['N/A', 'N/A', 'N/A', 'QLS Tech Support'], 5773: ['FMT2', 'CUP', 'N/A', 'Ink and Metal'], 6038: ['SAC', 'N/A', 'N/A', 'Tino Techformers'], 6165: ['GOOG', 'FMT4', 'N/A', 'MSET CuttleFish'], 6949: ['FMT1', 'SC', 'N/A', 'Einstein Eagles'], 7128: ['SAC', 'N/A', 'N/A', '28 Karat'], 7303: ['FMT1', 'GB', 'N/A', 'RoboAvatars'], 7316: ['SANM', 'N/A', 'N/A', 'Iron Panthers'], 7390: ['FMT1', 'CUP', 'N/A', 'MSET JellyFish'], 7593: ['N/A', 'N/A', 'N/A', 'TigerBots'], 7610: ['SANM', 'N/A', 'N/A', 'Tino Frontier'], 7641: ['DALY', 'GB', 'N/A', 'MSET BettaFish'], 7854: ['GOOG', 'FMT1', 'N/A', 'MidKnight Madness'], 8367: ['FMT1', 'SC', 'CUP', 'ACME Robotics'], 8375: ['GOOG', 'DALY', 'N/A', 'Vulcan Robotics'], 8381: ['DALY', 'SC', 'N/A', 'M'], 8404: ['DALY', 'FMT2', 'DROPPED', 'Quixilver'], 8872: ['FMT1', 'GB', 'N/A', 'Robopocalypse'], 9578: ['SJ1', 'N/A', 'N/A', 'Purple Pi'], 9614: ['FMT4', 'SAC', 'N/A', 'Hyperion'], 9656: ['FMT4', 'N/A', 'N/A', 'Omega'], 9657: ['DROPPED', 'DALY', 'SC', 'Athena Robotics'], 9784: ['GOOG', 'DALY', 'N/A', 'Dry Ice'], 10023: ['N/A', 'N/A', 'N/A', 'GatorBots'], 10163: ['N/A', 'N/A', 'N/A', 'Axes of Revolution'], 11039: ['GOOG', 'FMT1', 'N/A', 'Innov8rz'], 11099: ['N/A', 'N/A', 'N/A', 'Tacobots'], 11201: ['FMT2', 'GB', 'N/A', 'Piedmont Pioneers'], 11311: ['GB', 'SJ1', 'N/A', 'Paragon'], 11466: ['SANM', 'N/A', 'N/A', 'Tinosaurus'], 11467: ['SANM', 'N/A', 'N/A', 'Audacious Pioneers'], 11475: ['FMT2', 'CUP', 'N/A', 'Teravoltz'], 11575: ['FMT2', 'CUP', 'N/A', 'Robust Robots'], 11689: ['PIE', 'SJ1', 'CUP', 'We Love Pi'], 12516: ['N/A', 'N/A', 'N/A', 'TBD'], 12628: ['N/A', 'N/A', 'N/A', 'Fremont Hawk'], 12635: ['GOOG', 'N/A', 'N/A', 'Kuriosity Robotics'], 12804: ['SAC', 'N/A', 'N/A', 'LED'], 12869: ['FMT1', 'PIE', 'N/A', 'Voyager 6+'], 12962: ['GOOG', 'FMT2', 'N/A', 'Zenith'], 13035: ['SC', 'N/A', 'N/A', 'Boundless Robotics'], 13050: ['PIE', 'CUP', 'N/A', 'SharkBytes'], 13180: ['FMT4', 'SC', 'N/A', 'Roverdrive'], 13217: ['FMT2', 'SANM', 'N/A', 'AstroBruins'], 13218: ['SC', 'N/A', 'N/A', 'Taro'], 13223: ['GOOG', 'SAC', 'N/A', 'Endgame'], 13274: ['DALY', 'SJ1', 'N/A', 'Longhorn Robotics'], 13345: ['GOOG', 'DALY', 'GB', 'Polaris'], 13356: ['FMT4', 'FMT1', 'N/A', 'RoboForce'], 13380: ['FMT1', 'SANM', 'N/A', 'Quantum Stinger'], 14078: ['SANM', 'SJ1', 'N/A', 'Mechanical Lemons'], 14162: ['GOOG', 'FMT1', 'N/A', 'Bots&amp;Bytes'], 14214: ['FMT1', 'PIE', 'CUP', 'NvyUs'], 14259: ['DALY', 'SAC', 'N/A', 'TURB? V8'], 14298: ['SAC', 'N/A', 'N/A', 'Lincoln Robotics'], 14300: ['FMT1', 'SC', 'N/A', 'Animatronics'], 14318: ['GOOG', 'PIE', 'N/A', 'BioBots'], 14341: ['DROPPED', 'FMT2', 'N/A', 'Hypercube Robotics'], 14473: ['FMT4', 'SAC', 'N/A', 'Future'], 14502: ['FMT1', 'N/A', 'N/A', 'Chocolate Cyborgs'], 14504: ['DALY', 'CUP', 'N/A', 'SerenityNow!'], 14525: ['GOOG', 'SANM', 'N/A', 'TerraBats'], 14663: ['DALY', 'PIE', 'N/A', 'Killabytez'], 14784: ['GOOG', 'SJ1', 'N/A', 'Robotic Rampage'], 14969: ['GOOG', 'FMT2', 'N/A', 'Vortex'], 15068: ['SC', 'N/A', 'N/A', 'Blood Type Zeta'], 15385: ['GOOG', 'DALY', 'N/A', 'MidKnight Mayhem'], 15453: ['SAC', 'N/A', 'N/A', 'RaiderBots'], 16026: ['FMT2', 'GB', 'N/A', 'Alphabots'], 16177: ['FMT1', 'CUP', 'N/A', 'Acmatic'], 16194: ['SC', 'N/A', 'N/A', 'Roses &amp; Rivets'], 16197: ['CUP', 'SC', 'N/A', 'SWARM'], 16236: ['SC', 'CUP', 'N/A', 'Juice'], 16247: ['N/A', 'N/A', 'N/A', 'Thor Bots'], 16278: ['SJ1', 'N/A', 'N/A', 'Wookie Patrol'], 16306: ['GB', 'SANM', 'N/A', 'Incognito'], 16481: ['SANM', 'N/A', 'N/A', 'Robo racers'], 16532: ['N/A', 'N/A', 'N/A', 'Sparkbots'], 16533: ['N/A', 'N/A', 'N/A', 'Infernobots'], 16535: ['FMT2', 'CUP', 'N/A', 'LEGIT'], 16561: ['N/A', 'N/A', 'N/A', 'Navigators'], 16594: ['FMT2', 'SANM', 'N/A', 'Hyper Geek Turtles'], 16656: ['DALY', 'CUP', 'N/A', 'Thunderbots'], 16688: ['N/A', 'N/A', 'N/A', 'Wolfbotics'], 16689: ['N/A', 'N/A', 'N/A', 'Team Yantra'], 16778: ['FMT1', 'N/A', 'N/A', 'Cyber Wizards'], 16898: ['PIE', 'CUP', 'N/A', 'Poseidon'], 16944: ['FMT2', 'N/A', 'N/A', 'FM493RS'], 17099: ['DALY', 'FMT1', 'SC', 'NaH Robotics'], 17390: ['FMT4', 'N/A', 'N/A', 'TechnoG.O.A.Ts'], 17488: ['N/A', 'N/A', 'N/A', 'Firebotics'], 17571: ['DROPPED', 'CUP', 'N/A', 'Quantum Leapers'], 17759: ['FMT2', 'N/A', 'N/A', 'Mind'], 18023: ['N/A', 'N/A', 'N/A', 'South Tahoe Vikings Robotics'], 18096: ['GOOG', 'N/A', 'N/A', 'PizzaBots1'], 18133: ['FMT2', 'N/A', 'N/A', 'CyberCats'], 18134: ['GB', 'SJ1', 'N/A', 'Arkatron'], 18143: ['SANM', 'N/A', 'N/A', 'Brainy Probotics'], 18203: ['N/A', 'N/A', 'N/A', 'MCII'], 18219: ['GB', 'N/A', 'N/A', 'Primitive Data'], 18223: ['N/A', 'N/A', 'N/A', 'EmberBots'], 18233: ['SJ1', 'N/A', 'N/A', 'M.E.R.C.Y.B.'], 18247: ['DALY', 'N/A', 'N/A', 'Gilded Gears'], 18254: ['GOOG', 'FMT1', 'PIE', 'The Inzain Bots'], 18271: ['N/A', 'N/A', 'N/A', 'BPC RoBawks'], 18272: ['DALY', 'CUP', 'SC', 'Sigma'], 18307: ['SC', 'FMT4', 'N/A', 'Robo Stars'], 18309: ['FMT2', 'CUP', 'N/A', 'Dream Machines'], 18311: ['FMT4', 'SC', 'N/A', 'Icon Maniacs'], 18320: ['N/A', 'N/A', 'N/A', 'Plus Ultra 3'], 18321: ['N/A', 'N/A', 'N/A', 'Plus Ultra'], 18322: ['N/A', 'N/A', 'N/A', 'Plus Ultra 5'], 18323: ['N/A', 'N/A', 'N/A', 'Plus Ultra 4'], 18324: ['N/A', 'N/A', 'N/A', 'Plus Ultra 2'], 18325: ['N/A', 'N/A', 'N/A', 'Plus Ultra 6'], 18326: ['N/A', 'N/A', 'N/A', 'Tech-DREAMS FTC'], 18337: ['N/A', 'N/A', 'N/A', 'Artisans'], 18340: ['GB', 'N/A', 'N/A', 'Polaris Robotics'], 18343: ['N/A', 'N/A', 'N/A', 'Chartwell FTC 3'], 18344: ['N/A', 'N/A', 'N/A', 'Chartwell FTC 2'], 18345: ['N/A', 'N/A', 'N/A', 'Chartwell FTC 1'], 18346: ['FMT2', 'CUP', 'N/A', 'AA Batteries'], 18371: ['N/A', 'N/A', 'N/A', 'Wolf Pack'], 18373: ['SANM', 'N/A', 'N/A', 'Blizzard Robotics'], 18412: ['SJ1', 'N/A', 'N/A', 'OtterPups'], 18413: ['SJ1', 'N/A', 'N/A', 'SealPups'], 18451: ['SAC', 'N/A', 'N/A', 'Bots of Thunder'], 18466: ['N/A', 'N/A', 'N/A', 'Mastermindz'], 18481: ['N/A', 'N/A', 'N/A', 'CAF Robotics'], 18490: ['SANM', 'N/A', 'N/A', 'Green Machine'], 18504: ['GB', 'SAC', 'N/A', 'MAGIC BOTS'], 18510: ['N/A', 'N/A', 'N/A', 'MH Plus Ultra'], 18513: ['DALY', 'SAC', 'N/A', 'Gear Toes'], 18536: ['N/A', 'N/A', 'N/A', 'Robodores FTC'], 18563: ['N/A', 'N/A', 'N/A', 'Landslide'], 18564: ['DALY', 'PIE', 'FMT2', 'Techbots'], 18569: ['FMT2', 'SJ1', 'N/A', 'Seal Team Schicks'], 18604: ['N/A', 'N/A', 'N/A', 'Robo R0ckstars'], 18712: ['N/A', 'N/A', 'N/A', 'Impact Robotics'], 18715: ['GB', 'SJ1', 'CUP', 'Artemis'], 18726: ['PIE', 'SJ1', 'N/A', 'Ninjabots'], 18729: ['FMT2', 'N/A', 'N/A', 'TeamFirst-FTC'], 18756: ['SAC', 'N/A', 'N/A', 'FTC Horner Team 4'], 18767: ['SJ1', 'SAC', 'N/A', 'The Techarinos'], 18786: ['FMT1', 'GB', 'N/A', 'Liverbots'], 18788: ['N/A', 'N/A', 'N/A', 'ZeusTech'], 18837: ['N/A', 'N/A', 'N/A', 'Kronos'], 18897: ['PIE', 'CUP', 'N/A', 'Raider Robotics'], 17252: ['SJ1', 'N/A', 'N/A', 'HT7']}
    comps = {'SANM': [4475, 5206, 7316, 7610, 11466, 11467, 13217, 13380, 14078, 14525, 16306, 16481, 16594, 18143, 18373, 18490], 'GB': [7303, 7641, 8872, 11201, 11311, 13345, 16026, 16306, 18134, 18219, 18340, 18504, 18715, 18786], 'DALY': [524, 3470, 7641, 8375, 8381, 8404, 9657, 9784, 13274, 13345, 14259, 14504, 14663, 15385, 16656, 17099, 18247, 18272, 18513, 18564], 'PIE': [524, 11689, 12869, 13050, 14214, 14318, 14663, 16898, 18254, 18564, 18726, 18897], 'GOOG': [524, 6165, 7854, 8375, 9784, 11039, 12635, 12962, 13223, 13345, 14162, 14318, 14525, 14784, 14969, 15385, 18096, 18254], 'FMT2': [5773, 8404, 11201, 11475, 11575, 12962, 13217, 14341, 14969, 16026, 16535, 16594, 16944, 17759, 18133, 18309, 18346, 18564, 18569, 18729], 'FMT1': [4345, 4998, 6949, 7303, 7390, 7854, 8367, 8872, 11039, 12869, 13356, 13380, 14162, 14214, 14300, 14502, 16177, 16778, 17099, 18254, 18786], 'FMT4': [4345, 6165, 9614, 9656, 13180, 13356, 14473, 17390, 18307, 18311], 'SAC': [3470, 4950, 6038, 7128, 9614, 12804, 13223, 14259, 14298, 14473, 15453, 18451, 18504, 18513, 18756, 18767], 'SJ1': [9578, 11311, 11689, 13274, 14078, 14784, 16278, 18134, 18233, 18412, 18413, 18569, 18715, 18726, 18767, 17252], 'SC': [6949, 8367, 8381, 9657, 13035, 13180, 13218, 14300, 15068, 16194, 16197, 16236, 17099, 18272, 18307, 18311], 'CUP': [4345, 5206, 5773, 7390, 8367, 11475, 11575, 11689, 13050, 14214, 14504, 16177, 16197, 16236, 16535, 16656, 16898, 17571, 18272, 18309, 18346, 18715, 18897]}
    fairplay = [524, 4345, 4950, 4998, 5206, 5773, 6038, 6165, 6448, 6949, 7083, 7128, 7303, 7316, 7390, 7610, 7641, 7854, 8300, 8367, 8375, 8381, 8404, 8872, 9614, 9656, 9768, 9784, 11039, 11201, 11311, 11466, 11467, 11575, 11689, 12635, 12869, 13107, 13180, 13217, 13218, 13345, 13356, 13380, 14300, 14318, 14341, 14374, 14473, 14504, 14525, 14663, 14969, 15385, 16026, 16072, 16177, 16197, 16236, 16302, 16306, 16309, 16532, 16533, 16535, 16594, 16944, 17759, 18183, 18190, 18219, 18223, 18254, 18272, 18307, 18309, 18311, 18340, 18373, 18466, 18513, 18564]
    advancement = {'GOOG': [14525, 12635, 6165, 8375, 0, 11039, 11039, 9784, 13223, 18254, 9784, 13345, 12635, 18254, 8375, 14318, 0, 14162, 0, 7854], 'FMT4': [6165, 13356, 9656, 13180, 4345, 14473, 9656, 17390, 14473, 18311, 13356, 9614, 4345, 9614, 18307, 0, 6165, 0, 13180, 0], 'DALY': [8375, 9784, 8381, 8404, 8404, 13345, 8381, 14504, 8404, 14259, 7641, 17099, 9784, 18272, 14259, 18564, 13345, 14663, 9657, 18513], 'FMT1': [11039, 7303, 14300, 13356, 7390, 18254, 14300, 4345, 7854, 14162, 7390, 13380, 7303, 13380, 13356, 12869, 8872, 17099, 8367, 16778], 'FMT2': [14341, 17759, 13217, 5773, 8404, 16535, 11475, 11201, 13217, 18346, 14969, 11575, 8404, 5773, 11575, 16944, 16944, 18564, 14341, 18729], 'PIE': [12869, 18254, 14663, 16898, 11689, 14214, 524, 14318, 14318, 18564, 11689, 18726, 14214, 16898, 14663, 0, 13050, 0, 13050, 0], 'SC': [13180, 8381, 8381, 18311, 8367, 14300, 16236, 17099, 14300, 18272, 8367, 13035, 8381, 13218, 15068, 16197, 9657, 18307, 18307, 6949], 'GB': [18219, 7303, 7303, 13345, 8872, 11201, 11201, 11311, 7303, 18504, 18134, 7641, 7641, 11311, 18340, 18786, 16026, 18504, 16306, 13345], 'CUP': [], 'SJ1': [], 'SAC': [], 'SANM': []}
    qualified = {'GOOG': [14525, 12635, 6165], 'FMT4': [13356], 'DALY': [8375, 9784, 8381], 'FMT1': [11039, 7303, 14300], 'FMT2': [14341, 17759, 13217], 'PIE': [12869, 18254], 'SC': [13180, 18311], 'GB': [18219, 13345], 'CUP': [], 'SJ1': [], 'SAC': [], 'SANM': []}
    slots = ['Inspire, 1st', 'Next Rank', 'Inspire, 2nd', 'Next Rank', 'Inspire, 3rd', 'Next Rank', 'Think, 1st', 'Next Rank', 'Connect, 1st', 'Next Rank', 'Innovate, 1st', 'Next Rank', 'Control, 1st', 'Motivate, 1st', 'Design, 1st', 'Next Rank', 'Think, 2nd', 'Next Rank', 'Connect, 2nd', 'Next Rank']
    regionals = [6165, 7303, 8375, 8381, 9784, 11039, 12635, 12869, 13180, 13217, 13345, 13356, 14300, 14341, 14525, 17759, 18219, 18254, 18311]
    counters = {command.name: 0 for command in bot_commands}
