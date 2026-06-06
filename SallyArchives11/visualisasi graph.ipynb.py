import matplotlib.pyplot as plt

# Data
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

# Membuat plot
plt.plot(x, y, marker='o', linestyle='-', color='b')

# Menambahkan judul dan label
plt.title("Contoh Line Plot")
plt.xlabel("Sumbu X")
plt.ylabel("Sumbu Y")

# Menampilkan
plt.show()
