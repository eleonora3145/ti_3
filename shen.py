
import math
from tabulate import tabulate
import matplotlib.pyplot as plt
your_name = "кречківськаелеонораандріївна"

# Рахуємо частоту зустрічання кожної букви у вашому П.І.П.
freq_table = {}
for char in your_name:
    if char in freq_table:
        freq_table[char] += 1
    else:
        freq_table[char] = 1
# freq_table = {
#     '1': 0.12, '2': 0.11, '3': 0.08, '4': 0.06, '5': 0.16,
#     '6': 0.11, '7': 0.06, '8': 0.11, '9': 0.1, '10': 0.09
# }
# freq_table = {'1': 0.25, '2': 0.5, '3': 0.125, '4': 0.125}


def create_shannon_fano_graph(res):
    symbols = list(res.keys())
    probabilities = [freq_table[symbol] for symbol in symbols]

    # Графік кумулятивної функції розподілу для коду Шенона
    plt.figure(figsize=(8, 6))
    plt.plot(symbols, probabilities, marker='o', color='b', label='F(x)')
    plt.xlabel('Символ')
    plt.ylabel('Ймовірність')
    plt.title('Функція щільності ймовірності для коду Шенона')
    plt.xticks(range(len(symbols)), symbols)
    plt.legend()
    plt.grid(True)
    plt.show()

    # Графік відносної накопиченої ймовірності для коду Шенона
    cumulative_probabilities = [sum(probabilities[:i + 1]) for i in range(len(probabilities))]
    relative_cumulative_probabilities = [p / cumulative_probabilities[-1] for p in cumulative_probabilities]
    plt.figure(figsize=(8, 6))
    plt.plot(symbols, relative_cumulative_probabilities, marker='o', color='r', label='F(x)')
    plt.xlabel('Символ')
    plt.ylabel('Ймовірність')
    plt.title('Кумулятивна функція розподілу для коду Шенона')
    plt.xticks(range(len(symbols)), symbols)
    plt.legend()
    plt.grid(True)
    plt.show()

def check_kraft(name, check):
    kraft_sum = sum(2 ** -len(code) for code in check.values())
    print(f"\nПеревірка нерівності Крафта для коду {name}:", kraft_sum <= 1)

def expected_len(name, res,freq):
    expected_length = sum(freq[symbol] * len(code) for symbol, code in res.items())
    print(f"\nОчікувана довжина коду {name}:", expected_length)
# Функція для побудови коду Шенона
class ShannonFanoNode:
    def __init__(self, symbol, frequency):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None
        self.code = ""


def build_shannon_fano_tree(freq_table):
    nodes = [ShannonFanoNode(char, freq) for char, freq in freq_table.items()]
    sorted_nodes = sorted(nodes, key=lambda node: node.frequency, reverse=True)

    def recursive_shannon_fano(node_list):
        if len(node_list) < 2:
            return

        mid = len(node_list) // 2
        for node in node_list[:mid]:
            node.code += '0'
        for node in node_list[mid:]:
            node.code += '1'

        recursive_shannon_fano(node_list[:mid])
        recursive_shannon_fano(node_list[mid:])

    recursive_shannon_fano(sorted_nodes)

    shannon_fano_codes = {node.symbol: node.code for node in sorted_nodes}
    return list(shannon_fano_codes.items())
def print_t(name_of_table, freq, shannon_fano_codes):
    print(f"Кодова таблиця {name_of_table} :")
    table = [["Символ", "F(x)", "¯F(x)", "¯F(x)(Бінарне)", "Кодове слово (Шенона)", "Довжина кодового слова"]]
    cumulative_prob = 0
    previous_prob = 0
    for symbol, freq in sorted(freq.items()):
        cumulative_prob += freq
        prob = (previous_prob + cumulative_prob) / 2
        shannon_fano_code = shannon_fano_codes[symbol]
        binary_code = shannon_fano_code

        table.append([symbol, cumulative_prob, prob, f"0.{binary_code}", shannon_fano_code, len(shannon_fano_code)])
        previous_prob = cumulative_prob
    print(tabulate(table, headers="firstrow"))

# Calculate Shannon-Fano codes
shannon_fano_codes = dict(build_shannon_fano_tree(freq_table))
create_shannon_fano_graph(shannon_fano_codes)
# Print the table with Shannon-Fano codes
print_t('Шенона', freq_table, shannon_fano_codes)
expected_len('Шенона',shannon_fano_codes,freq_table)
check_kraft('Шенона',shannon_fano_codes)
# Ентропія розподілу
entropy = -sum(prob * math.log2(prob) for prob in freq_table.values())
print(entropy)
