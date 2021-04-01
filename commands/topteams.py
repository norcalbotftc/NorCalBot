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
    return content.find('$topteams') == 0

async def command(content, author, message, commands, client):
    lookup = content.split(' ')
    region = 'Global'

    if len(lookup) > 1:
        if lookup[1] == 'norcal':
            region = 'NorCal'
        elif lookup[1] == 'socal':
            region = 'SoCal'
        elif lookup[1] in ['cal', 'ca']:
            region = 'California'
        elif lookup[1] != 'global':
            await message.channel.send('Only Global, NorCal, SoCal, and CA Regions Supported')
            return

    await message.channel.send('Looking up ' + region + ' Top Team Data')
    info = discord.Embed(title = region + ' Top 15 Ranked Teams')
    info.set_footer(text = 'Source: FTC Stats API - https://dynamic.jackcrane.rocks/api/ftcstats/docs.php')

    response2 = None
    if region == 'Global':
        payload = {'rank': '<= 50'}
    else:
        payload = {'location': region}
        payload2 = {'rank': '<= 500'}
        response2 = requests.post('https://dynamic.jackcrane.rocks/api/ftcstats/fetch.php', data = payload2).json().get('data')
    response = requests.post('https://dynamic.jackcrane.rocks/api/ftcstats/fetch.php', data = payload).json().get('data')

    names = []
    for key in response.keys():
        if len(names) < 15:
            data = response.get(key)
            name = data.get('teamname')
            if names.count(name) == 0:
                rank = '-1'
                if region != 'Global':
                    names2 = []
                    for key2 in response2.keys():
                        name2 = response2.get(key2).get('teamname')
                        if names2.count(name2) == 0:
                            names2.append(name2)
                        if name == name2:
                            rank = str(len(names2))
                            break
                    if rank == '-1':
                        rank = '500+'

                info.add_field(name = str(len(names) + 1) + ') ' + str(data.get('teamnum')) + ' ' + data.get('teamname'), value = 'OPR: ' + str(data.get('opr')) + '\nMax score: ' + str(data.get('max_np_score')) + ('' if region == 'Global' else ('\nGlobal Rank: ' + rank)))
                names.append(name)

    await message.channel.send(content = None, embed = info)

topteams = Command('topteams', '$topteams [region]*', 'Shows top 15 teams in specified region', check, command)
