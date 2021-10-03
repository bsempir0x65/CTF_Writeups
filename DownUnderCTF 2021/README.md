## General Skills Quiz

 <img src="https://raw.githubusercontent.com/bsempir0x65/CTF_Writeups/main/DownUnderCTF%202021/General%20Skills%20Quiz.JPG" alt="General Skills Quiz" width="50%" height="50%">

 As with every Challenge you face in live you start at the beginning. Therefor we came up with the following plan:

- [ ] Figure out what to do
- [ ] Execute the exploit
- [ ] Drink something :tada:

According to the hint we shall answer some easy questions so we started a netcat session as described and see what happens.
Disclaimer: Never connect to something you don't know. So maybe not the best habbit to have. But what could possible go wrong :au:

After realizing it doesn't download a virus directly we started the game manually. We managed to reach step 4 before the connection got closed. We received:

> Welcome to the DUCTF Classroom! Cyber School is now in session!
> Press enter when you are ready to start your 30 seconds timer for the quiz... 
> Woops the time is always ticking...
> Answer this maths question: 1+1=?
> 2
> Well I see you are not a bludger then.
> 
> Decode this hex string and provide me the original number (base 10): 0xde
> 222
> You're better than a dog's breakfast at least.
> 
> Decode this hex string and provide me the original ASCII letter: 4d
> M
> Come on this isn't hard yakka
> 
> Decode this URL encoded string and provide me the original ASCII symbols: %21%2A%2B

After playing the games a few more times, we realized that:
* The timer at the beginning was no joke \(Yes we were sure that we don't drop the connection on our side\)
* The given values were randomly generated
* Manually solving the task is not humanly possible and our mate Kratos was not available <img src="https://upload.wikimedia.org/wikipedia/en/6/60/Kratos_PS4.jpg" alt="Kratos" width="4%" height="4%">

Now we thought the goal is to answer all questions to get the flag. So we needed someone who is smarter and faster than we are and since kratos was still not available <audio controls> <source src="https://upload.wikimedia.org/wikipedia/commons/3/35/Sad_Trombone-Joe_Lamb-665429450.ogg" type="audio/ogg">Your browser does not support the audio element.</audio>
we settled for the next best thing.  <g-emoji class="g-emoji" alias="computer" fallback-src="https://github.githubassets.com/images/icons/emoji/unicode/1f4bb.png">💻</g-emoji>

But First let us to the best thing:

- [x] Figure out what to do

Fells so good to cross things from lists, i mean to complete the first step.

So based on our google researches and experience with other ctf writeups from the past, we decided to use our favorite :snake: called Py-thron and the frame work [pwntools](https://docs.pwntools.com/en/stable/) Note: pwntools is <u>not</u> installed by default in kali

```python
#!/usr/bin/python3

from pwn import *
```
<b>Find the full script under solve.py</b>

We found as always all our answers on github to get started with pwntools [tutorial](https://github.com/Gallopsled/pwntools-tutorial/blob/master/tubes.md) to initialize a session and get a basic understanding how the framework works. So let us extend the script.
```python
io = remote('pwn-2021.duc.tf', 31905)
```
Based on the first trys we saw that every instruction ends with a ":" followed by the variable to work on. To reflect this behaviour we filtered for the variable by doing this:
```python
test = io.recvuntil(": ")

print(test)

test = io.recvline()

print(test[:-1])
```
Note: Yes we used a lot of prints cause no one told us that there is an interactive command for the remote object.

At this stage we were able to receive the messages from the server so our structure for sending messages is:
```python
io.sendline(variable) 
```
With this toolkit we were able to play the game via the script and could start to get the next questions. But before that please have a look into the code snipet for the initial steps (Yes we like our work):
```python
#answer for Answer this maths question: 1+1=?
io.sendline("2")
#Decode this hex string and provide me the original number (base 10):
hexvar = int(test[:-1],0)
print(hexvar)
hexvar2 = str(hexvar)
print(hexvar2)
io.sendline(hexvar2)
#decode this hex string and provide me the original ASCII letter:
hexascii = (test[:-1]).decode("ascii")
print(hexascii)
hexasciibyte = bytes.fromhex(hexascii)
print(hexasciibyte)
hexascii_string = hexasciibyte.decode("ASCII") #Yes nested functions are not our friends thank you, LOL
print(hexascii_string)
io.sendline(hexascii_string)
#Decode this URL encoded string and provide me the original ASCII symbols: 
url = urldecode(test[:-1].decode("utf-8"))
print(url)
io.sendline(url)
```
So finally we reached our first new questions.
```python
#Decode this base64 string and provide me the plaintext: "
varbase64 = b64d(test[:-1].decode("utf-8"))
print (varbase64)
io.sendline(varbase64)
#Encode this plaintext string and provide me the Base64:
varbase64encode = b64e(test[:-1])
print(varbase64encode)
io.sendline(varbase64encode)
#Decode this rot13 string and provide me the plaintext:
rot13var = codecs.encode(test[:-1].decode("utf-8"), 'rot_13')
print(rot13var)
io.sendline(rot13var)
#Encode this plaintext string and provide me the ROT13 equilavent:
rot13var2 = codecs.encode(test[:-1].decode("utf-8"), 'rot_13') #Listen and repeat, cause the alphabet i use has 26 characters
print(rot13var2)
io.sendline(rot13var2)
#Decode this binary string and provide me the original number (base 10):
bitvar = int(test[:-1],2) #Beware binary use as a base log2
print(bitvar)
io.sendline(str(bitvar))
#Encode this number and provide me the binary equivalent:
binvar = bin(int(test[:-1],0))
print(binvar)
io.sendline(binvar)
#Final Question, what is the best CTF competition in the universe?
io.sendline("DUCTF") #Not sure if you just could use any string
```
- [x] Execute the exploit

Another one from the list. :satisfied: So this time our exploit script did not printed out the next step so we were wondering what happend. Probably we reached the end of the journey and instead of searching for the next colon we searched for the end of a flag with }.
```python
test = io.recvuntil("}")
print(test)
```
With this last snippet we finally got our flag. Wohoo 2 hours later and a crash course in python + pwntools brought as our nice flag:
Bloody Ripper! Here is the grand prize!\n\n\n\n   .^.\n  (( ))\n   |#|_______________________________\n   |#||##############################|\n   |#||##############################|\n   |#||##############################|\n   |#||##############################|\n   |#||########DOWNUNDERCTF##########|\n   |#||########(DUCTF 2021)##########|\n   |#||##############################|\n   |#||##############################|\n   |#||##############################|\n   |#||##############################|\n   |#|'------------------------------'\n   |#|\n   |#|\n   |#|\n   |#|\n   |#|\n   |#|\n   |#|\n   |#|\n   |#|\n   |#|\n   |#|\n   |#|  DUCTF{you_aced_the_quiz!_have_a_gold_star_champion}
Hmmmmm yeah we still did not know that there was an interactive command. So here is the nice version:
Bloody Ripper! Here is the grand prize!



   .^.
  (( ))
   |#|_______________________________
   |#||##############################|
   |#||##############################|
   |#||##############################|
   |#||##############################|
   |#||########DOWNUNDERCTF##########|
   |#||########(DUCTF 2021)##########|
   |#||##############################|
   |#||##############################|
   |#||##############################|
   |#||##############################|
   |#|'------------------------------'
   |#|
   |#|
   |#|
   |#|
   |#|
   |#|
   |#|
   |#|
   |#|
   |#|
   |#|
   |#|  DUCTF{you_aced_the_quiz!_have_a_gold_star_champion}"

- [x] Drink something :tada:

## Task2


Hint:

Text.....

## Task3


Hint:

Text.....

## Task4


Hint:

Text.....

## Task5


Hint:

Text.....

## Task6


Hint:

Text.....

---