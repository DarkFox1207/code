# Реализация Speck128/128 с поддержкой длинных сообщений (ECB mode)
# ===============================================================
# Блок = 128 бит (2 слова по 64 бита)
# Ключ = 128 бит (2 слова по 64 бита)
# Раундов = 32

BLOCK_SIZE = 128
WORD_SIZE = 64
ROUNDS = 32
BYTES_PER_BLOCK = BLOCK_SIZE // 8  # 16 байт

# --------------------------
# Вспомогательные функции
# --------------------------

def rol(x, r, bits=WORD_SIZE):
    """Циклический сдвиг влево"""
    return ((x << r) & ((1 << bits) - 1)) | (x >> (bits - r))

def ror(x, r, bits=WORD_SIZE):
    """Циклический сдвиг вправо"""
    return (x >> r) | ((x << (bits - r)) & ((1 << bits) - 1))

def add_mod(x, y, bits=WORD_SIZE):
    """Сложение по модулю 2^WORD_SIZE"""
    return (x + y) % (1 << bits)

# --------------------------
# Ключевое расписание
# --------------------------
def expand_key(master_key):
    """
    master_key: список [k0, k1] из двух 64-битных чисел
    возвращает список раундовых ключей
    """
    l = [master_key[1]]
    k = [master_key[0]]
    for i in range(ROUNDS - 1):
        l_new = (ror(l[i], 8) + k[i]) % (1 << WORD_SIZE)
        l_new ^= i
        k_new = rol(k[i], 3) ^ l_new
        l.append(l_new)
        k.append(k_new)
    return k

# --------------------------
# Один раунд
# --------------------------
def round_encrypt(x, y, k):
    x = ror(x, 8)
    x = add_mod(x, y)
    x ^= k
    y = rol(y, 3)
    y ^= x
    return x, y

def round_decrypt(x, y, k):
    y ^= x
    y = ror(y, 3)
    x ^= k
    x = (x - y) % (1 << WORD_SIZE)
    x = rol(x, 8)
    return x, y

# --------------------------
# Шифрование и расшифрование блока
# --------------------------
def encrypt_block(plaintext, round_keys):
    x, y = plaintext
    for k in round_keys:
        x, y = round_encrypt(x, y, k)
    return x, y

def decrypt_block(ciphertext, round_keys):
    x, y = ciphertext
    for k in reversed(round_keys):
        x, y = round_decrypt(x, y, k)
    return x, y

# --------------------------
# Работа с текстом
# --------------------------
def text_to_blocks(text):
    """Преобразуем строку в список блоков (по 16 байт = 128 бит)"""
    data = text.encode("utf-8")
    # добиваем нулями до кратности 16
    if len(data) % BYTES_PER_BLOCK != 0:
        data = data.ljust(len(data) + (BYTES_PER_BLOCK - len(data) % BYTES_PER_BLOCK), b"\0")

    blocks = []
    for i in range(0, len(data), BYTES_PER_BLOCK):
        block = data[i:i+BYTES_PER_BLOCK]
        x = int.from_bytes(block[:8], "big")
        y = int.from_bytes(block[8:], "big")
        blocks.append((x, y))
    return blocks

def blocks_to_text(blocks):
    """Преобразуем список блоков обратно в строку"""
    data = b""
    for (x, y) in blocks:
        data += x.to_bytes(8, "big") + y.to_bytes(8, "big")
    return data.rstrip(b"\0").decode("utf-8", errors="ignore")

# --------------------------
# Шифрование/расшифровка сообщений
# --------------------------
def encrypt_message(text, round_keys):
    plaintext_blocks = text_to_blocks(text)
    ciphertext_blocks = [encrypt_block(b, round_keys) for b in plaintext_blocks]
    return ciphertext_blocks

def decrypt_message(ciphertext_blocks, round_keys):
    plaintext_blocks = [decrypt_block(b, round_keys) for b in ciphertext_blocks]
    return blocks_to_text(plaintext_blocks)

# --------------------------
# Демонстрация
# --------------------------
if __name__ == "__main__":
    # Ввод текста
    text = input("Введите текст для шифрования: ")

    # Мастер-ключ (128 бит = 2 слова по 64 бита)
    master_key = [0x0f0e0d0c0b0a0908, 0x0706050403020100]

    # Генерация раундовых ключей
    round_keys = expand_key(master_key)

    # Шифрование
    ciphertext_blocks = encrypt_message(text, round_keys)

    # Расшифровка
    decrypted_text = decrypt_message(ciphertext_blocks, round_keys)

    # Вывод
    print("\n=== Результаты ===")
    print("Открытый текст :", text)
    print("Шифртекст (блоки):")
    for c in ciphertext_blocks:
        print([hex(x) for x in c])
    print("Расшифровка     :", decrypted_text)
