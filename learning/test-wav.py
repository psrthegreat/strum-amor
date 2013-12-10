#call to test a wav
import pickle
from itertooks import imap, groupby
from operator import itemgetter
#load a trained model
model = pickle.load("trained/");
#BRAD ADD HERE
testex = getfeature("test1.wav");
outputseries = model.predict(testex);
outputcomp = list(imap(itemgetter(0), groupby(outputseries)));
print outputcomp


