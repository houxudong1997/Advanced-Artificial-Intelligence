graph = {
    "s": ["a", "b", "c"],
    "a": ["b","d"],
    "b": ["a", "f"],
    "c": ["e"],
    "d": ["a", "f", "g"],
    "e": ["c","f","g"],
    "f": ["b","d","e","g"],
    "g": []#"d","e","f"]
}

def DFS(graph, start):
    stack = []
    visitorder = []
    stack.append(start)
    seen = set()
    seen.add(start)
    parent = {start: None}
    while (len(stack)>0):
        vertex = stack.pop()
        nodes = graph[vertex]
        for w in nodes:
            if w not in seen:
                stack.append(w)
                seen.add(w)
                parent[w] = vertex
        visitorder.append(vertex)
    print(visitorder)
    print(parent)

DFS(graph,"s")