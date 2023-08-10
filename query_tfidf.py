import math
from collections import defaultdict
from string_processing import (
    run_normalization,
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
        float: Calculated IDF  = ln(M / 1 + DF)
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

    sorted_docs = []
    
    # preprocess the query string
    qt = get_query_tokens(query_string)
    
    # calculate norm of the query
    query_norm = 0.0
    query_token_counts = count_query_tokens(qt)
      
    for(term, tf) in query_token_counts:
        if term not in index:
            continue
        else:
            idf = calc_idf(doc_freq[term], num_docs)
            query_norm += (tf * idf)**2
    
    query_norm = math.sqrt(query_norm)
    
    # calculate consine similarity
    doc_to_score = defaultdict(float)
    
    for (term, tf_query) in query_token_counts:
        if term not in index:
            continue
        else:
            for (doc_id, tf_doc) in index[term]:
                idf = calc_idf(doc_freq[term], num_docs)
                
                tfidf_query = tf_query * idf
                tfidf_doc = tf_doc * idf
                
                doc_to_score[doc_id] += ((tfidf_query * tfidf_doc) / (doc_norm[doc_id] * query_norm))
    
    sorted_docs = sorted(doc_to_score.items(), key=lambda x:-x[1])
        
    return sorted_docs


if __name__ == '__main__':
    queries = [
        'Is nuclear power plant eco-friendly?',
        'How to stay safe during severe weather?',
    ]
    query_main(queries=queries, query_func=run_query, doc_norm_func=get_doc_to_norm)
