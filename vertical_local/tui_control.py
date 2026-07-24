#!/usr/bin/env python3
"""Curses TUI to control the Vertical AI boardroom runner.
Run with: python3 tui_control.py (works under Termux)

Controls:
  s - start server
  x - stop server
  p - populate persona_map
  i - install deps
  o - print boardroom URL
  l - tail logs
  q - quit
"""

import curses
import os
import subprocess
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RUN_SCRIPT = os.path.join(SCRIPT_DIR, 'run_boardroom.sh')
TMPDIR = os.environ.get('TMPDIR', '/data/data/com.termux/files/usr/tmp')
LOG = os.path.join(TMPDIR, 'vertical_uvicorn.log')
PIDFILE = os.path.join(TMPDIR, 'vertical_uvicorn.pid')
HOST = os.environ.get('HOST', '127.0.0.1')
PORT = os.environ.get('PORT', '8000')


def run_cmd(cmd):
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True, timeout=60, universal_newlines=True)
        return out
    except subprocess.CalledProcessError as e:
        return e.output
    except Exception as e:
        return str(e)


def start_server():
    return run_cmd(f"bash '{RUN_SCRIPT}' start")


def stop_server():
    return run_cmd(f"bash '{RUN_SCRIPT}' stop")


def status_server():
    return run_cmd(f"bash '{RUN_SCRIPT}' status")


def install_deps():
    return run_cmd(f"bash '{RUN_SCRIPT}' install-deps")


def populate():
    return run_cmd(f"bash '{RUN_SCRIPT}' populate")


def tail_log(lines=20):
    if not os.path.exists(LOG):
        return "(no log file yet)"
    try:
        out = subprocess.check_output(f"tail -n {lines} '{LOG}'", shell=True, universal_newlines=True)
        return out
    except Exception as e:
        return str(e)


def draw_help(stdscr):
    h = [
        "Vertical AI — Boardroom Control TUI",
        "s: start | x: stop | p: populate persona_map | i: install deps",
        "l: tail log | o: print boardroom URL | q: quit",
        "",
        "Status:",
    ]
    for idx,line in enumerate(h):
        stdscr.addstr(idx+1, 2, line)


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(False)
    while True:
        stdscr.clear()
        draw_help(stdscr)
        try:
            status = status_server()
        except Exception as e:
            status = str(e)
        stdscr.addstr(8, 4, status[:curses.COLS-8])
        stdscr.refresh()

        c = stdscr.getch()
        if c == -1:
            time.sleep(0.1)
            continue
        ch = chr(c)
        if ch == 'q':
            break
        elif ch == 's':
            out = start_server()
            stdscr.addstr(12, 2, 'Start => ' + out.replace('\n',' ')[:curses.COLS-6])
        elif ch == 'x':
            out = stop_server()
            stdscr.addstr(12, 2, 'Stop => ' + out.replace('\n',' ')[:curses.COLS-6])
        elif ch == 'p':
            out = populate()
            stdscr.addstr(12, 2, 'Populate => ' + out.replace('\n',' ')[:curses.COLS-6])
        elif ch == 'i':
            out = install_deps()
            stdscr.addstr(12, 2, 'Install => ' + out.replace('\n',' ')[:curses.COLS-6])
        elif ch == 'l':
            out = tail_log(40)
            stdscr.clear(); stdscr.addstr(1,1,out[:curses.LINES*curses.COLS]); stdscr.addstr(curses.LINES-1,1,'Press any key to return'); stdscr.getch()
        elif ch == 'o':
            stdscr.addstr(12,2, f'Open URL: http://{HOST}:{PORT}/boardroom')
        stdscr.refresh()
        time.sleep(0.2)

if __name__ == '__main__':
    curses.wrapper(main)
