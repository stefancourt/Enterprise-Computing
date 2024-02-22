#!/bin/sh
BLOGGER_EPT=localhost:3000/posts
TEXT="My first ever posting"
echo "{\"text\":\"$TEXT\"}" > js
curl -X POST -H "Content-Type:application/json" -d @js \
    $BLOGGER_EPT