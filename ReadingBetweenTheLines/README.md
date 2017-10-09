# Reading between the lines (100 points, Forensics)
Find the secret in the archive

>
> Evil Robot Corp accidently made their S3 bucket public and we were able to
> grab this backup archive before we were kicked out. We think there might be a
> secret in here, but we can't find it. Can you help us?
> https://cdn.squarectf.com/challenges/reading-between-the-lines.zip
> 

First things first, we extract the .zip file and have a look at its content.

```
$ unzip -d reading-between-the-lines reading-between-the-lines.zip 
Archive:  reading-between-the-lines.zip
  inflating: reading-between-the-lines/2017-07-23 12.38.54.jpg  
  inflating: reading-between-the-lines/2017-07-31 22.07.45.jpg  
  inflating: reading-between-the-lines/2017-08-09 09.58.30.jpg
```

The three files are all cats, not quite what we are looking for...

But judging by the title of the level there might be more to
it than what we can imediately see. A first thought is that 
perhaps the .zip file is more than just a .zip file?

Using binwalk we find that the file, altough not being more than a 
zip archive, it contains an additional zip archive file entry:

```
$ binwalk -e reading-between-the-lines.zip

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             Zip archive data, at least v2.0 to extract, name: 2017-07-23 12.38.54.jpg
1964934       0x1DFB86        Zip archive data, at least v2.0 to extract, name: 2017-07-31 22.07.45.jpg
3642492       0x37947C        Zip archive data, at least v2.0 to extract, name: 2017-08-09 09.58.30.jpg
5762609       0x57EE31        Zip archive data, at least v2.0 to extract, name: 2017-08-12 15.05.06.jpg
5853842       0x595292        End of Zip archive, footer length: 22
```

The new file that binwalk discovers for us, 2017-08-12 15.05.06.jpg, 
contains the flag:

![2017-08-12 15.05.06.jpg](2017-08-12%2015.05.06.jpg)

flag: `flag-a14ad96e767617586f7158353c25f7b5`
