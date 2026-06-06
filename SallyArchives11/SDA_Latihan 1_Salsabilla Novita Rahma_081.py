graph = {
      'A' : ['B', 'E'],
      'B' : ['C', 'F'],
      'C' : ['D', 'G'],
      'D' : ['H'],
      'E' : ['I'],
      'F' : ['E', 'J'],
      'G' : ['F', 'K'],
      'H' : ['G', 'L'],
      'I' : ['M'],
      'J' : ['I', 'N'],
      'K' : ['J', 'O'],
      'L' : ['K', 'P'],
      'M' : ['N'],
      'N' : ['I', 'N'],
      'O' : ['P'],
      'P' : [],
}

def dfs(graph, node, visited=None):
      if visited is None:
            visited = set()

      visited.add(node)
      print(node, end='->')

      for neighbor in graph[node]:
            if neighbor not in visited:
                  dfs(graph, neighbor, visited)

print("Alur penelusuran DFS sesuai arah panah:")
dfs(graph, 'A')
print("Selesai")