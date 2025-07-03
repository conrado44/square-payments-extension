#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Installing Square Payments Extension using UV...${NC}"

# Check if Hermit is installed
if ! command -v hermit &> /dev/null; then
    echo -e "${YELLOW}Hermit not found. Installing Hermit...${NC}"
    curl -fsSL https://github.com/cashapp/hermit/releases/download/stable/install.sh | bash
    echo -e "${GREEN}Hermit installed successfully.${NC}"
fi

# Activate Hermit environment
echo -e "${YELLOW}Activating Hermit environment...${NC}"
source bin/activate-hermit 2>/dev/null || {
    echo -e "${RED}Failed to activate Hermit environment.${NC}"
    echo -e "${YELLOW}Running Hermit initialization...${NC}"
    hermit init
    source bin/activate-hermit
}

# Install Python and UV using Hermit
echo -e "${YELLOW}Installing Python and UV via Hermit...${NC}"
hermit install

# Create a virtual environment using UV
echo -e "${YELLOW}Creating virtual environment...${NC}"
uv venv

# Install the package in development mode
echo -e "${YELLOW}Installing package in development mode...${NC}"
uv pip install -e .

echo -e "${GREEN}Installation complete!${NC}"
echo -e "${YELLOW}To activate the environment, run:${NC}"
echo -e "  source .venv/bin/activate"
echo -e "${YELLOW}Make sure to set the required environment variables:${NC}"
echo -e "  - SQUARE_APPLICATION_ID"
echo -e "  - SQUARE_LOCATION_ID"
echo -e "  - SQUARE_ACCESS_TOKEN"