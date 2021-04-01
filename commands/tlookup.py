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
    return '$tlookup' in content

async def command(content, author, message, commands, client):
    lookup = content.split(' ')
    if lookup[0] != '$tlookup' or len(lookup) != 2:
        await message.channel.send('For looking up a team, type "$tlookup", a space, and then the team number.')
    else:
        try:
            number = int(lookup[1])
            data = db.teams[number]
            info = discord.Embed(title = str(number) + ' Qualifier Registration', description = 'Qualifier Registration for ' + data[3])
            info.add_field(name = 'QT #1', value = data[0])
            info.add_field(name = 'QT #2', value = data[1])
            info.add_field(name = 'QT #3', value = data[2])
            info.add_field(name = 'Fair Play', value = 'Yes' if number in db.fairplay else 'No')
            info.set_footer(text = 'Source: NorCal FTC Team Status ' + str(number) + ' - https://www.norcalftc.org/ftc-team-status/?ftcteam=' + str(number))
            await message.channel.send(content = None, embed = info)
        except:
            await message.channel.send('For looking up a team, type "$tlookup", a space, and then the team number.')

tlookup = Command('tlookup', '$tlookup [team number]', 'Shows the competitions for the registered team', check, command)
