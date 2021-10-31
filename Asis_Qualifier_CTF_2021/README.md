# Disclaimer

This time we faced our first CTF which was a qualifier to find the top teams in da worldz. We know that it would be tuff and it was tuff. We only managed to crack one challenge and we were not even sure if we did it right, so happy to see other solutions also

# Factory

 <img src="factory" alt="factory" width="50%" height="50%">

We were presented with a binary and the hint :
> misco-graphy is the ratio of output to input!
The binary had a pdf header and was also able to be opened by libre office. The only word we saw in it was **Real-World Misco-graphy**. 

 <img src="factory_libre" alt="factory" width="50%" height="50%">
 
Cause this was also the hint in the Challenge description we started to google it. We only found unusful garbage like this [Misco-graphy](https://www.facebook.comMISCO.Refractometer/). So still no clue whats the deal with Misco-graphy but we were sure that we have something embeded in the file, cause thats the way our evilfriends hide whatever they want.
So we used binwalk to check if any other files based on their header were in the pdf. So we ran
```console
# binwalk factory.pdf

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PDF document, version: "1.5"
76            0x4C            Zlib compressed data, best compression
1506          0x5E2           Zlib compressed data, best compression
16311         0x3FB7          Zlib compressed data, best compression
24876         0x612C          Zlib compressed data, best compression
32901         0x8085          Zlib compressed data, best compression
49887         0xC2DF          Zlib compressed data, best compression
58998         0xE676          Zlib compressed data, best compression
67312         0x106F0         Zlib compressed data, best compression
74544         0x12330         Zlib compressed data, best compression
81977         0x14039         Zlib compressed data, best compression
82798         0x1436E         Zlib compressed data, best compression
83619         0x146A3         Zlib compressed data, best compression
84395         0x149AB         Zlib compressed data, best compression
85214         0x14CDE         Zlib compressed data, best compression
86033         0x15011         Zlib compressed data, best compression
86853         0x15345         Zlib compressed data, best compression
87673         0x15679         Zlib compressed data, best compression
88960         0x15B80         Zlib compressed data, best compression
91317         0x164B5         Zlib compressed data, best compression
91884         0x166EC         Zlib compressed data, default compression
93705         0x16E09         Zlib compressed data, default compression

```
So yeah there were definitly more insight so we let binwalk extract with -e everything and had a look into it. We found with a simple String search for **ASIS** that the first stream 0x4C was the only one matching.
So we opened the file in our favorite text editor (kidding just my favorite Text editor):

<img src="factory_text" alt="factory" width="50%" height="50%">

Based on the words we see here that probably it was an PDF in PDF, but no clue how to recover the header for that. Probably binwalk was not the right Tool to beginn with. Regardless we figured out that everything in the format [\(...\)] was part of the searched flag. Also based on the Welcome Flag we knew that the words must be linked together via _ . So we conculuded that empty brackets mean _ and after some text transformations we had:
**ASIS{PDF_1N_PDF_iZ_A_T4sK_fOR_fOreEnSic5_L0v3RS}**

We pasted it into the webside and voila we got our first and only challenge for the evening. We knew that there are better ways to solve this challenge, but many roads let to rome. Happy to see other Solutions to get an idea how data extraction with pdfs works in general. Cause would this be a real challenge we would not have had the hints that we are searching for a string with ASIS{..._..} and we did not had a valid secon pdf. But only 250 Teams had this solution at the end of the day so we were happy.

# Welcome

<img src="Welcome" alt="Welcome" width="50%" height="50%">

This was not really a challenge. You should just read the rules under [https://asisctf.com/rules](https://asisctf.com/rules) and we found at the end the flag:
**ASIS{W3lc0me_t0_The_ASIS_CTF_Mad3_w1th_L0ve}**
But the important part was that we knew now that all flags start with ASIS{ and the string inside the brackets are most likely connected with underscores. This was actually helpful for the only challenge we managed to finish.