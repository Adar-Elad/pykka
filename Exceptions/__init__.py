
class ErrorManagerMessage(Exception):
    """ An error exists in the ManagerMessage or the message wasn't supposed to received """
    pass


class ErrorWorkerMessage(Exception):
    """ An error exists in the WorkerMessage or the message wasn't supposed to received """
    pass


class ErrorStateMessage(Exception):
    """ An error exists in the State-Message or the message wasn't supposed to received """
    pass


