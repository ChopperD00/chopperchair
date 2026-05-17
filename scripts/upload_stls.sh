#!/usr/bin/env bash
# upload_stls.sh — Push all local STL files into ChopperD00/chopperchair
# Run this from your local machine (unicron) where the STLs live.
#
# Usage:
#   chmod +x scripts/upload_stls.sh
#   ./scripts/upload_stls.sh
#
# Requirements: git, with GitHub SSH or HTTPS auth already working.
# The script clones the repo fresh, copies STLs in, and pushes.

set -e

REPO_URL="git@github.com:ChopperD00/chopperchair.git"
STL_SOURCE="/Users/unicron/Chopper Chair/stl"
WORK_DIR="/tmp/chopperchair-stl-upload"

echo "ChopperChair STL Upload Script"
echo "================================"

# Clean slate
rm -rf "$WORK_DIR"
git clone "$REPO_URL" "$WORK_DIR"
cd "$WORK_DIR"

# Copy build1 STLs
echo "Copying Build 1 (Full Print) STLs..."
mkdir -p stl/build1_fullprint
cp "$STL_SOURCE/build1_fullprint"/*.stl stl/build1_fullprint/ 2>/dev/null && echo "  ✓ build1_fullprint" || echo "  ✗ No STLs found in build1_fullprint"

# Copy build2 STLs
echo "Copying Build 2 (Hybrid) STLs..."
mkdir -p stl/build2_hybrid
cp "$STL_SOURCE/build2_hybrid"/*.stl stl/build2_hybrid/ 2>/dev/null && echo "  ✓ build2_hybrid" || echo "  ✗ No STLs found in build2_hybrid"

# Also copy any loose STLs from the stl/ root
echo "Copying root-level STLs..."
cp "$STL_SOURCE"/*.stl stl/ 2>/dev/null && echo "  ✓ root STLs" || echo "  (none at root level)"

# Check if anything changed
if git diff --quiet && git diff --cached --quiet; then
  echo "No new STLs to push — repo already up to date."
  exit 0
fi

# Stage and push
git add stl/
git status --short
STL_COUNT=$(git diff --cached --name-only | grep -c '\.stl$' || true)
git commit -m "add STL files: Build 1 (full print) + Build 2 (hybrid) — ${STL_COUNT} files"
git push origin main

echo ""
echo "Done! STLs pushed to github.com/ChopperD00/chopperchair"
echo "Verify: https://github.com/ChopperD00/chopperchair/tree/main/stl"

# Cleanup
rm -rf "$WORK_DIR"
echo "Temp dir cleaned up."
