from Sequence_generator import save as save_txt
from Generate_text import create_seq_and_model, gen_text

from pickle import load
from keras.models import load_model

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
num_text = 10

for seed in seed_list:
    out_list.append(gen_text(model, mapping, seed, use_seed=True, seq_filename=seq_filename))

for i in range(num_text):
    out_list.append(gen_text(model, mapping, seq_filename=seq_filename))

save_txt(out_list, 'output.txt')
