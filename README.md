# bombchu

Simple data manipulation tool with a bang, inspired by [qu](https://github.com/jayswan/qu).

## Install

<img src="https://i.imgur.com/5XH9tQ2.png" align="left">

```
pip3 install bombchu --user
```
* Ensure that where Python cli tools are installed on your system is in your PATH.

## Usage

```
❯ # break on a delimiter 
❯ echo "d,d,b,a,a,b,c,d,d,e" | bombchu -d ','
['d', 'd', 'b', 'a', 'a', 'b', 'c', 'd', 'd', 'e']

❯ # same thing, but sort unique
❯ echo "d,d,b,a,a,b,c,d,d,e" | bombchu -d ',' -s -u
['a', 'b', 'c', 'd', 'e']

❯ # now output it separated by semi-colons
❯ echo "d,d,b,a,a,b,c,d,d,e" | bombchu -d ',' -s -u -o '; '
a; b; c; d; e

❯ # i got some csv data that looks like this...
❯ head -n 2 foo.csv
start_time,ip,port
"2022-04-10 06:00:10",10.13.37.42,51111

❯ # let's extract all the unique ips and put them on new lines defanged
❯ cat foo.csv | bombchu -c ip -u -n --defang
10[.]44[.]44[.]22
10[.]13[.]37[.]42
10[.]22[.]22[.]11

❯ # i gotta put this data in to splunk now in term format
❯ cat foo.csv | bombchu -c ip -u --term
(TERM(10.22.22.11) OR TERM(10.13.37.42) OR TERM(10.44.44.22))

❯ # now i got some json data that looks like this...
❯ cat foo.json
{
    "foo": {
        "id": 1234
    },
    "foo2": {
        "id": 1337
    },
    "foo3": {
        "id": 1111
    }
}

❯ # i need all these ids sorted
❯ cat foo.json | bombchu -j id -s
[1111, 1234, 1337]

❯ # gimme those ids on new lines with back ticks
❯ cat foo.json | bombchu -j id -s -n --add '`'
`1111`
`1234`
`1337`

❯ # now i got some log file that looks like this...
❯ head -n 2 foo.log
{"name": "joe", "id": 4242, "action": "bleh"}
{"name": "bob", "id": 1337, "action": "blah"}

❯ # let's see the users in these logs
❯ cat foo.log | bombchu -l name -o ', '
joe, bob, bob, bob, bob, john, john, bob, bob, susan, susan, bob

❯ # i need these sorted unique and ready to go into splunk
❯ cat foo.log | bombchu -l name -s -u --splunk
("bob", "joe", "john", "susan")

❯ # now throw that on my clipboard
❯ cat foo.log | bombchu -l name -s -u --splunk --copy
("bob", "joe", "john", "susan")

❯ # read in a python list
❯ echo "['62', '41', '27', '111', '55']" | bombchu -p --addl '=' -n
=62
=41
=27
=111
=55
```
