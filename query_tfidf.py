import math
from collections import defaultdict
from string_processing import (
    process_tokens,
    tokenize_text,
)
from query import (
    get_query_tokens,
    count_query_tokens,
    query_main,
)

def calc_idf(df, num_docs):
    """Calculate IDF of a particular term

    Args:
        df (int)       : Document frequency of a term
        num_docs (int) : Number of documents in the collection

    Returns:
        float: Calculated IDF
    """
    return 0 if df == num_docs else math.log(num_docs / (1 + df), math.e)

def get_doc_to_norm(index, doc_freq, num_docs):
    """Pre-compute the norms for each document vector in the corpus using tfidf.

    Args:
        index (dict(str : list(tuple(int, int)))): The index aka dictionary of posting lists
        doc_freq (dict(str : int)): document frequency for each term
        num_docs (int): number of documents in the corpus

    Returns:
        dict(int: float): a dictionary mapping doc_ids to document norms
    """

    doc_norms = defaultdict(float)
    
    for term in index:
        idf = calc_idf(doc_freq[term], num_docs)

        for (doc_id, tf) in index[term]:
            doc_norms[doc_id] += (tf*idf)**2
            
    for doc_id in doc_norms:
        doc_norms[doc_id] = math.sqrt(doc_norms[doc_id])

    return doc_norms


def run_query(query_string, index, doc_freq, doc_norm, num_docs):
    """ Run a query on the index and return a sorted list of documents. 
    Sorted by most similar to least similar.
    Documents not returned in the sorted list are assumed to have 0 similarity.

    Args:
        query_string (str): the query string
        index (dict(str : list(tuple(int, int)))): The index aka dictionary of posting lists
        doc_freq (dict(str : int)): document frequency for each term
        doc_norm (dict(int : float)): a map from doc_ids to pre-computed document norms
        num_docs (int): number of documents in the corpus

    Returns:
        list(tuple(int, float)): a list of document ids and the similarity scores with the query
        sorted so that the most similar documents to the query are at the top.
    """

    # TODO: Implement this function using tfidf
    # Hint: This function is similar to the run_query function in query.py
    #       but should use tfidf instead of term frequency
    sorted_docs = []

    return sorted_docs


if __name__ == '__main__':
    # query = "How to stay safe during severe weather?"
    # query = query.split()
    # new_query = []
    # stopwords = set(nltk.corpus.stopwords.words("english"))
    # for term in query:
    #     if(term in stopwords or term.lower() in stopwords):
    #         continue
    #     else:
    #         new_query.append(term)
    # print(new_query)
        
    queries = [
        'Is nuclear power plant eco-friendly?',
        'How to stay safe during severe weather?',
    ]
    query_main(queries=queries, query_func=run_query, doc_norm_func=get_doc_to_norm)
    
