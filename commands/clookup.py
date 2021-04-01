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
    return '$clookup' in content

async def command(content, author, message, commands, client):
    lookup = content.split(' ')
    if lookup[0] != '$clookup' or len(lookup) != 2:
        await message.channel.send('For looking up a competition, type "$clookup", a space, and then the competition ID.')
    else:
        try:
            id = lookup[1].upper()
            data = db.comps[id]
            fairplaycount = 0
            for team in data:
                if team in db.fairplay:
                    fairplaycount += 1
            try:
                description = 'Teams Registered for **' + COMP_NAMES[id] + '** Qualifier on **' + COMP_DATES[id] + '**'
            except:
                description = 'Teams Registered for ' + id + ' Qualifier'
            info = discord.Embed(title = id + ' Qualifier Registration', description = description)
            info.add_field(name = '# Teams', value = str(len(data)))
            info.add_field(name = '% Teams in Fair Play', value = str(int(fairplaycount / len(data) * 100)))
            info.set_footer(text = 'Teams in fairplay are marked with "*".')
            overflowcounter = 2
            for team in data:
                try:
                    info.add_field(name = str(team) + ('*' if team in db.fairplay else ''), value = db.teams[team][3])
                    overflowcounter += 1
                except:
                    pass
                if overflowcounter % 25 == 0 and overflowcounter != 0:
                    await message.channel.send(content = None, embed = info)
                    info = discord.Embed(title = id + ' Qualifier Registration (cont)', description = description)
                    info.set_footer(text = 'Teams in fairplay are marked with "*".')
            if overflowcounter % 25 != 0 and overflowcounter != 0:
                await message.channel.send(content = None, embed = info)
        except:
            await message.channel.send('For looking up a competition, type "$clookup", a space, and then the competition ID.')

clookup = Command('clookup', '$clookup [competition id]', 'Shows the registered teams for the specified competition', check, command)
