import os
import concurrent.futures

def process(i):
    print(f"Start {i}")
    return True

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    futures = []
    for i in range(1, 5):
        futures.append(executor.submit(process, i))
    for f in concurrent.futures.as_completed(futures):
        f.result()
