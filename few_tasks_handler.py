
def sort_few_tasks(user_tasks):
    
    spis_few_buttons = []
    letters = []
            
    inp_list = list(user_tasks)
    ready_word = ''
    while ',' in inp_list:
        pop = ''
        while pop != ',':
            pop = inp_list.pop()
            letters.append(pop)
                    
        letters.pop()
        letters.reverse()

        if letters[0] == ' ':
            letters.pop(0)
                
        ready_word = ''.join(letters)
        spis_few_buttons.append(ready_word)
        letters.clear()
                
    for i in range(len(inp_list)):
        pop = inp_list.pop()
        letters.append(pop)
                    
    letters.reverse()
    ready_word = ''.join(letters)
    spis_few_buttons.append(ready_word)
    letters.clear()
    spis_few_buttons.reverse()
    return spis_few_buttons


