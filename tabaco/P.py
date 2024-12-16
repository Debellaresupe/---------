import random

def generate_gtin():
    """Генерирует код товара (14 цифр)."""
    return ''.join(random.choices('0123456789', k=14))

def generate_serial_number():
    """Генерирует индивидуальный серийный номер (7 символов) из расширенного списка."""
    charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!\"%&'*+-./_,:;=<>?"
    return ''.join(random.choices(charset, k=7))

def generate_price():
    """Генерирует сумму максимальных розничных цен (6 символов)."""
    price_in_kopecks = random.randint(0, 999999)
    return str(price_in_kopecks).zfill(6)

def generate_verification_code():
    """Генерирует код проверки (4 символа)."""
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=4))

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

    # Без символов GS и FNC1
    mark_without_gs = (
        f"01{gtin}"
        f"21{serial_number}"
        f"8005{price}"
        f"93{verification_code}"
    )

    return mark_with_gs, mark_without_gs

def escape_hex_symbols(mark):
    """Экранирует символы разделителей в шестнадцатеричном формате."""
    return mark.replace("\x1D", "\\x1D")

# Генерация 10 уникальных маркировок
marks_with_gs = []
marks_without_gs = []

for _ in range(10):
    mark_with_gs, mark_without_gs = generate_mark()
    # Экранируем разделители в марках с символами GS
    marks_with_gs.append(escape_hex_symbols(mark_with_gs))
    marks_without_gs.append(mark_without_gs)

# Сохранение маркировок в файл
with open("marks_grouped.txt", "w", encoding="utf-8") as file:
    # Группа марок с символами GS
    file.write("Марки с символами GS:\n")
    for mark in marks_with_gs:
        file.write(mark + "\n")
    file.write("\n")

    # Группа марок без символов GS
    file.write("Марки без символов GS:\n")
    for mark in marks_without_gs:
        file.write(mark + "\n")

# Вывод результатов
print("Сгруппированные маркировки сохранены в файл 'marks_grouped.txt'")
