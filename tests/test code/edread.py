with open("/workspaces/lift-project/tests/test results/result5.txt", "r") as f:
    results = f.read()

results = results.split("\n")
results = "\n".join([result.replace("[", "").replace("]", "") for result in results])

with open("/workspaces/lift-project/tests/test results/result5.csv", "w") as f:
    f.write(results)
