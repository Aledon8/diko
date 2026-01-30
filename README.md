<p align="center">
  <img src="assets/Image.png" alt="diko logo" width="150"/>
</p>

# 💿 diko

**diko** — A powerful CLI tool for downloading and verifying Linux distribution ISO images.

---

## Features
- **Library of Distributions**: Access popular Linux distros (Ubuntu, Debian, Fedora, Arch, etc.) instantly.
- **High-Speed Download**: Built-in Java downloader with a visual progress bar.
- **Integrity Check**: Automatic SHA256 verification to ensure your ISO is safe and uncorrupted.
- **Smart Mirror Selection**: Multiple mirrors for each distribution to ensure availability.

## Requirements
- **Python 3.11+**

## Installation

### 🍺 Homebrew (macOS)
The recommended way to install on macOS.

```bash
brew tap aledon8/diko-dev
brew install diko
```

Or install directly from the formula:

```bash
brew install https://raw.githubusercontent.com/Aledon8/diko/main/Formula/diko.rb
```

### 🐧 Debian/Ubuntu (APT)
For Debian-based systems, we provide a pre-built `.deb` package.

1. Go to the [Releases](https://github.com/Aledon8/diko/releases) page.
2. Download the latest `diko_x.x.x_all.deb` file.
3. Install it using `apt` (this will automatically handle dependencies):

```bash
sudo apt install ./diko_*.deb
```

### From Source (Developers)
If you want to contribute or run the latest development version:

```bash
git clone https://github.com/Aledon8/diko.git
cd diko
pip install .
```

## Usage

### List available distributions
See what's available to download:
```bash
diko list
```

### Download an ISO
Download the latest Ubuntu LTS:
```bash
diko download ubuntu
```

Specify an output filename:
```bash
diko download ubuntu -o ubuntu-24.04.iso
```

Choose a specific mirror (if the default is slow):
```bash
diko download ubuntu -m 1
```

### Verify an ISO
Check the integrity of a downloaded file:
```bash
diko verify ubuntu-24.04.iso --distro ubuntu
```

## ❤️ Acknowledgements
A huge thank you to everyone who has contributed to **diko**!

- **Contributors**: Thank you for your code, bug reports, and suggestions.
- **Community**: Thanks to everyone who uses diko and helps make it better.
- **Open Source**: Built on the shoulders of giants like Python and Click.

Your support keeps this project alive and open for everyone.

## 📄 License
This project is licensed under the **Apache-2.0** License.
