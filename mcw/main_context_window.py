import utils 

BASE_DIR = Path(__file__).resolve().parent
parent_dir = os.path.dirname(BASE_DIR)

state_transition_obj = {}
mcw_hint_2_state = {}

def load_states(flow):
    state_transition_pfn = os.path.join(parent_dir, 'json_files/state_transition.json')
    global state_transition_obj
    global mcw_hint_2_state
    state_transition_obj = utils.read_json_file(state_transition_pfn)
    state_transition_states = state_transition_obj["states"]
    for next_state in state_transition_states:
        mcw_hint = state_transition_states[next_state]["mcw_hint"]
        mcw_hint_2_state[mcw_hint] = next_state
    return


def fill_initial_state(session):
    state_transition_path =  os.path.join(parent_dir, 'json_files/state_transition.json')
    state_transition = utils.read_json_file(state_transition_path)
    questions_list = state_transition["states"]['S0']
    session['id'] = questions_list['id']
    session['check_file'] = questions_list['check_file']
    
    for key, values in questions_list['conditions'].items():
        session[key] = values

    for key, values in questions_list['outgoing'].items():
        session[key] = values


def find_state(session):
    print("Entering find_state: ", context_window)
    # if len(state_transition_obj) == 0:
    load_states(flow)
    state_transition_config = state_transition_obj["config"]
    mcw_hint = ""
    for next_filter in state_transition_config:
        if next_filter == "feedback":
            continue
        if len(context_window[next_filter]) != 0:
            mcw_hint += next_filter
    if mcw_hint == "":
        mcw_hint = "start"
    if len(mcw_hint_2_state) == 0:
        load_states(flow)
    my_state = mcw_hint_2_state[mcw_hint]
    print("Exiting check_state2(): ", my_state)
    return my_state
        

def update_context(session, context):
    if len(session) == 0:
       fill_initial_state(session)
    currect_state = find_state(session)