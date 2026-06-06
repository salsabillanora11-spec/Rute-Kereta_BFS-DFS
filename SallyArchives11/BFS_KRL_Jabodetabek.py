from collections import deque
import time 

# Data Graph Stasiun Jabodetabek
stasiun = {
      'A' : "Gambir",
      'B' : "Manggarai",
      'C' : "Tanah Abang",
      'D' : "Duri",
      'E' : "Jatinegara",
      'F' : "Bekasi",
      'G' : "Depok",
      'H' : "Citayam",
      'I' : "Bogor",
      'J' : "Nambo",
      'K' : "Serpong",
      'L' : "Maja",
      'M' : "Cikarang",
      'N' : "Kampung Bandan",
      'O' : "Rajawali",
}

# 20 edge yang menghubungkan stasiun-stasiun tersebut
edges = [
      ('A', 'B'),
      ('A', 'C'),
      ('B', 'E'),
      ('B', 'G'),
      ('C', 'D'),
      ('C', 'K'),
      ('D', 'N'),
      ('D', 'O'),
      ('E', 'F'),
      ('E', 'J'),
      ('F', 'M'),
      ('G', 'H'),
      ('G', 'K'),
      ('H', 'I'),
      ('H', 'J'),
      ('I', 'J'),
      ('K', 'L'),
      ('M', 'F'),
      ('N', 'O'),
]

# adjacency list pakai huruf sebagai key
def create_adjacency_list(nodes: dict, edges: list[tuple]) -> dict:
    adj = {k: [] for k in nodes.keys()}
    for u, v in edges:
        if v not in adj[u]:
            adj[u].append(v)
        if u not in adj[v]:
            adj[v].append(u)
    for k in adj:
        adj[k].sort()
    return adj

# Algoritma BFS 
def bfs(adj: dict, simpul_awal: str) -> list[str]:
    visited = set()
    queue = deque([simpul_awal])
    visited.add(simpul_awal)
    urutan = []
 
    while queue:
        u = queue.popleft()
        urutan.append(u)
        for v in adj[u]:
            if v not in visited:
                visited.add(v)
                queue.append(v)
    return urutan

# Algoritma DFS Rekursif
def dfs_rekursif(adj: dict, simpul_awal: str) -> list[str]:
    visited = set()
    urutan = []
    def _dfs(u: str):
        visited.add(u)
        urutan.append(u)
        for v in adj[u]:
            if v not in visited:
                _dfs(v)
    _dfs(simpul_awal)
    return urutan

# Algoritma DFS Iteratif
def dfs_iteratif(adj: dict, simpul_awal: str) -> list[str]:
    visited = set()
    stack = [simpul_awal]
    urutan = []
    while stack:
        u = stack.pop()
        if u in visited:
            continue
        visited.add(u)
        urutan.append(u)
        for v in reversed(adj[u]):
            if v not in visited:
                stack.append(v)
    return urutan

# pengukuran Waktu
def ukur_waktu(fungsi, adj: dict, simpul_awal: str, n_iterasi: int = 10) -> tuple[list, list]:
    hasil = None
    waktu_list = []
    for _ in range(n_iterasi):
        t0 = time.perf_counter()
        hasil = fungsi(adj, simpul_awal)
        t1 = time.perf_counter()
        waktu_list.append((t1 - t0) * 1000)  # ms
    return hasil, waktu_list

# Analisis Rute BFS dan DFS
def hitung_rute_unik(adj: dict, urutan: list[str]) -> set[frozenset]:
    rute = set()
    for i in range(len(urutan) - 1):
        u, v = urutan[i], urutan[i + 1]
        if v in adj[u]:
            rute.add(frozenset({u, v}))
    return rute

# Mencetak hasil 
def cetak_urutan(urutan: list[str], label: str = ""):
    if label:
        print(f"\n  {label}")
    print("  " + " -> ".join(f"{stasiun[s]}" for s in urutan))
    print("  Indeks:", urutan)

def cetak_separator(char: str = "-", lebar: int = 60):
    print(char * lebar)

def cetak_statistik(nama: str, waktu_list: list[float]):
    avg = sum(waktu_list) / len(waktu_list)
    mn  = min(waktu_list)
    mx  = max(waktu_list)
    print(f"  Rata-rata : {avg:.4f} ms")
    print(f"  Min       : {mn:.4f} ms")
    print(f"  Maks      : {mx:.4f} ms")
    print(f"  Stdev     : {(sum((x-avg)**2 for x in waktu_list)/len(waktu_list))**0.5:.4f} ms")

# Main Program
def main():
    N_iterasi  = 10
    simpul_awal = 'A'  # Gambir
    adj = create_adjacency_list(stasiun, edges)

    print()
    cetak_separator("=")
    print("  BFS vs DFS - Jaringan KRL Jabodetabek")
    print(f"  Graf: {len(stasiun)} simpul | {len(edges)} sisi | Simpul awal: {stasiun[simpul_awal]}")
    print(f"  Iterasi pengukuran: {N_iterasi}x")
    cetak_separator("=")

    # Info Graf
    print("\n ADJACENCY LIST:")
    for i, tetangga in adj.items():
        nama_tet = [stasiun[t] for t in tetangga]
        print(f"  {stasiun[i]:20s} -> {', '.join(nama_tet)}")

    # BFS
    cetak_separator()
    print("\n BREADTH-FIRST SEARCH (BFS)")
    cetak_separator()
    hasil_bfs, waktu_bfs = ukur_waktu(bfs, adj, simpul_awal, N_iterasi)
    rute_bfs = hitung_rute_unik(adj, hasil_bfs)
    cetak_urutan(hasil_bfs, "Urutan kunjungan:")
    print(f"\n  Simpul dikunjungi : {len(hasil_bfs)} / {len(stasiun)}")
    print(f"  Rute unik (edge)  : {len(rute_bfs)}")

    # DFS Rekursif
    cetak_separator()
    print("\n DEPTH-FIRST SEARCH (DFS) - Rekursif")
    cetak_separator()
    hasil_dfs_r, waktu_dfs_r = ukur_waktu(dfs_rekursif, adj, simpul_awal, N_iterasi)
    rute_dfs_r = hitung_rute_unik(adj, hasil_dfs_r)
    cetak_urutan(hasil_dfs_r, "Urutan kunjungan:")

    # DFS Iteratif
    cetak_separator()
    print("\n DEPTH-FIRST SEARCH (DFS) — Iteratif (Stack)")
    cetak_separator()
    hasil_dfs_i, waktu_dfs_i = ukur_waktu(dfs_iteratif, adj, simpul_awal, N_iterasi)
    rute_dfs_i = hitung_rute_unik(adj, hasil_dfs_i)
    cetak_urutan(hasil_dfs_i, "Urutan kunjungan:")

if __name__ == "__main__":
    main()
