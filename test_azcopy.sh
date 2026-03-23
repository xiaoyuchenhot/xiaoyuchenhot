#!/bin/bash
# Simple azcopy test script for Azure Blob Storage
# Prerequisites: azcopy installed
#
# Usage (account-level SAS URL from Azure portal > Storage account > Shared access signature):
#   SAS_URL="https://<account>.blob.core.windows.net/?sv=..." CONTAINER=mycontainer ./test_azcopy.sh
#
# Or set individual vars:
#   STORAGE_ACCOUNT=myaccount CONTAINER=mycontainer SAS_TOKEN="?sv=..." ./test_azcopy.sh

set -e

# Accept a full Blob service SAS URL and parse account + token from it
if [ -n "${SAS_URL:-}" ]; then
    # Extract storage account name from URL: https://<account>.blob.core.windows.net/...
    STORAGE_ACCOUNT="$(echo "$SAS_URL" | sed 's|https://||;s|\.blob.*||')"
    # Extract query string (everything from ? onwards)
    SAS_TOKEN="?$(echo "$SAS_URL" | cut -d'?' -f2-)"
fi

STORAGE_ACCOUNT="${STORAGE_ACCOUNT:-mystorageaccount}"
CONTAINER="${CONTAINER:-testcontainer}"
SAS_TOKEN="${SAS_TOKEN:-}"  # must start with '?'

BLOB_URL="https://${STORAGE_ACCOUNT}.blob.core.windows.net/${CONTAINER}"

echo "=== AzCopy Basic Test ==="
echo "Storage account: $STORAGE_ACCOUNT"
echo "Container: $CONTAINER"
echo ""

# 1. Check azcopy version
echo "[1] azcopy version"
azcopy --version
echo ""

# 2. Create a local test file
echo "[2] Creating test file"
echo "hello from azcopy test $(date)" > /tmp/azcopy_test.txt
echo "Created /tmp/azcopy_test.txt"
echo ""

# 3. Ensure container exists, then upload the test file
echo "[3] Creating container (if not exists)"
azcopy make "${BLOB_URL}${SAS_TOKEN}" 2>&1 | grep -v "already exists" || true
echo ""

echo "[3b] Uploading test file to blob storage"
azcopy copy /tmp/azcopy_test.txt "${BLOB_URL}/azcopy_test.txt${SAS_TOKEN}" --overwrite=true
echo ""

# 4. List blobs in container
echo "[4] Listing blobs in container"
azcopy list "${BLOB_URL}${SAS_TOKEN}"
echo ""

# 5. Download the file back
echo "[5] Downloading file back"
azcopy copy "${BLOB_URL}/azcopy_test.txt${SAS_TOKEN}" /tmp/azcopy_test_downloaded.txt --overwrite=true
echo ""

# 6. Verify content matches
echo "[6] Verifying content"
if diff /tmp/azcopy_test.txt /tmp/azcopy_test_downloaded.txt > /dev/null; then
    echo "PASS: uploaded and downloaded files match"
else
    echo "FAIL: files differ"
    exit 1
fi
echo ""

# 7. Delete the blob (cleanup)
echo "[7] Cleaning up blob"
azcopy remove "${BLOB_URL}/azcopy_test.txt${SAS_TOKEN}"
echo ""

echo "=== All tests passed ==="
