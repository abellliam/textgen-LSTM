from Sequence_generator import gen_seq
from Sequence_generator import load as load_txt
from Sequence_generator import save as save_txt
from Model import create_model

from pickle import load
from keras.models import load_model
from keras.utils import to_categorical
from keras.preprocessing.sequence import pad_sequences

import random
from datetime import datetime


def create_seq_and_model(txt_filename, seq_filename, model_filename, units, epochs):
    gen_seq(txt_filename, seq_filename)
    create_model(seq_filename, model_filename, units, epochs)


def determine_seed(seed, use_seed, seq_filename):
    if type(seed) == str and use_seed:
        return seed
    elif not seed:
        # generate random number with random seed
        random.seed(datetime.now())
    else:
        # generate random number with seed
        random.seed(seed)
    # generate seed with random number
    sequence_text = load_txt(seq_filename)
    sequences = sequence_text.split('\n')
    while True:
        sequence = sequences[random.randint(1, len(sequences))]
        # make sure seed starts with a capital letter
        if sequence[0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            return sequence


def determine_repetition(line, num_reps):
    words = line.split()
    sentencelist = list()
    for word in words:
        wordlist = [word]
        for word_inner in words[words.index(word)+1:]:
            wordlist.append(word_inner)
            sentence = ' '.join(wordlist)
            identical_sentences = [x for x in sentencelist if x == sentence]
            if len(identical_sentences) == num_reps:
                return True
            sentencelist.append(sentence)
    return False


def gen_text(model, mapping, seed='', use_seed=False, seq_length=10, n_chars=1000, seq_filename=''):
    in_text = determine_seed(seed, use_seed, seq_filename)
    for j in range(n_chars):
        encoded = [mapping[char] for char in in_text]
        encoded = pad_sequences([encoded], maxlen=seq_length, truncating='pre')
        encoded = to_categorical(encoded, num_classes=len(mapping))
        # encoded = encoded.reshape(1, encoded.shape[0], encoded.shape[1])
        yhat = model.predict_classes(encoded, verbose=0)
        out_char = ''
        for char, index in mapping.items():
            if index == yhat:
                out_char = char
                break
        in_text += out_char
        if out_char in ['.', '!', '?']:
            break
    if determine_repetition(in_text, num_reps=3):
        print('REJECTED ' + in_text)
        return gen_text(model, mapping, seq_length=seq_length, n_chars=n_chars, seq_filename=seq_filename)
    else:
        return in_text


txt_filename = 'nursery_rhymes_clean.txt'
seq_filename = 'sequences.txt'
model_filename = 'model.h5'
mapping_filename = 'mapping.pkl'
output_filename = 'output.txt'

# create_seq_and_model(txt_filename, seq_filename, model_filename, 250, 50)
model = load_model(model_filename)
mapping = load(open(mapping_filename, 'rb'))

seed_list = ['The king', 'A queen', 'Maid\'s', 'I wouldn\'t', 'What is the', 'Once on a']
out_list = list()
num_text = 50

# for seed in seed_list:
#    out_list.append(gen_text(model, mapping, seed, use_seed=True, seq_filename=seq_filename))

for i in range(num_text):
    out_list.append(gen_text(model, mapping, seq_filename=seq_filename))

save_txt(out_list, 'output.txt')





