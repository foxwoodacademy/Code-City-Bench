CONTROL: Boardroom Run & Control

This file documents the TUI and Termux widget for the Vertical AI boardroom.

Run TUI (terminal):
- cd /storage/emulated/0/RootBase/vertical_local
- python3 tui_control.py

One-tap Termux widget:
- bash /storage/emulated/0/RootBase/tools/bardildo/create_termux_widget.sh /storage/emulated/0/RootBase/vertical_local
- Add Termux:Widget to home screen and pick 'vertical_boardroom_widget'

Quick single command:
- bash run_boardroom_menu.sh

Notes:
- Uses $TMPDIR for logs and PID files. Use Termux storage permissions and avoid in-place edits on SD.
- Scripts use bash invocation (works if filesystem is noexec).