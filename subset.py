#-------------------------------------------------------------------
#-------------------------------------------------------------------
## Subset secrets - Challenge program LiveRamp
## http://blog.liveramp.com/2013/03/13/subset-secrets/
#-----------------------------------------------------
## Developped By Mohammed Elalj - https://github.com/melalj/liveramp-subset
#-------------------------------------------------------------------
#-------------------------------------------------------------------

# Importing modules
from itertools import izip, cycle
import base64
import random


# Function that returns an encrypted message with a list of privateKeys
def encrypt(message, listKey):
	fullKey = 1
	for i,keyPart in enumerate(listKey):
		fullKey *= int(keyPart.split('_')[1])
	# We use XOR algorithm + base64_encode to encrypt the message using a key
	xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(message, cycle(str(fullKey))))
	return base64.encodestring(xored).strip()


# Function that returns a reconstruction of the secret from gathered people
def decrypt(secret, thePeople):
	builtFullKey = []
	for people in thePeople:
		for keyPeople in people:
			keyData = keyPeople.split('_')
			if keyData not in builtFullKey:
				builtFullKey.append(keyData)
	listSortedKey = sorted(builtFullKey,key= lambda x: x[0])
	fullKey = 1
	for i,keyPart in enumerate(listSortedKey):
		if len(keyPart)>1:
			fullKey *= int(keyPart[1])
	# We use base64_decode + XOR algorithm to decrypt a secret from a key
	secret = base64.decodestring(secret)
	xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(secret, cycle(str(fullKey))))
	return xored

# Function return a list of People with their keys and a list of privatekeys
def getPeopleKeys(N,M):
	# Return a list of private keys
	def getPrivateKeys():
		raw_key = []
		key = []
		# We have much keys as number of people
		for k in range(0,N):
			while True:
				# We generate big integer as a key greater than N
				generatedKey = random.randint(1,N*1000)
				if generatedKey not in raw_key:
					raw_key.append(generatedKey)
					key.append('%d_%d' % (k,generatedKey))
					break
		return key

	D = (N-M)
	people = []
	keyPos = 0
	privateKeys = getPrivateKeys()
	# We give people their keys
	print(D+1)
	for nb in range(0,N):
		people.append([])
		# We append to each user a list of his keys
		# Each one will have (N-M)+1 keys that we order like this :
		# Exemple (N = 4; M = 2): 
		#		1: key1 , key2, key3
		#		2: key4 , key1, key2
		#		3: key3 , key4, key1
		#		4: key2 , key3, key4
		for k in range(0,D+1):
			people[nb].append(privateKeys[keyPos])
			keyPos+=1
			if(keyPos==N):
				keyPos = 0
	return (people,privateKeys)

# We make our test !
message = "Hello LiveRamp !"
N = 30
M = 17

People , PrivateKeys = getPeopleKeys(N,M)
secret = encrypt( message, PrivateKeys)
print("Message : " + message)
print("")
print("All People:")
for i,person in enumerate(People):
	print "Person %d : %s" % (i,', '.join(person)) 

# we shuffle and get M person
randomRangePeople = [i for i in People]
random.shuffle(randomRangePeople)
randomRangePeople = randomRangePeople[0:M]
# • ISSUE ! 
# We can reconstruct the secret from [0:M-1] !

print("Secret : " + secret)
print("")
print("Reconstruction from secret using %d random people from %d : " % (len(randomRangePeople),N))
print(decrypt(secret,randomRangePeople))



