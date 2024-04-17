


def the_final_prompt(message):
    s1 = "Based on the message given to you, create a new question.\n"
    s1 += f"Message: {message} \n"
    s1 + " Modify the Message in a best way \n"
    return s1

def check_template(user_query):
    s1 = "Check in the  given USER_QUERY whether the user has given its own name or not . \n"
    s1 +=  "Answer it only in yes or no .\n"
    return s1