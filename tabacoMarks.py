import random

# Набор из 80 символов для кодирования
CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!\"%&'*+-./_,:;=<>?"

def encode_with_charset(value, length):
    """
    Кодирование числа в строку фиксированной длины с использованием 80-символьного набора.
    """
    result = []
    base = len(CHARSET)
    while value > 0:
        result.append(CHARSET[value % base])
        value //= base
    result = ''.join(reversed(result))
    return result.rjust(length, CHARSET[0])  # Добавляем ведущие символы для достижения нужной длины

def generate_gtin14():
    """Генерация GTIN-14 (14-значного кода)"""
    gtin = "0" + str(random.randint(100000000000, 999999999999))
    return gtin

def generate_serial_number():
    """Генерация серийного номера (7 символов, закодированных в 80-символьном наборе)"""
    random_number = random.randint(0, 80**7 - 1)
    return encode_with_charset(random_number, 7)

def generate_mpl():
    """Генерация MPL (4 символа, закодированных в 80-символьном наборе)"""
    random_number = random.randint(0, 80**4 - 1)
    return encode_with_charset(random_number, 4)

def generate_crypto_tail():
    """Генерация криптохвоста (4 случайных символа из 80-символьного набора)"""
    return ''.join(random.choice(CHARSET) for _ in range(4))

def generate_code():
    """Сборка строки из 29 символов"""
    gtin14 = generate_gtin14()
    serial_number = generate_serial_number()
    mpl = generate_mpl()
    crypto_tail = generate_crypto_tail()

    return f"{gtin14}{serial_number}{mpl}{crypto_tail}"

# Генерация примера кода
if __name__ == "__main__":
    mark_code = generate_code()
    print("Сгенерированная марка:", mark_code)
