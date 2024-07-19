
class Message(object):
    def __init__(self, actor_id, payload):
        self.actor_id= actor_id
        self.payload = payload

    def __str__(self):
        return "Generic-MSG"


class IsDoneMessage(Message):
    """ A query message for an actor execution state """
    def __init__(self, actor_id):
        super().__init__(actor_id, payload=None)

    def __str__(self):
        return "IsDone-MSG"


class WorkerMessage(Message):
    """ A generic message intended to/for worker-id """
    def __init__(self, worker_id, payload):
        super().__init__(actor_id=worker_id, payload=payload)

    def __str__(self):
        return "Worker-Message"


class WorkerTaskMessage(WorkerMessage):
    """ An assignment message intended to worker-id """
    def __init__(self, worker_id, assignment):
        super().__init__(worker_id=worker_id, payload=assignment)

    def __str__(self):
        return "Worker-Task-Message"


class WorkerStateMessage(WorkerMessage):
    """ A message passing the state from worker-id """
    WORKER_STATE_DONE = 0
    WORKER_STATE_EXEC = 1
    WORKER_STATE_IDLE = 2

    def __init__(self, worker_id, state, result):
        super().__init__(worker_id=worker_id, payload=(state, result))

    def __str__(self):
        return "Worker-State-Message"


class ManagerMessage(Message):
    """ A generic message for/to manager with manager-id """
    def __init__(self, manager_id, payload):
        super().__init__(actor_id=manager_id, payload=payload)
        self.manager_id = manager_id
        self.payload = payload

    def __str__(self):
        return "Manager-Message"


class ManagerHireMessage(ManagerMessage):
    """ A message passing workers to manager with manager-id"""
    def __init__(self, manager_id, workers):
        super().__init__(manager_id=manager_id, payload=workers)
        self.workers = workers

    def __str__(self):
        return "Manager-Hiring-Message"


class ManagerStartMessage(ManagerMessage):
    """ A message passing the state from worker-id """
    def __init__(self, manager_id, assignment):
        super().__init__(manager_id=manager_id, payload=assignment)

    def __str__(self):
        return "Manager-Start-Exe-Message"
