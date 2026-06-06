import time                                 # mengukur waktu eksekusi
import random                               # mengacak urutan tetangga saat eksperimen
from statistics import mean, median, stdev  # menghitung statistik hasil eksperimen
from collections import deque               # queue algoritma BFS
import matplotlib.pyplot as plt             # visualisasi graph
import matplotlib.patches as mpatches       # legend visualisasi
import matplotlib.animation as animation    # membuat animasi 
from matplotlib.lines import Line2D         # lingkaran untuk legend
import networkx as nx                       # membuat dan mengukur graph      

# DATA GRAPH
stasiun = {                        # mapping kode huruf -> nama stasiun
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
graph = {                         # hubungan antar stasiun
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

pos = {                    # koordinat node untuk digambar di grafik
    'A': (3.0, 5.0), 'B': (3.0, 6.2), 'C': (1.8, 4.2),
    'D': (1.8, 5.0), 'E': (3.0, 7.4), 'F': (0.2, 7.8),
    'G': (1.0, 7.2), 'H': (1.0, 5.8), 'I': (1.2, 3.4),
    'J': (4.4, 7.4), 'K': (5.8, 7.4), 'L': (3.0, 8.6),
    'M': (5.8, 8.6), 'N': (0.2, 6.4), 'O': (3.0, 9.8),
}

jalur_info = {                # informasi jalur KRL (node yg dilalui + warna jalur)
    'Bogor': {'nodes': ['A','B','E','J','L','O'], 'color': "#FFA9D4"},
    'Bekasi': {'nodes': ['A','B','E','J','K','M'], 'color': '#FFA9D4'},
    'Depok': {'nodes': ['A','D','C','I','H'], 'color': '#FFA9D4'},
    'Serpong': {'nodes': ['F','G','N','O'], 'color': '#FFA9D4'},
    'Tangerang': {'nodes': ['F','G','H','N'], 'color': '#FFA9D4'},
}

nodes = list(stasiun.keys())

def hitung_sisi(graph):               # menghitung jumlah edge (sisi) dengan menjumlahkan semua tetangga, lalu dibagi 2 (karena graph tidak berarah)
    return sum(len(v) for v in graph.values()) // 2

# BFS (queue (deque) dengan mengimplementasikan FIFO, traversal : level by level(semua tetangga diperiksa dulu sebelum lanjut))
def bfs(graph, start, end=None, acak=False):
    visited = {start: None}              # simpan parent node
    queue = deque([start])               # queue FIFO
    steps = []                           # menyimpan urutan node yang dikunjungi

    start_time = time.perf_counter()

    while queue:                         # karena O(1)- super cepat
        v = queue.popleft()              # simpan urutan node yang dikunjungi
        steps.append(v)                

        if end is not None and v == end:   # jika node tujuan ditemukan
            break                          # hentikan pencarian 

        neighbors = graph[v][:]            # ambil semua tetangga dari node v
        if acak:
            random.shuffle(neighbors)      # jika mode acak, urutan tetangga diacak
        else:
            neighbors = sorted(neighbors)  # jika tidak, urutan tetangga dibuat tetap (sorted)

        for w in neighbors:              # periksa setiap tetangga w dari node v
            if w not in visited:         # jika tetangga belum pernah dikunjungi 
                visited[w] = v           # simpan parent (asalnya dari v)
                queue.append(w)          # masukkan tetangga ke queue untuk diperiksa nanti

    waktu_ms = (time.perf_counter() - start_time) * 1000   # fungsi python untuk menghitung waktu dengan presisi tinggi

    if end is None:                      # BFS/DFS hanya dijalankan untuk eksperimen traversal (menelusuri semua node) tanpa mencari rute tertentu
        return steps, waktu_ms                  
    
 # rekonstruksi rute dari tujuan ke awal (dg parent yg disimpan)
    path, cur = [], end           # mulai dari node tujuan      
    while cur is not None:        # selama masih ada parent 
        path.append(cur)          # tambahkan node ke path
        cur = visited.get(cur)    # geser ke parent node
    path.reverse()                # balik urutan supaya dari start -> end

    if not path or path[0] != start:      # path kosong, dapat terjadi kalau algoritma tidak menemukan jalur dari start ke end
        path = []                         # jika salah satu kondisi benar, maka path direset menjadi list kosong

    return steps, path, waktu_ms          # fungsi mengembalikkan tiga hal, step, path(start ke end), waktu_ms

# DFS (stack dengan prinsip LIFO, akan menulusuri kedlm satu cbng seblum backtracking)
def dfs(graph, start, end=None, acak=False):      
    visited = {v: False for v in graph}         # semua node ditandai belum dikunjungi
    stack = []                                  # stack untuk traversal (LIFO)
    steps = []                                  # urutan node yang dikunjungi

    stack.append(start)                  # masukkan node awal ke stack
    visited[start] = True                # tandai node awal sudah dikunjungi
    steps.append(start)                  # simpan urutan kunjungan untuk analisis/animasi

    start_time = time.perf_counter()    # menyimpan waktu eksekusi untuk menghitung durasi algoritma

    while stack:                         
        current = stack[-1]              # ambil node paling atas (peek) tanpa menghapus
        found_unvisited = False          # penanda ada/tidak tetangga baru

        if end is not None and current == end:     # jika tujuan ditemukan, jika tujuan(end) maka pencarian berhenti
            break                              
        
        # ambil daftar tetangga dari node saat ini, bisa diacak untuk eksperimen, atau diurutkan agar konsisten
        neighbors = graph[current][:]    
        if acak:
            random.shuffle(neighbors)    # eksperimen urutan tetangga diacak (pola traversal dpt berbeda)
        else:
            neighbors = sorted(neighbors)   # pencarian rute urutan tetap
        
        # kunjungi tetangga
        for w in neighbors:              
            if not visited[w]:           
                stack.append(w)            # masukkan tetangga ke stack 
                visited[w] = True          # tandai sudah dikunjungi
                steps.append(w)            # simpan urutan kunjungan 
                found_unvisited = True     # ada tetangga baru
                break                      # berhenti, DFS hanya ambil satu cabang dulu

        if not found_unvisited:          
            stack.pop()                  # jika tidak ada tetangga baru, mundur/backtrack (dg menghapus node dri stack)

    waktu_ms = (time.perf_counter() - start_time) * 1000    # untuk membandingkan performa BFS & DFS 

    if end is None:                      # jika tidak ada tujuan(end) hanya mengebalikkan urutan kunjungan + waktu
        return steps, waktu_ms           # jika ada tujuan -> mengembalikkan steps, steps lagi sebagai rute 

    return steps, steps, waktu_ms        # mode pencarian rute DFS (DFS tidak menyimpan parent seperti BFS, jdi rutenya = urutan kunjungan)

# analisis hasil eksperimen BFS & DFS
def analyze_results(hasil):                      # list berisi dictionary hasil eksperimen BFS/DFS
    waktu_list = [h['waktu'] for h in hasil]     # membuat list berisi semua waktu eksekusi dari hasil eksperimen
    rute_unik = set(tuple(h['rute']) for h in hasil)    # mengubah rute(list) menjadi tuple, lalu dimasukkan ke dlm set

    return {               # distionary hasil analisis 
        'min': min(waktu_list),
        'median': median(waktu_list),
        'avg': mean(waktu_list),
        'stdev': stdev(waktu_list) if len(waktu_list) > 1 else 0,   
        'max': max(waktu_list),
        'rute_unik': len(rute_unik),
    }

# menjalankan eksperimen BFS & DFS dengan vertex awal tetap dan urutan tetangga diacak
def jalankan_eksperimen():      # mendefinisikan fungsi untuk menjalankan eksperimen perbandingan BFS & DFS
    vertex_awal = 'A'           # menemtukan node awal pecarian, yaitu 'A', semua eksperimen BFS & DFS akan dimulai dari node ini
    jumlah_iterasi = 10         # BFS & DFS dijalankan dg 10x eksperimen, untuk melihat variasi rute dan waktu eksekusi
    
    # 2 list kosong untuk menyimpan hasil eksperimen
    hasil_bfs = []      # hasil berupa, rute (urutan node yg dikunjungi), waktu (lama eksekusi)
    hasil_dfs = []

    print("\nEKSPERIMEN BFS dan DFS")
    print(f"Vertex awal : {vertex_awal} ({stasiun[vertex_awal]})")
    print(f"Jumlah iterasi : {jumlah_iterasi}")

    print("\nHasil Penelusuran BFS:")
    print(f"{'Eks':>3}  {'Rute Penelusuran':<55}  {'Waktu':>8}")
    print("-" * 75)

    for i in range(1, jumlah_iterasi + 1):         # loop dari 1 sampai jumlah iterasinya, jadi  BFS akan dijalankan dg memanggil jumlah iterasinya
        rute, waktu = bfs(graph, vertex_awal, acak=True)    # memanggil fungsi BFS dengan, graph KRL yg sudah didefinisikan, node awal (A), urutan tetangga diacak supaya hasil rute bisa berbeda tiap iterasi
        hasil_bfs.append({'rute': rute, 'waktu': waktu})    # hasil BFS berupa urutan nodde yang dikunjungi, dan lama eksekusi 
        print(f"{i:>3}  {'->'.join(rute):<55}  {waktu:.3f} ms")

    print("\nHasil Penelusuran DFS:")
    print(f"{'Eks':>3}  {'Rute Penelusuran':<55}  {'Waktu':>8}")
    print("-" * 75)

    for i in range(1, jumlah_iterasi + 1):            # eksperimen sebnyk 10x 
        rute, waktu = dfs(graph, vertex_awal, acak=True)
        hasil_dfs.append({'rute': rute, 'waktu': waktu})
        print(f"{i:>3}  {'->'.join(rute):<55}  {waktu:.3f} ms")

    stats_bfs = analyze_results(hasil_bfs)         # menganalisis hasil BFS (min, median, rata-rata, stdev, max, jumlah rute unik)
    stats_dfs = analyze_results(hasil_dfs)         # menganalisis hasil DFS (min, median, rata-rata, stdev, max, jumlah rute unik)
    rasio = stats_dfs['avg'] / stats_bfs['avg']    # menghitung rasio rata-rata waktu DFS dibanding BFS

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
    cmap = {}                                # dictionary kosong untuk menyimpan mapping node -> warna
    for info in jalur_info.values():         # loop, mengambil setiap jalur dari jalur_info
        for n in info['nodes']:              # mengambil setiap node (stasiun) dalam jalur tersebut  
            if n not in cmap:                # jika node belum punya warna, beri warna sesuai jalurnya
                cmap[n] = info['color']      # jadi setiap node akan diwarnai sesuai jalur KRL yg melewatinya
    return [cmap.get(n, "#FFA9D4") for n in nodes]     # mengembalikkan list warna untuk semua node

def default_edge_colors(G):
    cmap = {}                     # Dictionary kosong untuk menyimpan mapping edge → warna.
    for info in jalur_info.values():       # loop, mengambil setiap jalur dari jalur_info
        ns = info['nodes']                 # Ambil daftar node dalam jalur tersebut.
        for i in range(len(ns) - 1):       # Loop pasangan node berurutan dalam jalur
            key = tuple(sorted([ns[i], ns[i+1]]))       # Membuat pasangan node sebagai key (diurutkan supaya konsisten, misalnya (A,B) sama dengan (B,A))
            cmap[key] = info['color']      # Simpan warna edge sesuai jalur
    return [cmap.get(tuple(sorted([u, v])), "#FFA9D4") for u, v in G.edges()]  # Mengembalikan list warna untuk semua edge di graph G. Jika edge tidak ada di cmap, default warnanya #FFA9D4

#gambar frame animasi
def draw_frame(ax, G, node_colors, edge_colors,            # Urutan penggambaran 
               start, end, current=None,
               path_edges=None, title=''):
    ax.clear()                                  # bersihkan frame sebelumnya agar tidak menumpuk
    ax.set_facecolor("#f6def3")              # warna latar belakang
    ax.axis('off')                             # hilangkan sumbu koordinat           
    ax.set_xlim(-0.6, 7.0)                     # batas horizontal
    ax.set_ylim(2.2, 11.2)                     # batas vertikal

    # Edge biasa (pink), 
    nx.draw_networkx_edges(          # menggambar edge biasa dengan warna default (pink pastel)
        G, pos, ax=ax,
        edge_color=edge_colors, width=3, alpha=0.75
    )

    # Edge rute hasil pencarian ditampilkan di atas edge biasa (ditimpa jauh lebih tebal)
    if path_edges:                     # Jika ada rute hasil pencarian, edge tersebut digambar ulang di atas edge biasa dengan warna merah tebal (#FF0381) agar menonjol.
        nx.draw_networkx_edges(
            G, pos, ax=ax,
            edgelist=path_edges,
            edge_color='#FF0381', width=5.5, alpha=1.0
        )

    # Node: ring hitam -> warna jalur
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color='black', node_size=850)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=720, alpha=0.95)

    # Ring tebal untuk asal & tujuan diberi ring tebal berwarna merah muda tua transparant
    for node, ring_color in [(start, "#FF0381"), (end, "#FF0381")]:
        nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=[node],
                               node_color=ring_color, node_size=1050, alpha=0.35)

    # Highlight node yang sedang diperiksa diberi highlight warna pink muda
    if current and current not in (start, end):
        nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=[current],
                               node_color="#F6BBD8", node_size=1000, alpha=0.4)

    # Label kode huruf node didalam lingkaran
    nx.draw_networkx_labels(
        G, pos, ax=ax,
        labels={n: n for n in nodes},
        font_color='white', font_size=11, font_weight='bold'
    )

    # menampilkan nama stasiun di bawah node dengan font kecil miring
    for node, (x, y) in pos.items():
        ax.text(x, y - 0.38, stasiun[node],
                fontsize=7, color="#050003",
                ha='center', va='top', style='italic',
                fontfamily='monospace')

    # Legend (keterangan)
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

    # menampilkan judul frame 
    ax.set_title(title, color='#FF0381', fontsize=10,
                 fontfamily='monospace', pad=10)

# Pencarian rute
def jalankan_animasi(start, end, algo='BFS', interval_ms=400):
    G = nx.Graph()                       # Membuat objek graph G menggunakan NetworkX.
    for u, neighbors in graph.items():   # Loop semua node (u) dan tetangganya (neighbors) dari adjacency list graph.
        for v in neighbors:            
            if not G.has_edge(u, v):    # memastikan edge tidak digambar dua kali (karena graph tidak berarah).
                G.add_edge(u, v)       # menambahkan edge ke graph

    base_nc = default_node_colors()    # list warna default untuk node sesuai jalur KRL (dari fungsi default_node_colors()).
    base_ec = default_edge_colors(G)   #  list warna default untuk edge sesuai jalur KRL (dari fungsi default_edge_colors()).

    # Jalankan algoritma pencarian sesuai pilihan
    if algo == 'BFS':           # jika algo == 'BFS' -> jalankan BFS
        steps, path, waktu = bfs(graph, start, end)      # hasil steps(urutan node yg dikunjungi), path(rute dari start->end), waktu(lama eksekusi dlm milidetik)
    else:                       # jika algo == 'DFS' -> jalankan DFS
        steps, path, waktu = dfs(graph, start, end)     # hasil steps(urutan node yg dikunjungi), path(rute dari start->end), waktu(lama eksekusi dlm milidetik)

    total_frames = len(steps) + 1           # Jumlah frame animasi = banyaknya langkah (steps) + 1 frame terakhir (untuk menampilkan rute hasil pencarian).

    fig, ax = plt.subplots(figsize=(13, 9))    # Membuat canvas figure dengan ukuran 13x9.
    fig.patch.set_facecolor("#f8e2f1")       # Background figure diberi warna pastel 
    fig.suptitle(
        f'Jaringan KRL Jabodetabek  —  {algo}: '
        f'{stasiun[start]} -> {stasiun[end]}',
        color='#FF0381', fontsize=13, fontweight='bold', y=0.98     # Judul berwarna merah (#FF0381), font tebal, posisi agak ke atas (y=0.98)
    )

    visited_nodes = []          # List kosong untuk menyimpan node yang sudah dikunjungi selama animasi.
    
    # akan bertahap di fungsi animate() untuk menandai node visited
    def animate(frame):             # dipanggil setiap kali frame animasi digambar.
        nonlocal visited_nodes      # agar variabel visited_nodes di luar fungsi bisa diubah di dalam fungsi.

        if frame < len(steps):
            current = steps[frame]             # node yang sedang diperiksa
            visited_nodes = steps[:frame + 1]  # semua node yang sudah dikunjungi sampai frame ini

            # Warna tiap node sesuai statusnya
            nc = []
            for n in nodes:
                if n == start:
                    nc.append("#0C2A52")       # node asal → biru tua
                elif n == end:
                    nc.append('#0C2A52')      # node tujuan → biru tua
                elif n == current: 
                    nc.append('#0C2A52')      # node sedang diperiksa → biru tua
                elif n in visited_nodes[:-1]:
                    nc.append('#0C2A52')      # node sudah dikunjungi → biru tua
                else:
                    nc.append(base_nc[nodes.index(n)])     # node lain → warna default jalur

            # Memanggil draw_frame() untuk menggambar frame dengan judul: Langkah ke-X | Memeriksa: node (nama stasiun).
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
            if path:            # Buat list path_edges berisi edge dari rute hasil pencarian.
                for i in range(len(path) - 1):
                    path_edges.append((path[i], path[i+1]))

            nc = []
            for n in nodes:
                if n in path:
                    nc.append('#FFA9D4')      # node dalam rute → pink pastel
                elif n in visited_nodes:
                    nc.append('#FFA9D4')      # node visited → pink pastel
                else:
                    nc.append(base_nc[nodes.index(n)])

            if path:                                      # Jika rute ditemukan:
                rute_str = ' -> '.join(                   # Buat string rute lengkap dengan nama stasiun.
                    f"{n}({stasiun[n]})" for n in path    # Judul menampilkan jenis rute, panjang edge, waktu eksekusi.
                )

                jenis_rute = "Rute terbaik" if algo == "BFS" else "Rute hasil DFS"

                title = (
                    f"[{algo}] {jenis_rute} ditemukan! "
                    f"Panjang: {len(path)-1} edge | Waktu: {waktu:.4f} ms\n"
                    f"{rute_str}"
                )

            # Jika tidak ada rute → tampilkan pesan gagal.
            else:
                title = f"[{algo}] Tidak ada rute dari {start} ke {end}."
            
            # Menggambar frame terakhir dengan rute hasil pencarian.
            draw_frame(
                ax, G, nc, base_ec,
                start, end,
                path_edges=path_edges,
                title=title
            )
    
    # Membuat animasi dengan FuncAnimation.
    anim = animation.FuncAnimation(       
        fig, animate,
        frames=total_frames,       # jumlah frame sesuai langkah + hasil akhir
        interval=interval_ms,      # kecepatan animasi (ms per frame)
        repeat=False               # animasi tidak diulang 
    )

    plt.tight_layout(rect=[0, 0, 1, 0.96])       # menyesuaikan layout agar tidak tumpang tindih.
    plt.show()                                   # menampilkan animasi ke layar.

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

    tampilkan_info_graph()       # Memanggil fungsi tampilkan_info_graph() untuk menampilkan: Jumlah simpul (node) dan sisi (edge), Kompleksitas algoritma BFS/DFS, Adjacency list graph KRL.

    while True:                 # Membuat loop tak terbatas (while True) agar menu terus ditampilkan sampai pengguna keluar.
        print("\nMENU PROGRAM")                # menampilkan menu utama :
        print("1. Eksperimen BFS dan DFS")     # membandingkan performa kedua algoritma
        print("2. Pencarian rute")             # mencari jalur dari stasiun asal ke tujuan dengan animasi.

        pilihan = input("Pilih menu: ").strip()   # meminta pengguna memilih menu

        if pilihan == '1':
            jalankan_eksperimen()
        elif pilihan == '2':
            pencarian_rute()
        else:                             # Jika input selain '1' atau '2' → tampilkan pesan "Pilihan tidak valid."
            print("Pilihan tidak valid.")

if __name__ == '__main__':
    main()