"""Execute every printed chapter program and compare its displayed output."""
from __future__ import annotations

import datetime
import difflib
import hashlib
import json
from pathlib import Path
import re
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from numerical_lab import chapter_programs, run_program


def main():
    results = {}
    with tempfile.TemporaryDirectory(prefix='turbulence-code-checks-') as folder:
        for path in sorted(ROOT.glob('chapter-[0-9][0-9]-*.html')):
            checks = []
            for i, (code, expected) in enumerate(chapter_programs(path), 1):
                run = run_program(code, folder, f'chapter_{path.name[8:10]}_{i}.py')
                actual = run.stdout.rstrip('\n')
                passed = run.returncode == 0 and actual == expected
                stderr = re.sub(r'[A-Za-z]:[\\/][^\n]*', '<local path>', run.stderr[-1500:])
                checks.append({'listing': i, 'returncode': run.returncode, 'output_matches': passed,
                               'listing_sha256': hashlib.sha256(code.encode()).hexdigest(),
                               'stdout_sha256': hashlib.sha256(run.stdout.encode()).hexdigest(),
                               'stderr': stderr,
                               'output_diff': [] if passed else list(difflib.unified_diff(expected.splitlines(), actual.splitlines(), fromfile='printed', tofile='executed'))[:45]})
            status = 'passed' if checks and all(c['output_matches'] for c in checks) else 'failed'
            results[path.name] = {'status': status, 'checks': checks}
            print(path.name, status, flush=True)
    passed = len(results) == 20 and all(r['status'] == 'passed' for r in results.values())
    report = {'checked_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'status': 'passed' if passed else 'failed',
              'scope': 'Actual isolated execution and exact printed-output comparison after newline normalization and terminal-newline trimming; not a new scientific review',
              'python': sys.version, 'chapters': results}
    (ROOT / 'chapter-code-validation.json').write_bytes((json.dumps(report, indent=2) + '\n').encode())
    raise SystemExit(0 if passed else 1)


if __name__ == '__main__':
    main()
