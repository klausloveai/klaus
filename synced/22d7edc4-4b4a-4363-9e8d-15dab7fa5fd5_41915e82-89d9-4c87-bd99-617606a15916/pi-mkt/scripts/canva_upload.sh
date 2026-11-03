#!/bin/bash
# Usage: canva_upload.sh <file> <upload_url from create-upload-url>
# Prints {"mediaId":"..."}. Each URL is single-use; get a fresh one per file.
curl -s -X POST -H "Content-Type: application/octet-stream" --data-binary @"$1" "$2"
echo
