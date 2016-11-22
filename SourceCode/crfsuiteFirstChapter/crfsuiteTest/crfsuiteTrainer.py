import crfsuite
import os.path
import sys


class Trainer(crfsuite.Trainer):

    def __init__(self, pathToTrainingFile):
        if not os.path.isfile(pathToTrainingFile):
            raise FileNotFoundError(pathToTrainingFile)
        self.pathToTrainingFile = pathToTrainingFile
        
        super().__init__()
        

    # @override
    def message(self, s):
        sys.stdout.write(s)

    def readModelParameter(self):
        with open(self.pathToTrainingFile, "r") as fil:
            xseq = crfsuite.ItemSequence()
            labels = crfsuite.StringList()
            
            for line in fil:
                # An empty line presents an end of a sequence.
                line = line.strip()
                if not line:
                    self.append(xseq, labels, 0)  # add to training data
                    
                    xseq = crfsuite.ItemSequence()
                    labels = crfsuite.StringList()
                    continue
                
                fields = line.split('\t')
                item = crfsuite.Item()  # item contains all features of one x
                for field in fields[1:]:
                    item.append(crfsuite.Attribute(field))
                xseq.append(item)
                labels.append(fields[0])

    def trainModel(self):
        # Use L2-regularized SGD and 1st-order dyad features (bigram features).
        self.select('l2sgd', 'crf1d')
        # Set the coefficient for L2 regularization to 0.1
        self.set('c2', '0.1')
        # also feature with negative values
        self.set("feature.possible_states", "1")
    
        self.readModelParameter()
                 
        self.train("lillteExample.model", -1)

if __name__ == '__main__':
    trainer = Trainer("train.txt")  # Trainer("train.txt")
    trainer.trainModel()
