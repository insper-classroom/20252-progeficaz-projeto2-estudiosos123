

def load_template(filename):
    with open(f'templates/{filename}', 'r', encoding='utf-8') as f:
        return f.read()