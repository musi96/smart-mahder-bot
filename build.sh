#!/bin/bash
set -o errexit

# Install system dependencies for Pillow
apt-get update
apt-get install -y \
    libjpeg-dev \
    libtiff5-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    zlib1g-dev

# Install Python packages
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
