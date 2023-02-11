from multiprocessing import Manager

manager = Manager()
store = manager.dict()

def on_starting(server):
    """
    Do something on server start
    """
    print("Server has started")
    store['value'] = 'Hi!'
