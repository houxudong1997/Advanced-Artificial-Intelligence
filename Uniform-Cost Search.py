
import heapq

graph = {
    "s": {"a": 8, "b": 5, "c": 10},
    "a": {"b": 7, "d": 9},
    "b": {"a": 7, "f": 17},
    "c": {"e": 13},
    "d": {"a": 9, "f": 16, "g":31},
    "e": {"c": 13,"f":11,"g":29},
    "f": {"b":17,"d":16,"e":11,"g":4},
    "g": {"d":31,"e":29,"f":4}
}

class Dijkstra:
    def init_distance(self, graph, start):
        distance = {start: 0}
        for key in graph.keys():
            if key != start:
                distance[key] = float('inf')
        return distance

    def dijkstra(self, graph, start):
        if not graph or not start:
            return None

        distance = self.init_distance(graph, start)
        pqueue = []
        visitorder=[]
        heapq.heappush(pqueue, (0, start))
        seen = set()
        parent = {start: None}

        while pqueue:
            cur_distance, cur_node = heapq.heappop(pqueue)
            seen.add(cur_node)
            nodes = graph[cur_node]

            for node, dist in nodes.items():
                if node in seen:
                    continue
                elif distance[node] > cur_distance + dist:
                    heapq.heappush(pqueue, (dist + cur_distance, node))
                    parent[node] = cur_node
                    distance[node] = cur_distance + dist
            visitorder.append(cur_node)
        print(visitorder)
        return distance, parent


if __name__ == '__main__':
    s = Dijkstra()
    distance, parent = s.dijkstra(graph, "s")
    print(distance)
    print(parent)
