import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences#dict of words as keys and a list of lists having the feauters of each frame in small lists 
        self.hwords = all_word_Xlengths# same as self.words but instead of the list of lists we will have a tuple of  a numpy array of features, and a list of the lengths of frame sequences 
        self.sequences = all_word_sequences[this_word]#getting the needed word list of list sequences 
        self.X, self.lengths = all_word_Xlengths[this_word]#getting the needed word numpy sequences and lengths 
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose
        self.state_nums=range(self.min_n_components,self.max_n_components+1)#added this line here as the states_num list will be used in all model selectors

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):#will be used later to create the models and to also test them
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on BIC scores
        min_score=float("inf")
        best_model=None
        try:
            for state_num in self.state_nums:
                model=self.base_model(state_num)
                logL=model.score(self.X,self.lengths)
                #parameters are made of the sum of three components as per forum:
                #1. initial state which is simply N
                #2. transition states which is N*(N-1) considering a full mesh topology and we want the connections number
                #3. Emission probabilities = numStates*numFeatures*2 = numMeans+numCovars
                #sum is N**2 -N +N +2*N*features -1 =N**2+2*N*features -1 "after searching the number of features in hmmgaussian can be brought by model.n_features"
                #and N is the state_num
                p=state_num**2+2*state_num*model.n_features-1
                score=-2*logL + p* math.log(state_num)
                if score < min_score: #getting minimum score
                    min_score=score
                    best_model=model
        except:
            pass
        #if initial value of max_score_index was still false, i.e. there was an exception, then return n_contant, else return the bext model
        
        if best_model:
            return best_model
        
        return self.base_model(self.n_constant)        

class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    https://pdfs.semanticscholar.org/ed3d/7c4a5f607201f3848d4c02dd9ba17c791fc2.pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on DIC scores
        max_score=float("-inf")
        best_model=None
        try:
            for state_num in self.state_nums:
                model=self.base_model(state_num)
                logL=model.score(self.X,self.lengths)
                score_sum=0
                for word in self.words:#looping on all words as words are keys in the dictionary
                    if word == self.this_word:#skip the used word 
                        continue
                    other_X,other_lengths=self.hwords[word]#getting the numpy array and lengths of the other words
                    score_sum+=model.score(other_X,other_lengths)#using the same model since we are using the same state_num but for different words X numpy and lengths
                avg_score=score_sum/(len(self.words)-1) #subtracted one to ignore the "this_word" word
                dis_score=logL-avg_score
                if dis_score > max_score:
                    max_score=dis_score
                    best_model=model                  
        except:
            pass
        #if initial value of max_score_index was still false, i.e. there was an exception, then return n_contant, else return the best model
        if best_model:
            return best_model
        
        return self.base_model(self.n_constant)        

class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # TODO implement model selection using CV
        n_comp_scores=[]
        max_score_index=False
        split_method = KFold(random_state=self.random_state)
        
        try:
            for state_num in self.state_nums:
                model=self.base_model(state_num)
                k_fold_scores=[]
                for cv_train_idx, cv_test_idx in split_method.split(self.sequences):
                    test_X, test_length = combine_sequences(cv_test_idx, self.sequences)#this will bring the test sequences and test lengths 
                    k_fold_scores.append(model.score(test_X, test_length))
                n_comp_scores.append(np.mean(k_fold_scores))
            n_comp_scores=list(n_comp_scores)
            max_score_index=n_comp_scores.index(max(n_comp_scores))
        except:
            pass
        #if initial value of max_score_index was still false, i.e. there was an exception, then return n_contant, else return the bext model
        if max_score_index:
            return self.base_model(self.state_nums[max_score_index])
        
        return self.base_model(self.n_constant)
                
