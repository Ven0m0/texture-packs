# Upscayl Texture Upscaler

A repository for upscaling textures and images using Upscayl, an AI-powered image upscaling tool that uses neural networks to enhance image quality while preserving details.

## Features

- AI-powered image upscaling using neural networks
- Support for various image formats (PNG, JPG, JPEG, WEBP, TGA, BMP)
- Multiple upscaling factors (2x, 3x, 4x)
- Batch processing capabilities
- Preserves image details while reducing noise

## Installation

### Install Upscayl binary

Run the setup script to install Upscayl and its dependencies:

```bash
chmod +x setup.sh
./setup.sh
```

### Install Python dependencies

This project uses UV for dependency management. Install the Python dependencies with:

```bash
uv sync
```

Or if you prefer to install manually:

```bash
uv pip install -e .
```

## Usage

After installation, you can use Upscayl via command line or the desktop application.

### Command Line Usage

```bash
upscayl-ncnn -i input_image.png -o output_image.png -s 2
```

Where:
- `-i`: Input image path
- `-o`: Output image path  
- `-s`: Scaling factor (2, 3, or 4)

### Desktop Application

Launch the desktop application with:
```bash
upscayl-desktop
```

## Requirements

- Linux system (Debian/Ubuntu, Fedora, or Arch-based distributions are supported by the install script)
- GPU with Vulkan support (optional, for faster processing)

