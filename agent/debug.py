import datastore
from agent import graph

datastore.build()
q = "What was CBA's closing price in mid January 2015?"
for step in graph.stream({"question": q, "evidence": [],
                          "calculations": [], "retries": 0},
                         config={"recursion_limit": 15}):
    for node, out in step.items():
        print("=== node:", node)
        print(str(out)[:800])
        print()