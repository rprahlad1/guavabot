# Put your solution here.
import networkx as nx
import random

def solve(client):
    client.end()
    client.start()

    all_students = list(range(1, client.students + 1))
    non_home = list(range(1, client.home)) + list(range(client.home + 1, client.v + 1))

    student_response = {} #vertex : bots or no bots
    for i in non_home:
        responses = client.scout(i, all_students)
        count_T = 0
        count_F = 0
        for r in responses.values():
            if r == True:
                count_T += 1
            else:
                count_F += 1

        if count_T >= count_F:
            student_response[i] = True
        else:
            student_response[i] = False

    #MST lol
    mst = list(nx.minimum_spanning_edges(client.G))


    for _ in range(100):
        u, v = random.choice(list(client.G.edges()))
        client.remote(u, v)

    client.end()
