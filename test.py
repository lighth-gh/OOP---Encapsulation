'''Nhập vào một dãy các lũy thừa có dạng a^b trong đó a và b là 2 phân số. 
Rút gọn các lũy thừa trên và xuất dạng sau rút gọn ra màn hình. 
Input gồm nhiều dòng có dạng x/y, z/t'''

import math

class Luythua:
    def __init__(self, input_line):
        base_raw, exponent_raw = input_line.split()
        x, y = map(int, base_raw.split('/'))
        z, t = map(int, exponent_raw.split('/'))
        self.original_x = x
        self.original_y = y
        self.original_z = z
        self.original_t = t

    #check luỹ thừa vô định
    def is_batdinh(self, x, y, z, t):
        #0^b, b<=0
        if x == 0 and (z / t) <= 0:
            return True
        #base<0, mẫu mũ chẵn
        if (x / y) < 0 and (t % 2 == 0):
            return True
        return False

    #rút gọn phân số
    def simplify_fraction(self, a, b):
        if a * b > 0 and a < 0:
            a, b = -a, -b
        gcd_val = math.gcd(abs(a), abs(b))
        return a // gcd_val, b // gcd_val

    def nth_root_int(self, x, n):
        if x == 0:
            return 0
        if n <= 0:
            return None
        if x < 0:
            if n % 2 == 0:
                return None
            else:
                abs_x = -x
                root = self.nth_root_int(abs_x, n)
                return -root if root is not None else None
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
        max_i = 1

        for i in range(2, t + 1):
            x_root = self.nth_root_int(x, i)
            y_root = self.nth_root_int(y, i)
            if x_root is not None and y_root is not None:
                max_i = i

        x_root = self.nth_root_int(x, max_i) if max_i != 0 else x
        y_root = self.nth_root_int(y, max_i) if max_i != 0 else y

        x_new = x_root if x_root is not None else x
        y_new = y_root if y_root is not None else y

        z_new = z * max_i
        t_new = t

        base_simplified = self.simplify_fraction(x_new, y_new)
        exp_simplified = self.simplify_fraction(z_new, t_new)

        return (*base_simplified, *exp_simplified)

    #mấy trường hợp rút gọn đặc biệt
    def special(self):
        x, y, z, t = self.original_x, self.original_y, self.original_z, self.original_t

        #mẫu = 0
        if y == 0 or t == 0:
            self.result = f"({x}/{y})^({z}/{t})"
            return

        simple_x, simple_y = self.simplify_fraction(x, y)
        simple_z, simple_t = self.simplify_fraction(z, t)

        #check bất định
        if self.is_batdinh(simple_x, simple_y, simple_z, simple_t):
            self.result = f"({x}/{y})^({z}/{t})"
            return

        #căn bậc n
        rooted_x, rooted_y, rooted_z, rooted_t = self.nth_root(x, y, z, t)

        #xử lý dấu
        if rooted_z * rooted_t < 0:
            rooted_z, rooted_t = abs(rooted_z), abs(rooted_t)
            rooted_x, rooted_y = rooted_y, rooted_x

        #luỹ thừa = 1, trả về (1/1)^(0/1)
        if (rooted_x / rooted_y) ** (rooted_z / rooted_t) == 1:
            rooted_x, rooted_y, rooted_z, rooted_t = 1, 1, 0, 1

        #base = 0, trả về (0/1)^(1/1)
        if rooted_x == 0:
            rooted_x, rooted_y, rooted_z, rooted_t = 0, 1, 1, 1

        #xử lý mũ chẵn
        if rooted_z % 2 == 0 and rooted_t == 1:
            rooted_x, rooted_y = abs(rooted_x), abs(rooted_y)
        
        self.result = f"({rooted_x}/{rooted_y})^({rooted_z}/{rooted_t})"

def main():
    import sys
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        simplifier = Luythua(line)
        simplifier.special()
        print(simplifier.result)

if __name__ == "__main__":
    main()