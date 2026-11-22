# Sony BRAVIA BF1 (2024 BRAVIA 3)

The BF1 profile is Android TV 12 / Google TV, API 31, 32-bit ARM
(`armeabi-v7a`, legacy `armeabi`), and xhdpi (320 dpi).

Vistaar 0.3's universal Android APK meets these installation requirements.
It contains no native `.so` libraries, so it does not require a 64-bit Android
runtime. It has an Android TV launcher entry and does not require a touchscreen.
Its minimum SDK is 23; target SDK 34 does **not** require Android 14 to install.
Do not lower the target SDK or add an ARM64-only ABI filter for this TV.

## Install

1. Download the [fork's BF1 APK](../releases/Vistaar-0.3-BRAVIA-BF1-debug.apk).
2. Transfer the APK to the TV using a USB drive or a file transfer app.
3. Open it in a file manager. Allow **Install unknown apps** for that file manager
   when prompted, then choose **Install**.
4. Open **Vistaar** from the TV's app list. Use the D-pad and OK to navigate.

With network debugging enabled and the computer authorized by the TV:

```sh
adb connect <TV-IP>:5555
adb install -r releases/Vistaar-0.3-BRAVIA-BF1-debug.apk
```

The fork APK's SHA-256 is
`c0c4b25b93cbf4e3e6a770685177f142fdf3db5049726014c92604ec345bd2ea`.
It is built from this fork with local Android debug signing. It includes explicit
Media3 API opt-ins and replaces an API 24 map call to preserve API 23 support.
The source build and lint pass (0 errors, 75 pre-existing warnings).

If updating an existing upstream installation, the unchanged
[upstream APK](../releases/Vistaar-0.3-debug.apk) retains its original signing key.
Its SHA-256 is
`d93a6f4b2e9ee74bd1c58faefafff2c79a79d674fe396ed23e906930fce3e3e8`.

If installation fails, retain the exact error from `adb install`. A signature
mismatch means the installed copy and new APK were signed with different keys.
The fork APK uses a different debug key from upstream. Use the same signing key
for updates that preserve sign-in and favourites;
uninstalling clears the app's private data. CI debug builds use a runner's debug
key and are not guaranteed to update an upstream APK or another CI build.

## Build and validate

Follow the [Android build setup](../README.md#build-from-source), then run:

```sh
./gradlew assembleDebug lintDebug
python3 scripts/check-bravia-apk.py app/build/outputs/apk/debug/app-debug.apk \
  --build-tools "$ANDROID_HOME/build-tools/34.0.0"
```

The **Android TV / BRAVIA BF1 APK** GitHub Actions workflow also builds, lints,
checks the APK, and uploads it as a downloadable artifact. These are packaging
checks, not a claim of testing on a physical BF1. Channel availability, DRM,
hardware decoding, and remote behavior still need validation on the TV.

## Other Sony televisions

[Upstream issue #14](https://github.com/fortysev-en/vistaar/issues/14) describes
the KD-43X7002G running Sony's proprietary Linux firmware, rather than Android
TV. That device cannot install this APK. Changing SDK levels or CPU ABI does not
add an Android runtime. This BF1 update does not resolve that separate request.
