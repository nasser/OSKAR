import os
import subprocess

failures = []

for example in os.listdir("examples"):
    result = subprocess.run(["python", "compiler.py", f"examples/{example}", f"log/{example}.log"], stdout=subprocess.PIPE)
    ok = result.stdout.decode("utf-8").startswith("OK")
    if ok:
        print(".", end="", flush=True)
    else:
        print("!", end="", flush=True)
        failures.append(example)

print()

if len(failures) != 0:
    print("failed")
    for failure in failures:
        print(f"\t{failure}")
