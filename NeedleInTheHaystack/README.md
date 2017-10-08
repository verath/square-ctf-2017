# Needle in the haystack (500 points, Forensics)
Somewhere in this blob is the flag.

> We infiltrated Evil Robot Corp’s network and were able to get this partial
> data dump of one of their production hosts before their Android Monitoring
> Systems kicked us out. Can you do anything with it? We know they aren't
> good at developer best practices when doing app development.
> 
> https://cdn.squarectf.com/challenges/needle-in-the-haystack

We are given some file we don't really know what it is. Fortunately, binwalk can help us out:

```
$ binwalk needle-in-the-haystack 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
28672         0x7000          gzip compressed data, from Unix, last modified: 2017-08-12 19:24:07
167952        0x29010         HTML document header
168222        0x2911E         HTML document footer
256016        0x3E810         HTML document header
257469        0x3EDBD         HTML document footer
258064        0x3F010         HTML document header
259604        0x3F614         HTML document footer
260112        0x3F810         HTML document header
261635        0x3FE03         HTML document footer
301056        0x49800         Executable script, shebang: "/usr/bin/env ruby"
301058        0x49802         Unix path: /usr/bin/env ruby
303104        0x4A000         Executable script, shebang: "/usr/bin/env ruby"
303106        0x4A002         Unix path: /usr/bin/env ruby
305152        0x4A800         Executable script, shebang: "/usr/bin/env ruby"
305154        0x4A802         Unix path: /usr/bin/env ruby
307200        0x4B000         Executable script, shebang: "/usr/bin/env ruby"
307202        0x4B002         Unix path: /usr/bin/env ruby
309248        0x4B800         Executable script, shebang: "/usr/bin/env ruby"
309250        0x4B802         Unix path: /usr/bin/env ruby
411950        0x6492E         Unix path: /lib/assets/.keep

```

Since binwalk doesn't seem to have any problems recognizing the file, let's have 
it extract the contents of it too:

```
$ binwalk -eMr needle-in-the-haystack
```

Looking at the extracted files, we see that what we are looking at is a blog application written in
ruby on rails. But perhaps more interesting is the fact that there is also a `.git` directory, meaning
we probably have a whole git history for the application.

```
_needle-in-the-haystack.extracted/_7000.extracted$ ls -a
.  ..  blog  .git
```

The git index seems to be intact, and we can check the log. Nothing too interesting in the commit
messages though, and nothing seem to mention a 'flag-':

```
$ git status
On branch master
nothing to commit, working directory clean

$ git log --oneline
70659e6 Add security
3ac78ca Add association deletion
40c9d0a Deleting comments
69c17da Refactoring!!!!!!
3302b4e Add comment showing
6a05e75 Add comments controller generation
1ed7b8a Add comments model
117927a Add destroy articles feature
2939ae6 Add partials
55dfe80 Actually add update capability
e99e541 Add edit capability
fe4d8eb Add some article validation
d8478c2 Add links
abc1c7c Finish updating articles view
9045d75 Add show view
922c999 Fix controller to accept params
9dc9c9f Add article migration
ab6b638 Fix gemfile problems
cceee48 Finish populating article view/controller
c8acecb Basic article add
352dff6 Add route
393941d Change welcome index text
6d15d7d Add welcome controller
9331ed8 Initial commit

$ git log -S"flag-"
```


The most recent commit looks pretty interesting though. A `git show -p 70659e6` shows us that the commit
adds the following line to two of the files:

```rb
http_basic_authenticate_with name: "shh", password: "flap-12b36a752f93870393d8311b4e1529c1", except: [:index, :show]
```

It almost looks like a flag! By submitting it we are taken to a [youtube video](https://www.youtube.com/watch?v=dQw4w9WgXcQ),
making it pretty clear that this was not in fact the final solution...

So far we have only looked at the `master` branch, but there are actually multiple other ones. 
However, we quickly find that they are all merged to master already:

```
$ git branch
  comments
  deleting
* master
  refactoring
  security
$ git branch --no-merged master
```

What about deleted branched? A quick google for how to recover branches points us
towards the `git reflog` command, which seem to make it possible to list commits that
are no longer part of the "normal" log. The `reflog` command takes the same parameters
as the `log` command, so we can again use the `-S` flag to search for the
`flag-` string we are looking for. And this time we actually find the flag:


```
$ git reflog -S"flag-"
68490b1 HEAD@{51}: cherry-pick: fast-forward
68490b1 HEAD@{53}: commit: Basic article add

$ git show 68490b1 -p | grep -C 2 'flag-'
+  secret_key_base: 389e066b905e18624e71c9b84afd850c3232b72a027297ff6bb143ad069780357574c446da6ad5ac643f0a0e87bd5ca0d8855ecacc548cf00ffd29632aec0853
+
+flag: flag-a89a24c836bde785292b908a25b9241d
+
+# Do not keep production secrets in the repository,

```

flag: `flag-a89a24c836bde785292b908a25b9241d`
