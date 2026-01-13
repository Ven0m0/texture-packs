#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

echo "Upscayl Installation Script"
echo "============================="

# Detect the Linux distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$NAME
else
    echo "Cannot detect Linux distribution. This script supports Ubuntu/Debian, Fedora, and Arch-based systems."
    exit 1
fi

echo "Detected distribution: $DISTRO"

install_upscayl_arch() {
    echo "Installing Upscayl on Arch-based system..."
    
    # Check if paru is installed
    if ! command -v paru &> /dev/null; then
        echo "paru not found, checking for other AUR helpers..."
        
        if command -v yay &> /dev/null; then
            AUR_HELPER="yay"
        elif command -v pacman &> /dev/null; then
            AUR_HELPER="pacman"
        else
            echo "No AUR helper found. Installing paru..."
            git clone https://aur.archlinux.org/paru.git
            cd paru
            makepkg -si
            cd ..
            rm -rf paru
            AUR_HELPER="paru"
        fi
    else
        AUR_HELPER="paru"
    fi
    
    # Install Upscayl packages
    $AUR_HELPER -S --noconfirm upscayl-ncnn upscayl-desktop-git upscayl-models upscayl-models-desktop
    
    echo "Upscayl installed successfully on Arch-based system!"
}

install_upscayl_ubuntu_debian() {
    echo "Installing Upscayl on Ubuntu/Debian-based system..."
    
    # Add Upscayl PPA
    sudo add-apt-repository ppa:flexiondotorg/upscayl -y
    sudo apt update
    
    # Install Upscayl
    sudo apt install upscayl upscayl-cli -y
    
    echo "Upscayl installed successfully on Ubuntu/Debian-based system!"
}

install_upscayl_fedora() {
    echo "Installing Upscayl on Fedora-based system..."
    
    # Enable Copr repository for Upscayl
    sudo dnf copr enable atim/upscayl -y
    sudo dnf update -y
    
    # Install Upscayl
    sudo dnf install upscayl -y
    
    echo "Upscayl installed successfully on Fedora-based system!"
}

# Determine package manager and install accordingly
if [[ "$DISTRO" == *"Ubuntu"* ]] || [[ "$DISTRO" == *"Debian"* ]]; then
    install_upscayl_ubuntu_debian
elif [[ "$DISTRO" == *"Fedora"* ]]; then
    install_upscayl_fedora
elif [[ "$DISTRO" == *"Arch"* ]] || [[ "$DISTRO" == *"Manjaro"* ]]; then
    install_upscayl_arch
else
    echo "Unsupported distribution: $DISTRO"
    echo "Please install Upscayl manually from: https://github.com/upscayl/upscayl"
    exit 1
fi

# Verify installation
echo "Verifying installation..."
if command -v upscayl-ncnn &> /dev/null; then
    echo "✓ upscayl-ncnn is available"
else
    echo "⚠ Warning: upscayl-ncnn might not be available"
fi

if command -v upscayl-desktop &> /dev/null; then
    echo "✓ upscayl-desktop is available"
else
    echo "⚠ Warning: upscayl-desktop might not be available"
fi

echo ""
echo "Installation complete! You can now use Upscayl for image upscaling."
echo "For command-line usage: upscayl-ncnn -i input.png -o output.png -s 2"
echo "For GUI usage: upscayl-desktop"
