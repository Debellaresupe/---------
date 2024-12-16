import random

# Алфавит для кодирования
ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz0123456789!\"%&'*+-./_,:;=<>?"

# Функция для кодирования числа в систему с основанием 80
def encode_price(price):
    base = len(ALPHABET)
    encoded = ""
    while price > 0:
        remainder = price % base
        encoded = ALPHABET[remainder] + encoded
        price //= base
    # Дополняем строку до 4 символов, если необходимо
    while len(encoded) < 4:
        encoded = ALPHABET[0] + encoded
    return encoded

# Функция для генерации первого блока (14 цифр, начинающихся с нуля)
def generate_product_code():
    return "0" + ''.join(random.choices("0123456789", k=13))

# Функция для генерации второго блока (7 символов)
def generate_serial_number():
    return ''.join(random.choices(ALPHABET, k=7))

# Функция для генерации третьего блока (4 символа на основе цены)
def generate_encoded_price():
    random_price = random.randint(20000, 50000)  # Случайное число от 20000 до 50000
    return encode_price(random_price)

# Функция для генерации четвертого блока (4 символа)
def generate_verification_code():
    return ''.join(random.choices(ALPHABET, k=4))

# Функция для генерации одного кода
def generate_identification_code():
    group1 = generate_product_code()
    group2 = generate_serial_number()
    group3 = generate_encoded_price()
    group4 = generate_verification_code()
    return f"\"{group1}{group2}{group3}{group4}\","

# Функция для генерации кодов по блокам
def generate_codes_by_blocks():
    blocks = {
        "Block 1": 4,  # 4 марки
        "Block 2": 5,  # 5 марок
        "Block 3": 10, # 10 марок
        "Block 4": [10] * 5, # 5 групп по 10 марок
        "Block 5": [10] * 5 + [1] # 5 групп по 10 марок + 1 марка
    }

    result = {}
    for block, count in blocks.items():
        if isinstance(count, list):  # Если блок состоит из групп
            result[block] = []
            for group_size in count:
                group = [generate_identification_code() for _ in range(group_size)]
                result[block].append(group)
        else:  # Если блок состоит из одиночных марок
            result[block] = [generate_identification_code() for _ in range(count)]
    return result

# Функция для сохранения кодов в файл
def save_codes_to_file(codes_by_blocks, filename="tobacoMarks.txt"):
    with open(filename, "w", encoding="utf-8") as file:
        for block, codes in codes_by_blocks.items():
            file.write(f"{block}:\n")
            if isinstance(codes[0], list):  # Для групп
                for i, group in enumerate(codes, start=1):
                    file.write(f"  Group {i}:\n")
                    for code in group:
                        file.write(f"    {code}\n")
            else:  # Для одиночных марок
                for code in codes:
                    file.write(f"  {code}\n")
            file.write("\n")

# Генерация и сохранение кодов
if __name__ == "__main__":
    codes_by_blocks = generate_codes_by_blocks()
    save_codes_to_file(codes_by_blocks)
    print("Коды успешно сохранены в файл tobacoMarks.txt")
