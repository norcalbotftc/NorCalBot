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
    return '$suggest' in content

async def command(content, author, message, commands, client):
    suggestion = content.split(' ')
    if suggestion[0] != '$suggest' or len(suggestion) == 1:
        await message.channel.send('For suggesting a new command or reporting a bug, type "$suggest", a space, and your message. If you are suggesting a new command, include the command as well as what it is supposed to do. If you are reporting a bug, include the command that is not working as well as a detailed explanation of what went wrong.')
    else:
        await client.get_guild(TEST_GUILD).get_channel(TEST_CHANNEL).send('(' + author.mention + ') <@' + str(ADMIN_IDS[0]) + '> ' + ' '.join(suggestion[1:]))
        await message.channel.send('You suggestion has been sent!\nIf you suggested a new command, hopefully you sent the command as well as what it is supposed to do. If you reported a bug, hopefully you sent the command that was not working as well as a detailed explanation of what went wrong.\nIf you didn\'t do this, just send another suggestion.')

suggest = Command('suggest', '$suggest', 'Send a command suggestion or a bug report', check, command)
