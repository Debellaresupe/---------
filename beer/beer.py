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
    """Генерирует серийный номер (7 символов: первый символ - цифра, остальные буквы, цифры и разрешенные спецсимволы)."""
    charset = string.ascii_letters + string.digits + "!\"%&'*+-./_,:;=<>?"
    first_digit = random.choice(string.digits)
    remaining_chars = ''.join(random.choices(charset, k=6))
    return first_digit + remaining_chars

def generate_verification_code():
    """Генерирует код проверки (4 символа: буквы, цифры и разрешенные спецсимволы)."""
    charset = string.ascii_uppercase + string.digits + ":=+/"
    return ''.join(random.choices(charset, k=4))

def generate_mark():
    """Генерирует полную маркировку в заданном формате."""
    fnc1 = "<FNC1>"  # Символ FNC1 для GS1
    gs_separator = "<GS>"  # Символ GS (Group Separator)

    gtin = generate_gtin()
    serial_number = generate_serial_number()
    verification_code = generate_verification_code()

    # Формирование маркировки по шаблону
    mark = f"{fnc1}01{gtin}21{serial_number}{gs_separator}93{verification_code}"
    return mark

def escape_hex_symbols(mark):
    """Экранирует символы разделителей в шестнадцатеричном формате."""
    return mark.replace("<GS>", "\\x1D").replace("<FNC1>", "\\F")

# Генерация 10 уникальных маркировок
marks = [generate_mark() for _ in range(10)]
escaped_marks = [escape_hex_symbols(mark) for mark in marks]

# Создание списка маркировок без разделителей и крипто-хвоста
marks_without_extras = [mark.replace("<FNC1>", "").replace("<GS>", "").split("93")[0] for mark in marks]

# URL-кодировка маркировок с разделителями
marks_url_encoded = [urllib.parse.quote(mark) for mark in escaped_marks]

# Сохранение маркировок в файл
with open("beer.txt", "w", encoding="utf-8") as file:
    file.write("Маркировки с разделителями (GS1 стандарт):\n")
    for mark in escaped_marks:
        file.write(mark + "\n")
    file.write("\nМаркировки без разделителей и крипто-хвоста:\n")
    for mark in marks_without_extras:
        file.write(mark + "\n")
    file.write("\nМаркировки в URL-кодировке:\n")
    for mark in marks_url_encoded:
        file.write(mark + "\n")

# Вывод результатов
print("Маркировки сохранены в файл 'beer.txt'")
