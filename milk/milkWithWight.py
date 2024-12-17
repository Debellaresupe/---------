import random
import string
import urllib.parse

def generate_gtin():
    """Генерирует код товара (14 цифр согласно GS1)."""
    gtin_base = ''.join(random.choices('0123456789', k=13))
    check_digit = calculate_check_digit(gtin_base)
    return gtin_base + check_digit

def calculate_check_digit(gtin):
    """Рассчитывает контрольную цифру для кода GTIN по стандарту GS1."""
    total = sum((3 if i % 2 else 1) * int(num) for i, num in enumerate(gtin[::-1]))
    return str((10 - (total % 10)) % 10)

def generate_serial_number():
    """Генерирует серийный номер (6 символов: буквы, цифры и разрешенные спецсимволы)."""
    charset = string.ascii_letters + string.digits + "!\"%&'*+-./_,:;=<>?"
    return ''.join(random.choices(charset, k=6))

def generate_verification_code():
    """Генерирует код проверки (4 символа: буквы, цифры и разрешенные спецсимволы)."""
    charset = string.ascii_uppercase + string.digits + ":=+/"
    return ''.join(random.choices(charset, k=4))

def generate_extra_code():
    """Генерирует 6-значный дополнительный код (цифры)."""
    return ''.join(random.choices('0123456789', k=6))

def generate_mark():
    """Генерирует полную маркировку с разделителями."""
    fnc1 = "<FNC1>"  # Символ FNC1 для GS1
    gs_separator = "<GS>"  # Символ GS (Group Separator)

    gtin = generate_gtin()
    serial_number = generate_serial_number()
    verification_code = generate_verification_code()
    extra_code = generate_extra_code()

    # Полная маркировка с 6-значным блоком
    mark = (f"{fnc1}01{gtin}"
            f"21{serial_number}"
            f"{gs_separator}93{verification_code}"
            f"{gs_separator}3101{extra_code}")
    return mark

def escape_hex_symbols(mark):
    """Экранирует символы разделителей в шестнадцатеричном формате."""
    return mark.replace("<GS>", "\\x1D").replace("<FNC1>", "\\F")

def strip_delimiters_and_extra_code(mark):
    """Удаляет разделители и последние 6 цифр из маркировки."""
    return mark.replace("<FNC1>", "").replace("<GS>", "").rsplit("3101", 1)[0] + "3101"

def strip_extra_code_and_url_encode(mark):
    """Удаляет последние 6 цифр и кодирует маркировку в URL-формат."""
    mark = mark.rsplit("3101", 1)[0] + "3101"
    return urllib.parse.quote(escape_hex_symbols(mark))

# Генерация 10 базовых маркировок
base_marks = [generate_mark() for _ in range(10)]

# Создание всех вариантов из одной и той же маркировки
marks_with_hex = [escape_hex_symbols(mark) for mark in base_marks]
marks_without_delimiters = [strip_delimiters_and_extra_code(mark) for mark in base_marks]
marks_url_encoded_full = [urllib.parse.quote(escape_hex_symbols(mark)) for mark in base_marks]
marks_url_encoded_4th = [strip_extra_code_and_url_encode(mark) for mark in base_marks]

# Сохранение всех наборов в файл
with open("milkWithWight.txt", "w", encoding="utf-8") as file:
    # Набор 1: Маркировка с разделителями в шестнадцатеричном формате
    file.write("Маркировки с разделителями (в шестнадцатеричном формате):\n")
    for mark in marks_with_hex:
        file.write(mark + "\n")
    file.write("\n")

    # Набор 2: Маркировка без разделителей
    file.write("Маркировки без разделителей:\n")
    for mark in marks_without_delimiters:
        file.write(mark + "\n")
    file.write("\n")

    # Набор 3: Маркировка в URL-кодировке (полная)
    file.write("Маркировки в URL-кодировке (с полным набором разделителей и 6 цифрами):\n")
    for mark in marks_url_encoded_full:
        file.write(mark + "\n")
    file.write("\n")

    # Набор 4: Маркировка в URL-кодировке (без последних 6 цифр, но с 3101)
    file.write("Маркировки в URL-кодировке (без последних 6 цифр, с 3101):\n")
    for mark in marks_url_encoded_4th:
        file.write(mark + "\n")

# Вывод результатов
print("Маркировки сохранены в файл 'milkWithWight.txt'")
