import time
import random
import os
import statistics
from collections import deque
import matplotlib.pyplot as plt   # type: ignore
import matplotlib.patches as mpatches   # type: ignore
import networkx as nx  # type: ignore
import matplotlib.colors as mcolors 
# 1. DEFINISI GRAF — KRL JABODETABEK (15 Simpul (Stasiun), 20 Sisi (Koneksi Jalur))

# Label simpul (Nama Stasiun KRL)
stasiun = {
    'A': 'Manggarai',
    'B': 'Sudirman',
    'C': 'Gondangdia',
    'D': 'Cikini',
    'E': 'Tebet',
    'F': 'Pasar Minggu',
    'G': 'Depok',
    'H': 'Bogor',
    'I': 'Bekasi',
    'J': 'Klender',
    'K': 'Jatinegara',
    'L': 'Tanah Abang',
    'M': 'Palmerah',
    'N': 'Kebayoran',
    'O': 'Serpong',
}

# Adjacency List — Graf Tak Berarah, Tak Berbobot
# Struktur konektivitas merefleksikan jaringan KRL Jabodetabek
graph = {
    'A': ['B', 'D'],            # Manggarai -> Sudirman, Cikini
    'B': ['A', 'E'],            # Sudirman -> Manggarai, Tebet
    'C': ['D', 'H'],            # Gondangdia -> Cikini, Bogor
    'D': ['A', 'C', 'I'],       # Cikini -> Manggarai, Gondangdia, Bekasi
    'E': ['B', 'J', 'L'],       # Tebet -> Sudirman, Klender, Tanah Abang
    'F': ['G', 'N'],            # Pasar Minggu -> Depok, Kebayoran
    'G': ['F', 'H', 'N'],       # Depok -> Pasar Minggu, Bogor, Kebayoran
    'H': ['C', 'G', 'I', 'N'],  # Bogor -> Gondangdia, Depok, Bekasi, Kebayoran
    'I': ['D', 'H'],            # Bekasi -> Cikini, Bogor
    'J': ['E', 'K', 'L'],       # Klender -> Tebet, Jatinegara, Tanah Abang
    'K': ['J', 'M'],            # Jatinegara -> Klender, Palmerah
    'L': ['E', 'J', 'O'],       # Tanah Abang -> Tebet, Klender, Serpong
    'M': ['K', 'L'],            # Palmerah -> Jatinegara, Tanah Abang
    'N': ['F', 'G', 'H', 'O'],  # Kebayoran -> Pasar Minggu, Depok, Bogor, Serpong
    'O': ['L', 'N'],            # Serpong -> Tanah Abang, Kebayoran
}

# Verifikasi jumlah sisi
def hitung_sisi(graph):
    total = sum(len(v) for v in graph.values())
    return total // 2  # Graf tak berarah -> bagi 2

print("=" * 60)
print("  GRAF JARINGAN KRL JABODETABEK")
print("=" * 60)
print(f"  Jumlah simpul (V) : {len(graph)}")
print(f"  Jumlah sisi   (E) : {hitung_sisi(graph)}")
print()
print("  Daftar Simpul (Stasiun):")
for kode, nama in stasiun.items():
    print(f"    {kode} = {nama}")
print()
print("  Adjacency List:")
for simpul, tetangga in graph.items():
    nama_simpul = stasiun[simpul]
    nama_tetangga = ', '.join([f"{t}({stasiun[t]})" for t in tetangga])
    print(f"    {simpul} ({nama_simpul:15s}) -> {nama_tetangga}")
print()

# 2. ALGORITMA BFS (Menggunakan antrian (queue) FIFO)

def bfs(graph, start):
    
    visited = {v: False for v in graph}
    queue = deque()
    route = []

    queue.append(start)
    visited[start] = True

    start_time = time.time()

    while queue:
        v = queue.popleft()       

        neighbors = sorted(graph[v])
        random.shuffle(neighbors)  

        for w in neighbors:
            if not visited[w]:
                visited[w] = True
                queue.append(w)   

    end_time = time.time()
    waktu_ms = (end_time - start_time) * 1000

    return route, waktu_ms

# 3. ALGORITMA DFS (Menggunakan tumpukan (stack) LIFO — iteratif)

def dfs(graph, start):
    
    visited = {v: False for v in graph}
    stack = [start]
    route = [start]

    stack.append(start)
    visited[start] = True
    route.append(start)

    start_time = time.time()

    while stack:
        current = stack[-1]       
        found_unvisited = False

        neighbors = sorted(graph[current])
        random.shuffle(neighbors)  

        for w in neighbors:
            if not visited[w]:
                stack.append(w)
                visited[w] = True
                route.append(w)
                found_unvisited = True
                break             

        if not found_unvisited:
            stack.pop()           

    end_time = time.time()
    waktu_ms = (end_time - start_time) * 1000

    return route, waktu_ms

# 4. EKSPERIMEN dengan 10 ITERASI
#    Simpul awal: A (Manggarai) — titik pusat/hub utama

SIMPUL_AWAL = 'A'
JUMLAH_ITERASI = 10

print("=" * 60)
print(f"  EKSPERIMEN: {JUMLAH_ITERASI} Iterasi | Simpul Awal: {SIMPUL_AWAL} ({stasiun[SIMPUL_AWAL]})")
print("=" * 60)

hasil_bfs = []
hasil_dfs = []

# Jalankan BFS 10 kali
print("\n Hasil Penelusuran BFS:")
print(f"  {'Eks':>3}  {'Rute Penelusuran':<55}  {'Waktu':>8}")
print("  " + "-" * 70)
for i in range(1, JUMLAH_ITERASI + 1):
    rute, waktu = bfs(graph, SIMPUL_AWAL)
    hasil_bfs.append({'rute': rute, 'waktu': waktu})
    rute_str = '->'.join(rute)
    print(f"  {i:>3}  {rute_str:<55}  {waktu:.3f} ms")

# Jalankan DFS 10 kali
print("\n Hasil Penelusuran DFS:")
print(f"  {'Eks':>3}  {'Rute Penelusuran':<55}  {'Waktu':>8}")
print("  " + "-" * 70)
for i in range(1, JUMLAH_ITERASI + 1):
    rute, waktu = dfs(graph, SIMPUL_AWAL)
    hasil_dfs.append({'rute': rute, 'waktu': waktu})
    rute_str = '->'.join(rute)
    print(f"  {i:>3}  {rute_str:<55}  {waktu:.3f} ms")

# 5. ANALISIS HASIL
def analyze_results(hasil, nama_algo):
    waktu_list = [h['waktu'] for h in hasil]
    rute_unik = set(tuple(h['rute']) for h in hasil)

    stats = {
        'min':   min(waktu_list),
        'median' : statistics.median(waktu_list), 
        'avg':   sum(waktu_list) / len(waktu_list),
        'max':   max(waktu_list),
        'rute_unik': len(rute_unik),
        'waktu_list': waktu_list,
    }
    return stats

stats_bfs = analyze_results(hasil_bfs, 'BFS')
stats_dfs = analyze_results(hasil_dfs, 'DFS')
rasio = stats_dfs['avg'] / stats_bfs['avg']

print()
print("=" * 60)
print("  ANALISIS PERBANDINGAN BFS vs DFS")
print("=" * 60)
print(f"  {'Metrik':<25} {'BFS':>12} {'DFS':>12}")
print("  " + "-" * 52)
print(f"  {'Waktu Minimum':<25} {stats_bfs['min']:>10.3f}ms {stats_dfs['min']:>10.3f}ms")
print(f"  {'Waktu Rata-rata':<25} {stats_bfs['avg']:>10.3f}ms {stats_dfs['avg']:>10.3f}ms")
print(f"  {'Waktu Maksimum':<25} {stats_bfs['max']:>10.3f}ms {stats_dfs['max']:>10.3f}ms")
print(f"  {'Jumlah Rute Unik':<25} {stats_bfs['rute_unik']:>12} {stats_dfs['rute_unik']:>12}")
print(f"  {'Rasio DFS/BFS':<25} {'—':>12} {rasio:>11.2f}x")
print()
print(f"  -> DFS {rasio:.2f}x lebih lambat dari BFS secara empiris")
print(f"  -> Keduanya memiliki kompleksitas teoritis O(V+E) = O({len(graph)}+{hitung_sisi(graph)}) = O({len(graph)+hitung_sisi(graph)})")

# 6. VISUALISASI

fig = plt.figure(figsize=(18, 14))
fig.patch.set_facecolor('#0f1117')

# Plot 1: Struktur Graf KRL
ax1 = fig.add_subplot(2, 2, (1, 2))
ax1.set_facecolor('#1a1d2e')
ax1.set_title('Struktur Graf Jaringan KRL Jabodetabek\n(15 Simpul, 20 Sisi — Tak Berarah, Tak Berbobot)',
              color='white', fontsize=13, pad=12)

G_nx = nx.Graph()
G_nx.add_nodes_from(graph.keys())
for simpul, tetangga in graph.items():
    for t in tetangga:
        G_nx.add_edge(simpul, t)

# Layout posisi — diatur manual agar menyerupai peta geografis KRL
pos = {
    'H': (0.0, 0.0),    # Bogor (paling selatan)
    'G': (0.5, 1.0),    # Depok
    'F': (1.0, 2.0),    # Pasar Minggu
    'E': (1.5, 3.0),    # Tebet
    'A': (2.5, 4.0),    # Manggarai (hub utama)
    'D': (2.0, 5.2),    # Cikini
    'C': (2.8, 5.8),    # Gondangdia
    'B': (3.5, 5.2),    # Sudirman
    'K': (3.5, 3.0),    # Jatinegara
    'J': (4.5, 2.5),    # Klender
    'I': (5.5, 2.0),    # Bekasi (paling timur)
    'L': (1.5, 5.2),    # Tanah Abang
    'M': (0.8, 4.5),    # Palmerah
    'N': (0.2, 3.5),    # Kebayoran
    'O': (-0.5, 2.5),   # Serpong (barat daya)
}

# Warna node berdasarkan kelompok jalur
warna_node = {
    'A': '#FF6B35', 'B': '#4FC3F7', 'C': '#4FC3F7', 'D': '#4FC3F7',
    'E': '#81C784', 'F': '#81C784', 'G': '#81C784', 'H': '#81C784',
    'I': '#FFD54F', 'J': '#FFD54F', 'K': '#FF6B35',
    'L': '#CE93D8', 'M': '#CE93D8', 'N': '#CE93D8', 'O': '#CE93D8',
}
node_colors = [warna_node[n] for n in G_nx.nodes()]
labels = {n: f"{n}\n{stasiun[n]}" for n in G_nx.nodes()}

nx.draw_networkx_edges(G_nx, pos, ax=ax1, edge_color='#555577',
                       width=2.0, alpha=0.8)
nx.draw_networkx_nodes(G_nx, pos, ax=ax1, node_color=node_colors,
                       node_size=1200, alpha=0.95)
nx.draw_networkx_labels(G_nx, pos, labels=labels, ax=ax1,
                        font_size=6.5, font_color='black', font_weight='bold')

# Legend jalur
legend_items = [
    mpatches.Patch(color='#FF6B35', label='Hub Utama (Manggarai/Jatinegara)'),
    mpatches.Patch(color='#4FC3F7', label='Lintas Kota (Bogor-Jak)'),
    mpatches.Patch(color='#81C784', label='Lintas Bogor/Depok'),
    mpatches.Patch(color='#FFD54F', label='Lintas Bekasi'),
    mpatches.Patch(color='#CE93D8', label='Lintas Serpong/Rangkasbitung'),
]
ax1.legend(handles=legend_items, loc='lower right', facecolor='#1a1d2e',
           edgecolor='#555577', labelcolor='white', fontsize=8)
ax1.axis('off')

# Plot 2: Perbandingan Waktu Eksekusi
ax2 = fig.add_subplot(2, 2, 3)
ax2.set_facecolor('#1a1d2e')
iterasi = list(range(1, JUMLAH_ITERASI + 1))
ax2.plot(iterasi, stats_bfs['waktu_list'], 'o-', color='#4FC3F7',
         linewidth=2, markersize=7, label='BFS', alpha=0.9)
ax2.plot(iterasi, stats_dfs['waktu_list'], 's-', color='#FF6B35',
         linewidth=2, markersize=7, label='DFS', alpha=0.9)
ax2.axhline(y=stats_bfs['avg'], color='#4FC3F7', linestyle='--',
            alpha=0.5, linewidth=1.2, label=f"Rata-rata BFS: {stats_bfs['avg']:.3f}ms")
ax2.axhline(y=stats_dfs['avg'], color='#FF6B35', linestyle='--',
            alpha=0.5, linewidth=1.2, label=f"Rata-rata DFS: {stats_dfs['avg']:.3f}ms")

ax2.set_title('Perbandingan Waktu Eksekusi BFS vs DFS\n(10 Iterasi, Simpul Awal: A/Manggarai)',
              color='white', fontsize=11)
ax2.set_xlabel('Eksperimen ke-', color='#aaaacc')
ax2.set_ylabel('Waktu Eksekusi (ms)', color='#aaaacc')
ax2.tick_params(colors='#aaaacc')
ax2.legend(facecolor='#1a1d2e', edgecolor='#555577', labelcolor='white', fontsize=8)
ax2.spines['bottom'].set_color('#555577')
ax2.spines['left'].set_color('#555577')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.grid(True, color='#333355', linestyle='--', alpha=0.5)
ax2.set_xticks(iterasi)

# Plot 3: Ringkasan Statistik
ax3 = fig.add_subplot(2, 2, 4)
ax3.set_facecolor('#1a1d2e')
ax3.axis('off')
ax3.set_title('Ringkasan Analisis Komparatif', color='white', fontsize=11)

tabel_data = [
    ['Metrik', 'BFS', 'DFS'],
    ['Waktu Min', f"{stats_bfs['min']:.3f} ms", f"{stats_dfs['min']:.3f} ms"],
    ['Waktu Rata-rata', f"{stats_bfs['avg']:.3f} ms", f"{stats_dfs['avg']:.3f} ms"],
    ['Waktu Maks', f"{stats_bfs['max']:.3f} ms", f"{stats_dfs['max']:.3f} ms"],
    ['Rute Unik', str(stats_bfs['rute_unik']), str(stats_dfs['rute_unik'])],
    ['Rasio DFS/BFS', '—', f"{rasio:.2f}x"],
    ['Kompleksitas', 'O(V+E)', 'O(V+E)'],
    ['Pola Traversal', 'Radial/Level', 'Linear/Depth'],
    ['Konsistensi', 'Tinggi', 'Sedang'],
    ['Efisiensi Spasial', 'Kurang optimal', 'Lebih rasional'],
]

tabel = ax3.table(
    cellText=tabel_data[1:],
    colLabels=tabel_data[0],
    cellLoc='center',
    loc='center',
    bbox=[0, 0, 1, 1]
)
tabel.auto_set_font_size(False)
tabel.set_fontsize(9)

for (baris, kolom), sel in tabel.get_celld().items():
    sel.set_edgecolor('#555577')
    if baris == 0:
        sel.set_facecolor('#2a2d4e')
        sel.set_text_props(color='white', fontweight='bold')
    elif kolom == 0:
        sel.set_facecolor('#1e2035')
        sel.set_text_props(color='#aaaacc')
    elif kolom == 1:
        sel.set_facecolor('#162030')
        sel.set_text_props(color='#4FC3F7')
    else:
        sel.set_facecolor('#251820')
        sel.set_text_props(color='#FF6B35')

plt.suptitle(
    'Analisis Komparatif BFS & DFS Graf Jaringan KRL Jabodetabek\n'
    'Diadaptasi dari: Prasetyo et al. (2026), DOI: 10.55601/jsm.v27i1.1941',
    color='white', fontsize=13, y=0.98,
    fontweight='bold'
)
plt.tight_layout(rect=[0, 0, 1, 0.96])

output_dir = r"C:\Users\Hype\.vscode\SallyArchives11\outputs"
os.makedirs(output_dir, exist_ok=True) # Akan membuat folder krna folder blm ada

output_path = os.path.join(output_dir, "bfs_dfs_krl_jabodetabek.png") 
# nb : os.path.join() akan menggabungkan path dengan benar sesuai OS 

# Menyimpan gmbr dg wanra background  
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#0f1117')
plt.show()

print(f"\n   Visualisasi tersimpan: {output_path}")

# 7. CETAK RUTE TERBAIK (CONTOH)
print()
print("=" * 60)
print("  CONTOH RUTE TRAVERSAL (Eksperimen ke-1)")
print("=" * 60)

# memilih stasiun awal
print("\nDaftar Stasiun : ")
for kode, nama in stasiun.items():
    print(f"  {kode} = {nama}")

pilihan = input("\nPilih stasiun keberangkatan (ex: A): ").strip().upper()
if pilihan not in graph:
    print("Kode tidak valid, default ke A (Manggarai)")
    pilihan = 'A'

# menjalankan BFS & DFS dari stasiun pilihan
rute_bfs, waktu_bfs = bfs(graph, pilihan)
rute_dfs, waktu_dfs = dfs(graph, pilihan)

print(f"\n   BFS — Pola Radial (level-by-level) dari {pilihan} ({stasiun[pilihan]}):")
for i, simpul in enumerate(rute_bfs, 1):
    print(f"    Langkah {i:>2}: {simpul} — {stasiun[simpul]}")

print(f"\n   DFS — Pola Linear (depth-first) dari {pilihan} ({stasiun[pilihan]}):")
for i, simpul in enumerate(rute_dfs, 1):
    print(f"    Langkah {i:>2}: {simpul} — {stasiun[simpul]}")

print()
print("=" * 60)
print("  KESIMPULAN")
print("=" * 60)