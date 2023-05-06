import re
from collections import defaultdict

class TextProcessor:
    stop_words = {"a", "able", "about", "above", "abst", "accordance", "according", "accordingly", "across", "act", 
        "actually", "added", "adj", "affected", "affecting", "affects", "after", "afterwards", "again", "against", 
        "ah", "all", "almost", "alone", "along", "already", "also", "although", "always", "am", 
        "among", "amongst", "an", "and", "announce", "another", "any", "anybody", "anyhow", "anymore", 
        "anyone", "anything", "anyway", "anyways", "anywhere", "apparently", "approximately", "are", "aren", "arent", 
        "arise", "around", "as", "aside", "ask", "asking", "at", "auth", "available", "away", 
        "awfully", "b", "back", "be", "became", "because", "become", "becomes", "becoming", "been", 
        "before", "beforehand", "begin", "beginning", "beginnings", "begins", "behind", "being", "believe", "below", 
        "beside", "besides", "between", "beyond", "biol", "both", "brief", "briefly", "but", "by", 
        "c", "ca", "came", "can", "cannot", "can't", "cause", "causes", "certain", "certainly", 
        "co", "com", "come", "comes", "contain", "containing", "contains", "could", "couldnt", "d", 
        "date", "did", "didn't", "different", "do", "does", "doesn't", "doing", "done", "don't", 
        "down", "downwards", "due", "during", "e", "each", "ed", "edu", "effect", "eg", 
        "eight", "eighty", "either", "else", "elsewhere", "end", "ending", "enough", "especially", "et", 
        "et-al", "etc", "even", "ever", "every", "everybody", "everyone", "everything", "everywhere", "ex", 
        "except", "f", "far", "few", "ff", "fifth", "first", "five", "fix", "followed", 
        "following", "follows", "for", "former", "formerly", "forth", "found", "four", "from", "further", 
        "furthermore", "g", "gave", "get", "gets", "getting", "give", "given", "gives", "giving", 
        "go", "goes", "gone", "got", "gotten", "h", "had", "happens", "hardly", "has", 
        "hasn't", "have", "haven't", "having", "he", "hed", "hence", "her", "here", "hereafter", 
        "hereby", "herein", "heres", "hereupon", "hers", "herself", "hes", "hi", "hid", "him", 
        "himself", "his", "hither", "home", "how", "howbeit", "however", "hundred", "i", "id", 
        "ie", "if", "i'll", "im", "immediate", "immediately", "importance", "important", "in", "inc", 
        "indeed", "index", "information", "instead", "into", "invention", "inward", "is", "isn't", "it", 
        "itd", "it'll", "its", "itself", "i've", "j", "just", "k", "keep	keeps", "kept", 
        "kg", "km", "know", "known", "knows", "l", "largely", "last", "lately", "later", 
        "latter", "latterly", "least", "less", "lest", "let", "lets", "like", "liked", "likely", 
        "line", "little", "'ll", "look", "looking", "looks", "ltd", "m", "made", "mainly", 
        "make", "makes", "many", "may", "maybe", "me", "mean", "means", "meantime", "meanwhile", 
        "merely", "mg", "might", "million", "miss", "ml", "more", "moreover", "most", "mostly", 
        "mr", "mrs", "much", "mug", "must", "my", "myself", "n", "na", "name", 
        "namely", "nay", "nd", "near", "nearly", "necessarily", "necessary", "need", "needs", "neither", 
        "never", "nevertheless", "new", "next", "nine", "ninety", "no", "nobody", "non", "none", 
        "nonetheless", "noone", "nor", "normally", "nos", "not", "noted", "nothing", "now", "nowhere", 
        "o", "obtain", "obtained", "obviously", "of", "off", "often", "oh", "ok", "okay", 
        "old", "omitted", "on", "once", "one", "ones", "only", "onto", "or", "ord", 
        "other", "others", "otherwise", "ought", "our", "ours", "ourselves", "out", "outside", "over", 
        "overall", "owing", "own", "p", "page", "pages", "part", "particular", "particularly", "past", 
        "per", "perhaps", "placed", "please", "plus", "poorly", "possible", "possibly", "potentially", "pp", 
        "predominantly", "present", "previously", "primarily", "probably", "promptly", "proud", "provides", "put", "q", 
        "que", "quickly", "quite", "qv", "r", "ran", "rather", "rd", "re", "readily", 
        "really", "recent", "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively", 
        "research", "respectively", "resulted", "resulting", "results", "right", "run", "s", "said", "same", 
        "saw", "say", "saying", "says", "sec", "section", "see", "seeing", "seem", "seemed", 
        "seeming", "seems", "seen", "self", "selves", "sent", "seven", "several", "shall", "she", 
        "shed", "she'll", "shes", "should", "shouldn't", "show", "showed", "shown", "showns", "shows", 
        "significant", "significantly", "similar", "similarly", "since", "six", "slightly", "so", "some", "somebody", 
        "somehow", "someone", "somethan", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", 
        "specifically", "specified", "specify", "specifying", "still", "stop", "strongly", "sub", "substantially", "successfully", 
        "such", "sufficiently", "suggest", "sup", "sure", "t", "take", "taken", "taking", "tell", "tends", "th", "than", "thank",
        "thanks", "thanx", "that", "that'll", "thats", "that've", "the", "their", "theirs", "them", "themselves", "then", "thence", "there",
        "thereafter", "thereby", "thered", "therefore", "therein", "there'll", "thereof", "therere", "theres", "thereto", "thereupon", "there've",
        "these", "they", "theyd", "they'll", "theyre", "they've", "think", "this", "those", "thou", "though", "thoughh", "thousand", "throug",
        "through", "throughout", "thru", "thus", "til", "tip", "to", "together", "too", "took", "toward", "towards", "tried", "tries", "truly",
        "try", "trying", "ts", "twice", "two", "u", "un", "under", "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "up", "upon", "ups",
        "us", "use", "used", "useful", "usefully", "usefulness", "uses", "using", "usually", "v", "value", "various", "'ve", "very", "via", "viz",
        "vol", "vols", "vs", "w", "want", "wants", "was", "wasnt", "way", "we", "wed", "welcome", "we'll", "went", "were", "werent", "we've", "what",
        "whatever", "what'll", "whats", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "wheres", "whereupon",
        "wherever", "whether", "which", "while", "whim", "whither", "who", "whod", "whoever", "whole", "who'll", "whom", "whomever", "whos", "whose",
        "why", "widely", "willing", "wish", "with", "within", "without", "wont", "words", "world", "would", "wouldnt", "www", "x", "y", "yes",
        "yet", "you", "youd", "you'll", "your", "youre", "yours", "yourself", "yourselves", "you've", "z", "zero"}
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
    
    @staticmethod
    def tokenize(webpage_text: str) -> list[str]:
        #O(1) since the list will always start as empty
        tokens = list()

        # O(1) since regex inits will takes constant time as input increases
        alphaNumeric = r"[0-9a-zA-Z]+"
        filtered_web_text = re.sub(r"\n", "", webpage_text)
        all_tokens = re.findall(alphaNumeric, filtered_web_text)

        for token in all_tokens:
            if token not in TextProcessor.stop_words:
                tokens.append(token.lower())
        
        return tokens
    
    @staticmethod
    def tokenizeWNoFilterCount(webpage_text: str) -> list[str]:
        #O(1) since the list will always start as empty
        tokens = list()

        # O(1) since regex inits will takes constant time as input increases
        alphaNumeric = r"[0-9a-zA-Z]+"
        filtered_web_text = re.sub(r"\\n|\\t", "", webpage_text)
        all_tokens = re.findall(alphaNumeric, filtered_web_text)
        
        return len(all_tokens)
    
    ''' O(M*N)
        Where M is the number of tokens and 
        N is the size of "tokenCount" 
        Since we update dict for every token in "tokenCount"'''
    @staticmethod
    def computeWordFrequencies(tokens: list[str]) -> defaultdict[str, int]:

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
    @staticmethod
    def printTokenAndFreq(tokenMap: defaultdict[str, int]):
        
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
    
    @staticmethod
    def getNTokenAndFreq(tokenMap: defaultdict[str, int], n: int):

        topNLis = []
        
        # Sort the token alphabetically since python sorting is in place
        sortedFreqByTok = dict(sorted(tokenMap.items(), key=lambda x: (x[0])))

        # Then sort by frequency since python sorting is in place
        sortedFreq = sorted(sortedFreqByTok.items(), key=lambda x: (x[1]), reverse=True)

        # go through the first top n freq and return them
        count = 0
        for pair in sortedFreq:
            topNLis.append(pair)
            count += 1
            if count == n:
                return topNLis
        return topNLis
    
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


    
    
