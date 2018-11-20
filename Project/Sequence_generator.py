def load(filename):
    file = open(filename, 'r')
    out_text = file.read()
    file.close()
    return out_text


def save(lines, filename):
    data = '\n'.join(lines)
    file = open(filename, 'w')
    file.write(data)
    file.close()


def gen_seq(in_filename, out_filename):
    length = 10
    text = load(in_filename)
    tokens = text.split()
    text = ' '.join(tokens)
    sequences = list()
    for i in range(length, len(text)):
        seq = text[i-length:i+1]
        sequences.append(seq)
    save(sequences, out_filename)
