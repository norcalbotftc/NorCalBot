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
    return content.find('$dscores') == 0

async def command(content, author, message, commands, client):
    lookup = content.split(' ')
    if lookup[0] != '$dscores' or len(lookup) != 3:
        await message.channel.send('For looking up a team\'s detailed scores, type "$dscores", a space, the competition ID, a space, and the team number.')
    else:
        try:
            id = lookup[1].upper()
            team = lookup[2]
            code = API_CODES.get(id)

            info = discord.Embed(title = id + ' Scores for ' + db.teams[int(team)][3])
            info.set_footer(text = 'Source: FIRST API - https://ftc-events.firstinspires.org/services/API')

            apiInfo = first_request('scores/' + code + '/qual?teamnumber=' + team).json().get('MatchScores')
            if len(apiInfo) == 0:
                await message.channel.send('FIRST API Error')
            else:
                count = 0
                for data in apiInfo:
                    matchData = data.get('scores')
                    penalty = ' (penalties -' + str(matchData['penaltyPoints']) + ')' if matchData['penaltyPoints'] > 0 else ''
                    info.add_field(name = 'Match ' + str(data['matchNumber']), value = 'Total: ' + str(matchData['totalPoints']) + ' pts' + penalty + '\nAuto: ' + str(matchData['autoPoints']) + ' pts\nTeleOp: ' + str(matchData['dcPoints'] + matchData['endgamePoints']) + ' pts', inline = False)

                    info.add_field(name = 'Auto Rings', value = 'High: ' + str(matchData['autoTowerHigh']) + '\nMid: ' + str(matchData['autoTowerMid']) + '\nLow: ' + str(matchData['autoTowerLow']))
                    info.add_field(name = 'Auto Powershots', value = str(matchData['autoPowerShotPoints'] // 15))
                    park = 'Yes' if matchData['navigated1'] else 'No'
                    info.add_field(name = 'Auto Wobble/Park', value = 'Delivered: ' + str(matchData['autoWobblePoints'] // 15) + '\nParked: ' + park)

                    info.add_field(name = 'TeleOp Rings', value = 'High: ' + str(matchData['dcTowerHigh']) + '\nMid: ' + str(matchData['dcTowerMid']) + '\nLow: ' + str(matchData['dcTowerLow']))
                    info.add_field(name = 'TeleOp Powershots', value = str(matchData['endPowerShotPoints'] // 15))
                    wobble = ['', '']
                    wobble[0] = 'Drop Zone' if matchData['wobbleEnd1'] == 2 else ('Start Line' if matchData['wobbleEnd1'] == 1 else 'N/A')
                    wobble[1] = 'Drop Zone' if matchData['wobbleEnd2'] == 2 else ('Start Line' if matchData['wobbleEnd2'] == 1 else 'N/A')
                    info.add_field(name = 'TeleOp Wobble', value = 'Delivered: ' + wobble[0] + ', ' + wobble[1] + '\nRings: ' + str(matchData['wobbleRingPoints'] // 5))

                    count += 1
                    if count % 2 == 0:
                        await message.channel.send(content = None, embed = info)
                        info = discord.Embed(title = id + ' Scores for ' + db.teams[int(team)][3] + ' (cont)')
                        info.set_footer(text = 'Source: FIRST API - https://ftc-events.firstinspires.org/services/API')
        except:
            await message.channel.send('The competition ID or team number is invalid or the detailed scores have not been published yet.')

dscores = Command('dscores', '$dscores [competition id] [team number]', 'Shows a detailed breakdown of a team\'s scores at a competition', check, command)
