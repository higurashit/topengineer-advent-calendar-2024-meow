import random

def lambda_handler(event, context):
    return {
        "my_cats": list(range(random.randrange(10)))
    }