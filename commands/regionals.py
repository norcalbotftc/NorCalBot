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

from command import *

def check(content, author):
    return '$regionals' in content

async def command(content, author, message, commands, client):
    info = discord.Embed(title = 'NorCal Regionals Qualifying Teams', description = 'This is a list of all of NorCal teams that have qualified for regionals. Teams in fairplay are marked with "*".')
    info.add_field(name = 'Number of Teams', value = str(len(db.regionals)))

    fairplaycount = 0
    for team in db.regionals:
        if team in db.fairplay:
            fairplaycount += 1
    info.add_field(name = '% of Teams in Fair Play', value = str(int(fairplaycount / len(db.regionals) * 100)))
    info.set_footer(text = 'Source: NorCal FTC Advancement Summary - https://www.norcalftc.org/2020-advancement-summary/')
    overflowcounter = 2
    for index in range(len(db.regionals)):
        team = db.regionals[index]
        try:
            info.add_field(name = str(team) + ('*' if team in db.fairplay else ''), value = db.teams[team][3])
            overflowcounter += 1
        except:
            pass
        if overflowcounter % 25 == 0 and overflowcounter != 0:
            await message.channel.send(content = None, embed = info)
            info = discord.Embed(title = 'NorCal Regionals Qualifying Teams (cont)', description = 'This is a list of all of NorCal teams that have qualified for regionals. Teams in fairplay are marked with "*".')
            info.set_footer(text = 'Source:  NorCal FTC Advancement Summary - https://www.norcalftc.org/2020-advancement-summary/')
    if overflowcounter % 25 != 0 and overflowcounter != 0:
        await message.channel.send(content = None, embed = info)

regionals = Command('regionals', '$regionals', 'Shows a list of all teams qualified to NorCal Regionals', check, command)
