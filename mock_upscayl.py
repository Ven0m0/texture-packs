#!/usr/bin/env python3
import sys
import time

def main():
    time.sleep(0.5)  # Simulate some work
    print(f"Mock upscayl success: {' '.join(sys.argv)}")
    sys.exit(0)

if __name__ == '__main__':
    main()
