# 🐧 diko

**diko** — CLI tool for downloading and verifying Linux distribution ISO images.

## Features
- 📋 Library of popular distributions
- 🚀 Fast download (Java Downloader with progress bar)
- 🔍 Integrity check (SHA256)
- 🪞 Multiple mirrors for each distribution

## Requirements
- Python 3.8+
- Java 8+ (for the downloader)

## Installation
```bash
git clone https://github.com/aleksandr/diko.git
cd diko
pip install -e .
```

## Usage

### List distributions
```bash
diko list
```

### Download ISO
```bash
diko download ubuntu
diko download ubuntu -o ubuntu-24.04.iso
diko download ubuntu -m 1  # choose mirror #1
```

### Verify hash
```bash
diko verify ubuntu-24.04.iso
diko verify ubuntu-24.04.iso --distro ubuntu
```

## Architecture
- Python CLI (`diko/cli.py`) — `list`, `download`, `verify` commands
- Java Downloader (`java/Downloader.java`) — downloading with progress indicator
- Library (`diko/library.json`) — list of distributions, mirrors, sizes

## Makefile (optional)
After adding Makefile, the following commands are available:
```bash
make help
make install
make java
make build
```

## License
Apache-2.0
