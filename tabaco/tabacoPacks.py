import random
import urllib.parse

def calculate_check_digit(gtin_without_check_digit):
    """
    Вычисляет контрольную цифру для GTIN по стандарту GS1.
    Алгоритм основан на модифицированном модуле 10.
    """
    total = 0
    for i, digit in enumerate(reversed(gtin_without_check_digit)):
        multiplier = 3 if i % 2 == 0 else 1
        total += int(digit) * multiplier
    remainder = total % 10
    return str((10 - remainder) % 10)

def generate_gtin():
    """Генерирует корректный GTIN-14."""
    gtin_without_check_digit = ''.join(random.choices('0123456789', k=13))  # 13 цифр без контрольной
    check_digit = calculate_check_digit(gtin_without_check_digit)
    return gtin_without_check_digit + check_digit

def generate_serial_number():
    """Генерирует индивидуальный серийный номер (7 символов) из расширенного списка."""
    charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!\"%&'*+-./_,:;=<>?"
    return ''.join(random.choices(charset, k=7))

def generate_price():
    """Генерирует сумму максимальных розничных цен (6 символов)."""
    price_in_kopecks = random.randint(0, 999999)
    return str(price_in_kopecks).zfill(6)

def generate_verification_code():
    """
    Генерирует код проверки (криптохвост) (4 символа).
    Допускаются символы `=`, `/`, `+` и `:`.
    """
    charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789=+/:"  # Допустимые символы
    return ''.join(random.choices(charset, k=4))

def generate_mark():
    """Генерирует полную маркировку, совместимую с GS1 DataMatrix."""
    fnc1 = "\\F"  # Символ FNC1 для GS1
    gs_separator = "\x1D"  # Символ GS (Group Separator)

    gtin = generate_gtin()
    serial_number = generate_serial_number()
    price = generate_price()
    verification_code = generate_verification_code()

    # С маркерами GS и FNC1
    mark_with_gs = (
        f"{fnc1}01{gtin}"
        f"21{serial_number}"
        f"{gs_separator}8005{price}"
        f"{gs_separator}93{verification_code}"
    )

    # Без символов GS, без последнего блока
    mark_without_gs = (
        f"01{gtin}"
        f"21{serial_number}"
        f"8005{price}"
    )

    return mark_with_gs, mark_without_gs

def escape_hex_symbols(mark):
    """Экранирует символы разделителей в шестнадцатеричном формате."""
    return mark.replace("\x1D", "\\x1D")

def url_encode_mark(mark):
    """Преобразует марку в URL-кодировку."""
    return urllib.parse.quote(mark)

# Генерация 14 уникальных маркировок
marks_with_gs = []
marks_without_gs = []
marks_url_encoded = []

for _ in range(14):
    mark_with_gs, mark_without_gs = generate_mark()
    # Экранируем разделители в марках с символами GS
    escaped_mark_with_gs = escape_hex_symbols(mark_with_gs)
    marks_with_gs.append(escaped_mark_with_gs)
    # Заключаем марки без символов GS в двойные кавычки
    marks_without_gs.append(f'"{mark_without_gs}"')
    # Преобразуем марку с символами GS в URL-кодировку
    marks_url_encoded.append(url_encode_mark(mark_with_gs))

# Группировка маркировок
groups_with_gs = {
    "Group 1 (1 марка)": marks_with_gs[:1],
    "Group 2 (1 марка)": marks_with_gs[1:2],
    "Group 3 (1 марка)": marks_with_gs[2:3],
    "Group 4 (5 марок)": marks_with_gs[3:8],
    "Group 5 (6 марок)": marks_with_gs[8:14],
}

groups_without_gs = {
    "Group 1 (1 марка)": marks_without_gs[:1],
    "Group 2 (1 марка)": marks_without_gs[1:2],
    "Group 3 (1 марка)": marks_without_gs[2:3],
    "Group 4 (5 марок)": marks_without_gs[3:8],
    "Group 5 (6 марок)": marks_without_gs[8:14],
}

groups_url_encoded = {
    "Group 1 (1 марка)": marks_url_encoded[:1],
    "Group 2 (1 марка)": marks_url_encoded[1:2],
    "Group 3 (1 марка)": marks_url_encoded[2:3],
    "Group 4 (5 марок)": marks_url_encoded[3:8],
    "Group 5 (6 марок)": marks_url_encoded[8:14],
}

# Сохранение маркировок в файл
with open("Табак:блоки.txt", "w", encoding="utf-8") as file:
    # Группа марок с символами GS
    file.write("Марки с символами GS:\n")
    for group_name, group_marks in groups_with_gs.items():
        file.write(f"{group_name}:\n")
        for mark in group_marks:
            file.write(mark + "\n")
        file.write("\n")

    # Группа марок без символов GS
    file.write("Марки без символов GS и последнего блока:\n")
    for group_name, group_marks in groups_without_gs.items():
        file.write(f"{group_name}:\n")
        for mark in group_marks:
            file.write(mark + "\n")
        file.write("\n")

    # Группа марок в URL-кодировке
    file.write("Марки в URL-кодировке:\n")
    for group_name, group_marks in groups_url_encoded.items():
        file.write(f"{group_name}:\n")
        for mark in group_marks:
            file.write(mark + "\n")
        file.write("\n")

# Вывод результатов
print("Сгруппированные маркировки сохранены в файл 'marks_grouped.txt'")
