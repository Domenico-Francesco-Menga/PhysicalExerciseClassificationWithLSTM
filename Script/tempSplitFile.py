import numpy as np
from keras.layers import Dense
from keras.layers import LSTM
from keras.models import Sequential
from numpy import hstack
import lista

#split delle sequenze
def split_sequences(sequences,output, n_steps, n_shift):
    X, y = list(), list()
    shift = 0
    i = 0
    nStepInTarget = 0
    while i < len(sequences):
        #for i in range(len(sequences)):
        # find the end of this pattern
        end_ix = i + n_steps
        # check if we are beyond the dataset
        if end_ix > len(sequences) - 1:
            break
        # gather input and output parts of the pattern
        seq_x, seq_y = sequences[shift:end_ix, :], target[nStepInTarget]#sequences[end_ix, :]
        X.append(seq_x)
        y.append(seq_y)
        shift += n_shift
        i += n_shift
        nStepInTarget += 1

    return np.array(X), np.array(y)

#arrayVal = list(np.loadtxt("prova.txt"))
in_seq1 = np.array(np.genfromtxt(r"C:\Users\menga\OneDrive\Desktop\\aaa.csv", delimiter=",",dtype=float))

out = [[0.0,0.0,1.0],[1.0,0.0,0.0],[1.0,0.0,0.0],[0.0,1.0,0.0]]
out_seq = np.array(out)
# horizontally stack columns
dataset = np.vstack((in_seq1))
target = np.vstack(out_seq)


# choose a number of time steps
n_steps_in, shiftBetweenMatrrix = 35, 3
# covert into input/output
print(len(dataset))
X, y = split_sequences(dataset,target, n_steps_in,shiftBetweenMatrrix)

# summarize the data
print(len(X))

for i in range(len(X)):
	print(X[i], y[i])
'''

# caricamento dei file di training in matrici numpy
array_from_file_squat_train = np.loadtxt("prova.txt.txt", dtype=float)
array_from_file_squat_train = array_from_file_squat_train.reshape((len(array_from_file_squat_train), 1))



print(array_from_file_squat_train)
'''
