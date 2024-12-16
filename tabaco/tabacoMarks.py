import random
import urllib.parse

# Алфавит для кодирования
ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz0123456789!\"%&'*+-./_,:;=<>?"
SERIAL_ALLOWED = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!\"%&'()*+,-./:;<=>?"  # Разрешенные символы GS1 для серийных номеров
VERIFICATION_ALLOWED = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ=/+:."  # Разрешенные символы для криптохвостов

# Функция для генерации номера продукта согласно стандарту GS1
# GTIN-14 (Global Trade Item Number)
def generate_gtin14():
    base_gtin = "0" + ''.join(random.choices("0123456789", k=12))  # 12 цифр плюс префикс 0
    check_digit = calculate_check_digit(base_gtin)
    return base_gtin + str(check_digit)

# Функция для вычисления контрольной цифры для GTIN-14
def calculate_check_digit(gtin):
    odd_sum = sum(int(gtin[i]) for i in range(0, len(gtin), 2))
    even_sum = sum(int(gtin[i]) for i in range(1, len(gtin), 2))
    total_sum = odd_sum * 3 + even_sum
    check_digit = (10 - (total_sum % 10)) % 10
    return check_digit

# Функция для кодирования МРЦ (максимальной розничной цены)
def encode_price(price):
    base = len(ALPHABET)
    encoded = ""
    while price > 0:
        remainder = price % base
        encoded = ALPHABET[remainder] + encoded
        price //= base
    while len(encoded) < 4:  # Дополняем до 4 символов
        encoded = ALPHABET[0] + encoded
    return encoded

# Функция для генерации серийного номера согласно стандарту GS1
# Серийный номер из 7 символов (включает разрешенные спецсимволы)
def generate_serial_number():
    return ''.join(random.choices(SERIAL_ALLOWED, k=7))

# Функция для генерации проверочного кода (криптохвост из 4 символов, включает новые разрешенные символы)
def generate_verification_code():
    return ''.join(random.choices(VERIFICATION_ALLOWED, k=4))

# Функция для генерации МРЦ (максимальная розничная цена)
def generate_encoded_price():
    price = random.randint(20000, 50000)  # Случайная цена в копейках
    return encode_price(price)

# Функция для генерации полного GS1 кода
def generate_gs1_code():
    product_code = generate_gtin14()  # Код товара - 14 символов
    serial = generate_serial_number()  # Серийный номер - 7 символов
    encoded_price = generate_encoded_price()  # МРЦ - 4 символа
    verification_code = generate_verification_code()  # Код проверки - 4 символа
    full_code = f"{product_code}{serial}{encoded_price}{verification_code}"
    url_encoded_code = urllib.parse.quote(full_code)  # URL-кодирование
    return url_encoded_code, f"{product_code}{serial}{encoded_price}"

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
    secondary_result = {}
    for block, count in blocks.items():
        if isinstance(count, list):  # Если блок состоит из групп
            result[block] = []
            secondary_result[block] = []
            for group_size in count:
                group = []
                secondary_group = []
                for _ in range(group_size):
                    full_code, secondary_code = generate_gs1_code()
                    group.append(full_code)
                    secondary_group.append(secondary_code)
                result[block].append(group)
                secondary_result[block].append(secondary_group)
        else:  # Если блок состоит из одиночных марок
            result[block] = []
            secondary_result[block] = []
            for _ in range(count):
                full_code, secondary_code = generate_gs1_code()
                result[block].append(full_code)
                secondary_result[block].append(secondary_code)
    return result, secondary_result

# Функция для сохранения кодов в файл
def save_codes_to_file(codes_by_blocks, secondary_codes_by_blocks, filename="tobacoMarks.txt"):
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

        file.write("\nSecondary Marks:\n\n")

        for block, codes in secondary_codes_by_blocks.items():
            file.write(f"{block}:\n")
            if isinstance(codes[0], list):  # Для групп
                for i, group in enumerate(codes, start=1):
                    file.write(f"  Group {i}:\n")
                    for sub_code in group:
                        file.write(f"    {sub_code}\n")
            else:  # Для одиночных марок
                for code in codes:
                    file.write(f"  {code}\n")
            file.write("\n")

# Генерация и сохранение кодов
if __name__ == "__main__":
    codes_by_blocks, secondary_codes_by_blocks = generate_codes_by_blocks()
    save_codes_to_file(codes_by_blocks, secondary_codes_by_blocks)
    print("Коды успешно сохранены в файл tobacoMarks.txt")
