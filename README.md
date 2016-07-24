mienfield bot
=============

a bot to play mienfield. mienfield is a html5 mmo minesweeper.

http://mienfield.com/

i created this because i like to code how to solve a game
more than solving the game itself.
also because i like to practice how to automate boring clicks.

the bot works by taking a screenshot, then image recognition,
then calculating minesweeper logic, then clicking.

how to use
----------

* firefox load mienfield.com
* put fullscreen
* start bot
* switch to firefox
* wait
* see clicks unfold

note that the mienfield guys asked to not use bots.
you will be blocked they say. and you will disappear from leaderboards.

limitations
------------

there is no way to recognize custom flags.

for now only number and open and closed cells are recognized.
everything else is assumed to be a flag.

only numbers 1 to 6 is recognized.
because i have not encountered a 7 yet.

only number cells with neighbouring closed cells are considered to click.
if number in cell is equal to number of flags
then left click to open closed cells.
if number in cell minus number of flags is equal to closed cells
then right click to flag closed cells.

dependencies
------------

* scrot
* visgrep from xautomation
* xte from xautomation
* convert from imagemagick
* PIL/Pillow

license
-------

Copyright 2016  Lesmana Zimmer

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
