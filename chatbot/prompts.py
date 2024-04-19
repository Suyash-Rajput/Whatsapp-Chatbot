from .Bigquery import GCP_big_query

# 
company_name = "Mars Consulting"
dataset_id = "Chatbot_messages_dataset"
table_id = "Jobs_data"


def the_final_prompt(message, prompt_function):
    if  prompt_function == "job_template":
        print("In job template")
        return job_template(message)
    else:
        return default(message)


def check_template(user_query, question):
    s1 = f"User Query: {user_query}\n"
    s1 += f"Question: {question}\n"
    s1 += "Please evaluate the given user query to determine if it can effectively answer the provided question.\n"
    s1 += "Respond with 'yes' if the query is suitable for answering the question, otherwise respond with 'no'.\n"
    return s1
     
def job_template(message):
    gcp = GCP_big_query()
    rows = gcp.retrieve(table_id, dataset_id, company_name)
    s1 = "Act as experienced recruiter .\n"
    for row_tuple in rows:
        prompt = ' Company name'   
        count = 0
        for row_data in row_tuple:
            count +=1
            if count == 1: 
               prompt +=' ' + str(row_data)
            elif count == 2:
                prompt += ' ' + ' JOB-Location  '  + str(row_data)
            elif count == 3:
                prompt += ' ' + ' JOB-ID  '  + str(row_data)
            elif count == 4:
                prompt += ' ' + ' JOB-URL '   + str(row_data)
        s1 += f"Message: {message}{prompt} \n"
    s1 += "Based on the Message given to you, create a new question which is in proper formet like .\n"
    s1 += "JOB_ID : JOB-ID  LOCATION :  JOB-Location JOB_URL : JOB-URL \n"
    s1 += "for all the give JOB-ID   JOB-Location  JOB-URL\n"
    s1 + " Modify the Message in a best way as a recruiter \n"
    return s1


def default(message):
    s1 = "Act as experienced recruiter .\n"
    s1 += f"Message: {message} \n"
    s1 += "Based on the Message given to you, create a Question .\n"
    s1 + " create a Question in a best way such that it is asked in chatbot . \n"
    s1 += " There should be any tags other than question . \n"
    return s1