# Returns the predicted Q-values from the policy_net for the specific state-action paris.
def get_current(policy_net, states, actions):
    return policy_net(states).gather(dim=1, index=actions.unsqueeze(1))

# Returns the maximum Q-values among the possible actions that can be taken from the next states.
def get_next(target_net, next_states):
    return target_net(next_states).max(dim=1)[0].detach()
