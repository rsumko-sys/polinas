#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ARCHIVE_DIR="$ROOT_DIR/archives/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$ARCHIVE_DIR"
mv_count=0

echo "Archiving artifacts into: $ARCHIVE_DIR"

# Explicit known artifact paths
KNOWN=(
  "$ROOT_DIR/kharkiv_horse_clubs_map.html"
  "$ROOT_DIR/data/terrain/route_1625m_40pts.svg"
)

for f in "${KNOWN[@]}"; do
  if [ -f "$f" ]; then
    rel="${f#$ROOT_DIR/}"
    dest_dir="$ARCHIVE_DIR/$(dirname "$rel")"
    mkdir -p "$dest_dir"
    mv -v "$f" "$dest_dir/"
    mv_count=$((mv_count+1))
  fi
done

# Also pick up any top-level .html/.svg (excluding .git and virtualenvs)
find "$ROOT_DIR" -maxdepth 2 -type f \( -iname '*.html' -o -iname '*.svg' \) \
  -not -path "$ROOT_DIR/.git/*" -not -path "$ROOT_DIR/.venv/*" -not -path "$ROOT_DIR/.venv311/*" -not -path "$ARCHIVE_DIR/*" \
  -print0 | while IFS= read -r -d '' file; do
    # skip if already moved
    case "$file" in
      "$ROOT_DIR/kharkiv_horse_clubs_map.html"|"$ROOT_DIR/data/terrain/route_1625m_40pts.svg")
        ;;
      *)
        rel="${file#$ROOT_DIR/}"
        dest_dir="$ARCHIVE_DIR/$(dirname "$rel")"
        mkdir -p "$dest_dir"
        mv -v "$file" "$dest_dir/"
        mv_count=$((mv_count+1))
        ;;
    esac
done

echo "Archived $mv_count file(s) to $ARCHIVE_DIR"
echo "$ARCHIVE_DIR" > "$ROOT_DIR/.last_archive"

exit 0
