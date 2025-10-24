#!/usr/bin/env python

# SPDX-FileCopyrightText: 2025 Tendry Lab
# SPDX-License-Identifier: Apache-2.0

import sys

if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")

import os
import argparse
from datetime import date

license_text_cpp = f"""/*
 * SPDX-FileCopyrightText: {date.today().year} Tendry Lab
 * SPDX-License-Identifier: Apache-2.0
 */"""

license_text_html = f"""<!--
SPDX-FileCopyrightText: {date.today().year} Tendry Lab
SPDX-License-Identifier: Apache-2.0
-->"""

license_text_python = f"""# SPDX-FileCopyrightText: {date.today().year} Tendry Lab
# SPDX-License-Identifier: Apache-2.0"""

SKIP_DIRS = {'.git', 'node_modules', 'build', 'dist', '.astro', 'coverage'}


def get_license(file_name: str) -> tuple[str, str]:
    """Returns (license_text, comment_start) tuple"""
    if file_name.endswith((".cpp", ".h", ".c", ".ts", ".tsx", ".js", ".css")):
        return (license_text_cpp, "/*")

    if file_name.endswith((".html", ".astro")):
        return (license_text_html, "<!--")

    if file_name.endswith(".py"):
        return (license_text_python, "#")

    return ("", "")


def verify_header(args: argparse.Namespace):
    for root, dirs, files in os.walk(args.path):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for file_name in files:
            license, comment_start = get_license(file_name)
            if license == "":
                continue

            file_path = os.path.join(root, file_name)

            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                if not content.startswith(comment_start):
                    if args.fmt:
                        with open(file_path, 'w', encoding='utf-8') as file:
                            file.write(license + '\n\n' + content)
                        print(f'Added Apache 2.0 header: {file_path}')
                    else:
                        print(f'Missing Apache 2.0 header: {file_path}', file=sys.stderr)

            except Exception as e:
                print(f'Error processing {file_path}: {e}', file=sys.stderr)


def parse_args():
    parser = argparse.ArgumentParser(description='Verify Apache 2.0 License Header')
    parser.add_argument('--path', help='Project path', required=True)
    parser.add_argument('--fmt', help='Add license header', action='store_true')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    verify_header(args)


if __name__ == '__main__':
    main()
