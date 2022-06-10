# <a name="SEETF"></a>Welcome to a new Challenge

We went to a new Challenge from our friends the [Social Engineering Experts](https://ctftime.org/team/151372/). It was quite tough bt what do you expect from experts <g-emoji class="g-emoji" alias="tada" fallback-src="https://github.githubassets.com/images/icons/emoji/unicode/1f389.png">🎉</g-emoji>. So we tried our best and we were not that bad as before. So lets have a look into the easy challenges we managed to solve.

# <a name="babyreeee"></a>babyreeee

 <img src="https://raw.githubusercontent.com/bsempir0x65/CTF_Writeups/main/SEETF_CTF_2022/img/babyreeee.png" alt="Babyre" width="50%" height="50%">

So based on the description it seems to be a binary which just checks if we have the right flag. So we started to understand what this binary does by loading it into[ghidra](https://ghidra-sre.org/), which gave us already some nice insights:
Disclaimer: Never execute something you don't know. So maybe not the best habit to have. But what could possible go wrong

>  uStack44 = 0x5e; //more values loaded into the stack above
>  local_28 = 0x50;
>  uStack36 = 0x86;
>  uStack32 = 0x89;
>  uStack28 = 0x89;
>  local_18 = 0x48;
>  uStack20 = 0x4f;
>  uStack16 = 0x49;
>  uStack12 = 0xf1;
>  fgets(local_158,0x80,stdin); //here we get asked for our input
>  sVar4 = strlen(local_158); // gets the length of our input
>  if (sVar4 == 0x35) { // 0x35 in decimal is 53 , since we put \n as our input by pressing enter we are searching for a 52 length value 
>    puts("Good work! Your flag is the correct size.");
>    puts("On to the flag check itself...");
>    sVar4 = strlen(local_158);
>    uVar5 = 0;
>    do {
>      uVar6 = uVar5 & 0xffffffff;
>      if (sVar4 - 1 == uVar5) {
>        puts("Success! Go get your points, champ.");
>        return 0;
>      }
>      pcVar1 = local_158 + uVar5; // loads our input
>      puVar2 = local_d8 + uVar5; // loads a value from above
>      bVar3 = (byte)uVar5;
>      uVar5 = uVar5 + 1;
>    } while ((byte)*puVar2 == (byte)(*pcVar1 + 0x45U ^ bVar3)); // does a check if the input we gave after transformation is equal to the loaded value
>    printf("Flag check failed at index: %d",uVar6);
>  }
>  else {
>    printf("Flag wrong. Try again.");
>  }
>  return 1;
>}

- [x] Let's figure out what to do

So clever people have seem to have figured out how to convert (byte)(*pcVar1 + 0x45U ^ bVar3)) into a simple script and let it do the magic. But we used something different here:

>printf("Flag check failed at index: %d",uVar6);

every time the input does not match the right value the program tells us what was the index value of the error. This piece of information can be used as a checker if the input is correct and if so move to the next value. This dramatically reduces the time you need for a brute-force attack. So that's what we did:

```python
#!/usr/bin/python

from pwn import *
from string import ascii_lowercase,ascii_uppercase,digits

checksolution = ("Success! Go get your points, champ.\n").encode('utf-8')

elf = ELF('./rev_babyreeee')

#We know that the flag starts with SEE{ and that the flag is in the format SEE{[ -~]+} plus ascii signs
current_flag = "SEE{" 
old_flag = ""
index = 4
checklist = ascii_uppercase + ascii_lowercase + digits + "_}" 

while current_flag != old_flag:
    missingvar = 51 - len(current_flag) #this is the amount of characters we have to find
    for c in checklist:

        io = elf.process()
        print(io.recvline(timeout=2))

        #this block here is to send the current sign of the flag to the binary and check the response
        sendvar = (current_flag + c + "A" * missingvar ).encode('utf-8')
        io.sendline(sendvar)
        print(sendvar)
        print(io.recvline(timeout=2))
        print(io.recvline(timeout=2))

        checkvar = io.recvall(timeout=2)
        checktest = ("Flag check failed at index: {}".format(index)).encode('utf-8')
        print(checkvar)
        print(checktest)

        #to check if we found the solution
        if checkvar == checksolution:
            current_flag = current_flag + c
            print(current_flag)
            old_flag = current_flag
            break
        else:
            print("next please")

        #check if we found the next correct character
        if checkvar != checktest:
            print(current_flag)
            old_flag = current_flag
            current_flag = current_flag + c
            break
        else:
            print("i said next")

        io.close()

        #was my error checker to ensure the script comes to an end
        if c == "}":
            print("shit")
            old_flag = current_flag
            break

    index += 1

print("welcome to the end")
print(current_flag)
```
- [x] Execute the exploit

So the FLAG is SEE{0n3_5m411_573p_81d215e8b81ae10f1c08168207fba396}

On our system it took not very long to brute force the flag so it was doable during the challenge. Its also not the nicest script in the world but it got the job done and maybe this was even an unintentional solution for the creators of the CTF. So if you're ever stuck on such issues you can always fall back to the old ways of cracking things ヾ( ͝° ͜ʖ͡°)ノ♪. Nevertheless it's a little neat challenge.

- [x] Do the happy dance

ヾ( ͝° ͜ʖ͡°)ノ♪ ヾ( ͝° ͜ʖ͡°)ノ♪ ヾ( ͝° ͜ʖ͡°)ノ♪

# <a name="BestSoftware"></a>Best Software

 <img src="https://raw.githubusercontent.com/bsempir0x65/CTF_Writeups/main/SEETF_CTF_2022/img/BestSoftware.png" alt="BestSoftware" width="50%" height="50%">

This time we need to help out our man Gelos to get the License key for the Best Software around. So at first glance we saw that we got an .exe file so we run "file" on it to see what it is exactly:

```console
└─$ file BestSoftware.exe 
BestSoftware.exe: PE32 executable (console) Intel 80386 Mono/.Net assembly, for MS Windows
```

Hah a good old .Net executable (ｰ ｰ;). Cause we did not have a Windows system around we needed to setup our Linux distro first to work on this. So we need:

- [ ] A way to execute the binary
- [ ] Inspect the PE 
- [ ] Get the Flag

So the easiest way probably would be to spin up windows for it but we found the following solutions for each problem:

- [x] A way to execute the binary -> install mono for it. We used the mono-complete based on the description to ensure that everything works [mono](https://www.mono-project.com/download/stable/) 
- [x] Inspect the PE -> We found a neat github project to bring ILSpy to Linux. Worked flawlessly [AvaloniaILSpy](https://github.com/icsharpcode/AvaloniaILSpy)  
- [ ] Get the Flag -> thats the next part

Okay so we had our setup so lets have a look into the file with ILSpy.

 <img src="https://raw.githubusercontent.com/bsempir0x65/CTF_Writeups/main/SEETF_CTF_2022/img/BestSoftware2.png" alt="BestSoftware" width="50%" height="50%">

Now we can see that the program is not too much of a hassle to go trough. In the main function we can see that we get asked the name and email we got from the challenge description and the searched license key. After that the Function CheckLicenseKey which takes our input and checks if the SHA256 of our name + "1_l0v3_CSh4rp" + email matches the one we used as a license key. With that knowledge we just need to create the SHA256 hash like in the function CalculateSHA256 and we get our flag. (Actually the flag is just the Licensekey so we do not actually run the program).

For that we just copied all the code we have into an online .Net compiler and instead of the check of the key we just write it out and voila. We called it the Keygenerator for the Best Software:
Disclaimer: Never execute to something you don't know. So maybe not the best habit to have. But what could possible go wrong?

```csharp
using System;
using System.Security.Cryptography;
using System.Text;

internal class Program
{
	private const string SECRET_KEY = "1_l0v3_CSh4rp";

	public static void Main()
	{
		Console.WriteLine("===== BestSoftware Keygenerator =====");
		Console.WriteLine("> Checking if you are from the police");
		Console.WriteLine("> (ㆁᴗㆁ✿)");
		Console.WriteLine("> (✿ㆁᴗㆁ)");
		Console.WriteLine("> Please enter your name...");
		Console.Write("> ");
		string name = Console.ReadLine();
		Console.WriteLine("> Please enter your email...");
		Console.Write("> ");
		string email = Console.ReadLine();
		Console.WriteLine("> Creating BestSoftware license...");
		
		string inputString = name + "1_l0v3_CSh4rp" + email;
		string value = CalculateSHA256(inputString);
		Console.WriteLine("> The key is " + value + " now go go");
		Console.WriteLine("> Press any key to run...");
        Console.ReadKey();
	}

	public static string CalculateSHA256(string inputString)
	{
		using SHA256 sHA = SHA256.Create();
		byte[] array = sHA.ComputeHash(Encoding.UTF8.GetBytes(inputString));
		StringBuilder stringBuilder = new StringBuilder();
		for (int i = 0; i < array.Length; i++)
		{
			stringBuilder.Append(array[i].ToString("X2"));
		}
		return stringBuilder.ToString();
	}
}
```

Sure, every great software should have also a great [Keygenerator](https://dotnetfiddle.net/rNaB1H). So with the given name and email the Flag is: SEE{28F313A48C1282DF95E07BCEF466D19517587BCAB4F7A78532FA54AC6708444E} . Again I think the reverse challenges are done by us not the way they should be.

- [x] Get the Flag 

we did it ヾ(๑ ³ㅿ³)ﾉ onto the next one

# <a name="Wayyang"></a>Wayyang

 <img src="https://raw.githubusercontent.com/bsempir0x65/CTF_Writeups/main/SEETF_CTF_2022/img/wayyang.png" alt="Wayyang" width="50%" height="50%">

So this time we got a little python script:

```python
#!/usr/local/bin/python
import os

FLAG_FILE = "FLAG"

def get_input() -> int:
    print('''                 ,#####,
                 #_   _#
                 |a` `a|
                 |  u  |            ________________________
                 \  =  /           |        WAYYANG         |
                 |\___/|           <     TERMINAL  v1.0     |
        ___ ____/:     :\____ ___  |________________________|
      .'   `.-===-\   /-===-.`   '.
     /      .-"""""-.-"""""-.      \
    /'             =:=             '\
  .'  ' .:    o   -=:=-   o    :. '  `.
  (.'   /'. '-.....-'-.....-' .'\   '.)
  /' ._/   ".     --:--     ."   \_. '\
 |  .'|      ".  ---:---  ."      |'.  |
 |  : |       |  ---:---  |       | :  |
  \ : |       |_____._____|       | : /
  /   (       |----|------|       )   \
 /... .|      |    |      |      |. ...\
|::::/'' jgs /     |       \     ''\::::|
'""""       /'    .L_      `\       """"'
           /'-.,__/` `\__..-'\
          ;      /     \      ;
          :     /       \     |
          |    /         \.   |
          |`../           |  ,/
          ( _ )           |  _)
          |   |           |   |
          |___|           \___|
          :===|            |==|
           \  /            |__|
           /\/\           /"""`8.__
           |oo|           \__.//___)
           |==|
           \__/''')
    print("What would you like to do today?")
    print("1. Weather")
    print("2. Time")
    print("3. Tiktok of the day")
    print("4. Read straits times")
    print("5. Get flag")
    print("6. Exit")

    choice = int(input(">> "))

    return choice


if __name__ == '__main__':
    choice = get_input()

    if choice == 1:
        print("CLEAR SKIES FOR HANDSOME MEN")
    elif choice == 2:
        print("IT'S ALWAYS SEXY TIME")
    elif choice == 3:
        print("https://www.tiktok.com/@benawad/video/7039054021797252399")
    elif choice == 4:
        filename = input("which news article you want babe :)   ")
        not_allowed = [char for char in FLAG_FILE]

        for char in filename:
            if char in not_allowed:
                print("NICE TRY. WAYYANG SEE YOU!!!!!")
                os.system(f"cat news.txt")
                exit()

        try:
            os.system(f"cat {eval(filename)}")
        except:
            pass
    elif choice == 5:
        print("NOT READY YET. MAYBE AFTER CTF????")
```

Here we can see that multiple options are offered to us and that all of them except "4" just prints some text or exits the session. So let's have a closer look onto number 4. We can see that another input question pops up. After that our input gets checked if any character was used which is part of FLAG_FILE which would be "F", "L", "A", "G" (if you ask yourself why it is this way just check [list-comprehensions](https://www.pythonforbeginners.com/basics/list-comprehensions-in-python) ). After that it checks our input we gave for the article if it has any of these characters and if you print out the news and that WAYYANG sees us. If it does not find a not allowed character it trys to execute "cat {eval(filename)}". So the idea is to bypass that check.

Honestly there is probably a real hacky way but what we just used are [bash macros](https://www.gnu.org/software/bash/manual/html_node/Miscellaneous-Commands.html). So we put as an input "*" to get any content of any file in the current directory. This gave us an error in the first place because of the way "input" makes an object. To circumvent that we just put in '*' and voila we had it.

```console
└─$ nc fun.chall.seetf.sg 50008
                 ,#####,
                 #_   _#
                 |a` `a|
                 |  u  |            ________________________
                 \  =  /           |        WAYYANG         |
                 |\___/|           <     TERMINAL  v1.0     |
        ___ ____/:     :\____ ___  |________________________|
      .'   `.-===-\   /-===-.`   '.
     /      .-"""""-.-"""""-.      \
    /'             =:=             '\
  .'  ' .:    o   -=:=-   o    :. '  `.
  (.'   /'. '-.....-'-.....-' .'\   '.)
  /' ._/   ".     --:--     ."   \_. '\
 |  .'|      ".  ---:---  ."      |'.  |
 |  : |       |  ---:---  |       | :  |
  \ : |       |_____._____|       | : /
  /   (       |----|------|       )   \
 /... .|      |    |      |      |. ...\
|::::/'' jgs /     |       \     ''\::::|
'""""       /'    .L_      `\       """"'
           /'-.,__/` `\__..-'\
          ;      /     \      ;
          :     /       \     |
          |    /         \.   |
          |`../           |  ,/
          ( _ )           |  _)
          |   |           |   |
          |___|           \___|
          :===|            |==|
           \  /            |__|
           /\/\           /"""`8.__
           |oo|           \__.//___)
           |==|
           \__/
What would you like to do today?
1. Weather
2. Time
3. Tiktok of the day
4. Read straits times
5. Get flag
6. Exit
>> 4
which news article you want babe :)   '*'
SEE{wayyang_as_a_service_621331e420c46e29cfde50f66ad184cc}WAYYANG DECLARED SEXIEST MAN ALIVE // <- the actual flag

SINGAPORE - In the latest edition of Mister Universe, Wayyang won again, surprising absolutely no one.
The judges were blown away by his awesome abdominals and stunned by his sublime sexiness.
When asked for his opinions on his latest win, Wayyang said nothing, choosing to smoulder into the distance.# /usr/bin/sh
python wayyang.pyHello there :D
#!/usr/local/bin/python
import os

FLAG_FILE = "FLAG"

def get_input() -> int:
    print('''                 ,#####,
                 #_   _#
                 |a` `a|
                 |  u  |            ________________________
                 \  =  /           |        WAYYANG         |
                 |\___/|           <     TERMINAL  v1.0     |
        ___ ____/:     :\____ ___  |________________________|
      .'   `.-===-\   /-===-.`   '.
     /      .-"""""-.-"""""-.      \\
    /'             =:=             '\\
  .'  ' .:    o   -=:=-   o    :. '  `.
  (.'   /'. '-.....-'-.....-' .'\   '.)
  /' ._/   ".     --:--     ."   \_. '\\
 |  .'|      ".  ---:---  ."      |'.  |
 |  : |       |  ---:---  |       | :  |
  \ : |       |_____._____|       | : /
  /   (       |----|------|       )   \\
 /... .|      |    |      |      |. ...\\
|::::/'' jgs /     |       \     ''\::::|
'""""       /'    .L_      `\       """"'
           /'-.,__/` `\__..-'\\
          ;      /     \      ;
          :     /       \     |
          |    /         \.   |
          |`../           |  ,/
          ( _ )           |  _)
          |   |           |   |
          |___|           \___|
          :===|            |==|
           \  /            |__|
           /\/\           /"""`8.__
           |oo|           \__.//___)
           |==|
           \__/''')
    print("What would you like to do today?")
    print("1. Weather")
    print("2. Time")
    print("3. Tiktok of the day")
    print("4. Read straits times")
    print("5. Get flag")
    print("6. Exit")

    choice = int(input(">> "))

    return choice


if __name__ == '__main__':
    choice = get_input()

    if choice == 1:
        print("CLEAR SKIES FOR HANDSOME MEN")
    elif choice == 2:
        print("IT'S ALWAYS SEXY TIME")
    elif choice == 3:
        print("https://www.tiktok.com/@benawad/video/7039054021797252399")
    elif choice == 4:
        filename = input("which news article you want babe :)   ")
        not_allowed = [char for char in FLAG_FILE]

        for char in filename:
            if char in not_allowed:
                print("NICE TRY. WAYYANG SEE YOU!!!!!")
                os.system(f"cat news")
                exit()

        try:
            os.system(f"cat {eval(filename)}")
        except:
            pass
    elif choice == 5:
        print("NOT READY YET. MAYBE AFTER CTF????")
                                               
```

Ofcourse we had some gubberish here but heh the assumption that the file is in the same directory worked and we probably have the shortest input solution (((o(*°▽°*)o))).
Flag: SEE{wayyang_as_a_service_621331e420c46e29cfde50f66ad184cc}

Buja already 3 down.

# <a name="angryzeyo2001"></a>angryzeyo2001

 <img src="https://raw.githubusercontent.com/bsempir0x65/CTF_Writeups/main/SEETF_CTF_2022/img/angryzeyu2001.png" alt="angryzeyu2001" width="50%" height="50%">

So based on the text we need to help to get a paycheck back ??? （￣ε￣） . So we downloaded the attached files and we got a folder with the pieces of the paycheck. It was 1219 jpegs all named with xxx.xxx.jpg and 10x10 pixel big. Based on these facts we assumed that we need to order the jpges and make one picture of it again.

We also assumed that the first part of the name would be the x coordinate of the small pic and the second one the y coordinate. With no clue how to make image magic we started googling around and found a tool called imagemagick. It also has a nice Feature called [Montage](https://imagemagick.org/Usage/montage/). It took us quite some time to figure out how to even use the tool and we had a little brain issue that we kept mixing x and y coordinates. So we only give you the important parts we found which you need to understand the solution

1. Based on the names and the amount of files the result picture should have 530x220 pixels. This is based on the fact that one picture is 10x10 and the naming we saw. Having this in mind this means the tile operator should be 53x22
2. We looked into one picture and we don't need any additional borders. Per default a border of 10 pixels is set by imagemagick. So we set it to +0+0.
3. Same idea is for the background. We don't need one so none was the choice.
4. The input imagemagick uses is based on the list given by bash. The files were sorted based on the x coordinate starting with 000. But Imagemagick adds picture to the right of the current picture until the column is full. After that it adds the column under the current one. But the list we get starts therefor on the bottom left instead of the top left we need. So we have to solutions. 
    * Either rotate the input images 90 degree or
    * sort the list based on the y coordinate starting with the top.

So having this in mind we had as a first solution:

```console
./magick montage -tile 53x23 -geometry +0+0 -background none pieces/*.220.jpg pieces/*.210.jpg pieces/*.200.jpg pieces/*.190.jpg pieces/*.180.jpg pieces/*.170.jpg pieces/*.160.jpg pieces/*.150.jpg pieces/*.140.jpg pieces/*.130.jpg pieces/*.120.jpg pieces/*.110.jpg pieces/*.100.jpg pieces/*.090.jpg pieces/*.080.jpg pieces/*.070.jpg pieces/*.060.jpg pieces/*.050.jpg pieces/*.040.jpg pieces/*.030.jpg pieces/*.020.jpg pieces/*.010.jpg pieces/*.000.jpg test.jpg
```

Which is kind of ugly as a one liner. After some time we also realized that:

```console
./magick montage -tile 23x53 -geometry +0+0 -background none -rotate 90 pieces/*.jpg flag.jpg
./magick convert -rotate 270 flag.jpg
```

Works perfectly the same and is a bit more elegant.

 <img src="https://raw.githubusercontent.com/bsempir0x65/CTF_Writeups/main/SEETF_CTF_2022/img/flag.jpg" alt="flag" width="50%" height="50%">

Weirdly the result seem still not to be perfect. But good enough to read the actual flag: SEE{boss_aint_too_happy_bout_me_9379c958d872435} 

Not sure what went wrong but if you read the other write ups from us then you see that we aim for good enough and not perfect (๑˃ᴗ˂)ﻭ

# <a name="sniffedtraffic"></a>sniffedtraffic

 <img src="https://raw.githubusercontent.com/bsempir0x65/CTF_Writeups/main/SEETF_CTF_2022/img/sniffedtraffic.png" alt="sniffedtraffic" width="50%" height="50%">

This time we got a nice pcap file to start wireshark up. When we first opened the file we saw over 4K packages ... . So lots of stuff to look into.
So we went first to the export options to see if any useful files are there based on the description that a file was downloaded via File -> Export Objects -> HTTP

 <img src="https://raw.githubusercontent.com/bsempir0x65/CTF_Writeups/main/SEETF_CTF_2022/img/sniffedtraffic2.png" alt="sniffedtraffic2" width="50%" height="50%">

Well well what do we see here ? a thingamajig.zip ( ͡ಠ ʖ̯ ͡ಠ) ROFL . Good start but when we tried to unzip it we were asked for a password. Since this is considered as an easy task we thought lets go trough the tcp streams and see if something is there.

 <img src="https://raw.githubusercontent.com/bsempir0x65/CTF_Writeups/main/SEETF_CTF_2022/img/sniffedtraffic3.png" alt="sniffedtraffic3" width="50%" height="50%">

Oho Passwords in clear text with a reference to [hunter2](https://knowyourmeme.com/memes/hunter2), we see what you did there. Okay once we had that a stuff file.

```console
└─$ file stuff_save      
stuff_save: data
```

Hmm so just data. When we looked into the file via a text editor you can see that the strings flag.txt are visible. Since unzip has not worked on it we just used foremost to see if it finds something.

```console
└─$ cat audit.txt                                                     
Foremost version 1.5.7 by Jesse Kornblum, Kris Kendall, and Nick Mikus
Audit File

Foremost started at Fri Jun  3 22:37:24 2022
Invocation: foremost stuff_save 
Output directory: /home/kali/CTF/CTF/SEETF_CTF_2022/forensics_sniffed_traffic/output
Configuration file: /etc/foremost.conf
------------------------------------------------------------------
File: stuff_save
Start: Fri Jun  3 22:37:24 2022
Length: 3 KB (3249 bytes)
 
Num      Name (bs=512)         Size      File Offset     Comment 

0:      00000001.zip          249 B            1000      
Finish: Fri Jun  3 22:37:24 2022

1 FILES EXTRACTED

zip:= 1
------------------------------------------------------------------
```

We are on something, let the hunt begin hunter2. Another zip again with a password. No further hints were found in the pcap so we tried good old brute forcing. For that we used [fcrackzip](https://www.kali.org/tools/fcrackzip/). We used the good old rockyoutxt wordlist and directly had luck:

```console
└─$ fcrackzip -u -D -p /usr/share/wordlists/rockyou.txt 00000001.zip                                                   130 ⨯


PASSWORD FOUND!!!!: pw == john
```

With that we could unzip again and got the flag.txt with the Flag: SEE{w1r35haRk_d0dod0_4c87be4cd5e37eb1e9a676e110fe59e3}

It was a tedious task to find all these small steps but thats what the call brain fucking ( ͡~ ͜ʖ ͡~). If you did not got all small steps don't be sad it was tuff in our opinion too.

# <a name="regex101"></a>regex101

 <img src="https://raw.githubusercontent.com/bsempir0x65/CTF_Writeups/main/SEETF_CTF_2022/img/regex101.png" alt="regex101" width="50%" height="50%">

This was actual one of the challenges which did not really had to do something with hacking. This was more or less a training task to recognize that being able to use regex expressions can be crucial. Based on the name of the challenge we thought this was a hint to use the side [regex101](https://regex101.com/) so that what we did. So we cat the attached file to have all 2999 and copied them into regex101.

 <img src="https://raw.githubusercontent.com/bsempir0x65/CTF_Writeups/main/SEETF_CTF_2022/img/regex101_1.png" alt="regex101" width="50%" height="50%">

As you can see in the Screenshot we already have only one match with the regex \[A-Z\]\{5\}\[1-9\]\{5\}\[A-Z\]\{6\} which brings us the flag SEE{RGSXG13841KLWIUO}. On the right side you also have a nice explanation why this regex matches and what the single parts do. Play around a bit with it and use the References or the regex quiz in the left side to improve your regex skills.

# <a name="Conclusion"></a>Conclusion

We had a lot of fun with these challenges and were also able to solve the one or the other ＠＾▽＾＠. We also were one of the lucky raffle winner thanks for that too. Overall also quite hard challenges so a good mix and we see but if time allows it we would be back 2023 again.