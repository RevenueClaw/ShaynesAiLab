#!/usr/bin/env bash
# Batch generate all 8 AI tool articles for the initial content push
set -euo pipefail

for i in $(seq 0 7); do
    echo "{\"index\":$i}" > /home/rock/shaynesailab/scripts/content_state.json
    echo "=== Generating topic $i/8 ==="
    cd /home/rock/shaynesailab && bash scripts/overnight/generate_content.sh 2>&1
    echo "=== Done topic $i/8 ==="
    sleep 5
done

echo "=== All articles generated ==="
ls /home/rock/shaynesailab/blog/*/index.html 2>/dev/null
echo "=== articles.json ==="
cat /home/rock/shaynesailab/blog/articles.json