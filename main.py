import heapq
import math
from tabulate import tabulate
import networkx as nx
import matplotlib.pyplot as plt

# Функція для побудови коду Хаффмана
def build_huffman_tree(freq_dict):
    heap = [[weight, [char, ""]] for char, weight in freq_dict.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    huffman_codes = sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))
    return huffman_codes

def print_t(name_of_table,result):
    print(f"Кодова таблиця {name_of_table} :")
    table = [["Символ", "Частота", "Кодове слово", "Довжина кодового слова"]]
    table.extend([[symbol, freq_dict[symbol], code, len(code)] for symbol, code in result])
    print(tabulate(table, headers="firstrow"))

def check_kraft(name,check):
    kraft_sum = sum(2 - len(code) for code in check.values())
    print(f"\nПеревірка нерівності Крафта для коду {name}:", kraft_sum <= 1)

def expected_len(name, res, freq):
    expected_length = sum(freq[symbol] * len(code) for symbol, code in res.items()) / sum(freq.values())
    print(f"\nОчікувана довжина коду {name}:", expected_length)

def print_t2(name_of_table, result, freq_dict):
    print(f"Кодова таблиця {name_of_table} :")
    table = [["Символ", "Частота", "Ймовірність", "Кодове слово", "Довжина кодового слова"]]
    total_symbols = sum(freq_dict.values())
    table.extend([[symbol, freq_dict[symbol], freq_dict[symbol] / total_symbols, code, len(code)] for symbol, code in result])
    print(tabulate(table, headers="firstrow"))

# ... (решта коду залишається незмінним) ...

# Виведення кодової таблиці Хаффмана з ймовірністю зустрічання символу

def create_huffman_graph(result):
    G = nx.DiGraph()
    node_labels = {}  # Створення словника для збереження міток вузлів

    for parent, (left, right) in enumerate(result):
        node_labels[parent] = str(parent)
        node_labels[left] = str(left)
        node_labels[right] = str(right)
        G.add_node(parent)
        G.add_node(left)
        G.add_node(right)
        G.add_edge(parent, left)
        G.add_edge(parent, right)

    pos = nx.spring_layout(G, seed=42)  # Використання spring_layout для отримання розташування вузлів
    plt.figure(figsize=(12, 6))
    nx.draw(G, pos, labels=node_labels, with_labels=True, node_size=2000, node_color="skyblue", font_size=10, font_weight="bold", arrows=True, connectionstyle='arc3,rad=0.1')
    plt.title("Схематичне дерево для коду Хаффмана")
    plt.axis('off')
    plt.show()

# Ваше П.І.П.
your_name = "кречківськаелеонораандріївна"

# Рахуємо частоту зустрічання кожної букви у вашому П.І.П.
freq_dict = {}
for char in your_name:
    if char in freq_dict:
        freq_dict[char] += 1
    else:
        freq_dict[char] = 1

# Бінарні коди Хаффмана і Шенона для  П.І.П.
huffman_result = build_huffman_tree(freq_dict)

# Виведення кодових таблиць delete
print_t("Хаффмана",huffman_result)

# Ваші кодові таблиці Хаффмана і Шенона
huffman_codes = dict(huffman_result)

# Перевірка нерівності Крафта для коду Хаффмана
check_kraft('Хаффмана',huffman_codes)
# Перевірка нерівності Крафта для коду Шенона

# Очікувана довжина коду Хаффмана і Шенона
expected_len("Хаффмана",huffman_codes,freq_dict)

# Ентропія вихідної послідовності
entropy = -sum((freq_dict[symbol] / len(your_name)) * math.log2(freq_dict[symbol] / len(your_name)) for symbol in freq_dict)
print_t2("Хаффмана", huffman_result, freq_dict)

# Виведення результатів
print("Ентропія вихідної послідовності:", entropy)

