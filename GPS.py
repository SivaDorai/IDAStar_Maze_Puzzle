from typing import Optional
penalty_score = -5
reward_score = 10
current_score = 0
cumulative_current_score = 0
goal_state = (5,5)
start_state=(0,0)
grid=None
moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
g = 0
def create_grid():
    position_index = 0
    rows = int(input("enter number of rows : "))
    cols = int(input("enter number of cols : "))
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    #print(f'matrix of dimension {rows} x {cols} is {grid}')
    #for i in range(rows):
    #    for j in range(cols):
    #        grid[i][j] = str(i)+str(j) + "0"

    return grid

def init_grid_with_blocks(grid):
    grid[2][3] = 'X'
    grid[3][2] = 'X'
    grid[4][5] = 'X'
    grid[5][3] = 'X'
    grid[2][5] = 'X'

    return grid


def is_valid(x, y):
    return 0 <= x < 6 and 0 <= y < 6 and grid[x][y] == 0


def heuristic_fn(current_state):
    return abs(goal_state[0] - current_state[0]) + abs(goal_state[1] - current_state[1])

# The method find_next_possible_valid_states will find the adjacent valid cells from the current position
def find_next_possible_valid_states(x,y):
    valid_states=[]
    for i, j in moves:
        new_x, new_y = x + i, y + j
        if is_valid(new_x, new_y):
            valid_states.append((new_x, new_y))
    return valid_states

def navigate(current_state,threshold,g,path_traversed):

    # f value is the total cost which is a sum of
    #  g which is actual cost which I have assumed to be 0 and
    # h which is the estimated heuristic cost
    # first start by finding the f value for the start node
    h = heuristic_fn((int(start_state[0]), int(start_state[1])))
    f = g + h
    child_f_list={}

    """
    # Scenario 1 = if f <= threshold explore the child nodes
    # Scenario 2 = if f > threshold - reset threshold with min f value of child nodes
    """
    if current_state== goal_state:
        return current_state, h,0,(0,0)

    if f > threshold:

        """
        #find child nodes of current node
        #find the f value of the child nodes
        #find the min among the values and reset threshold to min
        """
        valid_states = find_next_possible_valid_states(int(current_state[0]), int(current_state[1]))
        #find the f value for next states and add to a list
        for v_state in valid_states:
            if v_state not in path_traversed:
                f = g + 10+ heuristic_fn((v_state[0],v_state[1]))
                child_f_list[f]=v_state


        # the min key is the f value
        threshold = min(child_f_list.keys())
        next_node_to_explore = (child_f_list[threshold])
        path_traversed.insert(path_traversed.__len__()+1, next_node_to_explore)
        return next_node_to_explore,threshold,g,path_traversed

    if f <= threshold:
        # find the valid states or child nodes from the start position
        #current_state = eval(current_state)
        valid_states = find_next_possible_valid_states(int(current_state[0]), int(current_state[1]))

        #find the f value for next states and add to a list
        for v_state in valid_states:
            if v_state not in path_traversed:
                f = g + 10 + heuristic_fn((v_state[0],v_state[1]))
                child_f_list[f]=str(v_state) # if f is duplicate, overwrite of node will happen in dict. But since we interested in min f value it should be ok.


        threshold_breached = False
        for i in child_f_list.keys():
            # change logic from list to dict get the key and val as f and node
            child_f_val = i
            child_node = child_f_list[i]

            if int(child_f_val) > threshold:
                threshold_breached = True
                # node pruned
            else:
                threshold_breached = False
                #since this child node f value is less that threshold, explore this child node as current node
                next_node_to_explore = eval(child_node)
                path_traversed.insert(path_traversed.__len__()+1, next_node_to_explore)
                return next_node_to_explore, threshold,g+10, path_traversed


        if threshold_breached == True:
            # Revise the threshold to the min value of the child nodes.
            # This iteration is over and start with new threshold value for next iteration
            threshold = min(child_f_list.keys())

            return eval(child_node), threshold, g, path_traversed

    # current_state = str(grid[row_pos][col_pos])
    # if current_state.endswith("X"):
    #     #cannot move and hence go back to prev position
    #     current_pos = prev_pos
    # elif current_state.endswith("G"):
    #     # goal reached
    #     cumulative_current_score = check_adjacent_and_update_score(current_state,current_score)
    # else:
    #     cumulative_current_score = check_adjacent_and_update_score(current_state, current_score)
    #
    # return cumulative_current_score


def check_adjacent_and_update_score(current_state,current_score):
    row_pos = int(current_state[0])
    col_pos = int(current_state[1])
    if is_valid(row_pos,col_pos):
        current_score = current_score + reward_score
    else:
        current_score = current_score + penalty_score
    return current_score

grid  = init_grid_with_blocks(create_grid())
g = 0
path_traversed =[]
path_traversed.insert(0,(0,0))
# Initialize threshold to heuristic of start node
threshold = heuristic_fn((int(start_state[0]), int(start_state[1])))
curr_node = None
while True:
    if curr_node == None:
        curr_node = start_state

    curr_node,threshold,g,path_traversed = navigate(curr_node,threshold,g, path_traversed)

print(f'matrix is {grid}')