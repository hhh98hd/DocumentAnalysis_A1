import pickle
from string_processing import (
    process_tokens,
    tokenize_text,
)
import os
from multiprocessing.pool import ThreadPool

operation_map = {}

def intersect_query(doc_list1, doc_list2):
    res = []
    idx1 = 0
    idx2 = 0
    doc1 = 0
    doc2 = 0
    
    len1 = len(doc_list1)
    len2 = len(doc_list2)
    
    while idx1 < len1 and idx2 < len2:
        doc1 = doc_list1[idx1]
        doc2 = doc_list2[idx2]
        
        if(doc1 == doc2):
            res.append(doc1)
            idx1 += 1
            idx2 += 1
        elif(doc1 < doc2):
            idx1 += 1
        else:
            idx2 += 1

    return res

def union_query(doc_list1, doc_list2):
    res = []
    idx1 = 0
    idx2 = 0
    doc1 = 0
    doc2 = 0
    
    len1 = len(doc_list1)
    len2 = len(doc_list2)
    
    while idx1 < len1 or idx2 < len2:
        if(idx1 < len1 and idx2 < len2):
            doc1 = doc_list1[idx1]
            doc2 = doc_list2[idx2]
            
            if(doc1 == doc2):
                res.append(doc1)
                idx1 += 1
                idx2 += 1
            elif(doc1 < doc2):
                res.append(doc1)
                idx1 += 1
            elif(doc2 < doc1):
                res.append(doc2)
                idx2 += 1
                
        # Already at the end of list 1
        elif(idx1 >= len1):
            doc2 = doc_list2[idx2]
            res.append(doc2)
            idx2 += 1
            
        # Already at the end of list 2
        elif(idx2 >= len2):
            doc1 = doc_list1[idx1]
            res.append(doc1)
            idx1 += 1
    
    return res

def get_doc_list(term, posting_list, index):
    """Get posting list of term

    Args:
        query_string (str) : boolean query string
        posting_list (dict): Posting list of terms appear in the query
        index (dict)       : Posting lists for all terms appear in the gov data

    Returns:
        None
    """
    
    occurences = []
        
    if term not in index:
        return
    else:
        for doc in index[term]: # [(1, 2), (3, 4), (5, 6)]
            occurences.append(doc[0])
            
    posting_list[term] = occurences

def parse_query(query_string):
    """Parse a querry into 2 lists: 1 list of terms and 1 list of operations.
    \nReturns a tuple (terms, operations, message).
    \nIf the query has been parsed successfully, the message would be "OK"

    Args:
        query_string (str): boolean query string

    Returns:
        tupple(terms: list(int), operations: list(int), message: str)
    """
    
    terms = []
    ops = []
    
    query_string = query_string.split()
    
    if(query_string[0] in operation_map):
        return (terms, ops, "INVALID: Operation cannot be at the start of a query")
    
    previous_item = ""
    for item in query_string:
        if(item not in operation_map):
            if(previous_item not in operation_map and previous_item != ""):
                return (terms, ops, "INVALID: 2 terms cannot appear next to each other: {prev} {cur}".format(prev=previous_item, cur=item))
            else:
                terms.append(item.lower())
        else:
            if(previous_item in operation_map and previous_item != ""):
                return (terms, ops, "INVALID: 2 operations cannot appear next to each other: {prev} {cur}".format(prev=previous_item, cur=item))
            else:
                ops.append(item)
        previous_item = item
        
    return (terms, ops, "OK")

def run_boolean_query(query_string, index):
    """Runs a boolean query using the index.

    Args:
        query_string (str): boolean query string
        index (dict(str : list(tuple(int, int)))): The index aka dictionary of posting lists

    Returns:
        list(int): a list of doc_ids which are relevant to the query
    """
    
    posting_list = {}
    query_terms = []
    ops = []
    
    if(query_string == ""):
        return []
    
    (query_terms, ops, msg) =  parse_query(query_string)
    if(msg != "OK"):
        return [msg]
              
    # Concurrently retrieve document list corresponding to each query term
    core_num = os.cpu_count()
    if(core_num == None): core_num = 4
    pool = ThreadPool(core_num)
    args = []
    for term in query_terms:
        args.append((term, posting_list, index))
    pool.starmap(get_doc_list, args)
    
    # If there is only 1 term, then we only need to find occurences of that term
    if(1 == len(query_terms)):
        return posting_list[query_terms[0]]
    
    # As there is no procedence and bracket, we will save results obtained from previous queries to list1
    list1 = posting_list[query_terms[0]]
    list2 = posting_list[query_terms[1]]
    operation = ops.pop(0)
    if operation not in operation_map:
        raise Exception("Please makse sure that you've added this operation to operation_map")
    # Invoke the corresponding operation
    list1 = operation_map[operation](list1, list2)
    
    for i in range(2, len(query_terms)):
        list2 = posting_list[query_terms[i]]
        operation = ops.pop(0)
        if operation not in operation_map:
            raise Exception("Please makse sure that you've added this operation to operation_map")
        list1 = operation_map[operation](list1, list2)
        
    return list1

#############  ADD OPERATION  ##############

operation_map["AND"] = intersect_query
operation_map["OR"] = union_query

############################################

if __name__ == '__main__':
    # load the stored index
    (index, doc_freq, doc_ids, num_docs) = pickle.load(open("stored_index.pkl", "rb"))

    print("Index length:", len(index))
    if len(index) != 808777:
        print("Warning: the length of the index looks wrong.")
        print("Make sure you are using `process_tokens_original` when you build the index.")
        raise Exception()

    # the list of queries asked for in the assignment text
    queries = [
        "Workbooks",
        "Australasia OR Airbase",
        "Warm AND WELCOMING",
        "Global AND SPACE AND economies",
        "SCIENCE OR technology AND advancement AND PLATFORM",
        "Wireless OR Communication AND channels OR SENSORY AND INTELLIGENCE",
    ]

    # run each of the queries and print the result
    ids_to_doc = {docid: path for (path, docid) in doc_ids.items()}
    for query_string in queries:
        print(query_string)
        doc_list = run_boolean_query(query_string, index)
        
        # Handle invalid queries
        if isinstance(doc_list[0], str):
            print(doc_list[0])
        else:
            res = sorted([ids_to_doc[docid] for docid in doc_list])
            for path in res:
                print(path)
            