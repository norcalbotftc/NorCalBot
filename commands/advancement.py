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
    return content.find('$advancement') == 0

async def command(content, author, message, commands, client):
    lookup = content.split(' ')
    if lookup[0] != '$advancement' or len(lookup) != 2:
        await message.channel.send('To look up a qualifier\'s advancing team order, type "$advancement", a space, and then the competition ID.')
    else:
        id = lookup[1].upper()
        if id not in db.advancement or len(db.advancement[id]) == 0:
            await message.channel.send('The competition ID is invalid or the advancement data has not been published yet.')
        else:
            info = discord.Embed(title = id + ' Qualifier Advancement', description = 'The teams that have advanced to NorCal Regionals are marked with a "*". Use $regionals to see all of the qualifying teams.')
            info.set_footer(text = 'Source: NorCal FTC Advancement Summary - https://www.norcalftc.org/2020-advancement-summary/')

            count = 0
            for slot in range(len(db.advancement[id])):
                team = db.advancement[id][slot]
                if team != 0:
                    info.add_field(name = str(count + 1) + ') ' + db.slots[slot] + ('*' if team in db.qualified[id] else ''), value = str(team) + ' (' + db.teams[team][3] + ')')
                    count += 1

            await message.channel.send(content = None, embed = info)

advancement = Command('advancement', '$advancement [competition id]', 'Shows the advancement order for the specified competition', check, command)
