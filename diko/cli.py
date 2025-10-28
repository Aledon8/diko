import argparse
import json
import subprocess
import sys
from pathlib import Path
from .utils import sha256sum

LIBRARY_FILE = Path(__file__).parent / "library.json"
JAVA_DIR = Path(__file__).parent.parent / "java"


def load_library():
    if not LIBRARY_FILE.exists():
        return {}
    with open(LIBRARY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def cmd_list(library):
    if not library:
        print("No distros available in library.json")
        return
    print("Available Linux distros:\n")
    for key, info in library.items():
        print(f"  {key:<10} {info['name']}")


def cmd_install(library, name, directory):
    if name not in library:
        print(f"Error: distro '{name}' not found in library.json")
        return

    distro = library[name]
    mirrors = distro["mirrors"]
    iso_url = mirrors[0] if mirrors else None
    checksum = distro.get("sha256")

    if not iso_url:
        print(f"No mirrors available for {name}")
        return

    target_dir = Path(directory).expanduser().resolve()
    target_dir.mkdir(parents=True, exist_ok=True)
    filename = iso_url.split("/")[-1]
    filepath = target_dir / filename

    print(f"Downloading {distro['name']}")
    print(f"From: {iso_url}")
    print(f"To:   {filepath}\n")

    try:
        process = subprocess.Popen(
            ["java", "-cp", str(JAVA_DIR), "Downloader", iso_url, str(filepath)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=0
        )

        while True:
            char = process.stdout.read(1)
            if not char and process.poll() is not None:
                break
            if char:
                sys.stdout.write(char.decode("utf-8", errors="ignore"))
                sys.stdout.flush()

        process.wait()
        if process.returncode != 0:
            print("Java downloader failed.")
            return

    except FileNotFoundError:
        print("Java runtime not found. Please install OpenJDK (e.g. `sudo pacman -S jre-openjdk`).")
        return

    # Проверка sha256
    if checksum and checksum != "placeholder":
        print("\nVerifying SHA256...")
        file_hash = sha256sum(filepath)
        if file_hash.lower() == checksum.lower():
            print("Checksum verified, file is authentic.")
        else:
            print("Checksum mismatch! The file may be corrupted or tampered with.")
    else:
        print("\nNo checksum available in library.json (skipped verification).")


def main():
    parser = argparse.ArgumentParser(
        prog="diko",
        description="Linux ISO package manager",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""Examples:
  diko list
  diko install ubuntu --dir ~/Downloads

"""
    )

    parser.add_argument(
        "--version",
        action="version",
        version="diko 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command", title="Commands")

    # list
    subparsers.add_parser(
        "list",
        help="Show all available distros"
    )

    # install
    install_parser = subparsers.add_parser(
        "install",
        help="Download a Linux distro ISO"
    )
    install_parser.add_argument("name", help="Name of the distro (e.g. ubuntu, debian)")
    install_parser.add_argument(
        "--dir",
        default=".",
        help="Directory to save the ISO (default: current directory)"
    )

    args = parser.parse_args()
    library = load_library()

    if args.command == "list":
        cmd_list(library)
    elif args.command == "install":
        cmd_install(library, args.name, args.dir)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
