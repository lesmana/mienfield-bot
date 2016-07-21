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

def convertcrop(screenshot, w, h):
  croppedfilename = 'screenshotcropped.png'
  result = run('convert {} -crop {}x{}+0+1 +repage {}'.format(screenshot, w, h, croppedfilename))
  if result.returncode:
    raise Exception('convert crop failed')
  return croppedfilename

def parse_mienfield_for_what(screenshot, what):
  try:
    poses = visgrep(screenshot, 'images/{}.png'.format(what))
  except Exception:
    return {}
  mienfield_what = {}
  for rx, ry in poses:
    cx = rx // 32
    cy = ry // 32
    mienfield_what[(cx, cy)] = what
  return mienfield_what

def parse_mienfield(screenshot):
  [(rbx, _)] = visgrep(screenshot, 'images/sidebar.png')
  [(_, rby)] = visgrep(screenshot, 'images/teleport.png')
  bx = rbx - (rbx % 32)
  by = rby - (rby % 32)
  screenshotcropped = convertcrop(screenshot, bx, by)
  mienfield = {}
  for what in ['1', '2', '3', '4', '5', '6', 'closed', 'open', 'mine']:
    mienfield_what = parse_mienfield_for_what(screenshotcropped, what)
    mienfield.update(mienfield_what)
  return mienfield

def main():
  print('put mienfield fullscreen')
  delay = 3
  if len(sys.argv) > 1:
    delay = int(sys.argv[1])
  wait_for_user(delay)
  screenshot = make_screenshot()
  mienfield = parse_mienfield(screenshot)
  for key in sorted(mienfield):
    print(key, mienfield[key])

if __name__ == '__main__':
  main()
