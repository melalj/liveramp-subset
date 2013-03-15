liveramp-subset
===============

Subset secrets - Challenge program LiveRamp from http://blog.liveramp.com/2013/03/13/subset-secrets/


===
Challenge problem
-
There is a secret that you wish to partially share amongst N people such that there is an M < N for which any M or more people can reconstruct the secret, but any K < M people cannot. How do you encode the secret?


===
Solution
-

Actually a secret can be reconstructed only if a minimum of M people are COMBINED...
The idea is to bring to each person sub-keys. The full key is formed by many "sub-keys", this one will allow us to encrypt the message (using XOR algorithm).
A combinaison of M people is enough to get the full key and decrypt the secret.

I wrote a python script that encrypt a message with a list of private sub-keys (generated randomly), and decrypt a secret from a set of people. However, it's working for K<M people...

We shall use Shamir Secret Sharing Algorithm to correct this issue:
http://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing
