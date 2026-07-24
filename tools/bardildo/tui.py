#!/usr/bin/env python3
"""Simple curses TUI for Bardildo: browse projects and run buddies interactively
Termux-safe: runs subprocesses and streams output to screen.
"""
import curses
import subprocess
from pathlib import Path
import os

ROOT = os.environ.get('BARD_ROOT', '/storage/emulated/0/RootBase')
BARD = str(Path(__file__).parent / 'bardildo.py')

BUDDIES = ['dustbunny','summarizer','archivist','qa']


def run_buddy(buddy, target):
    cmd = ["python3", BARD, "--buddy", buddy, "--target", str(target)]
    return subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=300).decode(errors='ignore')


def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    root = Path(ROOT)
    projects = [p for p in root.iterdir() if p.is_dir()]
    sel_proj = 0
    sel_buddy = 0
    while True:
        stdscr.erase()
        stdscr.addstr(0,0,f"Bardildo TUI — root: {ROOT} — q to quit")
        stdscr.addstr(1,0,"Projects:")
        h, w = stdscr.getmaxyx()
        for i,p in enumerate(projects[:h-8]):
            prefix = '>' if i==sel_proj else ' '
            stdscr.addstr(2+i,0,f"{prefix} {i}. {p.name}")
        stdscr.addstr(h-6,0,"Buddies:")
        for j,b in enumerate(BUDDIES):
            prefix = '>' if j==sel_buddy else ' '
            stdscr.addstr(h-5+j,0,f"{prefix} {b}")
        stdscr.addstr(h-1,0,"Enter: run buddy | arrows: move | q: quit")
        stdscr.refresh()
        c = stdscr.getch()
        if c==ord('q'):
            break
        elif c==curses.KEY_DOWN:
            sel_proj = min(sel_proj+1, len(projects)-1)
        elif c==curses.KEY_UP:
            sel_proj = max(sel_proj-1, 0)
        elif c==curses.KEY_RIGHT:
            sel_buddy = min(sel_buddy+1, len(BUDDIES)-1)
        elif c==curses.KEY_LEFT:
            sel_buddy = max(sel_buddy-1, 0)
        elif c==10:  # Enter
            stdscr.erase()
            stdscr.addstr(0,0,f"Running {BUDDIES[sel_buddy]} on {projects[sel_proj]}... (press any key to return)")
            stdscr.refresh()
            try:
                out = run_buddy(BUDDIES[sel_buddy], projects[sel_proj])
            except Exception as e:
                out = str(e)
            stdscr.erase()
            for idx,line in enumerate(out.splitlines()[:h-1]):
                stdscr.addstr(idx,0,line[:w-1])
            stdscr.getch()


if __name__ == '__main__':
    curses.wrapper(main)
