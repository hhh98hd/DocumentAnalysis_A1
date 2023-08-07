# Reference: https://www.geeksforgeeks.org/python-import-from-parent-directory/
import sys
import os
import math

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
#############################################################################

from query_tfidf import (calc_idf, get_doc_to_norm)

IDF_DF_IDX = 0
IDF_NUM_IDX = 1
IDF_OUTPUT_IDX = 2

IDF_TEST_CASES = [
    [3, 5, 0.22314355131],                                          # Normal case
    [4, 5, 0],                                                      # The term appears in almost all (N - 1) documents
    [0, 5, 1.60943791243],                                          # The term cannot be found in the collection
    [5, 5, 0]                                                       # The term appears in all documents
]

def test_idf(idx):
    test_case = IDF_TEST_CASES[idx]
    idf = calc_idf(test_case[IDF_DF_IDX], test_case[IDF_NUM_IDX]) 
    if abs(idf - test_case[IDF_OUTPUT_IDX]) <= 0.00001:
        print("[TC {id}] SUCCESS\n".format(id=idx))
        return True
    else:
        print("[TC{id}] FAILURE: Value mismatch".format(id=idx))
        print("Expected:", test_case[IDF_OUTPUT_IDX])
        print("ACtual  :", idf)
        return False
    
def test_get_docs_to_norms(idx):
    pass

if __name__ == '__main__':
    ####### TEST IDF CALCULATION #######
    idf_success_cnt = 0
    print("\n")
    for i in range(0, len(IDF_TEST_CASES)):
        if(test_idf(i)): idf_success_cnt += 1
    if(len(IDF_TEST_CASES) == idf_success_cnt):
        print("[IDF PASSED]\n")
    else:
        raise Exception("[IDF FAILED]")
    print("-----------------")
    
    ####### TEST IDF CALCULATION #######
    index = {}
    index["car"] = [(1, 1), (2, 5)]
    index["insurance"] = [(3, 1)]
    index["auto"] = [(1, 3), (4, 2)]
    
    doc_freq = {}
    doc_freq["car"] = 2
    doc_freq["insurance"] = 1
    doc_freq["auto"] = 2
    
    doc_num = 4
    expected_norms = {
        1 : 0.90973,
        2 : 1.43841,
        3 : 0.69314,
        4 : 0.57536
    }
    
    doc_norms = get_doc_to_norm(index, doc_freq, doc_num)
    if(len(doc_norms) != 4):
        print("FAILURE: Diffrence in length")
        print("Expected:", 4)
        print("Actual  :", len(doc_norms))
        
    norm_success_cnt = 0
    for doc_id in doc_norms:
        norm = doc_norms[doc_id]
        expected = expected_norms[doc_id]
        
        if abs(expected - norm) <= 0.0001:
            print("[TC{id}] SUCCESS\n".format(id = doc_id))
            norm_success_cnt += 1
        else:
            print("[TC{id} FAILURE: Difference in data\n".format(id = doc_id))
            print("At document ID = {id}: Expected: {expected}    Actual: {actual}".format(id=doc_id, expected=expected, actual=norm))
            
    if(norm_success_cnt == 4):
        print("[NORMS PASSED]")
    else:
        raise Exception("[NORMS FAILED]\n")
    print("-----------------")
     

