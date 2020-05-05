a = int(input('Enter the binary bits in a single string without spaces:  '))
reversed_bits = str(a)[::-1]
return_val = int(reversed_bits)
print(return_val)
print('\n',type(return_val))

class Solution:
    def reverseBits(self, n: int) -> int:
        return int(str(n)[::-1])

c = Solution()
value = c.reverseBits(a)
print("\nClass int",value)