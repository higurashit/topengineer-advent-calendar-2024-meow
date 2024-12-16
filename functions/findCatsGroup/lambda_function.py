import random

def lambda_handler(event, context):

    names = [
        'Alice', 'Bob', 'Carol', 'Charlie', 'Dave', 'Ellen', 'Eve', 'Frank', 'Isaac', 'Ivan',
        'Justin', 'Mallory', 'Marvin', 'Mallet', 'Matilda', 'Oscar', 'Pat', 'Peggy', 'Victor',
        'Plod', 'Steve', 'Trent', 'Trudy', 'Walter', 'Zoe', 'Darwin'
    ]
    my_cats = []
    my_cats_length = random.randrange(6) + 1 # 1～7匹
    
    for cat in range(my_cats_length):
        name = pick_name(names, my_cats)
        my_cats.append(name)

    return {
        "my_cats": my_cats
    }

def pick_name(names, ignores):
    name = random.choice(names)
    if name in ignores:
        return pick_name(names, ignores)
    return name