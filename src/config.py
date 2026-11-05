"""Validation of the experimental scope before any data selection."""
def validate(config):
    data = config['data']
    mode, classes = data['mode'], data['classes']
    if mode not in ('single', 'all'):
        raise ValueError('mode must be single or all')
    if not classes or len(set(classes)) != len(classes) or set(classes) - set('ABCDE'):
        raise ValueError('classes must be unique and within A–E')
    if mode == 'single' and len(classes) != 1:
        raise ValueError('single requires exactly one road class')
    if mode == 'all' and set(classes) != set('ABCDE'):
        raise ValueError('all requires A–E')
    return config
