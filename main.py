import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import matplotlib

matplotlib.use('Agg')

filename = "output_5_allocate_where_popular"

def load_data():
    with open(filename, "r") as file:
        allocation_cost = int(file.readline().strip())
        allocation_matrix = [list(map(int, file.readline().split())) for _ in range(5)]
        allocation_matrix = np.array(allocation_matrix)

        transfer_data = {}
        for i in range(3):
            file.readline()
            for j in range(5):
                transfers = list(map(int, file.readline().split()))
                for k, transfer in enumerate(transfers):
                    if transfer > 0:
                        transfer_data[(j + 1, k + 1, i + 1)] = transfer

        return allocation_cost, allocation_matrix, transfer_data

allocation_cost, allocation_matrix, transfer_data = load_data()


fig, ax = plt.subplots(figsize=(10, 8))
cax = ax.matshow(allocation_matrix, cmap='Blues')
ax.set_xticks(np.arange(len(allocation_matrix[0])))
ax.set_yticks(np.arange(len(allocation_matrix)))
ax.set_xticklabels([f"Film {i+1}" for i in range(allocation_matrix.shape[1])])
ax.set_yticklabels([f"Serwer {i+1}" for i in range(allocation_matrix.shape[0])])
fig.colorbar(cax)
plt.title("Alokacja filmów na serwerach")
plt.savefig(filename + "allocation_matrix.png")
plt.close()

G = nx.DiGraph()
for v in range(1, 6):
    G.add_node(v, label=f"Serwer {v}")

for (v1, v2, m), data in transfer_data.items():
    if v1 != v2:  # Tylko, gdy film jest przesyłany z serwera 1 na serwer 2
        G.add_edge(v1, v2, weight=data, label=f"Film {m}: {data} MB")

pos = nx.spring_layout(G)
labels = nx.get_edge_attributes(G, 'label')

plt.figure(figsize=(8, 6))
nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=12, font_weight='bold')
nx.draw_networkx_edge_labels(G, pos, edge_labels={key: f"Film {key[2]}: {value} MB" for key, value in transfer_data.items() if key[0] != key[1]})
plt.title("Przesyłanie danych między serwerami")
plt.savefig(filename+"data_transfer_graph.png")
plt.close()


