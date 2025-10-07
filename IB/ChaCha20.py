"""
ChaCha20 (pure Python) — демонстрация шифрования/дешифрования произвольного текста.

Особенности:
- Реализация блока ChaCha20 (20 раундов) согласно RFC-подходу (quarter round).
- Генератор 64-байтных блоков кейстрима.
- Шифрование/дешифрование произвольных байтов (stream cipher).
- Печать ключа (32 байта) и nonce (12 байт) в hex, чтобы можно было повторно расшифровать.
- Подробные комментарии и небольшие оптимизации (локальные переменные, bytearray XOR).
- В целях демонстрации: используется initial_counter = 1 (RFC 7539 часто рекомендует 1).
"""

from typing import Generator
import struct
import os

# -------------------------
# НИЗКОУРОВНЕВЫЕ операции
# -------------------------

def _rotl32(v: int, c: int) -> int:
    """Циклический сдвиг влево для 32-битного слова."""
    return ((v << c) & 0xFFFFFFFF) | (v >> (32 - c))

def _quarter_round(state: list, a: int, b: int, c: int, d: int) -> None:
    """
    Quarter round: модифицирует state in-place.
    Операции: add (mod 2^32), XOR, rotate left.
    """
    # Используем локальные ссылки для скорости
    sa = state
    sa[a] = (sa[a] + sa[b]) & 0xFFFFFFFF
    sa[d] ^= sa[a]; sa[d] = _rotl32(sa[d], 16)

    sa[c] = (sa[c] + sa[d]) & 0xFFFFFFFF
    sa[b] ^= sa[c]; sa[b] = _rotl32(sa[b], 12)

    sa[a] = (sa[a] + sa[b]) & 0xFFFFFFFF
    sa[d] ^= sa[a]; sa[d] = _rotl32(sa[d], 8)

    sa[c] = (sa[c] + sa[d]) & 0xFFFFFFFF
    sa[b] ^= sa[c]; sa[b] = _rotl32(sa[b], 7)

def _chacha20_block(key: bytes, counter: int, nonce: bytes) -> bytes:
    """
    Построение одного 64-байтного блока кейстрима:
    - key: 32 байта
    - counter: 32-битное целое (обычно начинается с 1)
    - nonce: 12 байт (96 бит) — как в RFC 7539
    Возвращает 64 байта keystream block.
    """
    # Проверки входа
    if len(key) != 32:
        raise ValueError("Key must be 32 bytes")
    if len(nonce) != 12:
        raise ValueError("Nonce must be 12 bytes")

    # Константы в виде 4 слов little-endian ("expand 32-byte k")
    constants = (b"expa", b"nd 3", b"2-by", b"te k")
    state = [struct.unpack("<I", c)[0] for c in constants]  # 4 слова

    # ключ -> 8 слов (little-endian)
    state += list(struct.unpack("<8I", key))

    # counter (1 слово) и nonce (3 слова)
    state.append(counter & 0xFFFFFFFF)
    state += list(struct.unpack("<3I", nonce))

    # рабочее состояние
    working = state.copy()

    # 20 раундов: 10 итераций column+diagonal rounds
    for _ in range(10):
        # column rounds
        _quarter_round(working, 0, 4, 8, 12)
        _quarter_round(working, 1, 5, 9, 13)
        _quarter_round(working, 2, 6, 10, 14)
        _quarter_round(working, 3, 7, 11, 15)
        # diagonal rounds
        _quarter_round(working, 0, 5, 10, 15)
        _quarter_round(working, 1, 6, 11, 12)
        _quarter_round(working, 2, 7, 8, 13)
        _quarter_round(working, 3, 4, 9, 14)

    # добавляем исходное состояние (mod 2^32) и упаковываем в bytes little-endian
    out_words = [(working[i] + state[i]) & 0xFFFFFFFF for i in range(16)]
    return struct.pack("<16I", *out_words)  # 64 байта

# -------------------------
# Генератор кейстрима
# -------------------------

def chacha20_keystream(key: bytes, nonce: bytes, initial_counter: int = 1) -> Generator[bytes, None, None]:
    """
    Генератор бесконечного кейстрима, возвращает 64-байтные блоки.
    initial_counter по RFC обычно 1, но можно передать 0 в тестовых целях.
    """
    counter = initial_counter & 0xFFFFFFFF
    while True:
        yield _chacha20_block(key, counter, nonce)
        counter = (counter + 1) & 0xFFFFFFFF

# -------------------------
# XOR-операция (быстро)
# -------------------------

def xor_bytes_into(out: bytearray, keystream: bytes, offset: int) -> None:
    """
    XOR keystream (bytes) с out[offset:offset+len(keystream)], inplace.
    Предполагается, что out достаточно большой.
    Эта функция помогает делать XOR поблочно и эффективно.
    """
    # Используем local для скорости
    ks = keystream
    o = out
    end = offset + len(ks)
    # memoryview для производительности при присваивании
    mv = memoryview(o)
    for i in range(len(ks)):
        mv[offset + i] = mv[offset + i] ^ ks[i]

# -------------------------
# Шифрование / Расшифрование
# -------------------------

def chacha20_encrypt_bytes(key: bytes, nonce: bytes, data: bytes, initial_counter: int = 1) -> bytes:
    """
    Шифрование/дешифрование произвольного массива байт.
    Поскольку ChaCha20 — потоковый шифр, encrypt == decrypt.
    """
    if len(key) != 32:
        raise ValueError("Key must be 32 bytes")
    if len(nonce) != 12:
        raise ValueError("Nonce must be 12 bytes")

    ks_gen = chacha20_keystream(key, nonce, initial_counter)
    out = bytearray(data)  # результирующий шифротекст (in-place XOR)
    n = len(data)
    pos = 0
    # поблочно берем 64 байта кейстрима и XOR'им
    while pos < n:
        block = next(ks_gen)  # 64 байта
        take = min(64, n - pos)
        # XOR для take байт
        # faster path: use memoryview + loop
        mv_out = memoryview(out)
        for i in range(take):
            mv_out[pos + i] ^= block[i]
        pos += take
    return bytes(out)

# -------------------------
# Утилиты для текста
# -------------------------

def text_to_bytes(text: str) -> bytes:
    """Конвертируем str -> bytes (utf-8)."""
    return text.encode("utf-8")

def bytes_to_text(data: bytes) -> str:
    """Конвертируем bytes -> str (utf-8), игнорируем неверные байты."""
    return data.decode("utf-8", errors="ignore")

# -------------------------
# Демонстрация: интерактивно
# -------------------------

if __name__ == "__main__":
    print("ChaCha20 (pure Python) — демонстрация шифрования/расшифровки")
    # Ввод текста пользователем
    text = input("Введите текст для шифрования: ")

    # Генерируем случайный ключ и nonce (для демонстрации).
    # В реальном приложении храните ключ безопасно и используйте уникальный nonce.
    key = os.urandom(32)   # 32 байта = 256 бит
    nonce = os.urandom(12) # 12 байт = 96 бит
    initial_counter = 1    # обычно 1 в RFC 7539

    print("\nСгенерированный ключ (hex):", key.hex())
    print("Сгенерированный nonce (hex):", nonce.hex())
    print("initial_counter:", initial_counter)

    data = text_to_bytes(text)

    # Шифрование
    ciphertext = chacha20_encrypt_bytes(key, nonce, data, initial_counter)
    print("\n=== Результаты ===")
    print("Исходный текст :", text)
    print("Шифртекст (hex):", ciphertext.hex())

    # Дешифрование (тот же метод, потому что потоковый шифр)
    decrypted = chacha20_encrypt_bytes(key, nonce, ciphertext, initial_counter)
    print("Расшифровка     :", bytes_to_text(decrypted))

    # Проверка
    assert decrypted == data, "Ошибка: расшифровка не дала исходные данные"
    print("\nПроверка: расшифровка совпадает с исходным текстом ✅")
