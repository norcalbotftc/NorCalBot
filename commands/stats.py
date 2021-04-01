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
    return '$stats' in content

async def command(content, author, message, commands, client):
    stats = discord.Embed(title = 'NorCal Bot Command Counter', description = 'Shows the number of times each command is used')
    stats.add_field(name = 'Total', value = sum(db.counters.values()))
    overflowcounter = 1
    for index in range(len(commands)):
        stats.add_field(name = '$' + commands[index].name, value = db.counters[commands[index].name])
        overflowcounter += 1
        if overflowcounter % 25 == 0 and overflowcounter != 0:
            await message.channel.send(content = None, embed = stats)
            stats = discord.Embed(title = 'NorCal Bot Command Counter (cont)', description = 'Shows the number of times each command is used')
    if overflowcounter % 25 != 0 and overflowcounter != 0:
        await message.channel.send(content = None, embed = stats)

stats = Command('stats', '$stats', 'Shows the counters for each command', check, command)
