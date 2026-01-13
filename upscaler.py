#!/usr/bin/env python3
"""
Upscayl Image Upscaler
A Python wrapper for the Upscayl CLI tool that provides batch processing
and easy-to-use options for upscaling images.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from typing import List, Optional


def validate_scale_factor(scale: int) -> bool:
    """Validate that scale factor is 2, 3, or 4."""
    return scale in [2, 3, 4]


def get_supported_formats() -> List[str]:
    """Return list of supported image formats."""
    return ['.png', '.jpg', '.jpeg', '.webp', '.tga', '.bmp']


def find_images_in_directory(directory: Path, recursive: bool = False) -> List[Path]:
    """Find all supported image files in a directory."""
    supported_formats = get_supported_formats()
    images = []
    
    glob_method = directory.rglob if recursive else directory.glob
    for ext in supported_formats:
        images.extend(glob_method(f'*{ext}'))
        images.extend(glob_method(f'*{ext.upper()}'))  # Also check uppercase
    
    return images


def upscale_single_image(input_path: Path, output_path: Path, scale_factor: int, gpu: bool = True) -> bool:
    """
    Upscale a single image using Upscayl.
    
    Args:
        input_path: Path to input image
        output_path: Path to save upscaled image
        scale_factor: Scale factor (2, 3, or 4)
        gpu: Whether to use GPU acceleration (default: True)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        cmd = ['upscayl-ncnn', '-i', str(input_path), '-o', str(output_path), '-s', str(scale_factor)]
        
        if not gpu:
            cmd.append('-g')  # Disable GPU acceleration
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"Successfully upscaled: {input_path.name} -> {output_path.name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error upscaling {input_path.name}: {e.stderr}")
        return False
    except FileNotFoundError:
        print("Error: Upscayl not found. Please install Upscayl first.")
        return False


def upscale_batch(input_dir: Path, output_dir: Optional[Path], scale_factor: int, 
                  recursive: bool = False, gpu: bool = True) -> int:
    """
    Upscale a batch of images.
    
    Args:
        input_dir: Directory containing input images
        output_dir: Directory to save upscaled images (optional)
        scale_factor: Scale factor (2, 3, or 4)
        recursive: Whether to search subdirectories recursively
        gpu: Whether to use GPU acceleration
    
    Returns:
        Number of successfully upscaled images
    """
    images = find_images_in_directory(input_dir, recursive)
    
    if not images:
        print(f"No supported images found in {input_dir}")
        return 0
    
    # Create output directory if specified and doesn't exist
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    total_count = len(images)
    
    print(f"Found {total_count} images to upscale...")
    
    for i, img_path in enumerate(images, 1):
        print(f"Processing ({i}/{total_count}): {img_path.name}")
        
        # Determine output path
        if output_dir:
            output_path = output_dir / f"{img_path.stem}_upscaled_x{scale_factor}{img_path.suffix}"
        else:
            output_path = input_dir / f"{img_path.stem}_upscaled_x{scale_factor}{img_path.suffix}"
        
        if upscale_single_image(img_path, output_path, scale_factor, gpu):
            success_count += 1
    
    print(f"\nCompleted! Successfully upscaled {success_count} out of {total_count} images.")
    return success_count


def main():
    parser = argparse.ArgumentParser(
        description="Upscayl Image Upscaler - A tool for upscaling images using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -i image.jpg -o upscaled_image.jpg -s 2
  %(prog)s -d /path/to/images -s 3
  %(prog)s -d /path/to/images -o /path/to/output -s 2 --recursive
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-i', '--input', type=Path, 
                            help='Input image file')
    input_group.add_argument('-d', '--directory', type=Path, 
                            help='Directory containing images to upscale')
    
    # Output options
    parser.add_argument('-o', '--output', type=Path,
                        help='Output file or directory for upscaled images')
    
    # Scaling options
    parser.add_argument('-s', '--scale', type=int, default=2,
                        choices=[2, 3, 4],
                        help='Scale factor (2, 3, or 4) [default: 2]')
    
    # Processing options
    parser.add_argument('--recursive', action='store_true',
                        help='Process subdirectories recursively')
    parser.add_argument('--cpu', action='store_true',
                        help='Use CPU instead of GPU for processing')
    
    args = parser.parse_args()
    
    # Validate scale factor
    if not validate_scale_factor(args.scale):
        print(f"Error: Scale factor must be 2, 3, or 4. Got: {args.scale}")
        sys.exit(1)
    
    # Check if upscayl is available
    try:
        subprocess.run(['upscayl-ncnn', '--help'], 
                      capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: Upscayl not found. Please install Upscayl first by running:")
        print("  chmod +x setup.sh")
        print("  ./setup.sh")
        sys.exit(1)
    
    gpu = not args.cpu  # Use GPU unless --cpu is specified
    
    if args.input:
        # Single image mode
        if not args.input.exists():
            print(f"Error: Input file does not exist: {args.input}")
            sys.exit(1)
        
        if args.output is None:
            # Generate output filename automatically
            output_path = args.input.parent / f"{args.input.stem}_upscaled_x{args.scale}{args.input.suffix}"
        else:
            output_path = args.output
        
        success = upscale_single_image(args.input, output_path, args.scale, gpu)
        if not success:
            sys.exit(1)
    else:
        # Batch mode
        if not args.directory.exists():
            print(f"Error: Input directory does not exist: {args.directory}")
            sys.exit(1)
        
        upscale_batch(args.directory, args.output, args.scale, args.recursive, gpu)


if __name__ == "__main__":
    main()