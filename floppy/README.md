> # Floppy (1000 points, Reverse)
> 
> Our team of corn snakes formed an uneasy alliance with the office mice and slithered into the server room of Evil Robot Corp. They extracted an image of the VPN server before they had to retreat. Turns out sending a team of reptiles into a room whose main purpose is to keep its contents cold wasn’t the best idea.
> Can you figure out how this bootable floppy works and recover the secret data?

1. To get started, download and identify the file:
```
daMage@kalima:~/ctfs/squarectf2017/floppy$ file floppy.img
floppy.img: DOS/MBR boot sector
```
2. You can run it with qemu:
```
daMage@kalima:~/ctfs/squarectf2017/floppy$ qemu-system-i386 -fda floppy.img
```
And you see something like the following (enter abcd as the code):
```
Challenge: 51
Code?
ABCD
Nope
``
3. Then I took the route of static analysis and opened the floppy.img in hopper. Here is a relevant extract, which lead to solving the challenge:
```
00001403         mov        dword [ebp+var_48], edx
00001406         call       sub_1ba0						; call sha1?
0000140b         mov        word [ebp+var_22], ax
0000140f         movzx      ecx, word [ebp+var_1C]
00001413         movzx      edx, word [ebp+var_22]
00001417         cmp        ecx, edx						; compare results
00001419         jne        loc_1456						; if no match, jump to "Nope" => binary patch to show flag

0000141f         mov        eax, dword [ebp+var_28]
00001422         lea        ecx, dword [eax-0x120e+sub_2760+1583]               ; "flag-"
00001428         mov        dword [esp+0x68+var_68], ecx                        ; argument #1 for method write_to_stdout-0x14c0
0000142b         call       write_to_stdout-0x14c0
00001430         mov        eax, dword [ebp+var_28]
00001433         lea        ecx, dword [eax-0x120e+sub_2760+1624]               ; 0x2db8
00001439         mov        edx, 0x8
0000143e         mov        dword [esp+0x68+var_68], ecx                        ; argument #1 for method sub_1510
00001441         mov        dword [esp+0x68+var_64], 0x8                        ; argument #2 for method sub_1510
00001449         mov        dword [ebp+var_4C], edx
0000144c         call       sub_1510
00001451         jmp        loc_1467

             loc_1456:
00001456         mov        eax, dword [ebp+var_28]                             ; CODE XREF=sub_1200+537
00001459         lea        ecx, dword [eax-0x120e+sub_2760+1589]               ; "Nope"
0000145f         mov        dword [esp+0x68+var_68], ecx                        ; argument #1 for method write_to_stdout-0x14c0
00001462         call       write_to_stdout-0x14c0
```
4. At the offset 0x1419 we see a conditional jump to writing "Nope". Let's see what happens if I modify the code in such a way, that it'll always execute the branch, where "flag-" is printed.
5. Open the file in a hex editor and look for hex values `0F 85 37 00 00 00` and replace them with NOPs `90 90 90 90 90 90`
6. Re-Run the floppy with qemu, and you see something like:
```
Challenge: 58
Code?
ABCD
flag-774016D84709CB94
```
7. The output is accepted as the solution!
