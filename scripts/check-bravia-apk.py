#!/usr/bin/env python3
"""Check a signed APK against the Sony BRAVIA BF1 Android TV 12 profile."""
import argparse
from pathlib import Path
import re
import subprocess
import zipfile


def check(apk, build_tools):
    subprocess.run([str(build_tools / 'apksigner'), 'verify', str(apk)], check=True)
    badging = subprocess.check_output(
        [str(build_tools / 'aapt'), 'dump', 'badging', str(apk)], text=True
    )
    errors = []
    sdk = re.search(r"^sdkVersion:'(\d+)'", badging, re.M)
    if not sdk or int(sdk[1]) > 31:
        errors.append('Minimum SDK must be API 31 or lower.')
    if not re.search(r"^package: name='com\.vistaar\.tv'", badging, re.M):
        errors.append('Expected package com.vistaar.tv.')
    if 'leanback-launchable-activity:' not in badging:
        errors.append('A TV launcher activity is required.')
    if re.search(r"^\s*(?:uses-feature|uses-implied-feature): name='android.hardware.touchscreen'", badging, re.M):
        errors.append('Touchscreen must not be required.')
    densities = re.search(r'^densities:(.*)$', badging, re.M)
    if not densities or "'320'" not in densities[1]:
        errors.append('Expected xhdpi (320 dpi) resources.')
    with zipfile.ZipFile(apk) as archive:
        libraries = {}
        for name in archive.namelist():
            parts = name.split('/')
            if len(parts) == 3 and parts[0] == 'lib' and parts[2].endswith('.so'):
                libraries.setdefault(parts[2], set()).add(parts[1])
        for name, abis in libraries.items():
            if not abis.intersection({'armeabi-v7a', 'armeabi'}):
                errors.append(f'{name} has no 32-bit ARM version: {sorted(abis)}')
    if errors:
        raise SystemExit('\n'.join(errors))
    print('PASS: signed APK, API 31 compatible, TV launcher, no required touch, xhdpi, 32-bit ARM compatible.')
    print('Native libraries: ' + (', '.join(sorted(libraries)) or 'none (ABI independent)'))
    print('This checks packaging; playback and remote operation still require a real TV test.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('apk', type=Path)
    parser.add_argument('--build-tools', required=True, type=Path,
                        help='Android SDK build-tools directory containing aapt and apksigner')
    args = parser.parse_args()
    check(args.apk.resolve(), args.build_tools.resolve())
