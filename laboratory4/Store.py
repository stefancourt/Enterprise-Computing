store={}

def create(s,t):
    store[s] = {"id":s,"text":t}

def read(s):
    post = store.get(s)
    if post != None:
        return post
    else:
        return None

def delete(s):
    post = store.get(s)
    if post != None:
        del store[s]
        return True
    else:
        return False

def list():
    ss = []
    for s in store.keys():
        ss.append(s)
    return ss