import random 
import string
import urllib.parse
from datetime import datetime

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
    """Генерирует серийный номер (13 символов: буквы, цифры и разрешенные спецсимволы)."""
    charset = string.ascii_letters + string.digits + "!\"%&'*+-./_,:;=<>?"
    return ''.join(random.choices(charset, k=13))

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
    current_date = datetime.now().strftime("%y%m%d%H%M")  # Формат ГГММДДЧЧММ
    verification_code = generate_verification_code()

    # Формирование маркировки по новому шаблону
    mark = f"{fnc1}01{gtin}21{serial_number}7003{current_date}{gs_separator}93{verification_code}"
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
            serial_part = parts[0][18:31] if len(parts[0]) > 31 and parts[0][16:18] == "21" else ""
            date_start_index = parts[0].find("7003") + 4
            date_part = parts[0][date_start_index:date_start_index + 12] if date_start_index > 3 else ""
            verification_part = parts[1][2:] if len(parts) > 1 and parts[1].startswith("93") else ""

            segmented_mark = {
                "**_GTIN_**": gtin_part,
                "**_SerialNumber_**": serial_part,
                "**_Date_**": date_part,
                "**_VerificationCode_**": verification_part
            }
            segmented_marks.append(segmented_mark)
        except IndexError:
            segmented_marks.append({
                "**_GTIN_**": "",
                "**_SerialNumber_**": "",
                "**_Date_**": "",
                "**_VerificationCode_**": ""
            })
    return segmented_marks

def create_date_split_segments(marks_with_separators):
    """Создает марки, разделенные на два сегмента: BeforeDate и AfterDate."""
    date_split_segments = []
    for mark in marks_with_separators:
        fnc1 = "\\F"
        gs_separator = "\\x1D"
        try:
            date_index = mark.find("7003")
            if date_index != -1:
                before_date = mark[:date_index] + "7003"
                after_date = gs_separator + mark.split(gs_separator)[1]  # Включаем GS и криптохвост
                date_split_segments.append(f"{urllib.parse.quote(before_date)},{urllib.parse.quote(after_date)}")
            else:
                date_split_segments.append("", "")
        except IndexError:
            date_split_segments.append("", "")
    return date_split_segments

# Генерация 10 уникальных маркировок
marks = [generate_mark() for _ in range(10)]
escaped_marks = [escape_hex_symbols(mark) for mark in marks]

# Создание списка маркировок без разделителей и крипто-хвоста
marks_without_extras = [mark.replace("<FNC1>", "").replace("<GS>", "").split("93")[0] for mark in marks]

# URL-кодировка маркировок с разделителями в шестнадцатеричном формате
escaped_url_encoded_marks = [url_encode_hex_symbols(escape_hex_symbols(mark)) for mark in marks]

# Разделение маркировок на сегменты
segmented_marks = create_segmented_marks(escaped_marks)

# Разделение маркировок на два сегмента: до даты и после даты
date_split_segments = create_date_split_segments(escaped_marks)

# Сохранение маркировок в файл
with open("milkWithShellife.txt", "w", encoding="utf-8") as file:
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
    file.write("\nМаркировки разбитые на два сегмента (до даты и после даты):\n")
    for segment in date_split_segments:
        file.write(segment + "\n")

# Вывод результатов
print("Маркировки сохранены в файл 'milkWithShellife.txt'")