import sys

def modify_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    target = """    for i, img_path in enumerate(images, 1):
        print(f"Processing ({i}/{total_count}): {img_path.name}")

        # Determine output path
        if output_dir:
            output_path = output_dir / f"{img_path.stem}_upscaled_x{scale_factor}{img_path.suffix}"
        else:
            output_path = input_dir / f"{img_path.stem}_upscaled_x{scale_factor}{img_path.suffix}"

        if upscale_single_image(img_path, output_path, scale_factor, gpu):
            success_count += 1"""

    replacement = """    def process_image(idx_img):
        idx, img_path = idx_img
        print(f"Processing ({idx}/{total_count}): {img_path.name}")

        if output_dir:
            output_path = output_dir / f"{img_path.stem}_upscaled_x{scale_factor}{img_path.suffix}"
        else:
            output_path = input_dir / f"{img_path.stem}_upscaled_x{scale_factor}{img_path.suffix}"

        return upscale_single_image(img_path, output_path, scale_factor, gpu)

    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as executor:
        results = executor.map(process_image, enumerate(images, 1))
        success_count = sum(1 for r in results if r)"""

    if target in content:
        content = content.replace(target, replacement)
        with open(file_path, 'w') as f:
            f.write(content)
        print("Patched successfully")
    else:
        print("Target not found")

modify_file('upscaler.py')
