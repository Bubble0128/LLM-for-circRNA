"""Audit the downloaded MXfold2 v0.1.1 BPSEQ releases without extracting tar paths.

Preserve published split membership and all source labels. This is an inventory,
not a leakage-free train/test construction or verification of biological truth.
Run: python tools/audit_datasets.py
"""
import collections
import csv
import datetime
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import tarfile

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = 'https://github.com/mxfold/mxfold2/releases/download/v0.1.1/'


def parse_bpseq(text):
    rows = []
    for line in text.splitlines():
        fields = line.strip().split()
        if not fields or fields[0].startswith('#'):
            continue
        if len(fields) != 3:
            raise ValueError('Expected 3 BPSEQ columns')
        rows.append((int(fields[0]), fields[1], int(fields[2])))
    if not rows:
        raise ValueError('Empty record')
    n = len(rows)
    for position, (index, base, partner) in enumerate(rows, 1):
        if index != position or len(base) != 1:
            raise ValueError('Invalid index or nucleotide field')
        if not 0 <= partner <= n or partner == index:
            raise ValueError('Partner out of range or self-pair')
        if partner and rows[partner - 1][2] != index:
            raise ValueError('Asymmetric pairing labels')
    raw_sequence = ''.join(row[1] for row in rows)
    sequence = raw_sequence.upper().replace('T', 'U')
    partners = [row[2] for row in rows]
    pairs = [(i, j) for i, j in enumerate(partners, 1) if j > i]
    active_ends = []
    has_crossing = False
    for i, j in pairs:
        while active_ends and active_ends[-1] < i:
            active_ends.pop()
        if active_ends and j > active_ends[-1]:
            has_crossing = True
        active_ends.append(j)
    noncanonical = sum(sequence[i - 1] + sequence[j - 1] not in
                       {'AU', 'UA', 'CG', 'GC', 'GU', 'UG'} for i, j in pairs)
    return {'sequence': sequence, 'sequence_original': raw_sequence,
            'partner_index_1based': partners, 'length': n,
            'base_pair_count': len(pairs), 'crossing_pairs_present': has_crossing,
            'ambiguous_symbols': ''.join(sorted(set(sequence) - set('ACGU'))),
            'noncanonical_pair_count': noncanonical,
            'sequence_sha256': hashlib.sha256(sequence.encode()).hexdigest()}


def main():
    output = ROOT / 'processed'
    output.mkdir(exist_ok=True)
    audit = {'audited_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'normalization': 'Uppercase and T->U for normalized sequences and hashes; original sequence retained',
             'label_policy': 'Preserve pairs exactly; partner 0 means unpaired; no ambiguous-base filtering',
             'limitations': ['Exact sequence overlap only; no homology/family analysis',
                            'EVA pretraining overlap not audited',
                            'Linear RNA records are not labelled as circular',
                            'Canonicalized MXfold2 releases are not the full original databases'],
             'archives': {}, 'splits': {}, 'exact_sequence_overlap': []}
    hashes = {}
    for name in ('bpRNA', 'bpRNAnew', 'archiveII', 'RNAStrAlign'):
        path = ROOT / 'data' / (name + '.tar.gz')
        audit['archives'][name] = {'url': BASE_URL + path.name,
                                 'bytes': path.stat().st_size,
                                 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
        groups = collections.defaultdict(list)
        with tarfile.open(path) as archive:
            members = [m for m in archive.getmembers() if m.isfile()]
            member_names = {m.name for m in members}
            lists = {}
            for member in members:
                if member.name.endswith('.lst'):
                    entries = archive.extractfile(member).read().decode().splitlines()
                    lists[member.name] = {'entries': len(entries),
                                         'missing_members': sum(e not in member_names for e in entries)}
                elif member.name.endswith('.bpseq'):
                    split = name + ('_' + member.name.split('/')[-2] if name == 'bpRNA' else '')
                    groups[split].append(member)
            audit['archives'][name]['published_lists'] = lists
            for split, group in sorted(groups.items()):
                lengths, sequences, pairs_by_sequence = [], collections.Counter(), collections.defaultdict(set)
                counts = collections.Counter()
                errors = []
                with gzip.open(output / (split + '.jsonl.gz'), 'wt', encoding='utf-8') as stream:
                    for member in group:
                        try:
                            record = parse_bpseq(archive.extractfile(member).read().decode())
                        except (ValueError, UnicodeError) as error:
                            errors.append({'member': member.name, 'error': str(error)})
                            continue
                        record.update(id=Path(member.name).stem, split=split,
                                      source_archive=path.name, source_member=member.name,
                                      topology='not_verified_as_circular')
                        stream.write(json.dumps(record, separators=(',', ':')) + '\n')
                        lengths.append(record['length'])
                        digest = record['sequence_sha256']
                        sequences[digest] += 1
                        pairs_by_sequence[digest].add(tuple(record['partner_index_1based']))
                        counts['records_with_ambiguous_bases'] += bool(record['ambiguous_symbols'])
                        counts['records_with_crossing_pairs'] += record['crossing_pairs_present']
                        counts['noncanonical_pairs'] += record['noncanonical_pair_count']
                        counts['base_pairs'] += record['base_pair_count']
                hashes[split] = set(sequences)
                audit['splits'][split] = {
                    'archive_records': len(group), 'valid_records': len(lengths),
                    'min_length': min(lengths) if lengths else None,
                    'max_length': max(lengths) if lengths else None,
                    'unique_normalized_sequences': len(sequences),
                    'duplicate_sequence_records': sum(c - 1 for c in sequences.values()),
                    'sequences_with_multiple_pair_annotations': sum(len(v) > 1 for v in pairs_by_sequence.values()),
                    **counts, 'errors': errors}
    for a, b in itertools.combinations(hashes, 2):
        audit['exact_sequence_overlap'].append({'split_a': a, 'split_b': b,
                                                'unique_shared_sequences': len(hashes[a] & hashes[b])})
    (ROOT / 'dataset_audit.json').write_text(json.dumps(audit, indent=2) + '\n')
    with (ROOT / 'dataset_summary.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, lineterminator='\n', fieldnames=['split', 'archive_records', 'valid_records',
                              'min_length', 'max_length', 'unique_normalized_sequences',
                              'duplicate_sequence_records', 'records_with_ambiguous_bases',
                              'records_with_crossing_pairs', 'noncanonical_pairs'])
        writer.writeheader()
        for split, row in audit['splits'].items():
            writer.writerow({'split': split, **{key: row.get(key, 0) for key in writer.fieldnames if key != 'split'}})
    print(json.dumps({'splits': audit['splits'], 'nonzero_overlap': [v for v in audit['exact_sequence_overlap']
                      if v['unique_shared_sequences']]}, indent=2))


if __name__ == '__main__':
    main()
