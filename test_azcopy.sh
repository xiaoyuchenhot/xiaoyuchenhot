#!/bin/bash
# Simple azcopy test script for Azure Blob Storage
# Prerequisites: azcopy installed, Azure credentials configured

set -e

# Configuration - set these before running
STORAGE_ACCOUNT="${STORAGE_ACCOUNT:-mystorageaccount}"
CONTAINER="${CONTAINER:-testcontainer}"
SAS_TOKEN="${SAS_TOKEN:-}"  # Set via env var or Azure portal > Storage > Shared access signature

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

# 3. Upload the test file
echo "[3] Uploading test file to blob storage"
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
