import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set for each video in the data and return them in lists 

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood "each dictionary represents a video inside the data frame
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id "listing the highest score word in each video "
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    # TODO implement the recognizer
    # return probabilities, guesses
    probabilities = []
    guesses = []
    for video in range(0, len(test_set.get_all_Xlengths())):
        X, lengths = test_set.get_item_Xlengths(video)
        best_score = float("-inf") # max score
        best_word = None # max score word
        probabilities_dict = {}
        score = float("-inf")#initializing the score value
        for word, model in models.items():
            try:
                # Get model score
                score = model.score(X, lengths)#using the model.score directly for the word in the loop
                if score > best_score:
                    best_score=score
                    best_word=word
            except:
                pass
                


            probabilities_dict[word] = score
        guesses.append(best_word)
        probabilities.append(probabilities_dict)
    return probabilities, guesses
