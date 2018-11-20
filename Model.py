from Sequence_generator import load
from pickle import dump
import numpy as np
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, LSTM


def create_model(seq_filename, model_filename, units, epochs):
    text = load(seq_filename)
    lines = text.split('\n')
    chars = sorted(list(set(text)))
    mapping = dict((c, i) for i, c in enumerate(chars))
    sequences = list()

    for line in lines:
        encoded_seq = [mapping[char] for char in line]
        sequences.append(encoded_seq)
    vocab_size = len(mapping)
    sequences = np.array(sequences)
    X, y = sequences[:, :-1], sequences[:, -1]
    sequences = [to_categorical(x, num_classes=vocab_size) for x in X]
    X = np.array(sequences)
    y = to_categorical(y, num_classes=vocab_size)

    model = Sequential()
    model.add(LSTM(units, input_shape=(X.shape[1], X.shape[2])))
    model.add(Dense(vocab_size, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X, y, epochs=epochs, verbose=2)
    model.save(model_filename)
    dump(mapping, open('mapping.pkl', 'wb'))