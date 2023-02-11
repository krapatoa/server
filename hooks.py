from multiprocessing import Manager

manager = Manager()
store = manager.dict()

def on_starting(server):
    """
    Do something on server start
    """
    print("Server has started")
    flask_app = server.app.wsgi()
    flask_app.__setattr__('value', 'Hi!')
