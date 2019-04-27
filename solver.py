# Put your solution here.
import networkx as nx
import random

def solve(client):
    client.end()
    client.start()

    all_students = list(range(1, client.students + 1))
    non_home = list(range(1, client.home)) + list(range(client.home + 1, client.v + 1))
    student_response = {} #vertex : bots or no bots
    bot_locations = []
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
            bot_locations.append(i)
        else:
            student_response[i] = False

    #MST
    mst = nx.minimum_spanning_tree(client.G)

    #go thru bots that have majority yes and remote all the way home
    for b in bot_locations:
        path = nx.dijkstra_path(mst, b, client.home)
        for i in range(len(path)-1):
            num = client.remote(path[i], path[i+1])
            # stops remoting if there were no bots there
            if num == 0:
                break

    #changes to make:
    #try to remote from farthest vertex to reduce repetition
    #somehow try to use student's responses better/ weed out liars

    client.end()
