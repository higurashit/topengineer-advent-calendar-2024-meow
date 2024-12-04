import random

def lambda_handler(event, context):
    return {
        "myCats": list(range(random.randrange(10)))
    }