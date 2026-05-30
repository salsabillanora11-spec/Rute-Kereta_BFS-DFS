# kode 1 (perbandingan)

import time
import random 
import os
import statistics
from statistics import mean, median, stdev 
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx 
import matplotlib.colors as mcolors 

stasiun = {
    'A': 'Manggarai',
    'B': 'Sudirman',
    'C': 'Cikini',
    'D': 'Tebet',
    'E': 'Pasar Minggu',
    'F': 'Tanah Abang',
    'G': 'Palmerah',
    'H': 'Kebayoran',
    'I': 'Depok',
    'J': 'Jatinegara',
    'K': 'Bekasi',
    'L': 'Duri',
    'M': 'Tangerang',
    'N': 'Serpong',
    'O': 'Bogor',
}

# Adjacency List 
graph = {
    'A': ['B', 'D'],                # Manggarai -> Sudirman, Tebet
    'B': ['A', 'E'],                # Sudirman -> Manggarai, Pasar Minggu
    'C': ['D', 'H'],                # Cikini -> Tebet, Kebayoran
    'D': ['A', 'C', 'I'],           # Tebet -> Manggarai, Cikini, Depok
    'E': ['B', 'J', 'L'],           # Pasar Minggu -> Sudirman, Jatinegara, Duri
    'F': ['G', 'N'],                # Tanah Abang -> Palmerah, Serpong
    'G': ['F', 'H', 'N'],           # Palmerah -> Tanah Abang, Kebayoran, Serpong
    'H': ['C', 'G', 'I', 'N'],      # Kebayoran -> Cikini, Palmerah, Depok, Serpong
    'I': ['D', 'H'],                # Depok -> Tebet, Kebayoran
    'J': ['E', 'K', 'L'],           # Jatinegara -> Pasar Minggu, Bekasi, Duri
    'K': ['J', 'M'],                # Bekasi -> Jatinegara, Tangerang
    'L': ['E', 'J', 'O'],           # Duri -> Pasar Minggu, Jatinegara, Bogor 
    # 'L': ['E', 'J', 'M', 'O'],    # # Duri -> Pasar Minggu, Jatinegara, Tangerang, Bogor
    'M': ['K', 'L'],                # Tangerang -> Bekasi, Duri
    'N': ['F', 'G', 'H', 'O'],      # Serpong -> Tanah Abang, Palmerah, Kebayoran, Bogor
    'O': ['L', 'N'],                # Bogor -> Duri, Serpong
}

nodes = list(stasiun.keys())

def buat_adjacency_matrix(graph, nodes):
    matrix = []

    for node_asal in nodes:
        baris = []

        for node_tujuan in nodes:
            if node_tujuan in graph[node_asal]:
                baris.append(1)
            else:
                baris.append(0)
        
        matrix.append(baris)

    return matrix

adjacency_matrix = buat_adjacency_matrix(graph, nodes)

def hitung_sisi(graph):
      total = sum(len(v) for v in graph.values())
      return total // 2

def tampilkan_adjacency_matrix(matrix, nodes):
    print("\n  Adjacency Matrix:")
    print("      " + "  ".join(nodes))

    for i, row in enumerate(matrix):
        nilai_baris = "  ".join(str(nilai) for nilai in row)
        print(f"  {nodes[i]}   {nilai_baris}")

    print()

def tampilkan_info_graph():
     print("Graph Jaringan KRL Jabodetabek")
     
     print(f"Jumlah simpul (V) :{len(graph)}")
     print(f"Jumlah sisi (E) :{hitung_sisi(graph)}")
     print()

     print("Daftar Vertex (stasiun):")
     for code, name in stasiun.items():
          print(f"{code}: {name}")
     print()

     print("Adjacency List : ")
     for vertex, neighborhod in graph.items():
          nama_vertex = stasiun[vertex]
          nama_neighborhod = ','.join([f"{t}({stasiun[t]})" for t in neighborhod])
          print(f"{vertex} ({nama_vertex :15s}) -> {nama_neighborhod}")

     tampilkan_adjacency_matrix(adjacency_matrix, nodes) 


def tampilkan_perbandingan_representasi():
     jumlah_node = len(nodes)
     jumlah_sisi = hitung_sisi(graph)

     ruang_list = jumlah_node + jumlah_sisi
     ruang_matrix = jumlah_node * jumlah_node

     print("Perbandingan Representasi Graph")
     print(f"jumlah simpul (V) : {jumlah_node}")
     print(f"jumlah sisi (E) : {jumlah_sisi}")

     print("\n Adjacency List:")
     print(f"Menyimpan node dan sisi yang terhubung langsung")
     print(f"Kompleksitas ruang: O(V + E)")
     print(f"Perkiraan ruang: {jumlah_node} + {jumlah_sisi} = {ruang_list}")

     print("\n Adjacency Matrix:")
     print(f"Menyimpan semua kemungkinan hubungan antar node")
     print(f"Kompleksitas ruang: O(V^2)")
     print(f"Perkiraan ruang: {jumlah_node} x {jumlah_node} = {ruang_matrix}")

     if ruang_list < ruang_matrix:
        print("\n Untuk graph ini, adjacency list lebih hemat ruang.")
     else:
        print("\n Untuk graph ini, adjacency matrix masih cukup efisien.")

     print()

# BFS 
def bfs(graph, start):
     visited = {v: False for v in graph}
     queue = deque()
     route = []

     queue.append(start)
     visited[start] = True

     start_time = time.time()

     while queue:
          v = queue.popleft()
          route.append(v)

          neighborhod = sorted(graph[v])
          random.shuffle(neighborhod)

          for w in neighborhod:
               if not visited[w]:
                    visited[w] = True
                    queue.append(w)
      
     end_time = time.time()
     waktu_ms = (end_time - start_time) * 1000
     return route, waktu_ms

# DFS 
def dfs(graph, start):
     visited = {v:False for v in graph}
     stack = [start]
     route = []

     visited[start] = True
     route.append(start)

     start_time = time.time()

     while stack:
          current = stack[-1]
          found_unvisited = False

          neighborhod = sorted(graph[current], reverse=True)
          random.shuffle(neighborhod)

          for neighbor in neighborhod:
               if not visited[neighbor]:
                    stack.append(neighbor)
                    visited[neighbor] = True
                    route.append(neighbor)
                    found_unvisited = True
                    break
               
          if not found_unvisited:
               stack.pop()
      
     end_time = time.time()
     waktu_ms = (end_time - start_time)* 1000
     return route, waktu_ms

tampilkan_info_graph()
tampilkan_perbandingan_representasi()

def get_neighborhod_matrix(matrix, nodes, node):
    """Mengembalikan daftar tetangga dari sebuah node berdasarkan adjacency matrix"""
    idx = nodes.index(node)   # cari index node
    neighbors = []
    for j, val in enumerate(matrix[idx]):
        if val == 1:          # jika ada edge
            neighbors.append(nodes[j])
    return neighbors

#BFS matrix
def bfs_matrix(matrix, nodes, start):
    visited = {v: False for v in nodes}
    queue = deque()
    route = []

    queue.append(start)
    visited[start] = True

    start_time = time.perf_counter()

    while queue:
        v = queue.popleft()
        route.append(v)

        neighborhod = get_neighborhod_matrix(matrix, nodes, v)
        random.shuffle(neighborhod)

        for w in neighborhod:
            if not visited[w]:
                visited[w] = True
                queue.append(w)

    end_time = time.perf_counter()
    waktu_ms = (end_time - start_time) * 1000

    return route, waktu_ms

# DFS Matrix
def dfs_matrix(matrix, nodes, start):

    visited = {v: False for v in nodes}
    stack = []
    route = []

    stack.append(start)
    visited[start] = True
    route.append(start)

    start_time = time.perf_counter()

    while stack:
        current = stack[-1]
        found_unvisited = False

        neighborhod = get_neighborhod_matrix(matrix, nodes, current)
        random.shuffle(neighborhod)

        for w in neighborhod:
            if not visited[w]:
                stack.append(w)
                visited[w] = True
                route.append(w)
                found_unvisited = True
                break

        if not found_unvisited:
            stack.pop()

    end_time = time.perf_counter()
    waktu_ms = (end_time - start_time) * 1000

    return route, waktu_ms

# Eksperimen dg 10 Iterasi 
vertex_awal = 'A'
jumlah_iterasi = 10

print(f"Eksperimen : {jumlah_iterasi} iterasi | vertex awal: {vertex_awal} ({stasiun[vertex_awal]})")

hasil_bfs = []
hasil_dfs = []
hasil_bfs_matrix = []
hasil_dfs_matrix = []

# iterasi BFS
print("\n Hasil Penelusuran BFS : ")
print(f"  {'Eks':>3}  {'Rute Penelusuran':<55}  {'Waktu':>8}")
print("  " + "-" * 70)

for i in range(1, jumlah_iterasi + 1):
     rute, waktu = bfs(graph, vertex_awal)
     hasil_bfs.append({'rute': rute, 'waktu': waktu})
     rute_str = '->'.join(rute)
     print(f"{i :>3} {rute_str :<55} {waktu :.3f} ms")

# iterasi DFS
print("\n Hasil Penelusuran DFS : ")
print(f"  {'Eks':>3}  {'Rute Penelusuran':<55}  {'Waktu':>8}")
print("  " + "-" * 70)

for i in range(1, jumlah_iterasi + 1):
    rute, waktu = dfs(graph, vertex_awal)
    hasil_dfs.append({'rute': rute, 'waktu': waktu})
    rute_str = '->'.join(rute)
    print(f"  {i:>3}  {rute_str:<55}  {waktu:.3f} ms")

# iterasi BFS Matrix
print("\n Hasil Penelusuran BFS Matrix : ")
print(f"  {'Eks':>3}  {'Rute Penelusuran':<55}  {'Waktu':>8}")
print("  " + "-" * 70)

for i in range(1, jumlah_iterasi + 1):
    rute, waktu = bfs_matrix(adjacency_matrix, nodes, vertex_awal)
    hasil_bfs_matrix.append({
        'rute': rute,
        'waktu': waktu
    })

    rute_str = '->'.join(rute)
    print(f"  {i:>3}  {rute_str:<55}  {waktu:.3f} ms")

# iterasi DFS Matrix
print("\n Hasil Penelusuran DFS Matrix : ")
print(f"  {'Eks':>3}  {'Rute Penelusuran':<55}  {'Waktu':>8}")
print("  " + "-" * 70)

for i in range(1, jumlah_iterasi + 1):
    rute, waktu = dfs_matrix(adjacency_matrix, nodes, vertex_awal)
    hasil_dfs_matrix.append({
        'rute': rute,
        'waktu': waktu
    })

    rute_str = '->'.join(rute)
    print(f"  {i:>3}  {rute_str:<55}  {waktu:.3f} ms")

# Analisis Hasil 
def analyze_results(hasil, nama_algo):
     waktu_list = [h['waktu'] for h in hasil]
     rute_unik = set(tuple(h['rute']) for h in hasil)

     stats = {
          'min': min(waktu_list),
          'median': median(waktu_list),
          'avg': mean(waktu_list),
          'stdev': stdev(waktu_list) if len(waktu_list) > 1 else 0,
          'max': max(waktu_list),
          'rute_unik': len(rute_unik),
          'waktu_list': waktu_list,
      }

     return stats

stats_bfs = analyze_results(hasil_bfs, 'BFS')
stats_dfs = analyze_results(hasil_dfs, 'DFS')
stats_bfs_matrix = analyze_results(hasil_bfs_matrix, 'BFS Matrix')
stats_dfs_matrix = analyze_results(hasil_dfs_matrix, 'DFS Matrix')
rasio = stats_dfs['avg'] / stats_bfs['avg']
rasio_matrix = stats_dfs_matrix['avg'] / stats_bfs_matrix['avg']

print("Analisis Perbandingan BFS & DFS")

print(f"{'Matrik':<25} {'BFS':>12} {'DFS':>12}")
print("  " + "-" * 52)

print(f"{'Waktu Minimum':<25} {stats_bfs['min']:>10.3f}ms {stats_dfs['min']:>10.3f}ms")
print(f"{'Waktu Median':<25} {stats_bfs['median']:>10.3f}ms {stats_dfs['median']:>10.3f}ms")
print(f"{'Waktu Rata-rata':<25} {stats_bfs['avg']:>10.3f}ms {stats_dfs['avg']:>10.3f}ms")
print(f"{'Std Deviasi':<25} {stats_bfs['stdev']:>10.3f}ms {stats_dfs['stdev']:>10.3f}ms")
print(f"{'Waktu Maksimum':<25} {stats_bfs['max']:>10.3f}ms {stats_dfs['max']:>10.3f}ms")
print(f"{'Jumlah Rute Unik':<25} {stats_bfs['rute_unik']:>12} {stats_dfs['rute_unik']:>12}")

print(f"{'Rasio DFS/BFS':<25} {'-':>12} {rasio:>11.2f}x")
print()

print(f"DFS {rasio:.2f}x lebih lambat dari BFS secara empiris")
print(f"Keduanya memiliki kompleksitas teoritis O(V+E) = O({len(graph)}+{hitung_sisi(graph)}) = O({len(graph)+hitung_sisi(graph)})")

print("\nPerbandingan Adjacency List dan Adjacency Matrix")
print(f"{'Metode':<20} {'Avg':>10} {'Min':>10} {'Max':>10} {'Rute Unik':>12}")
print("-" * 70)

data_perbandingan = [
    ('BFS List', stats_bfs),
    ('BFS Matrix', stats_bfs_matrix),
    ('DFS List', stats_dfs),
    ('DFS Matrix', stats_dfs_matrix),
]

for nama, stats in data_perbandingan:
    print(f"{nama:<20} "
          f"{stats['avg']:>10.3f} "
          f"{stats['min']:>10.3f} "
          f"{stats['max']:>10.3f} "
          f"{stats['rute_unik']:>12}")

print()
print(f"Rasio DFS/BFS pada adjacency matrix: {rasio_matrix:.2f}x")

if stats_bfs['avg'] < stats_bfs_matrix['avg']:
    print("BFS dengan adjacency list lebih cepat dibanding BFS dengan adjacency matrix.")
else:
    print("BFS dengan adjacency matrix lebih cepat dibanding BFS dengan adjacency list.")

if stats_dfs['avg'] < stats_dfs_matrix['avg']:
    print("DFS dengan adjacency list lebih cepat dibanding DFS dengan adjacency matrix.")
else:
    print("DFS dengan adjacency matrix lebih cepat dibanding DFS dengan adjacency list.")

print("\nCatatan:")
print("Adjacency list lebih hemat ruang untuk graph sparse karena hanya menyimpan node yang terhubung langsung.")
print("Adjacency matrix menyimpan semua kemungkinan hubungan antar node, sehingga membutuhkan ruang O(V^2).")




# Visualisasi Graph
rute = {
    'Bogor'    : {'nodes': ['A','B','E','J','L','O'], 'color': '#ef4444'},
    'Bekasi'   : {'nodes': ['A','B','E','J','K','M'], 'color': '#3b82f6'},
    'Depok'    : {'nodes': ['A','D','C','I','H'],     'color': '#f59e0b'},
    'Serpong'  : {'nodes': ['F','G','N','O'],         'color': '#10b981'},
    'Tangerang': {'nodes': ['F','G','H','N'],         'color': '#8b5cf6'},
}
 
# Posisi manual mengikuti letak geografis KRL Jabodetabek
pos = {
    'A': (3.0, 5.0), 'B': (3.0, 6.2), 'C': (1.8, 4.2),
    'D': (1.8, 5.0), 'E': (3.0, 7.4), 'F': (0.2, 7.8),
    'G': (1.0, 7.2), 'H': (1.0, 5.8), 'I': (1.2, 3.4),
    'J': (4.4, 7.4), 'K': (5.8, 7.4), 'L': (3.0, 8.6),
    'M': (5.8, 8.6), 'N': (0.2, 6.4), 'O': (3.0, 9.8),
}
 
def visualisasi_graph(graph, stasiun, output_path='visualisasi_graph.png'):
    # Bangun NetworkX graph
    G = nx.Graph()
    for u, neighbors in graph.items():
        for v in neighbors:
            if not G.has_edge(u, v):
                G.add_edge(u, v)
 
    nodes_list = list(G.nodes())
    edges_list = list(G.edges())
 
    # Tentukan warna node (ambil warna jalur pertama yang cocok)
    node_rute = {}
    for info in rute.values():
        for n in info['nodes']:
            if n not in node_rute:
                node_rute[n] = info['color']
    n_colors = [node_rute.get(n, '#94a3b8') for n in nodes_list]
 
    # Tentukan warna edge
    edge_rute = {}
    for info in rute.values():
        ns = info['nodes']
        for i in range(len(ns) - 1):
            edge_rute[tuple(sorted([ns[i], ns[i+1]]))] = info['color']
    e_colors = [edge_rute.get(tuple(sorted([u, v])), '#cbd5e1') for u, v in edges_list]
 
    # Gambar 
    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#1e293b')
 
    # Edge
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=e_colors, width=3.5, alpha=0.85)
 
    # Node: cincin putih tipis + warna jalur
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color='white',    node_size=820)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=n_colors,   node_size=700, alpha=0.95)
 
    # Label huruf di dalam node
    nx.draw_networkx_labels(G, pos, ax=ax,
        labels={n: n for n in nodes_list},
        font_color='white', font_size=11, font_weight='bold')
 
    # Nama stasiun di bawah node
    for node, (x, y) in pos.items():
        ax.text(x, y - 0.38, stasiun[node],
                fontsize=7.5, color='#94a3b8',
                ha='center', va='top', style='italic',
                fontfamily='monospace')
 
    # Legend jalur
    legend_handles = [
        mpatches.Patch(color=info['color'], label=f"Jalur {jalur}")
        for jalur, info in rute.items()
    ]
    legend_handles.append(mpatches.Patch(color='#94a3b8', label='Lintas jalur'))
    ax.legend(handles=legend_handles, loc='lower left',
              facecolor='#1e293b', edgecolor='#334155',
              labelcolor='#f1f5f9', fontsize=9, framealpha=0.95,
              title='Jalur KRL', title_fontsize=9.5)
 
    # Judul & info
    ax.set_title('Visualisasi Graf — Jaringan KRL Jabodetabek',
                 fontsize=15, fontweight='bold', color='#f1f5f9', pad=16)
    ax.text(0.99, 0.01,
            f'{len(nodes_list)} Stasiun  |  {len(edges_list)} Koneksi',
            transform=ax.transAxes, fontsize=8, color='#64748b',
            ha='right', va='bottom')
 
    ax.axis('off')
    ax.set_xlim(-0.6, 7.0)
    ax.set_ylim(2.5, 11.0)
    plt.tight_layout(pad=1.5)
 
    # tampilkan gambar
    plt.savefig(output_path, dpi=160, bbox_inches='tight', facecolor='#0f172a')
    print(f"\nGraph disimpan sebagai '{output_path}'")
    plt.show()

visualisasi_graph(graph, stasiun, output_path='visualisasi_graph.png')