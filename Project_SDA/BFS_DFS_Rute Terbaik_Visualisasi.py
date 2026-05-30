# kode 2 (pencarian rute terbaik):

import time
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.animation as animation
import networkx as nx

# data graph
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
    'L': ['E', 'J', 'M', 'O'],      # Duri -> Pasar Minggu, Jatinegara, Tangerang, Bogor
    'M': ['K', 'L'],                # Tangerang -> Bekasi, Duri
    'N': ['F', 'G', 'H', 'O'],      # Serpong -> Tanah Abang, Palmerah, Kebayoran, Bogor
    'O': ['L', 'N'],                # Bogor -> Duri, Serpong
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
def bfs_path(graph, start, end):
    visited = {start: None}   # node: parent
    queue = deque([start])
    steps = []                # urutan kunjungan untuk animasi

    t0 = time.perf_counter()

    while queue:
        v = queue.popleft()
        steps.append(v)

        if v == end:
            break

        for w in sorted(graph[v]):
            if w not in visited:
                visited[w] = v
                queue.append(w)

    waktu_ms = (time.perf_counter() - t0) * 1000

    # Rekonstruksi jalur
    path, cur = [], end
    while cur is not None:
        path.append(cur)
        cur = visited.get(cur)
    path.reverse()

    if not path or path[0] != start:
        path = []

    return steps, path, waktu_ms

# DFS
def dfs_path(graph, start, end):
    visited = {start: None}
    stack   = [start]
    steps   = []

    t0 = time.perf_counter()

    while stack:
        v = stack.pop()
        if v in steps:
            continue
        steps.append(v)

        if v == end:
            break

        for w in reversed(sorted(graph[v])):
            if w not in visited:
                visited[w] = v
                stack.append(w)

    waktu_ms = (time.perf_counter() - t0) * 1000

    path, cur = [], end
    while cur is not None:
        path.append(cur)
        cur = visited.get(cur)
    path.reverse()

    if not path or path[0] != start:
        path = []

    return steps, path, waktu_ms

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

    ax.text(3.0, 2.4,
            "Jalur pink menendakan rute hasil pencarian. \n"
            "Itu adalah jalur tercepat dari stasiun asal ke tujuan.",
            fontsize=8, color='#050003', ha='center', va='top', 
            fontfamily='monospace')

    # Edge biasa
    nx.draw_networkx_edges(
        G, pos, ax=ax,
        edge_color=edge_colors, width=3, alpha=0.75
    )

    # Edge rute hasil pencarian ditampilkan di atas edge biasa (warna pink tebal)
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

    # Highlight node yang sedang diperiksa (berdenyut lebih terang)
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
        steps, path, waktu = bfs_path(graph, start, end)
    else:
        steps, path, waktu = dfs_path(graph, start, end)

    total_frames = len(steps) + 1   # +1 untuk frame hasil akhir

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
                    nc.append('#0C2A52')          # sedang diperiksa
                elif n in visited_nodes[:-1]:
                    nc.append('#0C2A52')          # sudah dikunjungi
                else:
                    nc.append(base_nc[nodes.index(n)])

            draw_frame(
                ax, G, nc, base_ec,
                start, end, current=current,
                title=(
                    f"[{algo}] Langkah {frame+1}/{len(steps)}"
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
                    nc.append('#FFA9D4')   # untuk path
                elif n in visited_nodes:
                    nc.append('#FFA9D4')   # node dikunjungi tapi bukan path
                else:
                    nc.append(base_nc[nodes.index(n)])

            if path:
                rute_str = '->'.join(
                    f"{n}({stasiun[n]})" for n in path
                )
                jenis_rute = "Rute terbaik" if algo == "BFS" else "Rute hasil DFS"

                title = (
                    f"[{algo}] {jenis_rute} ditemukan! "
                    f"Panjang: {len(path)-1} edge | Waktu: {waktu:.4f} ms\n"
                    f"{rute_str}\n"
                    f"Rute ini menunjukkan jalur tercepat dari {stasiun[start]} menuju [stasiun[end]]"
                    f"berdasarkan jumlah edge yang dilalui"
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
        pilihan = input("\n Masukkan pilihan (1/2) atau langsung ketik BFS/DFS:").strip().upper()
        if pilihan in ('1', 'BFS'):
            return 'BFS'
        if pilihan in ('2', 'DFS'):
            return 'DFS'
        print("Pilihan tidak valid.")

def pilih_kecepatan():
    print("\n  Kecepatan animasi:")
    print("1. Lambat (700 ms/langkah)")
    print("2. Normal (400 ms/langkah)  <- default")
    print("3. Cepat (200 ms/langkah)")
    print("4. Sangat cepat (80 ms/langkah)")
    pilihan = input("\n Pilih kecepatan [1-4, Enter=2]:").strip()
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
    print(f"Kompleksitas BFS/DFS : O(V+E) = O({len(graph)} + {hitung_sisi(graph)}) = O({len(graph)+hitung_sisi(graph)})")
    print()
    print("Adjacency List:")
    for v, nb in graph.items():
        n_str = ', '.join(f"{t}({stasiun[t]})" for t in nb)
        print(f"{v} ({stasiun[v]:<15}) -> {n_str}")

# Main
def main():
    print("KRL Jabodetabek - Pencarian Rute BFS & DFS")

    tampilkan_info_graph()

    while True:
        start = pilih_stasiun("Stasiun ASAL")
        end = pilih_stasiun("Stasiun TUJUAN")

        if start == end:
            print("Asal dan tujuan tidak boleh sama!")
            continue

        algo = pilih_algoritma()
        speed = pilih_kecepatan()

        print(f"\n Menjalankan {algo}: {start}({stasiun[start]}) -> {end}({stasiun[end]}) ...")
        print("(Tutup jendela grafik untuk melanjutkan)\n")

        steps, path, waktu = jalankan_animasi(start, end, algo, speed)
        tampilkan_hasil(algo, start, end, steps, path, waktu)

        lagi = input("\n Cari rute lain? (y/n): ").strip().lower()
        if lagi != 'y':
            break

    print("\n Terima kasih!\n")

if __name__ == '__main__':
    main()
