results = []
with open("/workspaces/lift-project/tests/test results/result5.csv", "r") as f:
    while line := f.readline():
        split = [int(num) for num in line.split(",")]
        differences = [abs(split[i] - split[i + 1]) for i in range(len(split) - 1)]
        results.append(str(sum(differences)))
results = "\n".join(results)

with open("/workspaces/lift-project/tests/test results/resultdiff5.csv", "w") as f:
    f.write(results)
