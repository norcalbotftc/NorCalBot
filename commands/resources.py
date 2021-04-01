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
    return '$resources' in content

async def command(content, author, message, commands, client):
    resources = discord.Embed(title = 'Game Manuals', description = 'Use gm for just game manuals')
    resources.add_field(name = 'GM0', value = '[Game Manual 0](https://gm0.org/en/stable/)')
    resources.add_field(name = 'GM1 - Traditional', value = '[Game Manual 1 - Traditional](https://www.firstinspires.org/sites/default/files/uploads/resource_library/ftc/game-manual-part-1-traditional-events.pdf)')
    resources.add_field(name = 'GM1 - Remote', value = '[Game Manual 1 - Remote](https://www.firstinspires.org/sites/default/files/uploads/resource_library/ftc/game-manual-part-1-remote-events.pdf)')
    resources.add_field(name = 'GM2 - Traditional', value = '[Game Manual 2 - Traditional](https://www.firstinspires.org/sites/default/files/uploads/resource_library/ftc/game-manual-part-2-traditional-events.pdf)')
    resources.add_field(name = 'GM2 - Remote', value = '[Game Manual 2 - Remote](https://www.firstinspires.org/sites/default/files/uploads/resource_library/ftc/game-manual-part-2-remote-events.pdf)')
    resources.add_field(name = 'UG Scorer', value = '[Ultimate Goal Scorer App](http://roboavatars.weebly.com/ultimategoalscorer.html)')
    resources.add_field(name = 'OpenOdo', value = '[OpenOdometry](https://openodometry.weebly.com/)')
    resources.add_field(name = 'NorCal FTC', value = '[norcalftc.org](https://www.norcalftc.org)')
    resources.add_field(name = 'FIRST API', value = '[FIRST API](https://ftc-events.firstinspires.org/services/API)')
    resources.add_field(name = 'FTC Stats API', value = '[FTC Stats API](https://dynamic.jackcrane.rocks/api/ftcstats/docs.php)')
    await message.channel.send(content = None, embed = resources)

resources = Command('resources', '$resources', 'Shows links for FTC resources', check, command)
