"""Download or verify the four pinned MXfold2 source archives using stdlib only."""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    value = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    sources = json.loads((ROOT / 'dataset_audit.json').read_text())['archives']
    (ROOT / 'data').mkdir(exist_ok=True)
    for name, source in sources.items():
        path = ROOT / 'data' / (name + '.tar.gz')
        if not path.exists():
            if args.verify_only:
                raise SystemExit('Missing archive: ' + str(path))
            partial = path.with_suffix(path.suffix + '.part')
            try:
                size = 0
                with urllib.request.urlopen(source['url'], timeout=60) as response, partial.open('wb') as output:
                    while True:
                        block = response.read(1024 * 1024)
                        if not block:
                            break
                        size += len(block)
                        if size > source['bytes']:
                            raise ValueError('Download exceeds recorded size: ' + name)
                        output.write(block)
                if size != source['bytes'] or digest(partial) != source['sha256']:
                    raise ValueError('Downloaded archive does not match recorded version: ' + name)
                partial.replace(path)
            finally:
                partial.unlink(missing_ok=True)
        if path.stat().st_size != source['bytes'] or digest(path) != source['sha256']:
            raise SystemExit('Checksum or size mismatch; existing file preserved: ' + str(path))
        print('PASS', path.name, source['sha256'])


if __name__ == '__main__':
    main()
