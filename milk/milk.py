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

def url_encode_hex_symbols(mark):
    """URL-кодирует маркировку с разделителями в шестнадцатеричном формате."""
    return urllib.parse.quote(mark)

def create_segmented_marks(marks_with_separators):
    """Создает марки, разбитые на сегменты с названиями."""
    segmented_marks = []
    for mark in marks_with_separators:
        try:
            # Удаляем FNC1 символ и разбиваем по разделителям
            clean_mark = mark.replace("\\F", "")
            parts = clean_mark.split("\\x1D")

            # Извлечение сегментов
            gtin_part = parts[0][2:16] if parts[0].startswith("01") else ""
            serial_part = parts[0][18:] if len(parts[0]) > 18 and parts[0][16:18] == "21" else ""
            verification_part = parts[1][2:] if len(parts) > 1 and parts[1].startswith("93") else ""

            segmented_mark = {
                "**_GTIN_**": gtin_part,
                "**_SerialNumber_**": serial_part,
                "**_VerificationCode_**": verification_part
            }
            segmented_marks.append(segmented_mark)
        except IndexError:
            segmented_marks.append({
                "**_GTIN_**": "",
                "**_SerialNumber_**": "",
                "**_VerificationCode_**": ""
            })
    return segmented_marks

# Генерация 10 уникальных маркировок
marks = [generate_mark() for _ in range(10)]
escaped_marks = [escape_hex_symbols(mark) for mark in marks]

# Создание списка маркировок без разделителей и крипто-хвоста
marks_without_extras = [mark.replace("<FNC1>", "").replace("<GS>", "").split("93")[0] for mark in marks]

# URL-кодировка маркировок с разделителями в шестнадцатеричном формате
escaped_url_encoded_marks = [url_encode_hex_symbols(escape_hex_symbols(mark)) for mark in marks]

# Разделение маркировок на сегменты
segmented_marks = create_segmented_marks(escaped_marks)

# Сохранение маркировок в файл
with open("milk.txt", "w", encoding="utf-8") as file:
    file.write("Маркировки с разделителями в шестнадцатеричном формате:\n")
    for mark in escaped_marks:
        file.write(mark + "\n")
    file.write("\nМаркировки без разделителей и крипто-хвоста:\n")
    for mark in marks_without_extras:
        file.write(mark + "\n")
    file.write("\nМаркировки в URL-кодировке (разделители в шестнадцатеричном формате):\n")
    for mark in escaped_url_encoded_marks:
        file.write(mark + "\n")
    file.write("\nМаркировки разбитые на сегменты:\n")
    for mark in segmented_marks:
        file.write(str(mark) + "\n")

# Вывод результатов
print("Маркировки сохранены в файл 'milk.txt'")
