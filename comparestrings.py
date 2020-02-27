# Not working properly

def compare_words(inpt, word):
    if inpt == word: # No errors.
        return 'equal'
    else: # There are errors.  
        if (len(word) < 5 and inpt != word) or (abs(len(word) - len(inpt)) > 3):
            return 'different'

        # Check for mistakes.
        _inpt = list(inpt)
        _word = list(word)
        mistakes = 0
        done = False

        # More letters than what they should be.
        # The idea is to remove them and then compare both lists...
        # ...to see if they match.
        if len(_inpt) > len(_word):
            while not done:
                for i in range(len(_word)):
                    if _inpt[i] != _word[i]:
                        _inpt.pop(i)
                        mistakes += 1
                        break
                else:
                    done = True
                    mistakes += abs(len(_inpt) - len(word))
                    break
        
        # Less letters than waht they should be.
        # The idea is to add them, then see whether both...
        # ...strings match.
        elif len(_inpt) < len(_word):
            while not done:
                for i in range(len(_inpt)):
                    if _inpt[i] != _word[i]:
                        _inpt.insert(i, _word[i])
                        mistakes += 1
                        break
                    
                    if len(_inpt) == len(_word):
                        done = True
                        break

                    if i+1 < len(_word) and i == len(_inpt) -1:
                        _inpt.append(_word[i+1])
                        mistakes += 1
                        break

        # The exact number of letters.
        # The idea is to remove letters from both strings...
        # ...then see if they match.
        else:
            while not done:
                for i in range(len(_inpt)):
                    if _inpt[i] != _word[i]:
                        _inpt.pop(i)
                        _word.pop(i)
                        mistakes += 0.5
                        break

                    if _inpt == _word:
                        done = True
                        break
                
                if len(_inpt) == 0:
                    done = True

        if mistakes < 3:
            return ('similar', word)
        else:
            return 'different'
