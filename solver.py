# Put your solution here.
import networkx as nx
import random
import operator
import numpy as np

def update_weight(client, s_weight, s_loss):
    epsilon = np.sqrt(np.log(client.students)/client.v)
    return s_weight*((1-epsilon)**(s_loss))


def findbots(client, mst):
    all_students = list(range(1, client.students + 1))
    non_home = list(range(1, client.home)) + list(range(client.home + 1, client.v + 1))

    losses = {} #keeps track of how many times a student has lied
    student_weights = {} #maps student: their weight
    paths = {} #vertex with a bot -> path to home
    student_response = {} #vertex: dict of student responses
    scores = {} #vertex: score from weights
    bots_found = 0
    #bot_locations = {} #keeps track of how many bots at each vertex
    remoted_to = []

    for student in all_students:
        student_weights[student] = 1
        losses[student] = 0

    for i in non_home:
        #scout
        student_response[i] = client.scout(i, all_students)
        scores[i] = sum(student_response[i].values())
        # bot_locations[i] = 0

    #bots = []    #where students say bots are
    while bots_found < client.bots: #and scores:
        if scores:
            max_vertex = max(scores.items(), key=operator.itemgetter(1))[0]
        else:
            break
        path = nx.dijkstra_path(mst, max_vertex, client.home)
        scores.pop(max_vertex)

        #incrementing bots_found HERE

        if path[0] not in remoted_to:
            num = client.remote(path[0], path[1])
            if num:
                paths[max_vertex] = path[1:]
            bots_found += num
            remoted_to.append(path[1])
        #update
        responses = student_response[max_vertex]
        for stud in responses.keys():
            if responses[stud] != num: # if student lied (False)
            #updated weight of student based on lie
                losses[stud] += 1
                new_weight = update_weight(client, student_weights[stud], losses[stud])
                student_weights[stud] = new_weight if new_weight > 0.5 else 0
                if losses[stud] >= client.v/2:
                    student_weights[stud] = 1
        #normalize student student_weights
        for s in student_weights.keys():
            total = sum(student_weights.values())
            student_weights[s] = student_weights[s]/total if total != 0 else 0

        #update score
        for v in scores.keys():
            resp = student_response[v]
            new_score = 0
            for stud in resp.keys():
                if resp[stud] == num and num != 0: #if they didn't lie
                    weight = student_weights[stud]
                    new_score += weight #*1 if resp[stud] else 0
            scores[v] = new_score
    #now paths has presumed bot locations : path to home #i hate this merge fml
    return paths



def solve(client):
    client.end()
    client.start()

    #MST
    mst = nx.minimum_spanning_tree(client.G)

    #paths = findbots(client, mst)
    paths = findbots(client, client.graph)
    bots_home = 0

    print("REMOTING HOME")
    #get all bots home naive solution
    for bot in paths.keys():
        botpath = paths[bot]
        for i in range(len(botpath)-1):
            num = client.remote(botpath[i], botpath[i+1])
            if num == 0:
                break
            if botpath[i+1] == client.home:
                bots_home += num

    print(bots_home)







    #changes to make:
    #try to remote from farthest vertex to reduce repetition
    #somehow try to use student's responses better/ weed out liars

    client.end()
