import utils 
from datetime import datetime, timezone
from chatbot import prompts as pt

BASE_DIR = Path(__file__).resolve().parent
parent_dir = os.path.dirname(BASE_DIR)

state_transition_obj = {}
mcw_name_2_state = {}

def load_states(flow):
    state_transition_pfn = os.path.join(parent_dir, 'json_files/state_transition.json')
    global state_transition_obj
    global mcw_name_2_state
    state_transition_obj = utils.read_json_file(state_transition_pfn)
    state_transition_states = state_transition_obj["states"]
    for next_state in state_transition_states:
        name = state_transition_states[next_state]["name"]
        mcw_name_2_state[name] = next_state
    return


def fill_initial_state(session):
    print("Entering fill_initial_state: ", session)
    state_transition_path =  os.path.join(parent_dir, 'json_files/state_transition.json')
    state_transition = utils.read_json_file(state_transition_path)
    questions_list = state_transition["states"]['S0']
    session['__check_file'] = questions_list['check_file']
    session["__user_pref"] = questions_list['outgoing'][0]['user_pref']
    session["__state"] = questions_list['id']
    session["__target_state"] =  questions_list['outgoing'][0]['id']
    session["__prompt"] = questions_list['outgoing'][0]["prompt"]
    session['__question'] = state_transition["config"][session['__target_state']]['question']
    print("Exiting fill_initial_state(): ", session)
    return

def find_state(session):
    print("Entering find_state: ", session)
    load_states(flow)
    state_transition_config = state_transition_obj["config"]
    mcw_name = ""
    for next_filter in state_transition_config:
        if len(session[next_filter]) != 0:
            mcw_name += next_filter
    my_state = mcw_hint_2_state[mcw_name]
    print("Exiting find_state(): ", my_state)
    return my_state
        
        
def set_target_state(session):
    print("Entering set_target_state() search_query: ", session)
    global state_transition_obj
    current_state = session["__state"]
    target_state = state_transition_obj["states"][current_state]["outgoing"][0]
    ts, up, q = "", "", ""
    if "user_pref" in target_state.keys():
        up = state_transition_obj["states"][current_state]["outgoing"][0]["user_pref"]
        if up != "":
            ts = target_state["id"]
            q = state_transition_obj["config"][up]["question"]
    session["__target_state"] = ts
    session["__user_pref"] = up
    session['__check_file'] = state_transition_obj["states"][ts]['check_file']
    session["__question"] = q
    session["__prompt"] = state_transition_obj["states"]["outgoing"][0]["prompt"]
    print("Exiting set_target_state() search_query: ", session)
    return


def update_context(session, query):
    session_started_time = session.get('time_started', None)
    check_status =  pt.check_template(query, session["__check_file"])
    if check_status.strip().lower() == "no":
        return 
    time_diff = 12
    if session_started_time is not None:
        time_diff = utils.print_time_taken(session['time_started'], datetime.now())        
    if 'To' in session and session['To'] == recipient_number and time_diff < 10:
        if len(session) == 0:
           fill_initial_state(session)
        session["__state"] = find_state(session)
        set_target_state(session)
    else: 
        session['time_started'] = datetime.now()  
        fill_initial_state(session) 
    session['To'] = recipient_number
    return