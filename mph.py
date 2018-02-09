# Perfect Minimal Hashing
# By Vladyslav Ovchynnykov
import sys


GLOBAL_DICTIONARY = "/usr/share/dict/words"  # Дефолтний словник слів на UNIX системах
USER_WORDS = sys.argv[1:]
if not len(USER_WORDS):
    USER_WORDS = ['hello', 'goodbye', 'dog', 'cat']


def hash(num, str):
    '''
    Обчислює певну хеш-функцію для заданого рядка. Кожне значення для
    цілого числа num призводить до різного хеш-значення
    '''
    if num == 0:
        num = 0x01000193

    # Використовуємо FNV алгоритм з http://isthe.com/chongo/tech/comp/fnv/
    for c in str:
        num = ((num * 0x01000193) ^ ord(c)) & 0xffffffff

    return num


def create_minimal_perfect_hash(input_dict):
    '''
    Обчислює мінімальну досконалу хеш-таблицю з використанням словника. Функція
    повертає кортеж (G, V). G і V - масиви. G містить проміжний продукт -
    таблиця значень, необхідну для обчислення індексу значення в V. V містить
    значення словника
    '''
    size = len(input_dict)

    # Крок 1: кладемо всі ключі в 'кошик'
    buckets = [[] for i in range(size)]
    G = [0] * size
    values = [None] * size

    for key in input_dict.keys():
        buckets[hash(0, key) % size].append(key)

    # Крок 2: сортуйємо кошики та обробляєсо ті, що мають найбільше елементів
    buckets.sort(key=len, reverse=True)
    for b in range(size):
        bucket = buckets[b]
        if len(bucket) <= 1:
            break

        d = 1
        item = 0
        slots = []

        # Повторно пробуємо різні значення d, доки ми не знайдемо хеш-функцю
        # якия поміщає всі предмети в кошик в вільні слоти
        while item < len(bucket):
            slot = hash(d, bucket[item]) % size
            if values[slot] is not None or slot in slots:
                d += 1
                item = 0
                slots = []
            else:
                slots.append(slot)
                item += 1

        G[hash(0, bucket[0]) % size] = d
        for i in range(len(bucket)):
            values[slots[i]] = input_dict[bucket[i]]

        if not b % 5000:
            print("bucket %d    r" % (b))

    # Лише кошикі з одним елементом залишаються. Обрабляємо їх швидше, безпосередньо
    # розміщуючи їх у вільному місці. Використовуємо негативне значення num для позначення цього
    freelist = []
    for i in range(size):
        if values[i] is None:
            freelist.append(i)

    for b in range(b, size):
        bucket = buckets[b]
        if len(bucket) == 0:
            break
        slot = freelist.pop()
        # Ми віднімаємо 1, щоб забезпечити його негативне значення, навіть якщо нульове місце
        # було використано
        G[hash(0, bucket[0]) % size] = -slot - 1
        values[slot] = input_dict[bucket[0]]
        if (b % 5000) == 0:
            print("bucket %d    r" % (b))

    return (G, values)


def perfect_hash_lookup(G, V, key):
    '''Знаходимо значення в хеш-таблиці, визначеному G і V'''
    d = G[hash(0, key) % len(G)]
    if d < 0:
        return V[-d - 1]
    return V[hash(d, key) % len(V)]


print("Reading words")
input_dict = {}
line = 1
for key in open(GLOBAL_DICTIONARY, "rt").readlines():
    input_dict[key.strip()] = line
    line += 1

print("Creating perfect hash")
(G, V) = create_minimal_perfect_hash(input_dict)

for word in USER_WORDS:
    line = perfect_hash_lookup(G, V, word)
    print("Word %s occurs on line %d" % (word, line))
