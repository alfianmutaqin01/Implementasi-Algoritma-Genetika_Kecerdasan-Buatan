# Seed untuk generator bilangan acak (digunakan sebagai pengganti random library)
SEED = 42

# Parameter GA
POP_SIZE = 100        # Ukuran populasi
GENE_LENGTH = 20      # Panjang gen untuk x1 dan x2
PC = 0.7              # Probabilitas crossover
PM = 0.01             # Probabilitas mutasi
MAX_GENERATIONS = 100  # Kriteria penghentian
ELITISM = 1           # Jumlah elitism

# Domain variabel
X1_MIN, X1_MAX = -10, 10
X2_MIN, X2_MAX = -10, 10

# Generator bilangan acak sederhana (Linear Congruential Generator)
def random_number():
    global SEED
    SEED = (1664525 * SEED + 1013904223) & 0xFFFFFFFF
    return SEED / 4294967296.0  # Normalisasi ke [0, 1)

# Fungsi objektif (tanpa math library)
def objective_function(x1, x2):
    # Implementasi sin, cos, tan, exp, dan sqrt secara manual
    def sin(x):
        x = x % (2 * 3.141592653589793)
        term = x
        sin_x = x
        for n in range(1, 10):
            term *= -x * x / ((2 * n) * (2 * n + 1))
            sin_x += term
        return sin_x

    def cos(x):
        x = x % (2 * 3.141592653589793)
        term = 1
        cos_x = 1
        for n in range(1, 10):
            term *= -x * x / ((2 * n - 1) * (2 * n))
            cos_x += term
        return cos_x

    def tan(x):
        return sin(x) / cos(x) if cos(x) != 0 else 1e10

    def exp(x):
        term = 1
        exp_x = 1
        for n in range(1, 20):
            term *= x / n
            exp_x += term
        return exp_x

    def sqrt(x):
        if x == 0:
            return 0
        guess = x / 2
        for _ in range(20):
            guess = (guess + x / guess) / 2
        return guess

    term1 = sin(x1) * cos(x2) * tan(x1 + x2)
    term2 = (3/4) * exp(1 - sqrt(x1 * x1))
    return -(term1 + term2)  # Minimalkan -f(x1, x2)

# 1. Inisialisasi populasi (tanpa random library)
def initialize_population():
    population = []
    for _ in range(POP_SIZE):
        x1_gene = [1 if random_number() > 0.5 else 0 for _ in range(GENE_LENGTH)]
        x2_gene = [1 if random_number() > 0.5 else 0 for _ in range(GENE_LENGTH)]
        population.append(x1_gene + x2_gene)
    return population

# 2. Dekode kromosom ke nilai x1 dan x2
def decode_chromosome(chromosome):
    def binary_to_float(gene, min_val, max_val):
        decimal = 0
        for i in range(len(gene)):
            decimal += gene[i] * (1 << (len(gene) - 1 - i))
        return min_val + (decimal / ((1 << len(gene)) - 1)) * (max_val - min_val)

    x1 = binary_to_float(chromosome[:GENE_LENGTH], X1_MIN, X1_MAX)
    x2 = binary_to_float(chromosome[GENE_LENGTH:], X2_MIN, X2_MAX)
    return x1, x2

# 3. Perhitungan fitness
def calculate_fitness(chromosome):
    x1, x2 = decode_chromosome(chromosome)
    return -objective_function(x1, x2)

# 4. Seleksi orangtua (tournament selection)
def select_parents(population, fitness_scores):
    parents = []
    for _ in range(2):
        tournament = []
        for _ in range(3):  # Ukuran turnamen = 3
            idx = int(random_number() * len(population))
            tournament.append((population[idx], fitness_scores[idx]))
        winner = max(tournament, key=lambda x: x[1])[0]
        parents.append(winner)
    return parents

# 5. Crossover (single-point)
def crossover(parent1, parent2):
    if random_number() < PC:
        point = int(random_number() * len(parent1))
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2
    return parent1, parent2

# 6. Mutasi (bit flip)
def mutate(chromosome):
    for i in range(len(chromosome)):
        if random_number() < PM:
            chromosome[i] ^= 1
    return chromosome

# 7. Pergantian generasi (elitism)
def next_generation(population, fitness_scores):
    # Elitism: Pertahankan individu terbaik
    elite_idx = max(range(len(fitness_scores)), key=lambda i: fitness_scores[i])
    new_population = [population[elite_idx]]

    # Isi populasi baru dengan anak hasil crossover dan mutasi
    while len(new_population) < POP_SIZE:
        parents = select_parents(population, fitness_scores)
        child1, child2 = crossover(parents[0], parents[1])
        new_population.extend([mutate(child1), mutate(child2)])
    return new_population[:POP_SIZE]

# Algoritma GA Utama
def genetic_algorithm():
    population = initialize_population()
    for generation in range(MAX_GENERATIONS):
        fitness_scores = [calculate_fitness(chrom) for chrom in population]
        best_idx = max(range(len(fitness_scores)), key=lambda i: fitness_scores[i])
        best_x1, best_x2 = decode_chromosome(population[best_idx])
        best_fitness = fitness_scores[best_idx]

        print(f"Generasi {generation + 1}: x1 = {best_x1:.4f}, x2 = {best_x2:.4f}, Fitness = {best_fitness:.4f}")

        population = next_generation(population, fitness_scores)

    # Output hasil terbaik
    best_chromosome = max(population, key=lambda chrom: calculate_fitness(chrom))
    best_x1, best_x2 = decode_chromosome(best_chromosome)
    best_fitness = calculate_fitness(best_chromosome)

    print("\n=== Hasil Terbaik ===")
    print(f"Kromosom Terbaik: {best_chromosome}")
    print(f"Nilai x1: {best_x1:.6f}")
    print(f"Nilai x2: {best_x2:.6f}")
    print(f"Fitness: {best_fitness:.6f}")

# Jalankan program
if __name__ == "__main__":
    genetic_algorithm()