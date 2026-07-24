#!/usr/bin/env python3
"""DustBunny: entropy & duplicate hunter for RootBase

Usage: python3 dustbunny.py --path /storage/emulated/0/RootBase/<proj> --preview [--write]

Designed to be safe on Termux: uses $TMPDIR for temp work, avoids in-place sed, and never mutates unless --write is passed.
"""
import argparse
import os
from pathlib import Path
import hashlib
import json
from datetime import datetime, timedelta

TMPDIR = os.environ.get('TMPDIR') or '/data/data/com.termux/files/usr/tmp'
if not os.path.isdir(TMPDIR):
    TMPDIR = '/data/data/com.termux/files/usr/tmp'


def sha256(path: Path, block_size=65536):
    h = hashlib.sha256()
    try:
        with path.open('rb') as f:
            for blk in iter(lambda: f.read(block_size), b''):
                h.update(blk)
    except Exception:
        return None
    return h.hexdigest()


def analyze(path: Path, days_old=180, large_mb=50):
    files = list(path.rglob('*'))
    files = [f for f in files if f.is_file()]
    now = datetime.now()

    # duplicates by hash
    hash_map = {}
    large_files = []
    old_files = []

    for f in files:
        if f.stat().st_size == 0:
            continue
        h = sha256(f)
        if not h:
            continue
        hash_map.setdefault(h, []).append(str(f))
        size_mb = f.stat().st_size / (1024*1024)
        if size_mb >= large_mb:
            large_files.append({'path': str(f), 'size_mb': round(size_mb,1)})
        mtime = datetime.fromtimestamp(f.stat().st_mtime)
        if (now - mtime).days >= days_old:
            old_files.append({'path': str(f), 'days_old': (now - mtime).days})

    duplicates = [v for v in hash_map.values() if len(v) > 1]

    # entropy: files without README in top-level
    readme = (path / 'README.md').exists() or (path / 'README').exists()

    return {
        'path': str(path),
        'total_files': len(files),
        'duplicates': duplicates,
        'large_files': large_files,
        'old_files': old_files,
        'has_readme': readme,
    }


def preview_report(report: dict):
    lines = []
    lines.append(f"DustBunny scan for: {report['path']}")
    lines.append(f"Total files scanned: {report['total_files']}")
    lines.append('')
    if report['duplicates']:
        lines.append('Duplicates found (groups):')
        for g in report['duplicates'][:10]:
            lines.append(' - ' + ', '.join(g[:3]) + ("..." if len(g)>3 else ''))
    else:
        lines.append('No duplicates found.')
    lines.append('')
    if report['large_files']:
        lines.append('Large files:')
        for lf in report['large_files'][:10]:
            lines.append(f" - {lf['path']} ({lf['size_mb']} MB)")
    else:
        lines.append('No large files found.')
    lines.append('')
    if report['old_files']:
        lines.append('Old files (modified > threshold):')
        for of in report['old_files'][:10]:
            lines.append(f" - {of['path']} ({of['days_old']} days old)")
    else:
        lines.append('No old files found.')
    lines.append('')
    lines.append('README present: ' + ('Yes' if report['has_readme'] else 'No'))
    return '\n'.join(lines)


def write_archive_suggestion(report: dict, outdir: Path):
    # produce a safe archive plan under outdir (no auto-move)
    plan = {'archive_time': datetime.now().isoformat(), 'target': report['path'], 'actions': []}
    # suggest archiving old files and large files into a tarball path
    if report['old_files']:
        plan['actions'].append({'type': 'archive', 'paths': [o['path'] for o in report['old_files']], 'suggested_archive': str(outdir / (Path(report['path']).name + '_old_files.tar.gz'))})
    if report['large_files']:
        plan['actions'].append({'type': 'review_large', 'paths': [l['path'] for l in report['large_files']]})
    if report['duplicates']:
        plan['actions'].append({'type': 'review_duplicates', 'groups': report['duplicates'][:20]})
    # write plan to file
    out = outdir / (Path(report['path']).name + '_dustbunny_plan.json')
    out.write_text(json.dumps(plan, indent=2), encoding='utf-8')
    return out


def main():
    p = argparse.ArgumentParser(prog='dustbunny')
    p.add_argument('--path', default='.', help='Project path to scan')
    p.add_argument('--days', type=int, default=180, help='Age threshold in days for old files')
    p.add_argument('--large', type=int, default=50, help='Large file threshold in MB')
    p.add_argument('--preview', action='store_true', help='Print preview report')
    p.add_argument('--write-plan', action='store_true', help='Write archive suggestion plan into $TMPDIR (preview-only by default)')
    args = p.parse_args()
    target = Path(args.path).resolve()
    if not target.exists():
        print('Path not found:', target)
        return
    report = analyze(target, days_old=args.days, large_mb=args.large)
    if args.preview or not args.write_plan:
        print(preview_report(report))
    if args.write_plan:
        outdir = Path(TMPDIR)
        out = write_archive_suggestion(report, outdir)
        print('\nArchive plan written to:', out)

if __name__ == '__main__':
    main()
