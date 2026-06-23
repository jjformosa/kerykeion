docker run -it -v .:/app -w /app \
    python:3.11-bookworm \
    sh
    pip3 install kerykeion -t python/lib/python3.11/site-packages/ \
    zip -r kerykeion_layer.zip python/