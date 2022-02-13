# <a name="Journey begins"></a>Journey begins

So what do you do when you need some talented people break down some code. Asking would be a bit easy right ? So of course you set up a neat little platform and make a game out of it. Which brings us to [Decompetition v2.0](https://decompetition.io/), lets welcome our new challenge. This CTF is focused around reverse engineering with different programm languages as a base and a direct exchange between the target source binary and your own code via dissambled outputs. Cause we have no clue also no fear to dive in.

# <a name="Baby_c"></a>Baby_c

We started with the probably "easy" C challenge base on the name. Our plan was to 

- [ ] Figure out what the binary does
- [ ] Figure out what the different assemble statements would be in conjunction to the behaviour do
- [ ] Figure out how to programm in C

Based on the tip of the maker we uplouded the binary to [binary ninja](https://cloud.binary.ninja) and realized why to stop there. So we went ahead and also used [ghidra](https://ghidra-sre.org/) and [ida](https://hex-rays.com/ida-free/). Which showed us already interesting outputs.

 <img src="https://raw.githubusercontent.com/bsempir0x65/CTF_Writeups/main/Decompetition_CTF_2022/img/baby_c_ghidra.png" alt="Ghidra" width="50%" height="50%">

 <img src="https://raw.githubusercontent.com/bsempir0x65/CTF_Writeups/main/Decompetition_CTF_2022/img/baby_c_ninja.png" alt="Binary Ninja" width="50%" height="50%">

 <img src="https://raw.githubusercontent.com/bsempir0x65/CTF_Writeups/main/Decompetition_CTF_2022/img/baby_c_ida.png" alt="IDA" width="50%" height="50%">

As you can see we have slightly 3 different versions when we use the decompiler of each tool. You know what they say more tools = more fun. 
But back to our plan what does the programm do ?
Based on the outputs we have at the start a variable which is set to 1 and an endless loop until the the break signal is sent to the binary, we think. Next observation is that we have a check on __ctype_b_loc() with the value 0x2000 and if that is true it writes out the input it took to stdout or the console. If that is false depending on the first variable it either uses toupper on the input or tolower and set the original variable to 0. 
Cause we were not sure if we should uses imports or not, cause they were already given as the starter code, we decided to use the ida output as base cause it did not need any additional imports:
```C
#include <ctype.h>
#include <stdio.h>
int __cdecl main(int argc, const char **argv, const char **envp)
{
  FILE *v3; // rbx
  int v4; // eax
  int v5; // eax
  char v7; // [rsp+Bh] [rbp-15h]
  int c; // [rsp+Ch] [rbp-14h]

  v7 = 1; // counter variable
  while ( 1 )
  {
    c = getc(stdin);
    if ( c == -1 )
      break;
    if ( ((*__ctype_b_loc())[c] & 0x2000) != 0 ) //no clue what that is 
    {
      putc(c, _bss_start); // based on google search and the other decompiler _bss_start in this case == stdout
      v7 = 1;
    }
    else
    {
      v3 = _bss_start;
      if ( v7 )
      {
        v4 = toupper(c);
        putc(v4, v3);
        v7 = 0;
      }
      else
      {
        v5 = tolower(c);
        putc(v5, v3);
      }
    }
  }
  return 0;
}
```
So after that we were sure its not malicious code so we also just ran the code in our VM and did a little black box testing. Cause some parts were still unclear for us.
After that we saw that whatever input we give if the first character is from an alphabet and its lower case the output would have an upper case and all other characters would be just printed out and if its from an alphabet it would be lower case.
So for example:
```console
└─$ ./baby-c             
hello
Hello
WORLD
World
123bs
123bs
bs123
Bs123
empir0x65
Empir0x65

```
**Disclaimer: Never execute something you don't know or trust. We are usually just stupid and execute everything from CTFs**

- [X] Figure out what the binary does

We were now confident that we know what the programm does so lets dive in and see what we can achive with the nice outputs our dicompilers.
The first thing we did was some clean up of the original code to make it more readable for us, with some comments for you:
```C
#include <ctype.h>
#include <stdio.h>
int main() //int __cdecl main(int argc, const char **argv, const char **envp) no clue why it was there but we don't need any input to start the programm
{
  // FILE *v3; // rbx again no clue why its heres based on the ghidra output for the decompiler the stdout stream is some kind of bit stream which can be declared this way in C we think
  // int v4; // eax not used after clean up
  // int v5; // eax not used after clean up
  char runtime_counter; // char v7; // [rsp+Bh] [rbp-15h] renamed to understand the code better 
  int input_output; // int c; // [rsp+Ch] [rbp-14h] same here

  runtime_counter = 1; // counter variable
  while ( 1 )
  {
    input_output = getc(stdin);
    if ( input_output == -1 )
      break;
    if ( isalpha(input_output) == 0  ) // based on our understanding this would be the check for the character of the input if its part of an alphabet
    {
      putc(input_output, stdout); // _bss_start replaced with stdout
      runtime_counter = 1;
    }
    else
    {
      if ( runtime_counter )
      {
        putc(toupper(input_output), stdout); // made it a one liner to kick out v4 and v5
        runtime_counter = 0;
      }
      else
      {
        putc(tolower(input_output), stdout); // made it a one liner to kick out v4 and v5
      }
    }
  }
  return 0;
}
```
With this code we were already quite near to the searched original code or one of its variations. Only the isalpha check was wrong. Instead of a JNE instruction we had a JE. Also we relaized that our code always make the first character of the input uppercase regardless of its position. 
So probably ((*__ctype_b_loc())[c] & 0x2000) != 0 is the culprit. Based on some googling we found out that 
* 0x2000 is a check if the char is big or small == 0x2000 2 == is a alphabet char and any of the 0 are for upper 1 would be lower [stackoverflow](https://stackoverflow.com/questions/37702434/ctype-b-loc-what-is-its-purpose)
* != 0 check if true or false 0 means false [stackoverflow](https://stackoverflow.com/questions/14267081/difference-between-je-jne-and-jz-jnz)
Not sure if the first observations is right or wrong but it make sense that it is a lookup on a given list. And based on the second finding and this nice instructions manual [intel](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html) we found on page 1000 whatever that JE and JNE in this context means that we would need a check if something is not equal instead of if something is equal. 

- [X] Figure out what the different assemble statements would be in conjunction to the behaviour do

We did it Jonny.

So for testing we did exchanged the isalpha with isdigit but it check 800 instead of 2000 of that list. Until now we have no clue what (*__ctype_b_loc())[c] & 0x2000) was originally the right function but when we just use this we have a 100% Solution:
```C
#include <ctype.h>
#include <stdio.h>

int main() {
  // glhf
  char runtime_counter; // [rsp+Bh] [rbp-15h]
  int input_output; // [rsp+Ch] [rbp-14h]

  runtime_counter = 1;
  while ( 1 )
  {
    input_output = getc(stdin);
    if ( input_output == -1 )
      break;
    if ( ((*__ctype_b_loc())[input_output] & 0x2000) != 0  ) //isalpha(input_output) == 0
    {
      putc(input_output, stdout);
      runtime_counter = 1;
    }
    else
    {
      if ( runtime_counter )
      {
        putc(toupper(input_output), stdout);
        runtime_counter = 0;
      }
      else
      {
        putc(tolower(input_output), stdout);
      }
    }
  }
  return 0;
}
```
Also we saw that with that implementation it also worked for us if the second character is from an alphabet it would not be made to upper case. So no clue what is difference but you cant argue with that

 <img src="https://raw.githubusercontent.com/bsempir0x65/CTF_Writeups/main/Decompetition_CTF_2022/img/baby_c_result.png" alt="Result" width="50%" height="50%">

We did not managed to do the last point on the list 

- [ ] Figure out how to programm in C

But at least we got something which was more than we expected and with this little story we might help a student to understand the pleps a bit better.

# <a name="Baby_rust"></a>Baby_rust

The next challenge we tried was the rust one. Rust seems to be not the best language to start for reversing. So we loaded the binary again up in the different tools and got really weird outputs, at least for us.

 <img src="https://raw.githubusercontent.com/bsempir0x65/CTF_Writeups/main/Decompetition_CTF_2022/img/baby_rust_ghidra.png" alt="Ghidra" width="50%" height="50%">

Based on the result we concluded the following:
* Calls like this core::ptr::drop_in_place<std::env::Args>(local_c8); means that from the library core which has library ptr has function drop_in_place is loaded
* The disassemble did not helped cause we rarely touched rust in the past and you should have a basic understanding of the compiler for this
* Ohh and we have multiple functions to create ;-)
* We still don't have a clue if this programm is safe or not sooo dynamic analysis was not an option __Disclaimer: Never execute something you don't know or trust.__

So from what we recalled back then and the first assemble statements

  mov   \[rsp+0xf6\], 0
  mov   \[rsp+0xf7\], 0

2 variables should be there with value 0 and we have to have a function called step based on the dropdown menu of the webside.
So we came to the clever idea to sneak at least something by doing this:

```rust
// this is a dummy function to get something
fn step(lhs: u32, rhs: u32) -> () { 
  if lhs == 0 {
    println!("fizzbuzz");
  } else {
        println!("{}", rhs);
    }
}

fn main() {
    // Wait a minute, why are you walking backwards?
    let integer_1 = 0; // the two variables we need
    let integer_2 = 0;
    
    step(integer_1, integer_2); // the function call
    
    println!("{}", integer_1); // rust has a clever compiler so we needed to use the integer variables other wise it would be skipped
    println!("{}", integer_2);
}
```
With this we actually got 2% so better than nothing. Wuup Wuup. But yeah better check other Write ups for a complete solution.

 <img src="https://raw.githubusercontent.com/bsempir0x65/CTF_Writeups/main/Decompetition_CTF_2022/img/baby_rust_result.png" alt="result" width="50%" height="50%">

# <a name="Blaise"></a>Blaise

Cause we have no clue about C++ either, we thougt why not.
