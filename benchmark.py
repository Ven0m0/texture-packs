import time
from pathlib import Path
from PIL import Image, ImageDraw
import sys

def create_images(num_images, directory):
    dir_path = Path(directory)
    dir_path.mkdir(exist_ok=True)

    for i in range(num_images):
        img = Image.new('RGB', (100, 100), color='red')
        draw = ImageDraw.Draw(img)
        draw.ellipse((25, 25, 75, 75), fill='blue')
        draw.text((40, 40), str(i), fill="white")
        img.save(dir_path / f'test_{i}.png')

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--create', type=int, default=0)
    parser.add_argument('--dir', type=str, default='bench_images')
    args = parser.parse_args()

    if args.create > 0:
        create_images(args.create, args.dir)
        print(f"Created {args.create} images in {args.dir}")

if __name__ == "__main__":
    main()
