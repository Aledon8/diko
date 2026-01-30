#!/bin/bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}diko demo${NC}"
echo "================================"

echo -e "${YELLOW}Checking dependencies...${NC}"
python3 --version >/dev/null || { echo -e "${RED}Python3 not found.${NC}"; exit 1; }
java -version >/dev/null 2>&1 || { echo -e "${RED}Java not found.${NC}"; exit 1; }
echo -e "${GREEN}Dependencies OK${NC}"

echo -e "${YELLOW}Installing diko...${NC}"
pip3 install -e . >/dev/null
echo -e "${GREEN}diko installed${NC}"

echo -e "${BLUE}Available distributions:${NC}"
diko list

echo -e "${BLUE}Hash verification test:${NC}"
echo "Hello, World!" > test.txt
diko verify test.txt
rm test.txt

echo -e "${GREEN}Demo complete.${NC}"
echo -e "${YELLOW}Try:${NC}"
echo "  diko download debian-netinst"