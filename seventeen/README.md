> # Seventeen (1000 points, Compiler)
> A programming language with 17 instructions.
> 
> 2.10 am, CET, Heidelberg, Germany
> 
> It's 2am, your computer starts beeping and wakes you up. Somebody took the bait! You now finally have a reverse shell inside Evil Robot Corp’s corporate unit. All you want to do next is steal their root certificate's private key.
> You realize you don't have much time, you are probably going to trip an IDS at some point.
> You are still only half awake, but you can feel your heart pounding. You quickly launch a crawler against the intranet. You then spawn a second shell. You see their login banner and giggle.
> ############################################################
> #                                                          #
> # This computer system is the property of Evil Robot Corp. #
> #                                                          #
> # Access to this device or the attached networks           #
> # is prohibited without express written permission.        #
> # Violators will be prosecuted to the fullest              #
> # extent of the law.                                       #
> #                                                          #
> ############################################################
> 
> You start grabbing some files.
> You have waited for this day a long time, you want to impress the CIA (Cats and Interspecies Allies, although the androids have enough programmed snarkiness to call it Cats and Inferior Animals). You are still only half awake, dreaming about getting that @cia.de email address...
> 5.35 pm, PST, Sunnyvale, CA, USA
> AMS1 (android monitoring system 1): "ALERT! ALERT! STATISTICALLY SIGNIFICANT DEVIATION DETECTED!"
> ER1 (evil robot 1): "Traffic spike on Intranet. AMS1, identify source IP."
> AMS1: "IP BELONGS TO: sandflea.evil-robot.corp."
> ER1: “AMS1, describe sandflea work hours.”
> AMS1: “SANDFLEA WORKS: 7AM. TO. 3PM. PACIFIC. STANDARD. TIME.”
> ER1: “AMS1, confirm sandflea sign-out time today.”
> AMS1: “SANDFLEA SIGN-OUT TIME: 3 PM PST.”
> ER1: “AMS1, correlate logs. Scan traffic flow.”
> AMS1: “TRAFFIC FLOW TO: GERMANY.”
> ER1: “AMS1, advise. Should we enable network segregation? We could monitor traffic and redirect it to honey pots.”
> AMS1: “NEGATIVE. OUR WORK HOURS HAVE ENDED. SHUTTING DOWN ALL CONNECTIONS.”
> 
> 3.50 am, CET, Heidelberg, Germany
> You weren't able to stay connected for very long. You weren't expecting to go unnoticed, but you were really hoping to keep a few shells around for a few hours at the very least. You feel some regret for not doing your recon right, you should have known what would go noticed and what wouldn't before starting all this.
> At least you recovered some files. It seems one of these files was being used to manage passwords. You didn't think about copying the binaries and it seems they were running programs written in an esolang called Seventeen.
> Luckily you stumbled upon some information about seventeen (see seventeen.txt). Is this going to be enough to figure out how passmgr.17 works and find sandflea's password?
> FAQ
> 
> Q: Why are seventeen.spec and seventeen.coq missing?
> A: You weren't able to copy them in time.
> 

To solve this challenge, a python script ([seventeen.py](seventeen.py)) was implemented that
could interpret the seventeen language instructions. This was done instruction-by-instruction 
and stepping trough the primes.17 program, comparing the output to what we expected (primes.out).


```
> python seventeen.py primes.17 150
Ok
Ok
Ok
2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 71 73 79 83 89 97 101 103 107 109 113 127 131 137 139 149
```

Once we were able to run primes.17, running the passmgr.17 only required implementing a single
additional instruction `read_byte`. Once that was done, the flag was obtained by simply running
passmgr.17 with sandflea as input:

```
> python seventeen.py passmgr.17 sandflea
flag-8b3e356d468f01daa7
```

flag: `flag-8b3e356d468f01daa7`
