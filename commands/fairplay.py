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
    return '$fairplay' in content

async def command(content, author, message, commands, client):
    info = discord.Embed(title = 'Fair Play Teams', description = 'A list of all of the fair play teams')
    info.add_field(name = 'Number of Fair Play Teams', value = str(len(db.fairplay)))
    info.add_field(name = '% of Teams in Fair Play', value = str(int(len(db.fairplay) / len(db.teams) * 100)))
    info.set_footer(text = 'Source: NorCal FTC Fair Play Team List - https://www.norcalftc.org/fair-play-team-list/')
    overflowcounter = 2
    for index in range(len(db.fairplay)):
        team = db.fairplay[index]
        try:
            info.add_field(name = team, value = db.teams[team][3])
            overflowcounter += 1
        except:
            pass
        if overflowcounter % 25 == 0 and overflowcounter != 0:
            await message.channel.send(content = None, embed = info)
            info = discord.Embed(title = 'Fair Play Teams (cont)', description = 'A list of all of the fair play teams')
            info.set_footer(text = 'Source: NorCal FTC Fair Play Team List - https://www.norcalftc.org/fair-play-team-list/')
    if overflowcounter % 25 != 0 and overflowcounter != 0:
        await message.channel.send(content = None, embed = info)

fairplay = Command('fairplay', '$fairplay', 'Shows a list of all of the fair play teams', check, command)
