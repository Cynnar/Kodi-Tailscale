#!/bin/bash

# Kodi Tailscale Addon - Package Script
# Creates a distributable ZIP file for the addon

ADDON_ID="plugin.program.tailscale"
VERSION=$(grep 'version=' addon.xml | sed 's/.*version="\([^"]*\)".*/\1/')
OUTPUT_FILE="${ADDON_ID}-${VERSION}.zip"

echo "Packaging ${ADDON_ID} version ${VERSION}..."

# Remove old zip if exists
if [ -f "../${OUTPUT_FILE}" ]; then
    rm "../${OUTPUT_FILE}"
    echo "Removed old package file"
fi

# Create zip excluding unnecessary files
cd ..
zip -r "${OUTPUT_FILE}" "${ADDON_ID}/" \
    -x "*/__pycache__/*" \
    -x "*/.git/*" \
    -x "*/bin/*" \
    -x "*/state/*" \
    -x "*/logs/*" \
    -x "*/.gitignore" \
    -x "*/package.sh" \
    -x "*.pyc" \
    -x "*.pyo" \
    -x "*.DS_Store" \
    -x "*/addon_data/*" \
    -x "*/nas_sources.json"

echo ""
echo "Package created: ${OUTPUT_FILE}"
echo "Size: $(du -h ${OUTPUT_FILE} | cut -f1)"
echo ""
echo "Installation instructions:"
echo "1. Copy ${OUTPUT_FILE} to your Kodi device"
echo "2. In Kodi: Settings > Add-ons > Install from zip file"
echo "3. Select ${OUTPUT_FILE}"
echo ""
