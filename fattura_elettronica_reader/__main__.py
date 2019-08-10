#
# __main__.py
#
# Copyright (c) 2018 Enio Carboni - Italy
# Copyright (C) 2019 Franco Masotti <franco.masotti@live.com>
#
# This file is part of fattura-elettronica-reader.
#
# fattura-elettronica-reader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# fattura-elettronica-reader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with fattura-elettronica-reader.  If not, see <http://www.gnu.org/licenses/>.
#
"""Call the CLI parser."""

import sys
import traceback
from .cli import CliInterface


def main(args=None):
    """Call the CLI interface and wait for the result."""
    retcode = 0
    try:
        ci = CliInterface()
        args = ci.parser.parse_args()
        result = args.func(args)
        if result is not None:
            print(result)
        retcode = 0
    except Exception:
        retcode = 1
        traceback.print_exc()
    sys.exit(retcode)


if __name__ == '__main__':
    main()
