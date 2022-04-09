import math
import random


def DecToBin(dec, length):
    """
    convert a decimal value to binary string, append 0s in the head to reach minimum length
    :param dec: original decimal value as an integer
    :param length: the minimum length of the output string
    :return: binary string
    """
    bin_str = bin(dec)[2:]
    while len(bin_str) < length:
        bin_str = '0' + bin_str
    return bin_str


class HammingBitProp:   #a hamming code have some properties
    def __init__(self):
        self.bin_index = '' #what is the index in binary, such as 0001, 0010
        self.isParity = False   #if this bit is a parity code
        self.ParityGroup = None #is it p1, p2? here is using the index of 1 as the group number


class HammingCode:
    def __init__(self, n):
        self.k = 1  #based on the encoding text length, set parity bit number
        while math.pow(2, self.k) < n + self.k + 1: #k is the number of parity code, also the number of checksums
            self.k += 1
        self.totalBit = int(math.pow(2, self.k)) - 1
        self.bits = []
        power = 0
        for i in range(1, self.totalBit + 1):   #from 1 to total bit count
            curr_bit = HammingBitProp() #initiate a new property class instance of hamming code
            curr_bit.bin_index = DecToBin(i, self.k)
            if i == math.pow(2, power): #when i is 2^0, 2^1, 2^2..., it means this is a parity bit.
                curr_bit.isParity = True
                curr_bit.ParityGroup = self.k - power - 1   #set the 1 bit position, then no need to recheck it again
                power += 1
            self.bits.append(curr_bit)  #this is in the reverse order, starting from right most to left

    def Encode(self, char):
        """
        convert a char to ASCII, and encode to its hamming code in binary string
        :param char: char
        :return: hamming code in ascii
        """
        ascii_dec = ord(char)
        ascii_bin = DecToBin(ascii_dec, 7)  #convert char to 7-bit string
        bin_list = list(ascii_bin)
        code_list = ['0'] * self.totalBit #placeholder for result
        for i in range(self.totalBit):
            bit_prop = self.bits[i]
            if not bit_prop.isParity and len(bin_list) > 0: #when this bit is not a parity code, put data bit on it
                code_list[i] = bin_list.pop()   #bit_prop is in the reverse order, so we pop the ascii from tail to head
        for p in range(self.k): #set the parity bit value. There are k parity codes. Each one must add up with itself data bit to make the sum even. There are k different parity code
            parity_position = 0
            odd = False
            for i in range(self.totalBit):
                bit_prop = self.bits[i]
                if bit_prop.isParity:
                    if bit_prop.ParityGroup == p:
                        parity_position = i
                else:
                    if bit_prop.bin_index[p] == '1' and code_list[i] == '1':
                        odd = not odd
            code_list[parity_position] = '1' if odd else '0'    #parity code is 1 when there are odd number of 1 in data bits
        encodes = ''
        for b in code_list:
            encodes = b + encodes
        return encodes

    def Decode(self, codings):
        """
        convert a hamming code in form of binary string back to a char in ascii. it will try to correct an error
        :param codings: binary string
        :return: char
        """
        if len(codings) > self.totalBit:
            print('the encoding is too long.')
            return 'ERROR'
        bin_list = list(codings)
        code_list = ['0'] * self.totalBit
        for i in range(len(bin_list)):
            code_list[i] = bin_list.pop()
        checksums = ''  #use checksum to detect which bit is wrong
        for p in range(self.k):
            curr_checksum_odd = False
            for i in range(self.totalBit):
                bit_prop = self.bits[i]
                if bit_prop.bin_index[p] == '1' and code_list[i] == '1':
                    curr_checksum_odd = not curr_checksum_odd
            checksums += '1' if curr_checksum_odd else '0'
        checksum_dec = int(checksums, 2)
        if checksum_dec != 0:   #checksum_dec is 0, means no error to correct. otherwise, it is the index which is wrong
            value = code_list[checksum_dec - 1]
            code_list[checksum_dec - 1] = '1' if value == '0' else '0'  #flip the value when it is wrong
        original_ascii_bin = '' #convert hamming code back to ascii in binary
        for i in range(self.totalBit):
            bit_prop = self.bits[i]
            if not bit_prop.isParity:   #remove parity code bits
                original_ascii_bin = code_list[i] + original_ascii_bin
        ascii_dec = int(original_ascii_bin, 2)
        ascii = chr(ascii_dec)
        return ascii


class Driver:
    def __init__(self):
        self.driver = HammingCode(7)

    def AddRandomError(self, binary_str, count):
        """
        AddRandomError introduce (count) number of bit error(s) in binary_str
        :param binary_str: original binary string
        :param count: number of bit errors
        :return: new binary string contains random errors
        """
        code = list(binary_str)
        length = len(binary_str)
        indexes = [*range(length)]
        errors = []
        for i in range(count):
            r = random.randint(0, len(indexes))
            i = indexes.pop(r)
            code[i] = '1' if code[i] == '0' else '0'
        return ''.join(code)

    def TestErrorCorrection(self):
        """
        use 'a' as an example to test if hamming code can correct 1-bit error and 2-bit error
        :return: no return
        """
        #when there is 1 error
        char = 'a'
        encodings = self.driver.Encode(char)
        oneError = self.AddRandomError(encodings, 1)
        decodeChar = self.driver.Decode(oneError)
        if char == decodeChar:
            print('Hamming code can correct 1 bit error.')
        else:
            print("Hamming code cannot correct 1 bit error.")
        #when there are 2 errors
        twoError = self.AddRandomError(encodings, 2)
        decodeChar = self.driver.Decode(twoError)
        if char == decodeChar:
            print('Hamming code can correct 2-bit error.')
        else:
            print('Hamming code cannot correct 2-bit error.')

    def EncodeString(self, input):
        """
        convert input string to be hamming code array
        :param input: string
        :return: array
        """
        arr = []
        for char in input:
            arr.append(self.driver.Encode(char))
        return arr

    def DecodeList(self, list):
        """
        convert array back to string
        :param list: input array
        :return: string
        """
        output = ''
        for bit in list:
            char = self.driver.Decode(bit)
            output += char
        return output


test = Driver()
test.TestErrorCorrection()
sample = """Oh praise Jehovah, all ye nations;
Laud him, all ye peoples.
For his lovingkindness is great toward us;
And the truth of Jehovah endureth for ever.
Praise ye Jehovah."""
encodings = test.EncodeString(sample)
print(encodings)
print(test.DecodeList(encodings))