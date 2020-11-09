from gym import envs

envdict = envs.registry.all()
for env in envdict:
    print(env)
