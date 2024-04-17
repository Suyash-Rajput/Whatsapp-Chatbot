


def the_final_prompt(message, prompt_function):
    if  prompt_function != "":
        prompt_function(message)
    #     return name_template(message)
    # elif  state == "JOB-ID":
    #     return name_template(message)
    # elif  state == "Current-Salary":
    #     return name_template(message)
    # elif  state == "Notice-period":
    #     return name_template(message)
    # elif  state == "Resume":
    #     return name_template(message)
    # elif  state == "Email":
    #     return name_template(message)
    # elif  state == "Invite":
    #     return name_template(message)
    # elif  state == "Email":
    #     return message
    else:
        return default(message)


def jcheck_template(user_query):
    s1 = "Check in the  given USER_QUERY whether the user has given its own name or not . \n"
    s1 +=  "Answer it only in yes or no .\n" 
    return s1

def default(message):
    s1 = "Based on the message given to you, create a new question.\n"
    s1 += f"Message: {message} \n"
    s1 + " Modify the Message in a best way \n"
    return s1