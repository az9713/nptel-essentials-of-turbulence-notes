"""List or run the Python programs printed in an Essentials of Turbulence chapter."""
from __future__ import annotations

import argparse
import html
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent


def chapter_programs(path):
    text = path.read_bytes().decode('utf-8')
    body = text.split('<!-- BOOK-CONTENT-START -->', 1)[1].split('<!-- BOOK-CONTENT-END -->', 1)[0]
    blocks = re.findall(r'<pre\b[^>]*>\s*<code([^>]*)>(.*?)</code>\s*</pre>', body, re.S)
    result = []
    for i, (attrs, source) in enumerate(blocks):
        if 'language-python' not in attrs:
            continue
        if i + 1 >= len(blocks) or 'language-python' in blocks[i + 1][0]:
            raise ValueError(f'{path.name}: Python listing lacks its printed output')
        clean = lambda value: html.unescape(re.sub(r'<!--[\s\S]*?-->', '', value)).replace('\r\n', '\n').replace('\r', '\n')
        result.append((clean(source), clean(blocks[i + 1][1]).strip('\n')))
    return result


def run_program(code, folder, name):
    path = Path(folder) / name
    path.write_bytes(code.encode('utf-8'))
    return subprocess.run([sys.executable, '-I', str(path)], cwd=folder,
                          capture_output=True, text=True, encoding='utf-8', timeout=180,
                          env={**os.environ, 'PYTHONIOENCODING': 'utf-8'})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--list', action='store_true', help='List chapter programs')
    group.add_argument('--chapter', type=int, choices=range(1, 21), metavar='1..20')
    args = parser.parse_args()
    paths = sorted(ROOT.glob('chapter-[0-9][0-9]-*.html'))
    if args.chapter is None:
        for path in paths:
            print(f'{int(path.name[8:10]):02d}: {path.stem[11:]} ({len(chapter_programs(path))} program(s))')
        return
    selected = [p for p in paths if int(p.name[8:10]) == args.chapter]
    if len(selected) != 1:
        parser.error('Expected one chapter file for the selected number')
    with tempfile.TemporaryDirectory(prefix='turbulence-lab-') as folder:
        for i, (code, _) in enumerate(chapter_programs(selected[0]), 1):
            run = run_program(code, folder, f'chapter_{args.chapter:02d}_{i}.py')
            print(run.stdout, end='')
            if run.stderr:
                print(run.stderr, end='', file=sys.stderr)
            if run.returncode:
                raise SystemExit(run.returncode)


if __name__ == '__main__':
    main()
