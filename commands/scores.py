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
    return content.find('$scores') == 0

async def command(content, author, message, commands, client):
    lookup = content.split(' ')
    if lookup[0] != '$scores' or len(lookup) != 3:
        await message.channel.send('For looking up a team\'s scores, type "$scores", a space, the competition ID, a space, and the team number.')
    else:
        try:
            id = lookup[1].upper()
            team = lookup[2]
            code = API_CODES.get(id)
            info = discord.Embed(title = id + ' Scores for ' + db.teams[int(team)][3], description = 'Use $dscores for detailed score breakdown')
            info.set_footer(text = 'Source: FIRST API - https://ftc-events.firstinspires.org/services/API')

            apiInfo = first_request('scores/' + code + '/qual?teamnumber=' + team).json().get('MatchScores')
            if len(apiInfo) == 0:
                await message.channel.send('FIRST API Error')
            else:
                for data in apiInfo:
                    matchData = data.get('scores')
                    penalty = ' (penalties -' + str(matchData['penaltyPoints']) + ')' if matchData['penaltyPoints'] > 0 else ''
                    info.add_field(name = 'Match ' + str(data['matchNumber']), value = 'Total: ' + str(matchData['totalPoints']) + ' pts\nAuto: ' + str(matchData['autoPoints']) + ' pts\nTeleOp: ' + str(matchData['dcPoints'] + matchData['endgamePoints']) + ' points\n' + penalty)

                await message.channel.send(content = None, embed = info)
        except:
            await message.channel.send('The competition ID or team number is invalid or the scores have not been published yet.')

scores = Command('scores', '$scores [competition id] [team number]', 'Shows a team\'s scores at a competition', check, command)
