#!/usr/bin/env bash
# Builds DOUGA as a native Safari extension (macOS).
# Needs the full Xcode app from the Mac App Store — the Command Line Tools alone are not enough.
#
#   ./scripts/build-safari.sh
#
# Afterwards: Safari ▸ Settings ▸ Advanced ▸ "Show features for web developers",
# then Develop ▸ "Allow Unsigned Extensions", then enable DOUGA in Safari ▸ Settings ▸ Extensions.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EXT="$ROOT/dist/extension"
OUT="$ROOT/build/safari"
APP_NAME="DOUGA"
BUNDLE_ID="io.github.vurado0.douga"

if ! xcrun --find safari-web-extension-converter >/dev/null 2>&1; then
  echo "✗ Xcode not found."
  echo "  Install Xcode from the App Store, open it once, then run:"
  echo "  sudo xcode-select -s /Applications/Xcode.app/Contents/Developer"
  exit 1
fi

if [ ! -f "$EXT/manifest.json" ]; then
  echo "→ dist/extension missing, building it first"
  python3 "$ROOT/scripts/build.py"
fi

rm -rf "$OUT"
mkdir -p "$OUT"

echo "→ Converting the web extension into an Xcode project"
xcrun safari-web-extension-converter "$EXT" \
  --project-location "$OUT" \
  --app-name "$APP_NAME" \
  --bundle-identifier "$BUNDLE_ID" \
  --swift --macos-only --copy-resources --no-open --no-prompt --force

PROJECT="$(find "$OUT" -maxdepth 2 -name '*.xcodeproj' | head -1)"
echo "→ Building $PROJECT (signed to run locally)"
xcodebuild -project "$PROJECT" -scheme "$APP_NAME" -configuration Release \
  -derivedDataPath "$OUT/DerivedData" \
  CODE_SIGN_IDENTITY="-" CODE_SIGN_STYLE=Manual DEVELOPMENT_TEAM="" \
  build | tail -5

APP="$(find "$OUT/DerivedData/Build/Products/Release" -maxdepth 1 -name '*.app' | head -1)"
echo "→ Opening $APP once so Safari registers the extension"
open "$APP"

cat <<'EOF'

✓ Done. Last steps in Safari:
  1. Safari ▸ Settings ▸ Advanced ▸ tick "Show features for web developers"
  2. Develop menu ▸ tick "Allow Unsigned Extensions" (Safari asks for your password;
     this switch resets when Safari quits — re-tick it after a restart)
  3. Safari ▸ Settings ▸ Extensions ▸ enable "DOUGA" and allow it on youtube.com
EOF
