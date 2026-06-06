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
# Total sisi: 20 (sama dengan artikel acuan)
graph = {
    'A': ['B', 'D'],          # Manggarai -> Sudirman, Cikini
    'B': ['A', 'E'],          # Sudirman -> Manggarai, Tebet
    'C': ['D', 'H'],          # Gondangdia -> Cikini, Bogor
    'D': ['A', 'C', 'I'],     # Cikini -> Manggarai, Gondangdia, Bekasi
    'E': ['B', 'J', 'L'],     # Tebet -> Sudirman, Klender, Tanah Abang
    'F': ['G', 'N'],          # Pasar Minggu -> Depok, Kebayoran
    'G': ['F', 'H', 'N'],     # Depok -> Pasar Minggu, Bogor, Kebayoran
    'H': ['C', 'G', 'I', 'N'],# Bogor -> Gondangdia, Depok, Bekasi, Kebayoran
    'I': ['D', 'H'],          # Bekasi -> Cikini, Bogor
    'J': ['E', 'K', 'L'],     # Klender -> Tebet, Jatinegara, Tanah Abang
    'K': ['J', 'M'],          # Jatinegara -> Klender, Palmerah
    'L': ['E', 'J', 'O'],     # Tanah Abang -> Tebet, Klender, Serpong
    'M': ['K', 'L'],          # Palmerah -> Jatinegara, Tanah Abang
    'N': ['F', 'G', 'H', 'O'],# Kebayoran -> Pasar Minggu, Depok, Bogor, Serpong
    'O': ['L', 'N'],          # Serpong -> Tanah Abang, Kebayoran
}

# Layout posisi — diatur manual agar menyerupai peta geografis KRL
pos = {
    'F': (-4, 2),   # Pasar Minggu -> bagian kiri atas
    'G': (-4, 1),   # Depok -> di bawah Pasar Minggu
    'N': (-5, 0),   # Kebayoran -> sisi kiri graf, terhubung ke F, G, H, dan O
    'H': (-3, 0),   # Bogor -> penghubung area kiri menuju tengah
    'I': (-2, -1),  # Bekasi -> berada di bawah H, menuju simpul D
    'C': (-2, 2),   # Gondangdia -> bagian atas tengah
    'D': (-1, -2),  # Cikini -> pusat koneksi antara A, C, dan I
    'A': (1, 0),    # Manggarai -> hub utama di tengah kanan
    'B': (2, -1),   # Sudirman -> cabang kanan dari A
    'E': (1, -3),   # Tebet -> penghubung area bawah
    'L': (-1, -4),  # Tanah Abang -> area kiri bawah tengah
    'J': (2, -4),   # Klender -> sisi kanan bawah
    'K': (3, -6),   # Jatinegara -> bagian kanan paling bawah
    'M': (1, -7),   # Palmerah -> titik paling bawah
    'O': (-4, -4),  # Serpong -> sisi kiri bawah
}