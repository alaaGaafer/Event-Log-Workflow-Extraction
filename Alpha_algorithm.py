from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from Event_logs import event_log1,event_log2,event_log3,event_log4
import networkx as nx


def choose_event_log():
    print("Choose an event log:")
    print("1. Example 1")
    print("2. Example 2")
    print("3. Example 3")
    print("4. Assignment 2 event log")
    print("5. Enter Custom Event Log")

    choice = input("Enter the number of your choice: ")

    if choice == '1':
        Event_log = event_log1
        # Add timestamps to event_log
        start_time = datetime.now()
        for event in Event_log:
            event['timestamp'] = start_time
            start_time += timedelta(minutes=15)
    elif choice == '2':
        # Load built-in event log 2
        Event_log = event_log2
        # Add timestamps to event_log
        start_time = datetime.now()
        for event in Event_log:
            event['timestamp'] = start_time
            start_time += timedelta(minutes=15)
    elif choice == '3':
        # Load built-in event log 3
        Event_log = event_log3
        # Add timestamps to event_log
        start_time = datetime.now()
        for event in Event_log:
            event['timestamp'] = start_time
            start_time += timedelta(minutes=15)
    elif choice == '4':
        # Load built-in event log 3
        Event_log = event_log4
        # Add timestamps to event_log
        start_time = datetime.now()
        for event in Event_log:
            event['timestamp'] = start_time
            start_time += timedelta(minutes=15)
    elif choice == '5':
        # Enter custom event log
        Event_log = enter_custom_event_log()
    else:
        print("Invalid choice. Please choose a number between 1 and 4.")
        return

    return Event_log


def enter_custom_event_log():
    # Let the user enter a custom event log row by row
    Event_log = []
    print("Enter your custom event log. Type 'done' to finish.")

    while True:
        event_id = input("Event ID: ")
        if event_id.lower() == 'done':
            break

        # Validate that event_id is an integer
        while not event_id.isdigit():
            print("Invalid input. Event ID must be an integer.")
            event_id = input("Event ID: ")

        case_id = input("Case ID: ")

        # Validate that case_id is an integer
        while not case_id.isdigit():
            print("Invalid input. Case ID must be an integer.")
            case_id = input("Case ID: ")

        activity = input("Activity: ")

        # Validate that activity is a letter
        while not activity.isalpha():
            print("Invalid input. Activity must be a letter.")
            activity = input("Activity: ")

        while True:
            timestamp_str = input("Timestamp (YYYY-MM-DDTHH:mm:ss like :2023-12-14T08:25:00): ")

            try:
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S")
                break  # Exit the timestamp input loop if the format is correct
            except ValueError:
                print("Invalid timestamp format. Please use the format YYYY-MM-DDTHH:mm:ss.")

        Event_log.append(
            {'event_id': int(event_id), 'case_id': int(case_id), 'activity': activity, 'timestamp': timestamp})

    return Event_log


def extract_workflow(Event_log):
    # Sort the event log based on timestamp
    sorted_log = sorted(Event_log, key=lambda x: (x['case_id'], x['timestamp']))

    # Initialize variables
    current_case_id = None
    current_activities = []

    workflow_dict = {}

    # Loop through the sorted log
    for Event in sorted_log:
        case_id = Event['case_id']
        activity = Event['activity']
        timestamp = Event['timestamp']

        if case_id != current_case_id:
            # Save the activities for the previous case_id
            if current_case_id is not None:
                workflow_dict[f'case_{current_case_id}'] = current_activities

            # Start a new list for the current case_id
            current_case_id = case_id
            current_activities = [activity]
        else:
            current_activities.append(activity)

    # Add the last case_id
    if current_case_id is not None:
        workflow_dict[f'case_{current_case_id}'] = current_activities

    # Remove duplicate lists based on order
    unique_workflow_dict = {}
    seen_lists = set()

    for case_id, activities in workflow_dict.items():
        activities_tuple = tuple(activities)
        if activities_tuple not in seen_lists:
            seen_lists.add(activities_tuple)
            unique_workflow_dict[case_id] = activities

    return unique_workflow_dict


def print_input_output_transitions(Workflow_result):
    Input_transitions = set()
    Output_transitions = set()

    for case_id, activities in Workflow_result.items():
        if activities:
            Input_transitions.add(activities[0])
            Output_transitions.add(activities[-1])

    return Input_transitions, Output_transitions


def find_direct_followers(Workflow_result):
    Direct_followers = []

    for case_id, activities in Workflow_result.items():
        if len(activities) > 1:
            for i in range(len(activities) - 1):
                pair = (activities[i], activities[i + 1])
                if pair not in Direct_followers:
                    Direct_followers.append(pair)

    # Sort the list based on the first element of each pair
    Direct_followers.sort(key=lambda x: x[0])
    return Direct_followers


def find_causality_parallelism(Direct_followers):
    Causality_relations = []
    Parallel_relations = []

    for relation in Direct_followers:
        reverse_relation = (relation[1], relation[0])

        if reverse_relation not in Direct_followers:
            Causality_relations.append(relation)
        else:
            if reverse_relation not in Parallel_relations and relation not in Parallel_relations:
                Parallel_relations.append(relation)

    return Causality_relations, Parallel_relations


def find_exclusiveness(Workflow_result, Direct_followers):
    Exclusive_relations = []
    Unique_transitions = []

    for case_id, transitions in Workflow_result.items():
        for i in range(len(transitions)):
            if transitions[i] not in Unique_transitions:
                Unique_transitions.append(transitions[i])
    Unique_transitions = sorted(Unique_transitions)
    for i in range(len(Unique_transitions)):
        for j in range(i + 1, len(Unique_transitions)):
            relation = (Unique_transitions[i], Unique_transitions[j])

            if relation not in Direct_followers and relation not in Exclusive_relations:
                Exclusive_relations.append(relation)

    return Exclusive_relations, Unique_transitions


def footprint_matrix(Direct_relations, Exclusive_relations, Causality_relations, Parallel_relations):
    all_transitions = sorted(set(
        transition
        for relations in [Direct_relations, Exclusive_relations, causality_relations]
        for relation in relations
        for transition in relation
    ))

    matrix_size = len(all_transitions)
    matrix = [[' ' for _ in range(matrix_size + 1)] for _ in range(matrix_size + 1)]

    # Add column headers
    matrix[0][1:] = all_transitions

    # Add row headers and fill the matrix
    for i, transition_i in enumerate(all_transitions):
        matrix[i + 1][0] = transition_i
        for j, transition_j in enumerate(all_transitions):
            reverse_relation = (transition_j, transition_i)
            if (transition_i, transition_j) in Causality_relations:
                matrix[i + 1][j + 1] = '->'
                matrix[j + 1][i + 1] = '<-'
            if (transition_i, transition_j) in Exclusive_relations or transition_i == transition_j or \
                    reverse_relation in Exclusive_relations:
                matrix[i + 1][j + 1] = '#'
            if (transition_i, transition_j) in Parallel_relations or reverse_relation in Parallel_relations:
                matrix[i + 1][j + 1] = '||'

    return matrix


def find_Xw(Causality_relations, Parallel_relations):
    Xw2 = [Causality_relations[0]]
    Yw2 = [Causality_relations[0]]
    added = 0
    for i in range(1, len(Causality_relations)):
        current_elem = Causality_relations[i]
        Xw2.append(current_elem)
        Yw2.append(current_elem)
        for j in range(0, i+added):
            elem = Xw2[j]
            if not isinstance(elem[0], tuple) and not isinstance(elem[1], tuple):
                parallel_elem = tuple(elem[1] + current_elem[1])
                rev_parallel_elem = tuple(current_elem[1] + elem[1])
                parallel_elem2 = tuple(elem[0] + current_elem[0])
                rev_parallel_elem2 = tuple(current_elem[0] + elem[0])
                if elem[0] == current_elem[
                    0] and parallel_elem not in Parallel_relations and rev_parallel_elem not in Parallel_relations:
                    new_elem = (current_elem[0], tuple(elem[1] + current_elem[1]))
                    Xw2.insert(Xw2.index(elem)+1, new_elem)
                    Yw2.insert(Yw2.index(elem)+1, new_elem)
                    Yw2.remove(elem)
                    Yw2.remove(current_elem)
                    added += 1
                elif elem[1] == current_elem[
                    1] and parallel_elem2 not in Parallel_relations and rev_parallel_elem2 not in Parallel_relations:
                    new_elem = (tuple(elem[0] + current_elem[0]), current_elem[1])
                    Xw2.insert(Xw2.index(elem)+1, new_elem)
                    Yw2.insert(Yw2.index(elem)+1, new_elem)
                    Yw2.remove(elem)
                    Yw2.remove(current_elem)
                    added += 1

    print("Xw: ", Xw2)
    print("Yw: ", Yw2)
    return Xw2, Yw2


# def find_Yw(Xw2):
#     Yw2 = list(Xw2)
#     i = 2  # Start checking from the third element
#     while i < len(Yw2):
#         current_elem = Yw2[i]
#         if isinstance(current_elem[1], tuple) or isinstance(current_elem[0], tuple):
#             # Check if it's in the form of ('A', ('B', 'D')) or (('C', 'D'), 'E')
#             prev_elem1 = Yw2[i - 1]
#             prev_elem2 = Yw2[i - 2]
#             if (prev_elem2[0] == prev_elem1[0] == current_elem[0] and prev_elem1[1] == current_elem[1][1] and
#                 prev_elem2[1] == current_elem[1][0]) or \
#                     (prev_elem2[1] == prev_elem1[1] == current_elem[1] and prev_elem1[0] == current_elem[0][1] and
#                      prev_elem2[0] == current_elem[0][0]):
#                 # Remove the previous two elements
#                 Yw2.pop(i - 2)
#                 Yw2.pop(i - 2)
#                 # Decrement i to continue checking with the next element
#                 i -= 2
#         i += 1
#
#     print("Yw: ", Yw2)
#     return Yw2


def find_places(Yw2):
    Pw2 = ['iw']
    for transition in Yw2:
        Pw2.append(f'P{transition}')

    Pw2.append('ow')

    return Pw2


def fw_algorithm(Yw2, TI, TO):
    Fw2 = []
    # Rule 1: (iw, t) for every t in TI
    for t in TI:
        Fw2.append(('iw', t))
    for pair in Yw2:
        A, B = pair
        # Rule 2: (a, p(A, B)) for every (A, B) in Yw and "a" in A
        for a in A:
            Fw2.append((a, f'P{pair}'))

        # Rule 3: (p(A, B), b) for every (A, B) in Yw and "b" in B
        for b in B:
            Fw2.append((f'P{pair}', b))

    # Rule 4: (t, ow) for every t in TO
    for t in TO:
        Fw2.append((t, 'ow'))

    return Fw2


def plot_petri_net(Tw2, Pw2, Fw2):
    G = nx.DiGraph()

    # Add transitions as rectangles
    for i, transition in enumerate(Tw2):
        G.add_node(transition, pos=(i * 2 + 3, 1))

    # Add places as circles interleaved between transitions
    for i, place in enumerate(Pw2):
        G.add_node(place, pos=(i * 2 + 2, 1))

    # Draw transitions and places
    plt.subplots(figsize=(15, 7))
    pos = nx.get_node_attributes(G, 'pos')

    # Draw rectangles
    nx.draw_networkx_nodes(G, pos, nodelist=Tw2, node_color='lightblue', node_shape='s', node_size=1000)

    # Draw circles
    nx.draw_networkx_nodes(G, pos, nodelist=Pw2, node_color='lightgreen', node_shape='o', node_size=1000)

    nx.draw_networkx_labels(G, pos, font_size=8)
    plt.title("Transitions and Places")

    # Add flow relations
    for arc in Fw2:
        G.add_edge(arc[0], arc[1])

    # Draw flow relations with more curvy edges
    nx.draw_networkx_edges(G, pos=pos, width=1.0, arrows=True, arrowstyle='->', connectionstyle='arc3,rad=0.3',
                           edge_color='black')

    plt.show()


event_log = choose_event_log()
print("event_log", event_log)
workflow_result = extract_workflow(event_log)
print("W = ", workflow_result)
input_transitions, output_transitions = print_input_output_transitions(workflow_result)
print("\nSet of Input Transitions (I):", input_transitions)
print("\nSet of Output Transitions (O):", output_transitions)
direct_relations = find_direct_followers(workflow_result)
print("\ndirect_relations", direct_relations)
causality_relations, parallel_relations = find_causality_parallelism(direct_relations)
print("\nCausality Relations:")
print(causality_relations)
print("\nParallel Relations:")
print(parallel_relations)
exclusive_relations, Tw = find_exclusiveness(workflow_result, direct_relations)
print("\nExclusive_relations:")
print(exclusive_relations, "\n")
result_matrix = footprint_matrix(direct_relations, exclusive_relations, causality_relations, parallel_relations)

print("        Foot print matrix", "\n")
for row in result_matrix:
    print('\t'.join(row))
print("        Foot print matrix", "\n")
print("Tw =", Tw)
Xw, Yw = find_Xw(causality_relations, parallel_relations)
Pw = find_places(Yw)
print("Pw =", Pw)
Fw = fw_algorithm(Yw, input_transitions, output_transitions)
print("Fw =", Fw)
print("α(W) = (PW,TW,FW).")
plot_petri_net(Tw, Pw, Fw)
