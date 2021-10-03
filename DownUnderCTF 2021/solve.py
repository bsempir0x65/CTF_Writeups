#!/usr/bin/python3

from pwn import *
from pwnlib.gdb import binary
from six import int2byte
import codecs
#yeah our dev env adds imports automatically for us. Increased attack vector intended. Thank you

io = remote('pwn-2021.duc.tf', 31905)
#io.sendline("\n")
test = io.recvuntil("...")

print(test)

io.sendline(" ")

test = io.recvuntil("1+1=?")

print(test)

io.sendline("2")

test = io.recvline()

print(test)

test = io.recvline()

print(test)

test = io.recvuntil(": ")

print(test)

test = io.recvline()

print(test[:-1])

hexvar = int(test[:-1],0)

print(hexvar)

hexvar2 = str(hexvar)

print(hexvar2)

io.sendline(hexvar2)

test = io.recvuntil(": ")

print(test)

test = io.recvline()

print(test[:-1])

hexascii = (test[:-1]).decode("ascii")

print(hexascii)

hexasciibyte = bytes.fromhex(hexascii)

print(hexasciibyte)

hexascii_string = hexasciibyte.decode("ASCII")

print(hexascii_string)

io.sendline(hexascii_string)

test = io.recvuntil(": ")

print(test)

test = io.recvline()

print(test[:-1])

url = urldecode(test[:-1].decode("utf-8"))

print(url)

io.sendline(url)

test = io.recvuntil(": ")

print(test)

test = io.recvline()

print(test[:-1])

varbase64 = b64d(test[:-1].decode("utf-8"))

print (varbase64)

io.sendline(varbase64)

test = io.recvuntil(": ")

print(test)

test = io.recvline()

print(test[:-1])

varbase64encode = b64e(test[:-1])

print(varbase64encode)

io.sendline(varbase64encode)

test = io.recvuntil(": ")

print(test)

test = io.recvline()

print(test[:-1])

rot13var = codecs.encode(test[:-1].decode("utf-8"), 'rot_13')

print(rot13var)

io.sendline(rot13var)

test = io.recvuntil(": ")

print(test)

test = io.recvline()

print(test[:-1])

rot13var2 = codecs.encode(test[:-1].decode("utf-8"), 'rot_13')

print(rot13var2)

io.sendline(rot13var2)

test = io.recvuntil(": ")

print(test)

test = io.recvline()

print(test[:-1])

bitvar = int(test[:-1],2)

print(bitvar)

io.sendline(str(bitvar))

test = io.recvuntil(": ")

print(test)

test = io.recvline()

print(test[:-1])

binvar = bin(int(test[:-1],0))

print(binvar)

io.sendline(binvar)

test = io.recvline()

print(test[:-1])

test = io.recvline()

print(test[:-1])

test = io.recvline()

print(test[:-1])

io.sendline("DUCTF")

test = io.recvuntil("}")

print(test)

test = io.recvline()

print(test[:-1])

