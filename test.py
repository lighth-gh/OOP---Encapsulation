import math
import sys

def parse_input(line):
    """Phân tích input thành các thành phần số học"""
    base, exponent = line.split()
    x, y = map(int, base.split('/'))
    z, t = map(int, exponent.split('/'))
    return x, y, z, t

def is_indeterminate(x, y, z, t):
    """Kiểm tra biểu thức không xác định"""
    # Mẫu số bằng 0
    if y == 0 or t == 0:
        return True
    # 0 mũ không dương
    if x == 0 and (z/t) <= 0:
        return True
    # Cơ số âm với mẫu mũ chẵn
    if (x/y) < 0 and (t % 2 == 0):
        return True
    return False

def simplify_fraction(a, b):
    """Rút gọn phân số và chuẩn hóa dấu"""
    # Xử lý dấu phân số
    if a * b > 0 and a < 0:
        a, b = -a, -b
    
    # Tìm ước chung lớn nhất
    gcd_val = math.gcd(abs(a), abs(b))
    return a//gcd_val, b//gcd_val

def find_integer_root(x, n):
    """Tìm căn bậc n nguyên bằng binary search"""
    if x == 0:
        return 0
    if n <= 0:
        return None
    
    # Xử lý số âm
    if x < 0:
        if n % 2 == 0:
            return None
        x = -x
        root = find_integer_root(x, n)
        return -root if root else None
    
    # Tìm kiếm nhị phân
    low, high = 1, x
    while low <= high:
        mid = (low + high) // 2
        power = mid ** n
        if power == x:
            return mid
        elif power < x:
            low = mid + 1
        else:
            high = mid - 1
    return None

def optimize_expression(x, y, z, t):
    """Tối ưu biểu thức bằng cách trích căn tối đa"""
    max_root = 1
    
    # Tìm bậc căn lớn nhất khả thi
    for i in range(2, t + 1):
        x_root = find_integer_root(x, i)
        y_root = find_integer_root(y, i)
        if x_root is not None and y_root is not None:
            max_root = i
    
    # Áp dụng trích căn
    new_x = find_integer_root(x, max_root) or x
    new_y = find_integer_root(y, max_root) or y
    
    # Điều chỉnh số mũ
    new_z = z * max_root
    new_t = t
    
    return (*simplify_fraction(new_x, new_y), *simplify_fraction(new_z, new_t))

def process_line(line):
    """Xử lý chính cho mỗi dòng input"""
    x, y, z, t = parse_input(line)
    
    # Kiểm tra mẫu số hợp lệ
    if y == 0 or t == 0:
        return f"({x}/{y})^({z}/{t})"
    
    # Rút gọn phân số
    sx, sy = simplify_fraction(x, y)
    sz, st = simplify_fraction(z, t)
    
    # Kiểm tra vô định
    if is_indeterminate(sx, sy, sz, st):
        return f"({x}/{y})^({z}/{t})"
    
    # Tối ưu biểu thức
    rx, ry, rz, rt = optimize_expression(sx, sy, sz, st)
    
    # Xử lý số mũ âm
    if (rz * rt) < 0:
        rz, rt = abs(rz), abs(rt)
        rx, ry = ry, rx
    
    # Trường hợp đặc biệt 1^0
    if (rx/ry) ** (rz/rt) == 1:
        rx, ry, rz, rt = 1, 1, 0, 1
    
    # Trường hợp 0^b
    if rx == 0:
        rx, ry, rz, rt = 0, 1, 1, 1
    
    # Xử lý mũ chẵn
    if rz % 2 == 0 and rt == 1:
        rx, ry = abs(rx), abs(ry)
    
    # Chuẩn hóa dấu phân số
    if rx * ry < 0 and ry < 0:
        rx, ry = -rx, abs(ry)
    
    return f"({rx}/{ry})^({rz}/{rt})"

def main():
    """Hàm chính đọc input và xử lý"""
    for line in sys.stdin:
        line = line.strip()
        if line:
            print(process_line(line))

if __name__ == "__main__":
    main()
