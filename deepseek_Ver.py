import math
import sys

class Luythua:
    def __init__(self, input_line):
        """Hàm khởi tạo, tách input thành phân số"""
        base_raw, exponent_raw = input_line.split()
        
        x, y = map(int, base_raw.split('/'))
        z, t = map(int, exponent_raw.split('/'))
        self.original_x = x
        self.original_y = y
        self.original_z = z
        self.original_t = t

    def is_batdinh(self, x, y, z, t):
        #mẫu số = 0
        if y == 0 or t == 0:
            return True
        
        #0^b với b <= 0
        if x == 0 and (z / t) <= 0:
            return True
        
        #cơ số âm, mẫu số mũ chẵn
        if (x / y) < 0 and (t % 2 == 0):
            return True
        
        return False

    def simplify_fraction(self, a, b):
        if a * b > 0 and a < 0:
            a, b = -a, -b
        gcd_val = math.gcd(abs(a), abs(b))
        return a // gcd_val, b // gcd_val

    def nth_root_int(self, x, n):
        """căn bậc n của x, dùng binary search"""
        if x == 0:
            return 0
        if n <= 0:
            return None
        
        #với x < 0, chia trường hợp n chẵn, n lẻ
        if x < 0:
            if n % 2 == 0:
                return None
            else:
                abs_x = -x
                root = self.nth_root_int(abs_x, n)
                return -root if root is not None else None
        
        # Tìm căn nguyên bằng binary search
        low = 1
        high = x
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

    def nth_root(self, x: int, y: int, z: int, t: int):
        """Tối ưu hóa biểu thức bằng cách trích căn lớn nhất có thể"""
        max_i = 1  # Lưu bậc căn lớn nhất tìm được
        
        # Tìm bậc căn lớn nhất mà cả tử và mẫu đều có căn nguyên
        for i in range(2, t + 1):
            x_root = self.nth_root_int(x, i)
            y_root = self.nth_root_int(y, i)
            if x_root is not None and y_root is not None:
                max_i = i

        # Áp dụng bậc căn lớn nhất tìm được
        x_root = self.nth_root_int(x, max_i) if max_i != 0 else x
        y_root = self.nth_root_int(y, max_i) if max_i != 0 else y

        # Cập nhật giá trị mới sau khi trích căn
        x_new = x_root if x_root is not None else x
        y_new = y_root if y_root is not None else y

        # Điều chỉnh số mũ tương ứng
        z_new = z * max_i
        t_new = t

        # Rút gọn lại các phân số
        base_simplified = self.simplify_fraction(x_new, y_new)
        exp_simplified = self.simplify_fraction(z_new, t_new)

        return (*base_simplified, *exp_simplified)

    def special_case(self):
        """Xử lý các trường hợp đặc biệt và xử lý số, dấu bla"""
        x, y, z, t = self.original_x, self.original_y, self.original_z, self.original_t

        #check mẫu số = 0
        if y == 0 or t == 0:
            self.result = f"({x}/{y})^({z}/{t})"
            return

        simple_x, simple_y = self.simplify_fraction(x, y)
        simple_z, simple_t = self.simplify_fraction(z, t)

        if self.is_batdinh(simple_x, simple_y, simple_z, simple_t):
            self.result = f"({x}/{y})^({z}/{t})"
            return

        rooted_x, rooted_y, rooted_z, rooted_t = self.nth_root(simple_x, simple_y, simple_z, simple_t)

        #số mũ âm => đảo cơ số
        if (rooted_z * rooted_t) < 0:
            rooted_z, rooted_t = abs(rooted_z), abs(rooted_t)
            rooted_x, rooted_y = rooted_y, rooted_x

        #1^n
        if (rooted_x / rooted_y) ** (rooted_z / rooted_t) == 1:
            rooted_x, rooted_y, rooted_z, rooted_t = 1, 1, 0, 1

        #cơ số = 0
        if rooted_x == 0:
            rooted_x, rooted_y, rooted_z, rooted_t = 0, 1, 1, 1

        #xoá dấu khi mũ chẵn
        if rooted_z % 2 == 0 and rooted_t == 1:
            rooted_x, rooted_y = abs(rooted_x), abs(rooted_y)
        
        #cho dấu phân số lên trước
        if rooted_x * rooted_y < 0 and rooted_y < 0:
            rooted_x = -rooted_x
            rooted_y = abs(rooted_y)
        
        self.result = f"({rooted_x}/{rooted_y})^({rooted_z}/{rooted_t})"

    def to_string(self):
        self.special_case()
        return self.result
    
def main():
    for l in sys.stdin.read().split('\n'):
        if l.strip():
            print(Luythua(l.strip()).to_string())

if __name__ == "__main__":
    main()