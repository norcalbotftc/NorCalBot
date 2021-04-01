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
    return content.find('$veriguds') == 0

async def command(content, author, message, commands, client):
    lookup = content.split(' ')
    if lookup[0] != '$veriguds' or len(lookup) != 2:
        await message.channel.send('For reacting "VERIGUDS" to a message, type "$veriguds", a space, and then the message id or message link. The message must be in this channel.')
    else:
        try:
            if len(lookup[1]) == 18:
                number = int(lookup[1])
            elif len(lookup[1].split('/')[-1]) == 18:
                number = int(lookup[1].split('/')[-1])
            else:
                number = 0
                await message.channel.send('For reacting "VERIGUDS" to a message, type "$veriguds", a space, and then the message id or message link. The message must be in this channel.')

            if number != 0:
                reactMessage = await message.channel.fetch_message(number)
                await reactMessage.add_reaction('🇻')
                await reactMessage.add_reaction('🇪')
                await reactMessage.add_reaction('🇷')
                await reactMessage.add_reaction('🇮')
                await reactMessage.add_reaction('🇬')
                await reactMessage.add_reaction('🇺')
                await reactMessage.add_reaction('🇩')
                await reactMessage.add_reaction('🇸')
        except:
            await message.channel.send('For reacting "VERIGUDS" to a message, type "$veriguds", a space, and then the message id or message link. The message must be in this channel.')

veriguds = Command('veriguds', None, None, check, command)
