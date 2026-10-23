"""Check the public book inventory, chapter-body digests, and evidence links."""
from __future__ import annotations

import datetime
import hashlib
import json
from pathlib import Path
import re

from build_book import original_body, read

ROOT = Path(__file__).resolve().parents[1]


def main():
    failures = []
    manifest = json.loads(read(ROOT / 'source-manifest.json'))
    completion = json.loads(read(ROOT / 'completion.json'))
    editorial = json.loads(read(ROOT / 'editorial-review-summary.json'))
    paths = sorted(ROOT.glob('chapter-[0-9][0-9]-*.html'))
    if len(paths) != 20 or len(manifest['chapters']) != 20:
        failures.append('Expected 20 chapter files and manifest entries')
    listings = solutions = 0
    for path in paths:
        body = original_body(read(path))
        actual = hashlib.sha256(body.encode()).hexdigest()
        if completion['chapter_body_sha256'].get(path.name) != actual:
            failures.append(f'{path.name}: baseline chapter-body mismatch')
        if not path.with_suffix('.meta.json').is_file():
            failures.append(f'{path.name}: missing source sidecar')
        listings += len(re.findall(r'<code[^>]*class="language-python"', body))
        solutions += len(re.findall(r'<summary\b[^>]*>\s*(?:Solution|Worked solution)', body, re.I))
    required = ('README.md', 'WORKFLOW.md', 'index.html', 'source-map.html', 'references.html',
                'numerical-lab.html', 'numerical_lab.py', 'source-validation-summary.json',
                'chapter-code-validation.json', 'reader-validation.json', 'assets/site-preview.png')
    for name in required:
        if not (ROOT / name).is_file():
            failures.append(f'Missing public file: {name}')
    for name in ('README.md', 'WORKFLOW.md'):
        for target in re.findall(r'\]\(([^)]+)\)', read(ROOT / name)):
            if '://' not in target and target != 'package-validation.json' and not (ROOT / target.split('#')[0]).exists():
                failures.append(f'{name}: broken relative link {target}')
    if editorial['final_independent_signoff_pending_chapters'] != [3, 6, 16, 17, 18, 19, 20]:
        failures.append('Known independent-review gaps must remain explicit')
    report = {'checked_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'status': 'failed' if failures else 'passed', 'scope': 'Public package inventory and exact chapter-body preservation, not scientific acceptance',
              'chapter_count': len(paths), 'python_listings': listings, 'worked_solution_disclosures': solutions,
              'chapter_bodies_preserved_from': '31a41f2', 'failures': failures,
              'final_independent_signoff_pending_chapters': editorial['final_independent_signoff_pending_chapters']}
    (ROOT / 'package-validation.json').write_bytes((json.dumps(report, indent=2) + '\n').encode())
    print(json.dumps(report, indent=2))
    raise SystemExit(1 if failures else 0)


if __name__ == '__main__':
    main()
