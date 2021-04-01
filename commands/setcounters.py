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
    return content.find('$setcounters') == 0 and str(author) in ADMINS

async def command(content, author, message, commands, client):
    counts = list(map(lambda c: int(c), content.split(' ')[1:]))
    if len(counts) == len(commands):
        counts = {commands[index].name: counts[index] for index in range(len(commands))}

        stats = discord.Embed(title = 'NorCal Bot Command Set Counters', description = 'Counters have been reset')
        stats.add_field(name = 'Total', value = sum(counts.values()))
        overflowcounter = 1
        for index in range(len(commands)):
            stats.add_field(name = '$' + commands[index].name, value = counts[commands[index].name])
            overflowcounter += 1
            if overflowcounter % 25 == 0 and overflowcounter != 0:
                await message.channel.send(content = None, embed = stats)
                stats = discord.Embed(title = 'NorCal Bot Command Set Counters (cont)', description = 'Counters have been reset')
        if overflowcounter % 25 != 0 and overflowcounter != 0:
            await message.channel.send(content = None, embed = stats)
        db.set_counters()
    else:
        await message.channel.send('Incorrect Number of Counters. You sent ' + str(len(counts)) + ' but ' + str(len(commands)) + ' are needed.')

setcounters = Command('setcounters', None, None, check, command)
