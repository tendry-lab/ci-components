#!/usr/bin/env python3

import pcbnew
import os
import sys


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: add_build_version.py <board_file.kicad_pcb>")
        sys.exit(1)

    board_path = sys.argv[1]
    project_id = os.environ.get("PROJECT_ID", "none")
    build_prefix = os.environ.get("BUILD_PREFIX", "0.0.0")
    build_number = os.environ.get("BUILD_NUMBER", "0")

    board = pcbnew.LoadBoard(board_path)

    new_text = f"Tendry Lab\n{project_id}\n{build_prefix}\n{build_number}"

    for item in board.GetDrawings():
        if isinstance(item, pcbnew.PCB_TEXT) and item.GetText().startswith("Tendry Lab"):
            item.SetText(new_text)

    pcbnew.SaveBoard(board_path, board)
