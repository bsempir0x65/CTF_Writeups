# <a name="DUCTF"></a>DUCTF

We came back to DUCTF once again, cause we had good memorys last time about it and it fitted our time schedule. We also try to write some solutions down for the Contest but we know that we will probably only repeat what you can already find on the excelent [github](https://github.com/DownUnderCTF/Challenges_2023_Public) from DUCTF. So hope one or two like our version even it is kinda late to publish. 

P.S: Just that you know we are so late that we can even make screenshots of the original challenges anymore (≧▽≦)

# <a name="blinkybill"></a>blinkybill

 <img src="https://raw.githubusercontent.com/bsempir0x65/CTF_Writeups/main/DownUnderCTF_2023/img/blinkybill_1.png" alt="Blinky Bill" width="50%" height="50%">

In this challenge we got a sound file provided which i think has the theme song of a kids tv show called "The Adventures of Blinky Bill" and some weird peeping noises when you hear it. In the past we had similar tasks, so we assumed that the peeping noise is some morse code. So together with [audacity](https://www.audacityteam.org/) we tried to filter out the morse code.

 <img src="https://raw.githubusercontent.com/bsempir0x65/CTF_Writeups/main/DownUnderCTF_2023/img/blinkybill_2.png" alt="Blinky Bill" width="50%" height="50%">

 <img src="https://raw.githubusercontent.com/bsempir0x65/CTF_Writeups/main/DownUnderCTF_2023/img/blinkybill_3.png" alt="Blinky Bill" width="50%" height="50%">

 So to figure out where you need to cut out Frequenz we used the frequenzanalysis tool of audacity at around 752HZ. We then tried to use an online tool to analyis the different character but we failed. Probably our resulting sound file was not good enough so we did the rest by hand and used [cyberchef](https://gchq.github.io/CyberChef/#recipe=From_Morse_Code('Space','Line%20feed')&input=LS4uLgouLS4KLi4KLS4KLS0uCi0uLi4KLi0KLS4tLgotLi0KLQouLi4uCi4KLQouLS4KLgouCi4uLg) to make some words out of it for us:

 <img src="https://raw.githubusercontent.com/bsempir0x65/CTF_Writeups/main/DownUnderCTF_2023/img/blinkybill_4.png" alt="Blinky Bill" width="50%" height="50%">

> -...
> .-.
> ..
> -.
> --.
> -...
> .-
> -.-.
> -.-
> -
> ....
> .
> -
> .-.
> .
> .
> ...

Flag: DUCTF{BRINGBACKTHETREES} 

Nice little challenge in which we had some hassleing with the tools

# <a name="bridgetsback"></a>bridgetsback

 <img src="https://raw.githubusercontent.com/bsempir0x65/CTF_Writeups/main/DownUnderCTF_2023/img/bridgetsback_1.png" alt="bridgets back" width="50%" height="50%">

In this challenge we did got a pic of a bridge and the question where this pic was taken. So for this you can either ask chatgpt or [google lens](https://www.google.com/imghp?hl=en)

 <img src="https://raw.githubusercontent.com/bsempir0x65/CTF_Writeups/main/DownUnderCTF_2023/img/bridgetsback_2.png" alt="bridgets back" width="50%" height="50%">

to tell you that it is a pic of the golden gate bridge. For us it was really tuff to say from which site the pic was taken but somehow ChatGPT knew it was taken from the north side of the bridge cause you can see San francisco in it (?!?). When then recognised that you can see a curve of the road so it must be taken behind that. So we checked in [google maps](https://www.google.com/maps/place/Golden+Gate+Bridge/@37.8323174,-122.4806974,16z/data=!4m6!3m5!1s0x808586deffffffc3:0xcded139783705509!8m2!3d37.8199286!4d-122.4782551!16zL20vMDM1cDM?entry=ttu) for some places which might fit for a traveler. We found a place called H. Dana Bowers Rest Area & Vista Point – Northbound and tried it with the hints on how to put in the flag and voila ヽ(ヅ)ノ there we have it.

Flag: DUCTF{H._Dana_Bowers_Memorial_Vista_Point}

A nice little challenge actually.

# <a name="comeacroppa"></a>comeacroppa

 <img src="https://raw.githubusercontent.com/bsempir0x65/CTF_Writeups/main/DownUnderCTF_2023/img/comeacroppa_1.png" alt="bridgets back" width="50%" height="50%">

To be fair we had no clue what to do in a sensful way to solve this challenge. We are not familiar with the suburbs in australia and based on the pic we got we did not saw anything which might help us. We asked first ChatGPT which failed and just explains to us what it can see. DUUUHA so only things we already knew. So we tried google lens again.

 <img src="https://raw.githubusercontent.com/bsempir0x65/CTF_Writeups/main/DownUnderCTF_2023/img/comeacroppa_2.png" alt="bridgets back" width="50%" height="50%">

It focused then automatically its search on the House you can see on the right site of the pic and boom there is a pic on a [museums webpage](https://tours.maldonmuseum.com.au/index.php/mobile/walks/9#site.47) which looks like the same. It randomly had an address on it and we tried that as a flag.

Flag: DUCTF{Maldon} 

And it was correct. No clue what was the intended way but we take that without having any clue. I mean even the signs on the pic we had were not really on the google pic, but luckely no one else built such a house and put it on the net.