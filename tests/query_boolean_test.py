# Reference: https://www.geeksforgeeks.org/python-import-from-parent-directory/
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

#############################################################################

from query_boolean import union_query, intersect_query, parse_query

LIST1_IDX = 0
LIST2_IDX = 1
EXPECTED_IDX = 2

PARSE_QUERY_IDX = 0
PARSE_TERMS_IDX = 1
PARSE_OPS_IDX = 2
PARSE_MSG_IDX = 3

TEST_UNION = "union"
TEST_INTERSECT = "intersect"

UNION_TEST_CASES = [
    [[1, 2, 3, 5], [4, 6, 7], [1, 2, 3, 4, 5, 6, 7]],                               # Normal case
    [[], [], []],                                                                   # Both lists are empty
    [[], [1, 2, 3], [1, 2, 3]],                                                     # One of the lists is empty
    [[1, 2, 3], [], [1, 2, 3]],                                                     # One of the lists is empty
    [[1, 2, 3], [1, 2, 3], [1, 2, 3]],                                              # Both lists are the same
    [[1, 3, 5], [3, 5, 4, 7, 8], [1, 3, 4, 5, 7, 8]],                               # Overlapping elements at a list's ends
    [[1, 2, 6], [4, 5, 6, 7, 8], [1, 2, 4, 5, 6, 7, 8]]                             # Overlapping elements at a list's middle
]

INTERSECT_TEST_CASES = [
    [[1, 2, 3], [2, 3, 5, 6], [2, 3]],                                              # Normal case
    [[], [], []],                                                                   # Both lists are empty
    [[1, 2, 3], [1, 2, 3], [1, 2, 3]],                                              # Both lists are the same
    [[0, 2, 4], [1, 3], []],                                                        # No intersect
    [[], [1, 2, 3], []],                                                            # One of the lists is empty
    [[4, 6], [], []],                                                               # One of the lists is empty
]

PARSE_TEST_CASES = [
    ["Workbooks", ["workbooks"], [], "OK"],
    ["Australasia OR Airbase", ["australasia", "airbase"], ["OR"], "OK"],
    ["SCIENCE OR technology AND advancement AND PLATFORM", ["science", "technology", "advancement", "platform"], ["OR", "AND", "AND"], "OK"],
    ["AND anu", [], [], "INVALID: Operation cannot be at the start of a query"],
    ["anu australia AND global", [], [], "INVALID: 2 terms cannot appear next to each other: anu australia"],
    ["computer AND science AND anu AND OR australia", [], [], "INVALID: 2 operations cannot appear next to each other: AND OR"],
    ["AND OR OR", [], [], "INVALID: Operation cannot be at the start of a query"],
    ["australia commonwealth canberra", [], [], "INVALID: 2 terms cannot appear next to each other: australia commonwealth"]
]

def test_parse(idx):
    test_case = PARSE_TEST_CASES[idx]
    
    query = test_case[PARSE_QUERY_IDX]
    expected_terms = test_case[PARSE_TERMS_IDX]
    expected_ops =  test_case[PARSE_OPS_IDX]
    expected_msg = test_case[PARSE_MSG_IDX]
    
    terms = []
    ops = []
    msg = ""
    (terms, ops, msg) = parse_query(query)
    
    if(msg == expected_msg):
        if(msg == "OK"):
            # Compare terms[]
            if(len(expected_terms) != len(terms)):
                print("[TC {id}] FAILURE: Diffrence in length of terms[]".format(id=idx))
                print("Expected:", len(expected_terms), expected_terms)
                print("Actual  :", len(terms), terms, "\n")
                return False
            
            for i in range(0, len(terms)):
                if(terms[i] != expected_terms[i]):
                    print("[TC{id}] FAILURE: Difference in data of terms[]".format(id=idx))
                    print("Expected:", expected_terms)
                    print("Actual  :", terms, "\n")
                    return False
                
            # Compare ops[]
            if(len(expected_ops) != len(ops)):
                print("[TC {id}] FAILURE: Diffrence in length of ops[]".format(id=idx))
                print("Expected:", len(expected_ops), expected_ops)
                print("Actual  :", len(ops), ops, "\n")
                return False
            
            for i in range(0, len(ops)):
                if(ops[i] != expected_ops[i]):
                    print("[TC{id}] FAILURE: Difference in data of ops[]".format(id=idx))
                    print("Expected:", expected_ops)
                    print("Actual  :", ops, "\n")
                    return False
    else:
        print("[TC{id}] FAILURE: Difference in returned message".format(id=idx))
        print("Expected:", expected_msg)
        print("Actual  :", msg, "\n")
        return False
    
    print("[TC {id}] SUCCESS\n".format(id=idx))
    return True

def test_query(type, idx):
    test_case = None
    res = []
    
    if(type == TEST_INTERSECT):
        test_case =  INTERSECT_TEST_CASES[idx]
    elif(type == TEST_UNION):
        test_case = UNION_TEST_CASES[idx]
    list1 = test_case[LIST1_IDX]
    list2 = test_case[LIST2_IDX]
    expected = test_case[EXPECTED_IDX]
    
    if(type == TEST_INTERSECT):
        res = intersect_query(list1, list2)
    elif(type == TEST_UNION):
        res = union_query(list1, list2)
    res.sort()
    
    if(len(res) != len(expected)):
        print("[TC {id}] FAILURE: Diffrence in length".format(id=idx))
        print("Expected:", len(expected), expected)
        print("Actual  :", len(res), res, "\n")
        return False
    
    for i in range(0, len(res)):
        if(res[i] != expected[i]):
            print("[TC{id}] FAILURE: Difference in data".format(id=idx))
            print("Expected:", expected)
            print("Actual  :", res, "\n")
            return False
    
    print("[TC {id}] SUCCESS\n".format(id=idx))
    return True
    

if __name__ == '__main__':
    #############################   TEST UNION QUERY   #############################
    union_success_cnt = 0
    print("\n")
    for i in range(0, len(UNION_TEST_CASES)):
        if(True == test_query(TEST_UNION, i)): union_success_cnt += 1
    print("-----------------")
    if(len(UNION_TEST_CASES) == union_success_cnt):
        print("[UNION PASSED]")
    else:
        raise Exception("[UNION FAILED]")
    ################################################################################


    ###########################   TEST INTERSECT QUERY   ###########################
    intersect_success_cnt = 0
    print("\n")
    for i in range(0, len(INTERSECT_TEST_CASES)):
        if(True == test_query(TEST_INTERSECT, i)): intersect_success_cnt += 1
    print("-----------------")
    if(len(INTERSECT_TEST_CASES) == intersect_success_cnt):
        print("[INTERSECT PASSED]")
    else:
        raise Exception("[INTERSECT FAILED]")
    ################################################################################
    
    #############################   TEST PARSE QUERY   #############################
    parse_success_cnt = 0
    print("\n")
    for i in range(0, len(PARSE_TEST_CASES)):
        if(True == test_parse(i)): parse_success_cnt += 1
    print("-----------------")
    if(len(PARSE_TEST_CASES) == parse_success_cnt):
        print("[PARSE PASSED]")
    else:
        raise Exception("[PARSE FAILED]")
    ################################################################################
