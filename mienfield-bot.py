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

def screenshot():
  result = run('scrot screenshot.png')
  if result.returncode:
    raise Exception('scrot failed')

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

def main():
  print('put mienfield fullscreen')
  delay = 3
  if len(sys.argv) > 1:
    delay = int(sys.argv[1])
  wait_for_user(delay)
  screenshot()
  try:
    [(tx, ty)] = visgrep('screenshot.png', 'images/teleport.png')
  except Exception:
    print('failed to find teleporter')
    print('are you sure that mienfield is on screen?')
    sys.exit(1)
  else:
    click(tx + 10, ty + 10)

if __name__ == '__main__':
  main()
