with open("/workspaces/lift-project/tests/test results/result.txt", "r") as f:
    results = f.read()

results = results.split("\n")
results = "\n".join([", ".join(result.split(" ")[3:]) for result in results])

with open("/workspaces/lift-project/tests/test results/result.csv", "w") as f:
    f.write(results)
