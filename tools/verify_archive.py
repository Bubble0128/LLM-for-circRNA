"""Check every file listed in FILE_MANIFEST.json; uses only Python stdlib."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    manifest = json.loads((ROOT / 'FILE_MANIFEST.json').read_text())
    problems = []
    for entry in manifest['files']:
        path = ROOT / entry['path']
        if not path.is_file():
            problems.append('Missing: ' + entry['path'])
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if path.stat().st_size != entry['bytes'] or digest != entry['sha256']:
            problems.append('Changed: ' + entry['path'])
    if problems:
        raise SystemExit('\n'.join(problems))
    print('PASS: %d archived files match size and SHA-256.' % len(manifest['files']))


if __name__ == '__main__':
    main()
