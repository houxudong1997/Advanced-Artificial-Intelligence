graph = {
    "s": ["a", "b", "c"],
    "a": ["b","d"],
    "b": ["a", "f"],
    "c": ["e"],
    "d": ["a", "f", "g"],
    "e": ["c","f","g"],
    "f": ["b","d","e","g"],
    "g": []
}

def BFS(graph, start):
    queue = []
    visitorder =[]
    queue.append(start)
    seen = set()
    seen.add(start)
    parent ={start:None}
    while (len(queue)>0):
        vertex = queue.pop(0)
        nodes = graph[vertex]
        for w in nodes:
            if w not in seen:
                queue.append(w)
                seen.add(w)
                parent[w]=vertex
        visitorder.append(vertex)
    print(visitorder)
    print (parent)

BFS(graph,"s")





