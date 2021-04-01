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
    return content.find('$rankings') == 0

async def command(content, author, message, commands, client):
    lookup = content.split(' ')
    if lookup[0] != '$rankings' or len(lookup) != 2:
        await message.channel.send('For looking up competition rankings, type "$rankings", a space, and then the competition ID.')
    else:
        try:
            id = lookup[1].upper()
            code = API_CODES.get(id)
            info = discord.Embed(title = 'Rankings for ' + id)
            info.set_footer(text = 'Source: FIRST API - https://ftc-events.firstinspires.org/services/API')

            apiInfo = first_request('rankings/' + code).json().get('Rankings')
            if len(apiInfo) == 0:
                await message.channel.send('FIRST API Error')
            else:
                for data in apiInfo:
                    info.add_field(name = str(data['rank']) + '. ' + str(data['teamNumber']) + ' (' + db.teams[data['teamNumber']][3] + ')', value = str(int(data['sortOrder1'])) + ' Ranking Pts\n' + str(int(data['sortOrder6'])) + ' Max Match Pts')
                await message.channel.send(content = None, embed = info)
        except:
            await message.channel.send('The competition ID is invalid or the rankings have not been published yet.')

rankings = Command('rankings', '$rankings [competition id]', 'Shows the rankings at a competition', check, command)
