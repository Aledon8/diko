#!/bin/bash

set -e

echo "diko installation and test"
echo "================================"

python3 --version || { echo "Python3 not found."; exit 1; }
java -version || { echo "Java not found."; exit 1; }

echo "Dependencies OK"

echo "Installing diko..."
pip3 install -e .

echo "Compiling Java downloader..."
cd java
javac Downloader.java
cd ..

echo "Testing commands:"
echo "1. Version:" && diko --version
echo "2. Help:" && diko --help | head -10
echo "3. List:" && diko list
echo "4. Verify:" && echo "test content" > test_file.txt && diko verify test_file.txt && rm test_file.txt

echo "All tests passed."
echo "diko is ready to use."
echo "Try: diko download debian-netinst"