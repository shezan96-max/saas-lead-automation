def calculate_score(budget : int, message : str):
    score = 0

    # Budget weight
    if budget >= 5000:
        score += 40
    elif budget >= 2000:
        score += 30
    elif budget >= 1000:
        score += 20
    else:
        score += 10
    
    # Message intent weight
    keywords = ["urgent","immediately","asap","need now","ready"]

    message = message.lower()

    if any(word in message for word in keywords):
        score += 30
    else:
        score += 10

    # Message length weight (serious clients write more)
    if len(message) > 100:
        score += 20
    else:
        score += 10

    return score