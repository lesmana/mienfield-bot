mienfield bot
=============

a bot to play mienfield. mienfield is a html5 mmo minesweeper.
sadly the game no longer exists on the internets.

this code will stay online for posterity.

i created this because i like to code how to solve a game
more than solving the game itself.
also because i like to practice how to automate boring clicks.

the bot works by taking a screenshot, then image recognition,
then calculating minesweeper logic, then clicking.

number cells with neighbouring closed cells are inspected.
if number in cell is equal to number of flags
then left click to open closed cells.
if number in cell minus number of flags is equal to closed cells
then right click to flag closed cells.

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

only numbers 1 to 7 is recognized.
because i have not encountered an 8 yet.

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

This program is free software.
It is licensed under the GNU GPL version 3 or later.
That means you are free to use this program for any purpose;
free to study and modify this program to suit your needs;
and free to share this program or your modifications with anyone.
If you share this program or your modifications
you must grant the recipients the same freedoms.
To be more specific: you must share the source code under the same license.
For details see https://www.gnu.org/licenses/gpl-3.0.html
