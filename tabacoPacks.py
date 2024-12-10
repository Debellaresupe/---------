import random
import string

def generate_serial_number(length=7):
    """Генерация серийного номера с учетом специальных символов."""
    chars = string.ascii_uppercase + string.digits + "!@#$%^&*"
    return ''.join(random.choices(chars, k=length))

def generate_check_code(length=4):
    """Генерация кода проверки (AI 93) с буквами."""
    chars = string.ascii_uppercase
    return ''.join(random.choices(chars, k=length))

def generate_code(global_id, quantity):
    """Генерация полного GS1 DM-кода."""
    serial_number = generate_serial_number()
    check_code = generate_check_code()
    code = (
        f"<FNC1>01{global_id}21{serial_number}<GS>"
        f"8005{quantity}<GS>93{check_code}"
    )
    return code

# Пример параметров для генерации
global_id = "04600439931256"  # 14 символов
quantity = "112000"          # 6 символов

# Генерация трех кодов
codes = [generate_code(global_id, quantity) for _ in range(10)]

# Вывод результатов
for idx, code in enumerate(codes, 1):
    print(f"Код {idx}: {code}")
