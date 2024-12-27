import random
import string
import urllib.parse
import os

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
    """Генерирует серийный номер (6 символов: первый символ цифра, остальные буквы, цифры и разрешенные спецсимволы по GS1)."""
    charset = string.ascii_uppercase + string.digits + "!\"%&'()*+,-./:;<=>?_"
    first_digit = random.choice(string.digits)
    other_characters = ''.join(random.choices(charset, k=5))
    return first_digit + other_characters

def generate_id_key():
    """Генерирует ИД ключа проверки (4 символа, включая буквы)."""
    charset = string.ascii_uppercase + string.digits
    return ''.join(random.choices(charset, k=4))

def generate_verification_code():
    """Генерирует код проверки (44 символа: буквы, цифры и спецсимволы для криптохвоста по GS1)."""
    charset = string.ascii_uppercase + string.digits + ":=+/"
    return ''.join(random.choices(charset, k=44))

def escape_hex_symbols(mark):
    """Экранирует символы разделителей в шестнадцатеричном формате."""
    return mark.replace("<GS>", "\\x1D").replace("\\F", "\\x1D")

def generate_mark(with_separators=True, include_verification=True):
    """Генерирует маркировку в формате GS1 с разделителями и опционально крипто-хвостом."""
    fnc1 = "\\F"  # GS1 символ FNC1
    gs = "\\x1D"   # GS1 символ Group Separator (GS)

    gtin = generate_gtin()
    serial_number = generate_serial_number()
    id_key = generate_id_key()
    verification_code = generate_verification_code() if include_verification else ""

    mark = (
        f"{fnc1}01{gtin}{gs}21{serial_number}{gs}91{id_key}{gs}92{verification_code}"
        if with_separators else f"01{gtin}21{serial_number}91{id_key}"
    )
    return mark

def create_marks_without_extras(marks_with_separators):
    """Создает марки без разделителей и крипто-хвоста."""
    marks_without_extras = []
    for mark in marks_with_separators:
        base_mark = mark.split("92")[0]  # Убираем крипто-хвост
        base_mark = base_mark.replace("\\F", "").replace("\\x1D", "")  # Убираем разделители
        marks_without_extras.append(base_mark)
    return marks_without_extras

def create_url_encoded_marks(marks_with_separators):
    """Создает марки в URL-кодировке."""
    return [urllib.parse.quote(mark) for mark in marks_with_separators]

def create_segmented_marks(marks_with_separators):
    """Создает марки, разбитые на сегменты с названиями."""
    segmented_marks = []
    for mark in marks_with_separators:
        parts = mark.split("\\x1D")
        segmented_mark = {
            "**_GTIN_**": parts[0].replace("\\F01", ""),
            "**_SerialNumber_**": parts[1].replace("21", ""),
            "**_IDKey_**": parts[2].replace("91", ""),
            "**_VerificationCode_**": parts[3].replace("92", "") if len(parts) > 3 else ""
        }
        segmented_marks.append(segmented_mark)
    return segmented_marks

# Генерация 10 уникальных маркировок
marks_with_separators = [generate_mark(with_separators=True, include_verification=True) for _ in range(10)]
marks_without_extras = create_marks_without_extras(marks_with_separators)
marks_url_encoded = create_url_encoded_marks(marks_with_separators)
marks_segmented = create_segmented_marks(marks_with_separators)

# Получение пути для сохранения файла в одной директории с исполняемым кодом
output_file_path = os.path.join(os.path.dirname(__file__), "ikra.txt")

# Сохранение маркировок в файл
with open(output_file_path, "w", encoding="utf-8") as file:
    file.write("Маркировки с разделителями (GS1 стандарт):\n")
    for mark in marks_with_separators:
        file.write(mark + "\n")
    file.write("\nМаркировки без разделителей и крипто-хвоста:\n")
    for mark in marks_without_extras:
        file.write(mark + "\n")
    file.write("\nМаркировки в URL-кодировке:\n")
    for mark in marks_url_encoded:
        file.write(mark + "\n")
    file.write("\nМаркировки разбитые на сегменты:\n")
    for mark in marks_segmented:
        file.write(str(mark) + "\n")

# Вывод результатов
print(f"Маркировки сохранены в файл '{output_file_path}'")
