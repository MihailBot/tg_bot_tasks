def short_sent(sent):
    short_sent = None
    if len(sent) > 30:
        index = len(sent) - 1
        list_sent = list(sent)
        while len(list_sent) > 30:
            list_sent.pop(index)
            index -= 1
        for i in range(3):
            list_sent.append('.')
        short_sent = ''.join(list_sent)
    else:
        short_sent = sent
        
    return(short_sent)

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


