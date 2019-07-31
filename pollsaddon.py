polls = {}
votes = {}

def demo():
    addpoll("evés")
    addpoll("ivás")
    addtopoll(0, "kenyér")
    addtopoll(0, "pizza")
    addtopoll(1, "víz")
    addtopoll(1, "tej")
    vote(0, "a", 0)
    vote(0, "b", 1)
    vote(1, "c", 0)
    vote(1, "d", 1)

def addpoll(pollname):
    global polls, votes
    i = 0
    while i in polls:
        i += 1
    polls[i] = (pollname, {})
    votes[i] = {}

def removepoll(poll):
    polls.pop(poll)
    votes.pop(poll)

def addtopoll(poll, text):
    global polls
    i = 0
    while i in polls[poll][1]:
        i += 1
    polls[poll][1][i] = (text)

def removefrompoll(poll, index):
    polls[poll][1].pop(index)
    for k, v in votes[poll].items():
        if v == index:
            votes[poll].pop(k)

def vote(poll, name,vt):
    votes[poll][name] = vt

def displaypolls():
    text = ""
    for x in polls:
        text += f"{x} : {polls[x][0]}\n"
    return text

def displaypoll(poll):
    text = ""
    for x in polls[poll][1]:
        text += f"{x} : {polls[poll][1][x]}\n"
    return text

def getvotes(poll):
    results = {}
    for x in votes[poll]:
        if votes[poll][x] in results:
            results[votes[poll][x]] += 1
        else:
            results[votes[poll][x]] = 1

    text = ""
    for y in results:
        text += f"{y} {polls[poll][1][y]} : {results[y]}\n"
    return text