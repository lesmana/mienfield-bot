#! /usr/bin/env python

import shlex
import subprocess
import sys
import time

def wait_for_user(howlong):
  for i in range(howlong, 0, -1):
    print(i)
    time.sleep(1)
  print('go!')

def run(command):
  splitcommand = shlex.split(command)
  result = subprocess.run(splitcommand,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True)
  return result

def make_screenshot():
  screenshotfilename = 'screenshot.png'
  result = run('scrot {}'.format(screenshotfilename))
  if result.returncode:
    raise Exception('scrot failed')
  return screenshotfilename

def visgrep(where, what):
  result = run('visgrep {} {}'.format(where, what))
  if not result.stdout:
    raise Exception('visgrep {} {} failed'.format(where, what))
  allcoords = []
  for output in result.stdout.splitlines():
    coords = output.split()[0]
    x, y = coords.split(',')
    intx = int(x)
    inty = int(y)
    allcoords.append((intx, inty))
  return allcoords

def click(x, y):
  result = run('xte "mousemove {} {}"'.format(x, y))
  if result.returncode:
    raise Exception('xte mousemove failed')
  result = run('xte "mouseclick 1"')
  if result.returncode:
    raise Exception('xte mouseclick failed')

def determine_borders(screenshot):
  [(rbx, _)] = visgrep(screenshot, 'images/sidebar.png')
  [(_, rby)] = visgrep(screenshot, 'images/teleport.png')
  dx, mx = divmod(rbx, 32)
  dy, my = divmod(rby, 32)
  bx = rbx - mx
  by = rby - my
  return dx, dy, bx, by

def convertcrop(screenshot, w, h):
  croppedfilename = 'screenshotcropped.png'
  result = run('convert {} -crop {}x{}+0+1 +repage {}'.format(
        screenshot, w, h, croppedfilename))
  if result.returncode:
    raise Exception('convert crop failed')
  return croppedfilename

class MienField():
  def __init__(self, width, height, cells):
    self.width = width
    self.height = height
    self.cells = cells

class Cell():
  def __init__(self, cellx, celly, pixelx, pixely, what):
    self.cellx = cellx
    self.celly = celly
    self.pixelx = pixelx
    self.pixely = pixely
    self.what = what

def parse_mienfield_for_what(screenshot, what):
  try:
    poses = visgrep(screenshot, 'images/{}.png'.format(what))
  except Exception:
    return {}
  mienfield_what = {}
  for rx, ry in poses:
    cx = rx // 32
    cy = ry // 32
    mienfield_what[(cx, cy)] = Cell(cx, cy, rx, ry, what)
  return mienfield_what

def complete_field(mienfield, dx, dy):
  for x in range(dx+1):
    for y in range(dy+1):
      if (x, y) not in mienfield:
        mienfield[(x, y)] = Cell(x, y, None, None, 'flag?')

def parse_mienfield(screenshot):
  dx, dy, bx, by = determine_borders(screenshot)
  screenshotcropped = convertcrop(screenshot, bx, by)
  mienfield = {}
  for what in ['1', '2', '3', '4', '5', '6', 'closed', 'open', 'mine']:
    print('looking for {}'.format(what))
    mienfield_what = parse_mienfield_for_what(screenshotcropped, what)
    mienfield.update(mienfield_what)
  complete_field(mienfield, dx, dy)
  mienfield = MienField(dx, dy, mienfield)
  return mienfield

def mark_borders(mienfield):
  for cell in mienfield.cells.values():
    if cell.cellx in (0, mienfield.width) or cell.celly in (0, mienfield.height):
      cell.border = True
    else:
      cell.border = False

def get_neighbours(mienfield, cx, cy):
  neighbours = []
  neighbours.append(mienfield.cells[(cx  , cy-1)])
  neighbours.append(mienfield.cells[(cx+1, cy-1)])
  neighbours.append(mienfield.cells[(cx+1, cy  )])
  neighbours.append(mienfield.cells[(cx+1, cy+1)])
  neighbours.append(mienfield.cells[(cx  , cy+1)])
  neighbours.append(mienfield.cells[(cx-1, cy+1)])
  neighbours.append(mienfield.cells[(cx-1, cy  )])
  neighbours.append(mienfield.cells[(cx-1, cy-1)])
  return neighbours

def count_neighbours(cell, neighbours):
  openlist = []
  closedlist = []
  flaglist = []
  for n in neighbours:
    if n.what in ('1', '2', '3', '4', '5', '6', 'open'):
      openlist.append(n)
    elif n.what == 'closed':
      closedlist.append(n)
    elif n.what in ('mine', 'flag?'):
      flaglist.append(n)
  return openlist, closedlist, flaglist

def classify_cells(mienfield):
  boring = []
  interesting = []
  clickopen = []
  clickflag = []
  for cell in mienfield.cells.values():
    if not cell.border:
      if cell.what in ('1', '2', '3', '4', '5', '6'):
        if len(cell.closedlist) > 0:
          if int(cell.what) + len(cell.flaglist) == len(cell.closedlist):
            clickflag.append(cell)
          elif int(cell.what) == len(cell.flaglist):
            clickopen.append(cell)
          else:
            interesting.append(cell)
        else:
          boring.append(cell)
      elif cell.what == 'open':
        boring.append(cell)
      elif cell.what == 'closed':
        if len(cell.openlist) > 0:
          interesting.append(cell)
        else:
          boring.append(cell)
      elif cell.what in ('mine', 'flag?'):
        boring.append(cell)
  return boring, interesting, clickopen, clickflag

def mark_neighbours(mienfield):
  for cell in mienfield.cells.values():
    if not cell.border:
      neighbours = get_neighbours(mienfield, cell.cellx, cell.celly)
      openlist, closedlist, flaglist = count_neighbours(cell, neighbours)
      cell.neighbours = neighbours
      cell.openlist = openlist
      cell.closedlist = closedlist
      cell.flaglist = flaglist

def count(mienfield):
  mark_borders(mienfield)
  mark_neighbours(mienfield)
  boring, interesting, clickopen, clickflag = classify_cells(mienfield)
  print('click to open')
  for cell in clickopen:
    print(cell.what, cell.cellx, cell.celly)
  print('click to flag')
  for cell in clickflag:
    print(cell.what, cell.cellx, cell.celly)

def main():
  print('put mienfield fullscreen')
  delay = 3
  if len(sys.argv) > 1:
    delay = int(sys.argv[1])
  wait_for_user(delay)
  screenshot = make_screenshot()
  mienfield = parse_mienfield(screenshot)
  count(mienfield)

if __name__ == '__main__':
  main()
