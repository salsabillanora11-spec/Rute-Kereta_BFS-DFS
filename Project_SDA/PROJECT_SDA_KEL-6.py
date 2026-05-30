import time                                 # mengukur waktu eksekusi
import random                               # mengacak urutan tetangga saat eksperimen
from statistics import mean, median, stdev  # menghitung statistik hasil eksperimen
from collections import deque               # queue algoritma BFS
import matplotlib.pyplot as plt             # visualisasi graph
import matplotlib.patches as mpatches       # legend visualisasi
import matplotlib.animation as animation    # membuat animasi 
from matplotlib.lines import Line2D         # lingkaran untuk legend
import networkx as nx                       # membuat dan mnegukur graph      

# DATA GRAPH
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

# representasi graph menggunakan adjacency list
graph = {
    'A': ['B', 'D'],
    'B': ['A', 'E'],
    'C': ['D', 'H'],
    'D': ['A', 'C', 'I'],
    'E': ['B', 'J', 'L'],
    'F': ['G', 'N'],
    'G': ['F', 'H', 'N'],
    'H': ['C', 'G', 'I', 'N'],
    'I': ['D', 'H'],
    'J': ['E', 'K', 'L'],
    'K': ['J', 'M'],
    'L': ['E', 'J', 'M', 'O'],
    'M': ['K', 'L'],
    'N': ['F', 'G', 'H', 'O'],
    'O': ['L', 'N'],
}

pos = {
    'A': (3.0, 5.0), 'B': (3.0, 6.2), 'C': (1.8, 4.2),
    'D': (1.8, 5.0), 'E': (3.0, 7.4), 'F': (0.2, 7.8),
    'G': (1.0, 7.2), 'H': (1.0, 5.8), 'I': (1.2, 3.4),
    'J': (4.4, 7.4), 'K': (5.8, 7.4), 'L': (3.0, 8.6),
    'M': (5.8, 8.6), 'N': (0.2, 6.4), 'O': (3.0, 9.8),
}

jalur_info = {
    'Bogor': {'nodes': ['A','B','E','J','L','O'], 'color': "#FFA9D4"},
    'Bekasi': {'nodes': ['A','B','E','J','K','M'], 'color': '#FFA9D4'},
    'Depok': {'nodes': ['A','D','C','I','H'], 'color': '#FFA9D4'},
    'Serpong': {'nodes': ['F','G','N','O'], 'color': '#FFA9D4'},
    'Tangerang': {'nodes': ['F','G','H','N'], 'color': '#FFA9D4'},
}

nodes = list(stasiun.keys())

def hitung_sisi(graph):
    return sum(len(v) for v in graph.values()) // 2

# BFS
def bfs(graph, start, end=None, acak=False):
    visited = {start: None}              # parent awal
    queue = deque([start])               
    steps = []                           # menyimpan urutan node yang dikunjungi

    start_time = time.perf_counter()

    while queue:                        
        v = queue.popleft()              
        steps.append(v)                

        if end is not None and v == end: # pencarian rute dan tujuan ditemukan
            break                        

        neighbors = graph[v][:]          
        if acak:
            random.shuffle(neighbors)    # urutan tetangga diacak
        else:
            neighbors = sorted(neighbors)# pencarian rute urutan tetap

        for w in neighbors:              
            if w not in visited:         
                visited[w] = v           
                queue.append(w)          

    waktu_ms = (time.perf_counter() - start_time) * 1000

    if end is None:                      # mode eksperimen
        return steps, waktu_ms

    path, cur = [], end                  # rekonstruksi rute dari tujuan ke awal
    while cur is not None:
        path.append(cur)
        cur = visited.get(cur)
    path.reverse()

    if not path or path[0] != start:
        path = []

    return steps, path, waktu_ms

# DFS
def dfs(graph, start, end=None, acak=False):
    visited = {v: False for v in graph}  
    stack = []                           
    steps = []                           

    stack.append(start)                  
    visited[start] = True                
    steps.append(start)                  

    start_time = time.perf_counter()

    while stack:                         
        current = stack[-1]              # top(stack) / peek tanpa pop
        found_unvisited = False          # penanda ada/tidak tetangga baru

        if end is not None and current == end: # pencarian rute dan tujuan ditemukan
            break                              

        neighbors = graph[current][:]    
        if acak:
            random.shuffle(neighbors)    # eksperimen urutan tetangga diacak
        else:
            neighbors = sorted(neighbors)# pencarian rute urutan tetap

        for w in neighbors:              
            if not visited[w]:           
                stack.append(w)          
                visited[w] = True        
                steps.append(w)          
                found_unvisited = True   
                break                    

        if not found_unvisited:          
            stack.pop()                  # untuk backtracking

    waktu_ms = (time.perf_counter() - start_time) * 1000

    if end is None:                      # mode eksperimen
        return steps, waktu_ms

    return steps, steps, waktu_ms        # mode pencarian rute DFS

# analisis hasil eksperimen BFS & DFS
def analyze_results(hasil):
    waktu_list = [h['waktu'] for h in hasil]
    rute_unik = set(tuple(h['rute']) for h in hasil)

    return {
        'min': min(waktu_list),
        'median': median(waktu_list),
        'avg': mean(waktu_list),
        'stdev': stdev(waktu_list) if len(waktu_list) > 1 else 0,
        'max': max(waktu_list),
        'rute_unik': len(rute_unik),
    }

# menjalankan eksperimen BFS & DFS dengan vertex awal tetap dan urutan tetangga diacak
def jalankan_eksperimen():
    vertex_awal = 'A'
    jumlah_iterasi = 10

    hasil_bfs = []
    hasil_dfs = []

    print("\nEKSPERIMEN BFS dan DFS")
    print(f"Vertex awal : {vertex_awal} ({stasiun[vertex_awal]})")
    print(f"Jumlah iterasi : {jumlah_iterasi}")

    print("\nHasil Penelusuran BFS:")
    print(f"{'Eks':>3}  {'Rute Penelusuran':<55}  {'Waktu':>8}")
    print("-" * 75)

    for i in range(1, jumlah_iterasi + 1):
        rute, waktu = bfs(graph, vertex_awal, acak=True)
        hasil_bfs.append({'rute': rute, 'waktu': waktu})
        print(f"{i:>3}  {'->'.join(rute):<55}  {waktu:.3f} ms")

    print("\nHasil Penelusuran DFS:")
    print(f"{'Eks':>3}  {'Rute Penelusuran':<55}  {'Waktu':>8}")
    print("-" * 75)

    for i in range(1, jumlah_iterasi + 1):
        rute, waktu = dfs(graph, vertex_awal, acak=True)
        hasil_dfs.append({'rute': rute, 'waktu': waktu})
        print(f"{i:>3}  {'->'.join(rute):<55}  {waktu:.3f} ms")

    stats_bfs = analyze_results(hasil_bfs)
    stats_dfs = analyze_results(hasil_dfs)
    rasio = stats_dfs['avg'] / stats_bfs['avg']

    print("\nAnalisis BFS & DFS")
    print(f"{'Metrik':<25} {'BFS':>12} {'DFS':>12}")
    print("-" * 52)
    print(f"{'Waktu Minimum':<25} {stats_bfs['min']:>10.3f}ms {stats_dfs['min']:>10.3f}ms")
    print(f"{'Waktu Median':<25} {stats_bfs['median']:>10.3f}ms {stats_dfs['median']:>10.3f}ms")
    print(f"{'Waktu Rata-rata':<25} {stats_bfs['avg']:>10.3f}ms {stats_dfs['avg']:>10.3f}ms")
    print(f"{'Std Deviasi':<25} {stats_bfs['stdev']:>10.3f}ms {stats_dfs['stdev']:>10.3f}ms")
    print(f"{'Waktu Maksimum':<25} {stats_bfs['max']:>10.3f}ms {stats_dfs['max']:>10.3f}ms")
    print(f"{'Jumlah Rute Unik':<25} {stats_bfs['rute_unik']:>12} {stats_dfs['rute_unik']:>12}")
    print(f"{'Rasio DFS/BFS':<25} {'-':>12} {rasio:>11.2f}x")

# warna untuk node & edge
def default_node_colors():
    cmap = {}
    for info in jalur_info.values():
        for n in info['nodes']:
            if n not in cmap:
                cmap[n] = info['color']
    return [cmap.get(n, "#FFA9D4") for n in nodes]

def default_edge_colors(G):
    cmap = {}
    for info in jalur_info.values():
        ns = info['nodes']
        for i in range(len(ns) - 1):
            key = tuple(sorted([ns[i], ns[i+1]]))
            cmap[key] = info['color']
    return [cmap.get(tuple(sorted([u, v])), "#FFA9D4") for u, v in G.edges()]

#gambar frame animasi
def draw_frame(ax, G, node_colors, edge_colors,
               start, end, current=None,
               path_edges=None, title=''):
    ax.clear()
    ax.set_facecolor("#f6def3")
    ax.axis('off')
    ax.set_xlim(-0.6, 7.0)
    ax.set_ylim(2.2, 11.2)

    # Edge biasa
    nx.draw_networkx_edges(
        G, pos, ax=ax,
        edge_color=edge_colors, width=3, alpha=0.75
    )

    # Edge rute hasil pencarian ditampilkan di atas edge biasa
    if path_edges:
        nx.draw_networkx_edges(
            G, pos, ax=ax,
            edgelist=path_edges,
            edge_color='#FF0381', width=5.5, alpha=1.0
        )

    # Node: ring hitam -> warna jalur
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color='black', node_size=850)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=720, alpha=0.95)

    # Ring tebal untuk asal & tujuan
    for node, ring_color in [(start, "#FF0381"), (end, "#FF0381")]:
        nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=[node],
                               node_color=ring_color, node_size=1050, alpha=0.35)

    # Highlight node yang sedang diperiksa
    if current and current not in (start, end):
        nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=[current],
                               node_color="#F6BBD8", node_size=1000, alpha=0.4)

    # Label huruf di dalam node
    nx.draw_networkx_labels(
        G, pos, ax=ax,
        labels={n: n for n in nodes},
        font_color='white', font_size=11, font_weight='bold'
    )

    # Nama stasiun di bawah node
    for node, (x, y) in pos.items():
        ax.text(x, y - 0.38, stasiun[node],
                fontsize=7, color="#050003",
                ha='center', va='top', style='italic',
                fontfamily='monospace')

    # Legend
    handles = [
    Line2D([], [], marker='o', ls='', color='#FF0381',
           markersize=9, label='Start / End'),
    Line2D([], [], marker='o', ls='', color='#0C2A52',
           markersize=9, label='Visited (sudah dikunjungi)'),
    Line2D([], [], marker='o', ls='', color='#A1939A',
           markersize=9, label='Current (sedang diperiksa)'),
    mpatches.Patch(color='#FF0381', label='Path (rute hasil)'),
    mpatches.Patch(color='#FFA9D4', label='Edge (jalur)'),
    ]

    ax.legend(handles=handles, loc='lower left',
              facecolor='#f6def3', edgecolor='#FF0381',
              labelcolor='#050003', fontsize=7,
              title='Keterangan', title_fontsize=8)

    ax.set_title(title, color='#FF0381', fontsize=10,
                 fontfamily='monospace', pad=10)

# Pencarian rute
def jalankan_animasi(start, end, algo='BFS', interval_ms=400):
    G = nx.Graph()
    for u, neighbors in graph.items():
        for v in neighbors:
            if not G.has_edge(u, v):
                G.add_edge(u, v)

    base_nc = default_node_colors()
    base_ec = default_edge_colors(G)

    # Jalankan algoritma
    if algo == 'BFS':
        steps, path, waktu = bfs(graph, start, end)
    else:
        steps, path, waktu = dfs(graph, start, end)

    total_frames = len(steps) + 1

    fig, ax = plt.subplots(figsize=(13, 9))
    fig.patch.set_facecolor("#f8e2f1")
    fig.suptitle(
        f'Jaringan KRL Jabodetabek  —  {algo}: '
        f'{stasiun[start]} -> {stasiun[end]}',
        color='#FF0381', fontsize=13, fontweight='bold', y=0.98
    )

    visited_nodes = []

    def animate(frame):
        nonlocal visited_nodes

        if frame < len(steps):
            current = steps[frame]
            visited_nodes = steps[:frame + 1]

            # Warna tiap node sesuai statusnya
            nc = []
            for n in nodes:
                if n == start:
                    nc.append("#0C2A52")
                elif n == end:
                    nc.append('#0C2A52')
                elif n == current:
                    nc.append('#0C2A52')
                elif n in visited_nodes[:-1]:
                    nc.append('#0C2A52')
                else:
                    nc.append(base_nc[nodes.index(n)])

            draw_frame(
                ax, G, nc, base_ec,
                start, end, current=current,
                title=(
                    f"[{algo}] Langkah {frame+1}/{len(steps)} "
                    f"| Memeriksa: {current} ({stasiun[current]})"
                )
            )

        else:
            # Frame terakhir: tampilkan rute hasil pencarian
            path_edges = []
            if path:
                for i in range(len(path) - 1):
                    path_edges.append((path[i], path[i+1]))

            nc = []
            for n in nodes:
                if n in path:
                    nc.append('#FFA9D4')
                elif n in visited_nodes:
                    nc.append('#FFA9D4')
                else:
                    nc.append(base_nc[nodes.index(n)])

            if path:
                rute_str = ' -> '.join(
                    f"{n}({stasiun[n]})" for n in path
                )

                jenis_rute = "Rute terbaik" if algo == "BFS" else "Rute hasil DFS"

                title = (
                    f"[{algo}] {jenis_rute} ditemukan! "
                    f"Panjang: {len(path)-1} edge | Waktu: {waktu:.4f} ms\n"
                    f"{rute_str}"
                )

            else:
                title = f"[{algo}] Tidak ada rute dari {start} ke {end}."

            draw_frame(
                ax, G, nc, base_ec,
                start, end,
                path_edges=path_edges,
                title=title
            )

    anim = animation.FuncAnimation(
        fig, animate,
        frames=total_frames,
        interval=interval_ms,
        repeat=False
    )

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

    return steps, path, waktu

# input di terminal untuk memilih stasiun, algoritma, dan kecepatan animasi
def tampilkan_daftar_stasiun():
    print("\n Daftar Stasiun:")
    for k, v in stasiun.items():
        print(f"{k} = {v}")

def pilih_stasiun(prompt):
    while True:
        tampilkan_daftar_stasiun()
        nilai = input(f"\n  {prompt} (masukkan kode huruf):").strip().upper()
        if nilai in stasiun:
            return nilai
        print(f"Kode '{nilai}' tidak valid. Coba lagi.")

def pilih_algoritma():
    while True:
        print("\n Pilih Algoritma:")
        print("1. BFS (Breadth-First Search)")
        print("2. DFS (Depth-First Search)")
        pilihan = input("\n Masukkan pilihan algoritma:").strip().upper()
        if pilihan in ('1', 'BFS'):
            return 'BFS'
        if pilihan in ('2', 'DFS'):
            return 'DFS'
        print("Pilihan tidak valid.")

def pilih_kecepatan():
    print("\n  Kecepatan animasi:")
    print("1. Lambat (700 ms/langkah)")
    print("2. Normal (400 ms/langkah)") # default
    print("3. Cepat (200 ms/langkah)")
    print("4. Sangat cepat (80 ms/langkah)")
    pilihan = input("\n Pilih kecepatan:").strip()
    mapping = {'1': 700, '2': 400, '3': 200, '4': 80, '': 400}
    return mapping.get(pilihan, 400)

def tampilkan_hasil(algo, start, end, steps, path, waktu):
    print(f"Hasil Pencarian {algo}")
    print(f"Asal   : {start} - {stasiun[start]}")
    print(f"Tujuan : {end} - {stasiun[end]}")
    print(f"Waktu  : {waktu:.4f} ms")
    print(f"\n Urutan kunjungan ({len(steps)} langkah):")
    print("  " + " -> ".join(steps))
    if path:
        if algo == 'BFS':
            print(f"\n Rute terbaik berdasarkan jumlah edge ({len(path)-1} edge):")
        else:
            print(f"\n Rute hasil DFS, bukan selalu rute terbaik ({len(path)-1} edge):")

        print("  " + " -> ".join(f"{n}({stasiun[n]})" for n in path))
    else:
        print("\n Tidak ada rute yang ditemukan.")
   
def tampilkan_info_graph():
    print("Graph Jaringan KRL Jabodetabek")
    print(f"Jumlah simpul (V) : {len(graph)}")
    print(f"Jumlah sisi   (E) : {hitung_sisi(graph)}")
    print(f"Kompleksitas BFS/1DFS : O(V+E) = O({len(graph)} + {hitung_sisi(graph)}) = O({len(graph)+hitung_sisi(graph)})")
    print()
    print("Adjacency List:")
    for v, nb in graph.items():
        n_str = ', '.join(f"{t}({stasiun[t]})" for t in nb)
        print(f"{v} {stasiun[v]:<15} -> {n_str}")

def pencarian_rute():
    while True:
        start = pilih_stasiun("Stasiun ASAL")
        end = pilih_stasiun("Stasiun TUJUAN")

        if start == end:
            print("Asal dan tujuan tidak boleh sama!")
            continue

        algo = pilih_algoritma()
        speed = pilih_kecepatan()

        print(f"\nMenjalankan {algo}: {start}({stasiun[start]}) -> {end}({stasiun[end]}) ...")
        print("(Tutup jendela grafik untuk melanjutkan)\n")

        steps, path, waktu = jalankan_animasi(start, end, algo, speed)
        tampilkan_hasil(algo, start, end, steps, path, waktu)

        lagi = input("\nCari rute lain? (y/n): ").strip().lower()
        if lagi != 'y':
            print("\nTerima kasih!\n")
            exit()

# MAIN PROGRAM
def main():
    print("KRL Jabodetabek - BFS & DFS")

    tampilkan_info_graph()

    while True:
        print("\nMENU PROGRAM")
        print("1. Eksperimen BFS dan DFS")
        print("2. Pencarian rute")

        pilihan = input("Pilih menu: ").strip()

        if pilihan == '1':
            jalankan_eksperimen()
        elif pilihan == '2':
            pencarian_rute()
        else:
            print("Pilihan tidak valid.")

if __name__ == '__main__':
    main()