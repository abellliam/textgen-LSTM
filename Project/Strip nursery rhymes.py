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


def strip_text(in_filename, out_filename):
    text = load(in_filename)
    tokens = text.split('\n')
    save(tokens, 'test.txt')
    for token in tokens:
        remove = True
        for char in token:
            if char == '_':
                break
            elif char in 'abcdefghijklmnopqrstuvwxyz':
                remove = False
                break
        if remove:
            tokens.remove(token)
        for i in range(len(token)):
            if token[i] != ' ' and not remove:
                tokens[tokens.index(token)] = token[i:]
                break
    save(tokens, out_filename)


strip_text('nursery_rhymes.txt', 'nursery_rhymes_clean.txt')
