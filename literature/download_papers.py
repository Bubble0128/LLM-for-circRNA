"""Download licensed paper PDFs from the URLs in papers.json after network access is approved.

Uses inherited proxy settings and TLS verification. No alternate-host bypasses.
Existing PDFs are verified and retained. link_only entries are never downloaded.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--metadata', type=Path, default=Path(__file__).with_name('papers.json'))
    parser.add_argument('--id', action='append', help='Retry only a particular paper ID; may repeat')
    args = parser.parse_args()
    root = args.metadata.resolve().parent
    metadata = json.loads(args.metadata.read_text())
    output = root / 'pdf'
    output.mkdir(exist_ok=True)
    max_size = 40 * 1024 * 1024
    for p in metadata['papers']:
        if args.id and p['id'] not in args.id:
            continue
        if p['archive_policy'] == 'link_only':
            print(json.dumps({'id': p['id'], 'status': 'link_only'}))
            continue
        destination = output / (p['id'] + '.pdf')
        try:
            data = destination.read_bytes() if destination.exists() else None
            if data is None:
                request = Request(p['pdf_url'], headers={'User-Agent': 'Research-reference-archive/1.0'})
                with urlopen(request, timeout=30) as response:
                    data = response.read(max_size + 1)
            if len(data) > max_size:
                raise ValueError('PDF exceeds 40 MiB bound')
            if not data.startswith(b'%PDF-') or b'%%EOF' not in data[-4096:]:
                raise ValueError('Response is not a complete PDF; no file saved')
            digest = hashlib.sha256(data).hexdigest()
            if p.get('sha256') and destination.exists() and p['sha256'] != digest:
                raise ValueError('Existing file hash does not match manifest; file preserved')
            if not destination.exists():
                destination.write_bytes(data)
            p.update(local_file=str(destination.relative_to(root)), sha256=digest,
                     bytes=len(data), download_status='downloaded', download_error=None,
                     downloaded_from=p['pdf_url'],
                     verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
        except Exception as error:
            p.update(download_status='not_downloaded', download_error=str(error))
        print(json.dumps({'id': p['id'], 'status': p['download_status'], 'error': p.get('download_error')}))
        args.metadata.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
