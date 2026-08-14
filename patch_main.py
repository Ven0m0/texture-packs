import sys

def modify_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    target_args = """    parser.add_argument('--cpu', action='store_true',
                        help='Use CPU instead of GPU for processing')"""

    replacement_args = """    parser.add_argument('--cpu', action='store_true',
                        help='Use CPU instead of GPU for processing')
    parser.add_argument('-j', '--jobs', type=int, default=3,
                        help='Number of concurrent jobs for batch processing [default: 3]')"""

    target_call = """        upscale_batch(args.directory, args.output, args.scale, args.recursive, gpu)"""

    replacement_call = """        upscale_batch(args.directory, args.output, args.scale, args.jobs, args.recursive, gpu)"""

    if target_args in content and target_call in content:
        content = content.replace(target_args, replacement_args)
        content = content.replace(target_call, replacement_call)
        with open(file_path, 'w') as f:
            f.write(content)
        print("Patched successfully")
    else:
        print("Target not found")
        if target_args not in content:
            print("args not found")
        if target_call not in content:
            print("call not found")

modify_file('upscaler.py')
