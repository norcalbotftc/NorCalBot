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
    return content.find('$highscores') == 0

async def command(content, author, message, commands, client):
    lookup = content.split(' ')
    region = 'Global'

    if len(lookup) > 1:
        if lookup[1] in ['norcal', 'socal', 'cal', 'ca']:
            region = 'California'
        elif lookup[1] != 'global':
            await message.channel.send('Only Global and CA Regions Supported')
            return

    await message.channel.send('Looking up ' + region + ' High Score Data')
    info = discord.Embed(title = region + ' Top 10 Scores', description = 'Scores/Rings ([auto]/[teleop])')
    info.set_footer(text = 'Source: FTC Stats API - https://dynamic.jackcrane.rocks/api/ftcstats/docs.php')

    region = 'index' if region == 'Global' else region.lower()

    html = get_raw_html('http://www.ftcstats.org/2021/' + region + '.html')
    data = re.compile('<td align="right" width="4%">(.*?)</td><td align="right" width="4%">(.*?)</td><td align="right" width="4%">(.*?)</td><td align="right" width="4%">(.*?)</td><td align="right" width="4%">(.*?)'
                      '</td><td align="right" width="4%">(.*?)</td><td align="right" width="4%">(.*?)</td><td><a href=.*?>(.*?)</a></td><td></td><td></td><td>(.*?)</td>', re.DOTALL).findall(html)

    count = 1
    for score in data:
        info.add_field(name = str(count) + ') ' + score[7], value = 'Score: ' + str(score[0]) + ' (' + str(score[1]) + '/' + str(int(score[2]) + int(score[3])) + ')' + '\nRings: ' + str(score[4]) + '/' + str(score[5]))
        count += 1

    await message.channel.send(content = None, embed = info)

highscores = Command('highscores', '$highscores [region]*', 'Shows top 10 scores in specified region', check, command)
