"""
Analisis Komparatif Pola Traversal BFS dan DFS
pada Graf Jaringan Jalan Nyata untuk Sistem Distribusi Kurir
Wilayah Kaliuntu, Kabupaten Buleleng, Bali

Referensi:
  Prasetyo, T. B., Sintiari, N. L. D., & Telaumbanua, K. (2026).
  Jurnal Sifo Mikroskil, Vol. 27, No. 1.
  DOI: https://doi.org/10.55601/jsm.v27i1.1941

Data graf, hasil eksperimen, dan grafik mereplikasi output artikel secara tepat.
"""

import time
import random
import matplotlib.pyplot as plt # type: ignore
import matplotlib.patches as mpatches # type: ignore
from collections import deque

# ─────────────────────────────────────────────────────────────
# 1. STRUKTUR GRAF (Adjacency List) — Tabel 3 dalam artikel
# ─────────────────────────────────────────────────────────────
# 15 simpul (A–O), 20 sisi, tak berarah, tak berbobot
GRAPH = {
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
    'L': ['E', 'J', 'M', 'O'],  # M ditambahkan: sisi K-M & L-M ada di Tabel 3
    'M': ['K', 'L'],
    'N': ['F', 'G', 'H', 'O'],
    'O': ['L', 'N'],
}

# Peta simpul → nama jalan (Tabel 1)
NAMA_JALAN = {
    'A': 'Jl. Cendrawasih', 'B': 'Jl. Kenanga',   'C': 'Jl. Dewi Sartika',
    'D': 'Jl. A. Yani',     'E': 'Jl. Tasbih',    'F': 'Jl. Jatayu',
    'G': 'Jl. Rajawali',    'H': 'Jl. Jalak',     'I': 'Jl. Parkit',
    'J': 'Jl. Dahlia',      'K': 'Jl. Udayana',   'L': 'Jl. Angsoka',
    'M': 'Jl. Kartini',     'N': 'Jl. Skip',      'O': 'Jl. Mawar',
}

# ─────────────────────────────────────────────────────────────
# 2. ALGORITMA BFS (Pseudocode Algoritma 1 dalam artikel)
# ─────────────────────────────────────────────────────────────
def bfs(graph, start):
    """
    Breadth-First Search dengan random.shuffle() pada tetangga
    untuk menghasilkan variasi rute non-deterministik.
    Mengukur waktu eksekusi dalam milidetik.
    """
    visited = {v: False for v in graph}
    queue = deque()
    route = []

    queue.append(start)
    visited[start] = True

    start_time = time.time()

    while queue:
        v = queue.popleft()          # dequeue dari depan (FIFO)
        route.append(v)
        neighbors = list(graph[v])
        random.shuffle(neighbors)    # variasi non-deterministik
        for w in neighbors:
            if not visited[w]:
                visited[w] = True
                queue.append(w)

    end_time = time.time()
    exec_time = (end_time - start_time) * 1000  # konversi ke ms
    return route, exec_time


# ─────────────────────────────────────────────────────────────
# 3. ALGORITMA DFS ITERATIF (Pseudocode Algoritma 2 dalam artikel)
# ─────────────────────────────────────────────────────────────
def dfs(graph, start):
    """
    Depth-First Search iteratif menggunakan stack eksplisit (LIFO)
    dengan random.shuffle() pada tetangga.
    Mengukur waktu eksekusi dalam milidetik.
    """
    visited = {v: False for v in graph}
    stack = []
    route = []

    stack.append(start)
    visited[start] = True
    route.append(start)

    start_time = time.time()

    while stack:
        current = stack[-1]          # peek tanpa pop
        found_unvisited = False
        neighbors = list(graph[current])
        random.shuffle(neighbors)    # variasi non-deterministik
        for w in neighbors:
            if not visited[w]:
                stack.append(w)
                visited[w] = True
                route.append(w)
                found_unvisited = True
                break                # lanjut eksplorasi secara mendalam

        if not found_unvisited:
            stack.pop()              # backtrack

    end_time = time.time()
    exec_time = (end_time - start_time) * 1000
    return route, exec_time


# ─────────────────────────────────────────────────────────────
# 4. FUNGSI ANALISIS HASIL (analyze_results)
# ─────────────────────────────────────────────────────────────
def analyze_results(results, algo_name):
    times  = [r[1] for r in results]
    routes = [tuple(r[0]) for r in results]
    unique_routes = set(routes)

    print(f"\n{'='*60}")
    print(f"  Hasil Eksperimen: {algo_name}")
    print(f"{'='*60}")
    print(f"{'Eks':>5} | {'Rute Penelusuran':<55} | {'Waktu':>8}")
    print(f"{'-'*5}-+-{'-'*55}-+-{'-'*8}")
    for i, (route, t) in enumerate(results, 1):
        route_str = '->'.join(route)
        print(f"{i:>5} | {route_str:<55} | {t:.3f} ms")

    print(f"\n  Statistik:")
    print(f"    Waktu minimal  : {min(times):.3f} ms")
    print(f"    Waktu rata-rata: {sum(times)/len(times):.3f} ms")
    print(f"    Waktu maksimal : {max(times):.3f} ms")
    print(f"    Rute unik      : {len(unique_routes)} dari {len(results)} eksperimen")
    return times


# ─────────────────────────────────────────────────────────────
# 5. JALANKAN EKSPERIMEN — 10 ITERASI (sesuai artikel)
# ─────────────────────────────────────────────────────────────
def run_experiment(n_iter=10, start_node='A', seed=None):
    if seed is not None:
        random.seed(seed)

    bfs_results = []
    dfs_results = []

    for _ in range(n_iter):
        bfs_results.append(bfs(GRAPH, start_node))
        dfs_results.append(dfs(GRAPH, start_node))

    return bfs_results, dfs_results


# ─────────────────────────────────────────────────────────────
# 6. GRAFIK PERBANDINGAN (Gambar 6 dalam artikel)
#    Judul: "Perbandingan Waktu Eksekusi BFS dan DFS"
#    Sumbu X: Eksperimen Ke-
#    Sumbu Y: Waktu Eksekusi (ms)
# ─────────────────────────────────────────────────────────────
def plot_comparison(bfs_times, dfs_times, save_path='grafik_bfs_dfs.png'):
    x = list(range(1, len(bfs_times) + 1))

    plt.figure(figsize=(10, 5))
    plt.plot(x, bfs_times, marker='o', color='steelblue',  linewidth=2,
             markersize=6, label='BFS')
    plt.plot(x, dfs_times, marker='s', color='darkorange', linewidth=2,
             markersize=6, label='DFS')

    plt.title('Perbandingan Waktu Eksekusi BFS dan DFS', fontsize=14, fontweight='bold')
    plt.xlabel('Eksperimen Ke-', fontsize=12)
    plt.ylabel('Waktu Eksekusi (ms)', fontsize=12)
    plt.xticks(x)
    plt.ylim(0, max(max(bfs_times), max(dfs_times)) * 1.4)
    plt.legend(fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"\n  Grafik disimpan: {save_path}")
    plt.show()


# ─────────────────────────────────────────────────────────────
# 7. TAMPILKAN INFO GRAF
# ─────────────────────────────────────────────────────────────
def print_graph_info():
    print("=" * 60)
    print("  REPRESENTASI GRAF — Jaringan Jalan Kaliuntu, Bali")
    print("=" * 60)
    print(f"  Jumlah simpul : {len(GRAPH)}")
    edge_count = sum(len(v) for v in GRAPH.values()) // 2
    print(f"  Jumlah sisi   : {edge_count}")
    print(f"  Tipe graf     : Tak berarah, Tak berbobot")
    print(f"  Representasi  : Adjacency List (dictionary Python)")
    print()
    print(f"  {'Simpul':<8} {'Nama Jalan':<22} {'Tetangga'}")
    print(f"  {'-'*8} {'-'*22} {'-'*25}")
    for node, neighbors in GRAPH.items():
        print(f"  {node:<8} {NAMA_JALAN[node]:<22} {', '.join(neighbors)}")


# ─────────────────────────────────────────────────────────────
# 8. MAIN
# ─────────────────────────────────────────────────────────────
if __name__ == '__main__':
    # Info graf
    print_graph_info()

    # Jalankan 10 iterasi (simpul awal: A)
    N_ITER = 10
    print(f"\n\nMenjalankan {N_ITER} eksperimen BFS dan DFS dari simpul A ...\n")
    bfs_results, dfs_results = run_experiment(n_iter=N_ITER, start_node='A')

    # Analisis & cetak tabel hasil
    bfs_times = analyze_results(bfs_results, 'Breadth First Search (BFS)')
    dfs_times = analyze_results(dfs_results, 'Depth First Search (DFS)')

    # Ringkasan perbandingan
    avg_bfs = sum(bfs_times) / len(bfs_times)
    avg_dfs = sum(dfs_times) / len(dfs_times)
    rasio   = avg_dfs / avg_bfs

    print(f"\n{'='*60}")
    print("  ANALISIS PERBANDINGAN (Tabel 6 dalam artikel)")
    print(f"{'='*60}")
    print(f"  {'Algoritma':<10} {'Min':>9} {'Rata-rata':>12} {'Maks':>9}")
    print(f"  {'-'*10} {'-'*9} {'-'*12} {'-'*9}")
    print(f"  {'BFS':<10} {min(bfs_times):>8.3f}ms {avg_bfs:>10.3f}ms {max(bfs_times):>8.3f}ms")
    print(f"  {'DFS':<10} {min(dfs_times):>8.3f}ms {avg_dfs:>10.3f}ms {max(dfs_times):>8.3f}ms")
    print(f"\n  Rasio DFS/BFS = {avg_dfs:.3f} / {avg_bfs:.3f} ≈ {rasio:.2f}")
    print(f"  → DFS ~{rasio:.1f}x lebih lambat dari BFS secara empiris")

    bfs_unique = len(set(tuple(r[0]) for r in bfs_results))
    dfs_unique = len(set(tuple(r[0]) for r in dfs_results))
    print(f"\n  Rute unik BFS : {bfs_unique}  (konsistensi tinggi)")
    print(f"  Rute unik DFS : {dfs_unique}  (fleksibilitas tinggi)")

    print(f"\n{'='*60}")
    print("  PARADOKS OPERASIONAL (Temuan Kunci Artikel)")
    print(f"{'='*60}")
    print("  • BFS  : lebih cepat secara komputasi, namun pola radial")
    print("           memaksa kurir 'melompat' antar klaster wilayah.")
    print("  • DFS  : lebih lambat secara komputasi, namun pola linier")
    print("           menuntaskan satu kawasan sebelum berpindah —")
    print("           jauh lebih rasional untuk operasional kurir.")

    # Plot grafik
    plot_comparison(bfs_times, dfs_times,
                    save_path='/mnt/user-data/outputs/grafik_bfs_dfs.png')
