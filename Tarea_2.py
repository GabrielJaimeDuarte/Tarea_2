import matplotlib.pyplot as plt
import networkx as nx
import heapq  # Cola de prioridad

def hierarchy_pos(G, root, width=1.0, vert_gap=0.3, vert_loc=0, xcenter=0.5):
    def _hierarchy_pos(G, root, leftmost, width, vert_gap, vert_loc, xcenter,
                       pos=None, parent=None):
        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)  
        if len(children) != 0:
            dx = width / len(children) 
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G, child, leftmost, dx, vert_gap,
                                     vert_loc-vert_gap, nextx, pos, root)
        return pos
    return _hierarchy_pos(G, root, 0, width, vert_gap, vert_loc, xcenter)


def ucs_visual(graph, start, goal):
    visited = set()
    pq = [(0, [start])]  

    G = nx.DiGraph()
    for node, neighbors in graph.items():
        for neighbor, cost in neighbors:
            G.add_edge(node, neighbor, weight=cost)

    pos = hierarchy_pos(G, start)

    plt.ion()

    while pq:
        cost, path = heapq.heappop(pq)
        node = path[-1]

        plt.clf()
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=800, font_size=10)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        nx.draw_networkx_nodes(G, pos, nodelist=visited, node_color="yellow", node_size=800)

        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color="orange", node_size=800)

        plt.title(f"Explorando: {node} | Costo acumulado: {cost}")
        plt.pause(1)

        if node == goal:
            plt.clf()
            nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=800, font_size=10)
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
            nx.draw_networkx_nodes(G, pos, nodelist=path, node_color="green", node_size=800)
            plt.title(f"Camino encontrado (UCS): {' → '.join(path)} | Costo: {cost}")
            plt.pause(3)
            plt.ioff()
            plt.show()
            return path, cost

        if node not in visited:
            visited.add(node)
            for neighbor, step_cost in graph.get(node, []):
                if neighbor not in visited:
                    new_path = list(path)
                    new_path.append(neighbor)
                    heapq.heappush(pq, (cost + step_cost, new_path))

    plt.ioff()
    plt.show()
    return None, None


graph = {
    'A' : [('B', 2), ('L', 4)],
    'B' : [('X', 2), ('C', 3)],
    'L' : [('O', 5), ('Q', 2)],
    'O' : [],
    'Q' : [],
    'C' : [('E', 4)],
    'E' : [('Z', 1)],
    'Z' : [],
    'X' : [('Y', 3)],
    'Y' : [('J', 2)],
    'J' : [('N', 6), ('M', 1)],
    'N' : [],
    'M' : [('G', 2)],
    'G' : []
}

start_node = 'A'
end_node = 'G'
print("Camino UCS:", ucs_visual(graph, start_node, end_node))