import nltk
from nltk.stem import PorterStemmer, SnowballStemmer, LancasterStemmer
import re

punctuation_marks = [".", "?", "!", ",", ";",
                     ":","\"", "'", "(", ")",
                     "[", "]", "{", "}", "'s",
                     "_", ";"]

patterns = [
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',                        # Email                         
    r'\b(?:https?://)?(?:www\.)?[A-Za-z0-9.-]+(?:\.[A-Z|a-z]{2,7})+\S*\b'           # Website
]

def process_tokens(toks):
    # return process_tokens_1(toks)                                                 # PorterStemmer only
    # return process_tokens_2(toks)                                                 # Filter before running PorterStemmer
    return process_tokens_3(toks)                                                 # Filter before running SnowballStemmer
    # return process_tokens_4(toks)                                                 # Filter before running LancasterStemmer
    # return process_tokens_5(toks)                                                   # Filter only
    # return process_tokens_original(toks)

# get the nltk stopwords list
stopwords = set(nltk.corpus.stopwords.words("english"))

def run_normalization(toks, stemmer):
    """ Perform processing on tokens. Before stemming and lemmanization apllied, 
        \nstopwords and punctuation marks will be removed. Apart from that, email
        \nand and websites will be taken from its containning token

    Args:
        toks (list(str)): all the tokens in a single document
        stemmer         : stemmer used (default not used)

    Returns:
        list(str): tokens after processing
    """
    
    processed_toks = []
    
    for tok in toks:
        # Remove all non-ASCII characters
        tok = str(tok).encode("ascii", "ignore").decode()
        if(tok == ""):
            continue
        
        # Convert to lower-case
        tok = tok.lower()
        
        if tok in stopwords:
            continue
        else:
            # Skip stemming for emails, websites
            for pattern in patterns:
                matches = re.findall(pattern, tok)
                if len(matches) != 0:
                    # Filter email, website from the token
                    for item in matches:
                        processed_toks.append(item)
                    continue
            
            # Remove punctuation mark in token
            for ch in tok:
                if ch in punctuation_marks:
                    tok =  tok.replace(ch, "")   
            if(tok == ""):
                continue
                
            # Stem
            if stemmer != None:
                tok = stemmer.stem(tok)
            
            processed_toks.append(tok)
    
    return processed_toks

def process_tokens_original(toks):
    """ Perform processing on tokens. This is the Linguistics Modules
    phase of index construction

    Args:
        toks (list(str)): all the tokens in a single document

    Returns:
        list(str): tokens after processing
    """
    new_toks = []
    for t in toks:
        # ignore stopwords
        if t in stopwords or t.lower() in stopwords:
            continue
        # lowercase token
        t = t.lower()
        new_toks.append(t)
    return new_toks

def process_tokens_1(toks):
    """ Perform processing on tokens. This is the Linguistics Modules
    phase of index construction

    Args:
        toks (list(str)): all the tokens in a single document

    Returns:
        list(str): tokens after processing
    """
    
    processed_toks = []
    stemmer = PorterStemmer()
    
    for tok in toks:
        # Remove all non-ASCII characters
        tok = str(tok).encode("ascii", "ignore").decode()
        if(tok == ""):
            continue
        
        tok = tok.lower()
        if tok in stopwords:
            continue
        else:
            tok = stemmer.stem(tok)
            
        processed_toks.append(tok)
    
    return processed_toks

def process_tokens_2(toks):
    """ Perform processing on tokens. This is the Linguistics Modules
    phase of index construction

    Args:
        toks (list(str)): all the tokens in a single document

    Returns:
        list(str): tokens after processing
    """
    
    stemmer = PorterStemmer()
    return run_normalization(toks, stemmer=stemmer)
    
def process_tokens_3(toks):
    """ Perform processing on tokens. This is the Linguistics Modules
    phase of index construction

    Args:
        toks (list(str)): all the tokens in a single document

    Returns:
        list(str): tokens after processing
    """
    
    stemmer = SnowballStemmer(language='english')
    return run_normalization(toks, stemmer=stemmer)

def process_tokens_4(toks):
    """ Perform processing on tokens. This is the Linguistics Modules
    phase of index construction

    Args:
        toks (list(str)): all the tokens in a single document

    Returns:
        list(str): tokens after processing
    """
    
    stemmer = LancasterStemmer()
    return run_normalization(toks, stemmer=stemmer)

def process_tokens_5(toks):
    """ Perform processing on tokens. This is the Linguistics Modules
    phase of index construction

    Args:
        toks (list(str)): all the tokens in a single document

    Returns:
        list(str): tokens after processing
    """
    
    return run_normalization(toks, None)

def tokenize_text(data):
    """Convert a document as a string into a document as a list of
    tokens. The tokens are strings.

    Args:
        data (str): The input document

    Returns:
        list(str): The list of tokens.
    """
    # split text on spaces
    tokens = data.split()
    return tokens
