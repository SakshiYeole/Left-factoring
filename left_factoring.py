# Write a program that takes a grammar as input and produces an equivalent left-factored grammar as output.

# Sakshi Shashikant Yeole
# 20CS01047

# Returns boolean if nth character of two productions matches.
def matching(production_i, production_j, n):
    if n >= len(production_i) and n >= len(production_j):
        return False
    if production_i[n] == production_j[n]:
        return True
    else:
        return False

# Returns a list of all common prefixes in two or more production in a given productions list
def common_prefix(productions):
    # returns list
    prefix_list = []
    visited = [0] * len(productions)

    for i in range(len(productions)):
        if visited[i]:
            continue
        else:
            visited[i] = 1
            temp_list = []
            for j in range(i+1, len(productions)):
                if visited[j]:
                    continue
                else:
                    if matching(productions[i], productions[j], 0):
                        temp_list.append(productions[j])
                        visited[j] = 1

            if temp_list:
                curr_index = 0
                for k in range(1, len(productions[i])):
                    ch = productions[i][k]
                    var = False
                    for t in range(len(temp_list)):
                        if temp_list[t][k] != ch:
                            var = True
                            break
                        
                    if var:
                        break

                    curr_index = k
                
                pre = productions[i][:curr_index+1]
                c = False
                for p in prefix_list:
                    if p == pre:
                        c = True
                
                if c == False:
                    prefix_list.append(pre)

    # print("prefix list: {}".format(prefix_list))
    return prefix_list

# Returns a dict with key as a prefix from a given prefix_list for given prodcutions and 
# value as its corrresponding list of production rule which starts with that specific prefix
def prefix_rules(list_prefixes, productions):
    # returns dict
    # print("list : {}".format(list_prefixes))
    # print("produc : {}".format(productions))
    dict_prefix_to_rules = {}
    
    for prefix in list_prefixes:
        dict_prefix_to_rules[prefix] = []
        for production in productions:
            if production.startswith(prefix):
                dict_prefix_to_rules[prefix].append(production)
    
    for production in productions:
        present = False
        for key in dict_prefix_to_rules:
            for right in dict_prefix_to_rules[key]:
                if right == production:
                    present = True

        if not present:
            dict_prefix_to_rules[production] = []
            dict_prefix_to_rules[production].append(production)

    # print("prefix to rules: {}".format(dict_prefix_to_rules))
    return dict_prefix_to_rules

# Returns a new non-terminal for the new production after left-factoring
def create_new_non_terminal(non_terminal, new_non_terminals):
    new_non_terminal = non_terminal + "'"
    while (new_non_terminal in non_terminal) or (new_non_terminal in new_non_terminals):
        new_non_terminal += "'"
    return new_non_terminal

def print_grammar(grammar):
    for non_terminal, productions in grammar.items():
        print(f"{non_terminal} -> {' | '.join(productions)}")

# main factoring function which left factors the given grammar using al the intermediate functions.
def left_factoring(grammar):
    new_non_terminals = []
    check = True

    while(check):
        check = False
        non_terminals = list(grammar.keys())
        for A in non_terminals:
            productions = grammar[A]
            # prefixes = common_prefix(productions)
            temp, itr = left_factoring_on_rule(A, productions, new_non_terminals)
            check = check or itr
            for keys in temp:
                grammar[keys] = temp[keys]

            # print("grammar : {}".format(grammar))

    return grammar

def left_factoring_on_rule(non_terminal, productions, new_non_terminals):
    prefixes = common_prefix(productions)
    temp_grammar = {}
    if prefixes:
        # check = True
        temp = prefix_rules(prefixes, productions)
        temp_grammar[non_terminal] = []

        for prefix in temp:
            rules = temp[prefix]

            if len(rules) > 1:
                new_non_terminal = create_new_non_terminal(non_terminal, new_non_terminals)
                temp_grammar[new_non_terminal] = []
                new_non_terminals.append(new_non_terminal)
                temp_grammar[non_terminal].append(prefix + new_non_terminal)

                for terms in rules:
                    t = terms[len(prefix):]
                    if t:
                        temp_grammar[new_non_terminal].append(terms[len(prefix):])
                    else:
                        temp_grammar[new_non_terminal].append("ε")
                
            else:
                temp_grammar[non_terminal].append(rules[0])

        # for production in productions:
        #     present = False
        #     for key in temp:
        #         for right in temp[key]:
        #             if right == production:
        #                 present = True

        #     if not present:
        #         temp_grammar[production] = production       
        #         # print("prodcution : {}".format(production))
        return temp_grammar, True

    else:
        temp_grammar[non_terminal] = productions
        return temp_grammar, False


def main():

    # # Debugging Part

    # prod = ['abB', 'acD', 'baD', 'bB', 'cDE', 'cDF', 'k']
    # li_of_pre = ['a', 'b', 'cD']
    # new = ["A'", "A''", "B'"]
    # print("new terminal = {}".format(create_new_non_terminal("A", new)))

    # p = prefix_rules(li_of_pre, prod)
    # print("rules = {}".format(p))
    
    # prod = ['abB', 'acD', 'baD', 'bB', 'cDE', 'cDF', 'k', 'zc']
    # new = []
    # print("left factoring on rule = {}".format(left_factoring_on_rule("A", prod, new)))

    
    # common_prefix(prod)
    # inp = ["adB", "aBc", "adc", "bc"]
    # prefix_rules(["a"], inp)
    
    # left_factoring(input_grammar)
    # print_grammar(input_grammar)
    # common_prefix(input_grammar)
    # left_factoring(input_grammar)

    # input_grammar = {
    #     '': []
    # }

    input_grammar = {
        'A': ['a', 'ab', 'abc', 'abcd', 'abcde']
    }
    # input_grammar = {
    #     'A': ['abB', 'acD', 'baD', 'bB', 'cDE', 'cDF', 'k', 'zc']
    # }
    # input_grammar = {
    # 'A': ['abB', 'acD', 'baD', 'bB', 'cDE', 'cDF', 'k']
    # }

    # input_grammar = {
    #     "A": ["ab1", "ab2", "ab3", "ac1", "ac2"],
    #     "B": ["bd1", "bd2", "bf1"],
    #     "C": ["ce1", "ce2"]
    # }
    
    # input_grammar = {
    #     'A': ['abB', 'abc', 'cA','cD'],
    #     'X': ['xY', 'xZ']
    # }

    # input_grammar = {
    #     'A': ["adB", "aBc", "adc", "bc"]
    # }

    print("Input Grammar: ")
    print_grammar(input_grammar)
    print()
    left_factored_grammar = left_factoring(input_grammar)
    print("Output Left Factored Grammar: ")
    print_grammar(left_factored_grammar)

if __name__ == "__main__":
    main()

