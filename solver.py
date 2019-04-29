# Put your solution here.
import networkx as nx
import random

def findbots(client):
    all_students = list(range(1, client.students + 1))
    non_home = list(range(1, client.home)) + list(range(client.home + 1, client.v + 1))
    student_response = {} #vertex : bots or no bots
    bot_locations = []
    bot_maybe = []
    for i in non_home:
        responses = client.scout(i, all_students)
        count_T = 0
        count_F = 0
        for r in responses.values():
            if r == True:
                count_T += 1
            else:
                count_F += 1

        if count_T > count_F:
            student_response[i] = True
            bot_locations.append(i)
        else:
            student_response[i] = False
            bot_maybe.append(i)

    return bot_locations, bot_maybe


def solve(client):
    client.end()
    client.start()

    bot_locations, bot_maybe = findbots(client)


    #MST
    mst = nx.minimum_spanning_tree(client.G)

    num_bots = 0

    #tuple: (len(path), path)
    foundbots= []

    #findbots from bot_locations and bots_maybe
    for b in bot_locations:
        path = nx.dijkstra_path(mst, b, client.home)
        num = client.remote(path[0], path[1])
        if num != 0:
            p = (len(path)-1, path[1:])
            foundbots.append(p)
            num_bots += num

    print(num_bots)
    print("MAJORITY YES DONE --------")

    if num_bots != client.bots:
        for m in bot_maybe:
            path = nx.dijkstra_path(mst, m, client.home)
            num = client.remote(path[0], path[1])
            if num != 0:
                p = (len(path)-1, path[1:])
                foundbots.append(p)
                num_bots += num
            if num_bots == client.bots:
                break

    print("SCOUTING DONE --------")

    #get all bots home naive solution
    remoted_on = []
    foundbots = sorted(foundbots, key=lambda x: x[0], reverse=True)
    bots_home = 0
    for bot in foundbots:
        lenbot = bot[0]
        botpath = bot[1]
        for i in range(lenbot-1):
            if botpath[i] not in remoted_on:
                num = client.remote(botpath[i], botpath[i+1])
                remoted_on.append(botpath[i])
                if botpath[i+1] == client.home:
                    bots_home += num

    print(num_bots)
    print(bots_home)
    print(foundbots)







    #changes to make:
    #try to remote from farthest vertex to reduce repetition
    #somehow try to use student's responses better/ weed out liars

    client.end()
