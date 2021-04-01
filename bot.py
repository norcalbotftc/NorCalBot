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
from bot_commands import *
import db
import discord
import re
from util import *

loop_counter = 0
client = discord.Client()

async def update():
    """
    update(): scrapes/saves data every 4 hours
    """

    global loop_counter

    await client.wait_until_ready()
    while not client.is_closed():
        teams = comps = advancement = qualified = counters = {}
        fairplay = slots = regionals = []

        stats = discord.Embed(title = 'NorCal Bot Command Counter', description = 'This runs every two hours.')
        stats.add_field(name = 'Total', value = sum(db.counters.values()))
        overflowcounter = 1
        STATS_CHANNEL = client.get_guild(TEST_GUILD).get_channel(TEST_CHANNEL)
        for index in range(len(bot_commands)):
            stats.add_field(name = '$' + bot_commands[index].name, value = db.counters[bot_commands[index].name])
            overflowcounter += 1
            if overflowcounter % 25 == 0 and overflowcounter != 0:
                await STATS_CHANNEL.send(content = None, embed = stats)
                stats = discord.Embed(title = 'NorCal Bot Command Counter (cont)', description = 'This runs every two hours.')
        if overflowcounter % 25 != 0 and overflowcounter != 0:
            await STATS_CHANNEL.send(content = None, embed = stats)
        await STATS_CHANNEL.send(' '.join([str(value) for value in db.counters.values()]))
        db.set_counters()

        if loop_counter % 2 == 0:
            html_code = get_html('https://www.norcalftc.org/norcal-ftc-team-list-new/')
            numList = re.compile('mn-1">\s*?(\S*?)\s*?</td>', re.DOTALL).findall(html_code)

            for team in numList:
                if int(team) <= 50000:
                    # print(team)
                    team_data = get_html('https://www.norcalftc.org/ftc-team-status/?ftcteam=' + team)
                    qt = re.compile('QT #\d.*?er">\s*?(\S*?)\s*?</td>', re.DOTALL).findall(team_data)
                    name = re.compile('am Name.*?">\s*?(\S.*?)\s*?</td>', re.DOTALL).findall(team_data)[0]
                    teams[int(team)] = [qt[0].upper() if len(qt) >= 1 else 'N/A', qt[1].upper() if len(qt) >= 2 else 'N/A', qt[2].upper() if len(qt) == 3 else 'N/A', name]
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

            for comp in headers:
                advancement[comp] = []
                qualified[comp] = []

            data = re.compile('td class=\"c.*?>(.*?)</td', re.DOTALL).findall(html_code)
            while data[0].find('I') == -1:
                data.pop(0)
            num_rows = 20
            num_cols = len(data) // num_rows

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
                            regionals.append(team)
                        else:
                            team = int(re.compile('\D*(\d*)\D*', re.DOTALL).findall(team)[0])
                        advancement[key].append(team)
                    else:
                        advancement[key].append(int(team) if team != '' else 0)

                    if advancement[key].count(0) == num_rows:
                        advancement[key] = []

            regionals.sort()

            # print(advancement)
            # print(qualified)
            # print(slots)
            # print(regionals)

            requests.patch('https://dynamic.jackcrane.rocks/api/ftcstats/fetch.php')

            db.teams, db.comps, db.fairplay, db.advancement, db.qualified, db.slots, db.regionals = teams, comps, fairplay, advancement, qualified, slots, regionals
            set()

        loop_counter += 1
        await asyncio.sleep(7200)

@client.event
async def on_ready():
    """
    on_ready(): sets up bot
    """

    await client.get_guild(TEST_GUILD).get_channel(TEST_CHANNEL).send('I Just Woke Up!')
    await client.change_presence(activity = discord.Game(name = '$help | ' + str(len(client.guilds)) + ' guilds'))

@client.event
async def on_message_edit(before, after):
    """
    on_message_edit(before, after): processed edited messages
    :param before: not used
    :param after: user message
    """

    await on_message(after)

@client.event
async def on_message(message):
    """
    on_message(message): main bot code, processes user messages
    :param message: user message
    """

    # Command Variables
    content = message.content.lower()
    author = message.author
    guild = message.guild.name if message.guild is not None else (author.name if str(author) in ADMINS else author.mention)

    # Process Command
    if str(author) != BOT_NAME:
        for command in bot_commands:
            if command.check(content, author):
                db.counters[command.name] += 1
                await client.get_guild(TEST_GUILD).get_channel(TEST_CHANNEL).send('(' + guild + ') ' + content)
                await command.command(content, author, message, bot_commands, client)
                break

# Run Bot
try:
    db.get()
except:
    db.backup(bot_commands)

client.loop.create_task(update())
client.run(DISCORD_TOKEN)
