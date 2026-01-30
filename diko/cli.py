#!/usr/bin/env python3
"""
diko - CLI tool for downloading and verifying ISO images.
"""

import asyncio
import json
import os
import sys
from pathlib import Path

import click

from .downloader import download_file, verify_file_async

# Paths
LIBRARY_PATH = Path(__file__).parent / "library.json"


def load_library():
    """Load distribution library from JSON file."""
    try:
        with open(LIBRARY_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        click.echo("Distribution library not found.", err=True)
        sys.exit(1)
    except json.JSONDecodeError:
        click.echo("Invalid library.json format.", err=True)
        sys.exit(1)


@click.group()
@click.version_option(version="0.1.0")
def main():
    """diko - CLI for downloading and verifying ISO images."""
    pass


@main.command()
def list():
    """Show available distributions."""
    library = load_library()

    click.echo("Available distributions:\n")
    for distro_id, info in library.items():
        click.echo(f"{click.style(distro_id, fg='cyan', bold=True)}")
        click.echo(f"   Name: {info.get('name', 'n/a')}")
        mirrors = info.get('mirrors', [])
        click.echo(f"   Mirrors: {len(mirrors)}")
        sha = info.get('sha256')
        if sha and sha != 'placeholder':
            click.echo(f"   SHA256: {sha[:16]}...")
        size = info.get('size')
        if size:
            click.echo(f"   Size: {size}")
        click.echo("")


@main.command()
@click.argument('distro')
@click.option('--output', '-o', help='Output file name')
@click.option(
    '--mirror', '-m', type=int, default=0,
    help='Mirror index (default 0)',
)
def download(distro, output, mirror):
    """Download a distribution ISO image."""
    library = load_library()

    if distro not in library:
        click.echo(f"Distribution '{distro}' not found.", err=True)
        click.echo("Use 'diko list' to see available distributions.")
        sys.exit(1)

    info = library[distro]
    mirrors = info.get('mirrors', [])
    if not mirrors:
        click.echo("No mirrors found for this distribution.", err=True)
        sys.exit(1)
    if mirror < 0 or mirror >= len(mirrors):
        click.echo(f"Mirror #{mirror} does not exist.", err=True)
        sys.exit(1)

    url = mirrors[mirror]
    if not output:
        output = url.split('/')[-1]

    click.echo(f"Downloading: {info.get('name', distro)}")
    click.echo(f"URL: {url}")
    click.echo(f"Output: {output}\n")

    try:
        asyncio.run(download_file(url, output))
        click.echo(f"\n✅ Download finished: {output}")
    except KeyboardInterrupt:
        click.echo("\nDownload interrupted by user.")
        if os.path.exists(output):
            try:
                os.remove(output)
            except Exception:
                pass
        sys.exit(1)
    except Exception as e:
        click.echo(f"Download failed: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument('file')
@click.option('--distro', help='Verify against a known distribution')
def verify(file, distro):
    """Verify SHA256 hash of an ISO file."""
    if not os.path.exists(file):
        click.echo(f"File '{file}' not found.", err=True)
        sys.exit(1)

    click.echo(f"Computing SHA256 for {file}...")
    expected = None
    if distro:
        library = load_library()
        if distro not in library:
            click.echo(
                f"Distribution '{distro}' not found in library.",
                err=True,
            )
            sys.exit(1)
        expected = library[distro].get('sha256')
        if not expected or expected == 'placeholder':
            click.echo(f"Hash for '{distro}' is not set in library.")
            expected = None

    try:
        file_hash, is_valid = asyncio.run(verify_file_async(file, expected))
        click.echo(f"SHA256: {file_hash}")

        if distro and expected:
            if is_valid:
                click.echo("Hash matches. File is valid.")
            else:
                click.echo("Hash mismatch. File may be corrupted.")
                click.echo(f"Expected: {expected}")
                sys.exit(1)
    except Exception as e:
        click.echo(f"Error computing hash: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
