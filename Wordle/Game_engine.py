from colorama import init, Fore, Back, Style
import random 

init()

# Her skal vi importere en fil med en masse ord, men for at teste bruger jeg et array 
word_list = ['Kaste','faste','klask','taske','falsk','snyde','flyde','tylle']

# loop kan bare sætte = med spillet stadie så det kun starter når det f.eks er ens tur 
loop = True
while loop:
    print('Welcome to game')
    command=input()
    if command == 'q':
        loop=False
    elif command == 'y':
        game_round=0
        #word=random.choice(word_list)
        word='kasse'
        
        print(game_round)
        print(word)
        while game_round <= 6:
            attempt=input()
            attempt_char = [char for char in attempt]

            if word == attempt:
                print('Du Gjorde Det!!!')
                loop=False
                break 
            else: 
                word_char = [char for char in word]
                word_dup = word
                result = [0, 0, 0, 0, 0]
                for index, char in enumerate(word):
                    #print(word_char, attempt_char)
                    if attempt_char[index] in word_char:
                        result[index] = 'Y'
                        word_char[word_char.index(attempt_char[index])] = '0'
                        
                        if attempt_char[index] == char:
                            result[index] = 'G'
                            word_char[index] = 0
                            
                    else:
                        result[index] = 'R'
                print(result)


