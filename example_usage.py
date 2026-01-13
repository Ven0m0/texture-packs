#!/usr/bin/env python3
"""
Example usage of the Upscayl Image Upscaler
This script demonstrates how to use the upscaler functionality.
"""

import subprocess
import sys
from pathlib import Path

def create_example_image():
    """Create a small example image for testing."""
    try:
        from PIL import Image, ImageDraw
        
        # Create a simple test image
        img = Image.new('RGB', (100, 100), color='red')
        draw = ImageDraw.Draw(img)
        draw.ellipse((25, 25, 75, 75), fill='blue')
        draw.rectangle((10, 10, 40, 40), fill='green')
        
        img.save('/workspace/example_input.png')
        print("Created example image: example_input.png")
        return True
    except ImportError:
        print("Pillow not available, skipping example image creation.")
        print("To create an example, install Pillow: pip install Pillow")
        return False

def run_upscaler_example():
    """Run an example upscaling operation."""
    input_file = Path('/workspace/example_input.png')
    output_file = Path('/workspace/example_output.png')
    
    if not input_file.exists():
        print(f"Input file does not exist: {input_file}")
        return False
    
    # Run the upscaler
    cmd = [
        sys.executable, '/workspace/upscaler.py',
        '-i', str(input_file),
        '-o', str(output_file),
        '-s', '2'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("Upscaling completed successfully!")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during upscaling: {e}")
        print(f"stderr: {e.stderr}")
        return False

def main():
    print("Upscayl Image Upscaler - Example Usage")
    print("======================================")
    
    # Create example image
    if create_example_image():
        # Run upscaling example
        if run_upscaler_example():
            print("\nExample completed successfully!")
            print(f"Original: /workspace/example_input.png")
            print(f"Upscaled: /workspace/example_output.png")
        else:
            print("\nExample failed during upscaling.")
    else:
        print("\nExample skipped due to missing dependencies.")
    
    print("\nTo use the upscaler with your own images:")
    print("Single image: python upscaler.py -i input.png -o output.png -s 2")
    print("Batch mode: python upscaler.py -d input_dir -o output_dir -s 3")

if __name__ == "__main__":
    main()