import re
from collections import defaultdict

class TextProcessor:

    # O(1) Since it always passes
    def __init__(self) -> None:
        pass
    
    ''' O(R*(2L+(W*(T+M))) 
        where R is the length of lines in the file,
        W is the legnth of words in "line", 
        T is the length of "word", 
        M is the length of "tokens" and 
        N is the length of "toks", 
        L is the length of next line in file 
        Since we are looping through each each line, to then word in each line, then searching through each word,
        to then add those searches to the token list'''
    def tokenize(self, fileName: str) -> list[str]:
        
        # O(1) all files take the same time to open
        try:
            f = open(fileName, "r",encoding='utf-8')
        except IOError:
            print("File Format not accepted")

        #O(1) since the list will always start as empty
        tokens = list()

        # O(1) since regex inits will takes constant time as input increases
        alphaNumeric = r"[0-9a-zA-Z]+"

        # O(L) where L is the length of next line in file
        line = f.readline()

        ''' O(R*(L+(W*(T+Max(M,N)))) 
            where R is the number of lines in the file, 
            W is the number of words in "line", 
            T is the length of "word", 
            M is the length of "tokens",
            L is the length of next line in file 
            Since we are looping through each each line, to then word in each line, then searching through each word,
            to then add those searches to the token list'''
        while line != "":

            ''' O(W*(T+N)) 
                where W is the number of words in "line", 
                T is the length of "word", 
                M is the length of "tokens" and 
                Since we are looping through each word in each line and searching through each word,
                to then add those searches to the token list'''
            for word in line.split():

                # O(T) where T is the length of "word" since it searches throughout the string
                toks = re.findall(alphaNumeric, word.lower())

                # O(M)) where M is the length of "toks"
                tokens += toks
            
            # O(L) where L is the length of next line in file
            line = f.readline()
        
        # O(1) since closing files is constant
        f.close()

        # O(1) return is constant
        return tokens
    
    ''' O(M*N)
        Where M is the number of tokens and 
        N is the size of "tokenCount" 
        Since we update dict for every token in "tokenCount"'''
    def computeWordFrequencies(self, tokens: list[str]) -> defaultdict[str, int]:

        # O(1) initialization would be constant no matter the size of input
        tokenCount = defaultdict(int)

        # O(M*N) Where M is the number of tokens and N is the size of "tokenCount" since we update dict for every token in "tokenCount"
        for token in tokens:

            # O(N) where N is the size of "tokenCount" dict since worse case in N in hashmap
            tokenCount[token] += 1
        
        # O(1) since return is constant
        return tokenCount
    
    ''' O(N + (2(N Log N)))
        Where N is the number of items in the "tokenMap" Dict
        Since we are sorting the Dicts twice, once by alphabet, then by frequency. 
        We then print out the contents which is just N'''
    def printTokenAndFreq(self, tokenMap: defaultdict[str, int]):
        
        # O(N log N) where N is the number of items in the "tokenMap" Dict
        sortedFreqByTok = dict(sorted(tokenMap.items(), key=lambda x: (x[0])))

        # O(N log N) where N is the number of items in the "sortedFreqByTok" Dict
        sortedFreq = sorted(sortedFreqByTok.items(), key=lambda x: (x[1]), reverse=True)

        # O(N) where N is the number of items in the "sortedFreq" dict
        for pair in sortedFreq:

            # O(1) print is constant
            print("<{}>\t<{}>".format(pair[0], pair[1]))
        
        # O(1) return is constant
        return
    
    ''' O((R*(2L+(W*(T+M))) + 2(N^2) + A)
        where R is the length of lines in the file,
        W is the legnth of words in "line", 
        T is the max length of the words in line, 
        M is the length of the token List from the file and
        L is the Max length of a line in file 
        N is the max size of tokens from the 2 files
        A is the Min of the 2 sets of tokens from the 2 files
        Since we are looping through each each line, to then word in each line, then searching through each word,
        to then add those searches to the token list. We do this twice. We Then turn these 2 into set, 
        where each item added to set hash is checked on the rest of the set. Lastly, we get the intersection by
        at most, we look through the smaller set since that the most the intersection would be.'''
    def intersection(self, fileName1: str, fileName2: str) -> set[str]:

        ''' O(R*(2L+(W*(T+M))) 
        where R is the length of lines in the file,
        W is the legnth of words in "line", 
        T is the max length of the words in line, 
        M is the length of the token List from the file and
        L is the Max length of a line in file 
        Since we are looping through each each line, to then word in each line, then searching through each word,
        to then add those searches to the token list'''
        tokens1 = self.tokenize(fileName1)

        ''' O(R*(2L+(W*(T+M))) 
        where R is the length of lines in the file,
        W is the legnth of words in "line", 
        T is the max length of the words in line, 
        M is the length of the token List from the file and
        L is the Max length of a line in file 
        Since we are looping through each each line, to then word in each line, then searching through each word,
        to then add those searches to the token list'''
        tokens2 = self.tokenize(fileName2)

        # O(N^2) Where N is the size of tokensSet1 Since each item added to set hash is checked on the rest of the set
        tokensSet1 = set(tokens1)

        # O(N^2) Where N is the size of tokensSet2 Since each item added to set hash is checked on the rest of the set
        tokensSet2 = set(tokens2)

        # O(Min(A) Where A is the size Min of "tokenSet1" and "tokenSet2" Since the smaller set will be the max size
        return set.intersection(tokensSet1, tokensSet2)


    
    
