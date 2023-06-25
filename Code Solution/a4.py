# importing required modules :- random, math 
import random                                                       
import math

#To generate random prime less than N
def randPrime(N):                                   
	primes = []
	for q in range(2,N+1):
		if(isPrime(q)):
			primes.append(q)
	return primes[random.randint(0,len(primes)-1)]

# To check if a number is prime
def isPrime(q):                                     
	if(q > 1):
		for i in range(2, int(math.sqrt(q)) + 1):
			if (q % i == 0):
				return False
		return True
	else:
		return False

#pattern matching
def randPatternMatch(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatch(q,p,x)

#pattern matching with wildcard
def randPatternMatchWildcard(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatchWildcard(q,p,x)

# return appropriate N that satisfies the error bounds
def findN(eps,m):                       
    """
    -> Let ni be the hashed_value of a substring of the given text such that the substring doesn't matches with the given pattern
    -> Let np be the hashed_value of the given pattern. Let q be the prime number used in modPatternMatch and modPatternMatchWildcard
    
    Error occurs => (ni % q == np % q) and (ni != np)
    => (ni - np) % q == 0.

    -> Let n be a number such that n = ni - np. Then n > 0 and n < 26**m
    => n % q = 0.

    -> maximum total number of prime factors of 26**m are m*log2(26).                   [Using claim 1]
    -> minimum total number of prime numbers below N are N/(2*log2(N))                  [Using claim 2]

    -> Probability of error = (maximum number of prime factors of 26**m)/(minimum number of prime numbers below)
    => (m*log2(26))/(N/(2*log2(N))) <= eps
    => N/log2(N) >= 2(m/eps)(log2(26))

    N must satisfy the inequality:-
    N/log2(N) >= 2(m/eps)(log2(26))

    -> Let c = RHS = 2(m/eps)(log2(26))
    
    We get the following inequality:-
    N >= c*log2(N)

    Here by Hit and trial, we get the following observations:-
    -> N = c does not satisfy the inequality
    -> N = c^2 satisfies the inequality
    Therefore N = c^2 satisfies the inequality

    But my checking further we get the following observations:-
    -> N = c*log2(c) does not satisfies the inequality
    -> N = 2c*log2(c) satisfies the inequality

    Therefore by solving the inequality by Hit and Trial and analysis we get:-
    N = 2c*log(c)
    """
    c = 2*(m/eps)*(math.log2(26))                       
    return int(2*c*(math.log2(c)))                    #? We get this expression by solving for N mathematically

def findN_test():                   #? findN testing module
    print(findN(0.9,32))
    print(findN(0.002, 232))
    print(findN(0.000232, 1))

# Return sorted list of starting indices where p matches x
def modPatternMatch(q,p,x):
    Alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"                            # string of capital latin alphabets
    char_hashing = dict()                                               # char_hashing : dictionary , maps Alphabets to integers from 0 to 25
    for i in range(26):                                                 #? mapping char_hashing
        char_hashing[Alphabets[i]] = i
    m = len(p)                                                          # length of the pattern
    n = len(x)                                                          # length of the text
    hashed_pattern = 0                                                  # hashed value of pattern
    occurences = []                                                     # list of the starting indices where p matches x
    curr_hashed_substring = 0                                           # hashed value of the current substring
    c = 1                                                               # initialzing c, the value of (2**m)%q
      
    for i in range(m):                                                  #? computing c, hashed_pattern, curr_hashed_substring
        c = (c*26)%q                                                    #? This takes O(log(q)) working memory

        hashed_pattern = 26*hashed_pattern + char_hashing[p[i]]         #? This also takes O(log(q)) working memory because hashed_pattern < q
        hashed_pattern %= q                                             #? This takes O(log(q)) working memory

        curr_hashed_substring = 26*curr_hashed_substring + char_hashing[x[i]]   #? This also takes O(log(q)) working memory because hashed_pattern < q
        curr_hashed_substring %= q                                              #? this step takes O(log(q)) space complexity
    
    if (curr_hashed_substring == hashed_pattern):                       #? If hashed_values matches for first index
        occurences.append(0)                                            # add 0 to list of occurences

    i = m                                                               # index of text
    while(i < n):                                                       # index must be less than n
        curr_hashed_substring = 26*curr_hashed_substring + char_hashing[x[i]]   #? recursive relation for computing next hashed_substring
                                                                                #? this takes O(log(q)) working memory as curr_hashed_substring < q
        curr_hashed_substring -= (c*char_hashing[x[i-m]])%q             #? this takes O(log(q)) working memory
        curr_hashed_substring %= q                                      #? this takes O(log(q)) working memory

        if (curr_hashed_substring == hashed_pattern):                   #? If hashed_value matches for (i-m+1)th index
            occurences.append(i-m+1)                                    # add i-m+1 to list of occurences 
        i += 1                                                          

    return occurences

def modPatternMatch_test():             #? modPatternMatch testing module
    print(modPatternMatch(11, "IF", "IFYOUCANKEEPYOURHEADWHENALLABOUTYOUARELOSINGTHEIRSANDBLAMINGITONYOUIFYOUCANTRUSTYOURSELFWHENALLMENDOUBTYOUBUTMAKEALLOWANCEFORTHEIRDOUBTINGTOOIFYOUCANWAITANDNOTBETIREDBYWAITINGORBEINGLIEDABOUTDONTDEALINLIESORBEINGHATEDDONTGIVEWAYTOHATINGANDYETDONTLOOKTOOGOODNORTALKTOOWISEIFYOUCANDREAMANDNOTMAKEDREAMSYOURMASTERIFYOUCANTHINKANDNOTMAKETHOUGHTSYOURAIMIFYOUCANMEETWITHTRIUMPHANDDISASTERANDTREATTHOSETWOIMPOSTORSJUSTTHESAMEIFYOUCANBEARTOHEARTHETRUTHYOUVESPOKENTWISTEDBYKNAVESTOMAKEATRAPFORFOOLSORWATCHTHETHINGSYOUGAVEYOURLIFETOBROKENANDSTOOPANDBUILDEMUPWITHWORNOUTTOOLSIFYOUCANMAKEONEHEAPOFALLYOURWINNINGSANDRISKITONONETURNOFPITCHANDTOSSANDLOSEANDSTARTAGAINATYOURBEGINNINGSANDNEVERBREATHEAWORDABOUTYOURLOSSIFYOUCANFORCEYOURHEARTANDNERVEANDSINEWTOSERVEYOURTURNLONGAFTERTHEYAREGONEANDSOHOLDONWHENTHEREISNOTHINGINYOUEXCEPTTHEWILLWHICHSAYSTOTHEMHOLDONIFYOUCANTALKWITHCROWDSANDKEEPYOURVIRTUEORWALKWITHKINGSNORLOSETHECOMMONTOUCHIFNEITHERFOESNORLOVINGFRIENDSCANHURTYOUIFALLMENCOUNTWITHYOUBUTNONETOOMUCHIFYOUCANFILLTHEUNFORGIVINGMINUTEWITHSIXTYSECONDSWORTHOFDISTANCERUNYOURSISTHEEARTHANDEVERYTHINGTHATSINITANDWHICHISMOREYOULLBEAMANMYSONIF"))
    # print(modPatternMatch(1000000007, "CD", "ABCDE"))
    # print(modPatternMatch(10000, "CD", "ABCDE"))      #? Exceptional testcase
    # print(modPatternMatch(1000000007, "AA", "AAAAA"))
    # print(modPatternMatch(2, "AA", "ACEGI"))

# Return sorted list of starting indices where p matches x
def modPatternMatchWildcard(q,p,x):     #? time complexity: O(nlog(q)); working memory: O(log(n) + log(q))
    Alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"                            # string of capital latin alphabets
    char_hashing = dict()                                               # char_hashing : dictionary , maps Alphabets to integers from 0 to 25
    for i in range(26):                                                 #? mapping char_hashing
        char_hashing[Alphabets[i]] = i    

    n = len(x)                                                          # length of text
    m = len(p)                                                          # length of pattern
    occurences = []                                                     # list of starting indices where p matches x
    curr_hashed_substring = 0                                           # hashed_value of current substring
    hashed_pattern = 0                                                  # hashed_value of pattern
    position_of_wildcard = 0                                            # index of '?' in the given pattern
    c = 1                                                               # initialzing value of (2**(m-1))%q
    c1 = 1                                                              # initialzing value of (2**(m-position_of_wildcard-1))%q

    for i in range(m):                                                  #? computing position_of_wildcard, takes O(m) time
        if (p[i] == '?'):
            position_of_wildcard = i
            break

    for i in range(m-1):                                                #? computing c
        c = (26*c)%q                                                    #? this takes O(log(q)) working memory

    for i in range(m - 1 - position_of_wildcard):                       #? computing c1
        c1 = (26*c1)%q                                                  #? this takes O(log(q)) working memory

    for i in range(m):                                                  #? computing hashed_pattern
        if (i != position_of_wildcard):                                 #? if -> p[i] != '?'
            hashed_pattern = 26*hashed_pattern + char_hashing[p[i]]     #? Recursive relation, this takes O(log(q)) working memory as hashed_pattern < q
            hashed_pattern %= q                                         #? this takes O(log(q)) working memory
        else:                                                           #? else -> p[i] == '?'
            hashed_pattern *= 26                                        #? Recursive relation, this takes O(log(q)) working memory as hashed_pattern < q
            hashed_pattern %= q                                         #? this takes O(log(q)) working memory

    for i in range(m):                                                  #? computing curr_hashed_substring for first substring
        if (i != position_of_wildcard):                                 #? if -> x[i]'s corresponding character in pattern is not '?'
            curr_hashed_substring = 26*curr_hashed_substring + char_hashing[x[i]]   #? Recursive relation, this takes O(log(q)) working memory as hashed_pattern < q
            curr_hashed_substring %= q                                              #? this takes O(log(q)) working memory
        else:                                                           #? else -> x[i]'s corresponding character in the pattern is '?'
            curr_hashed_substring *= 26                                 #? Recursive relation, this takees O(log(q)) working memory as curr_hashed_substring < q
            curr_hashed_substring %= q                                  #? this takes O(log(q)) working memory

    if(curr_hashed_substring == hashed_pattern):                        #? If hashed_values matches for first index
        occurences.append(0)                                            # add 0 to list of occurences

    i = m                                                               # index of text
                                                                        #? i takes O(log(n)) working memory
    while(i < n):                                                       #? index must be less than n
        curr_hashed_substring -= (c*char_hashing[x[i-m]])%q                             #? this takes O(log(q)) working memory
        curr_hashed_substring += (c1*char_hashing[x[i-m+position_of_wildcard]])%q       #? this takes O(log(q)) working memory
        curr_hashed_substring = 26*curr_hashed_substring + char_hashing[x[i]]           #? Recursive relation, takes O(log(q)) working memory as curr_hashed_substring < q
        curr_hashed_substring -= (c1*char_hashing[x[i-m+position_of_wildcard+1]])%q     #? this takes O(log(q)) working memory
        curr_hashed_substring %= q                                                      #? this takes O(log(q)) working memory
        
        if (curr_hashed_substring == hashed_pattern):                   #? If hashed_value matches for (i-m+1)th index    
            occurences.append(i-m+1)                                    # add i-m+1 to list of occurences 
        i += 1

    return occurences

def modPatternMatchWildcard_test():     #? modPatternMatchWildCard testing module
    print(modPatternMatchWildcard(1000000007, "D?", "ABCDE"))
    print(modPatternMatchWildcard(1000000007, "?A", "ABCDE"))
    print(modPatternMatchWildcard(1000000004, "E?", "ABCDE"))
    print(modPatternMatchWildcard(100000213, "OW?S", "ALKJSOWASLKJAKJOWSSLKJALKJOWSAOWGSAOWIS"))
    print(modPatternMatchWildcard(1000000003, "?", "AKDSSADL"))
    print(modPatternMatchWildcard(1000000007, "?A", "AAA" ))
    print(modPatternMatchWildcard(1000000007, "A?", "ABABAA"))

if (__name__ == "__main__"):            #? main testing module
#     findN_test()
#     modPatternMatchWildcard_test()
    modPatternMatch_test()
