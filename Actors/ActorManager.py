from Logger import Logger
from Exceptions import *
from Messages import *
import pykka


class ManagerActor(pykka.ThreadingActor):
    def __init__(self, logger_title, logger_severity=None):
        super().__init__()
        self.logger = Logger(logger_title, severity=logger_severity)
        self.logger.debug("Initializing Manager")
        self.final_result = {}
        self.workers = {}

    def on_failure(self, exception_type, exception_value, traceback) -> None:
        self.logger.error(f"Worker.on_failure({exception_type}, {exception_value}, {traceback}")

    def on_start(self) -> None:
        raise NotImplementedError

    def on_stop(self) -> None:
        raise NotImplementedError

    def on_receive(self, message):
        if isinstance(message, ManagerMessage):
            self.logger.debug("Manager received message from HQ")
            self.handle_manager_message(message)
        elif isinstance(message, WorkerMessage):
            self.logger.debug("Manager received message from worker")
            self.handle_worker_message(message)
        elif isinstance(message, IsDoneMessage):
            return len(self.workers) == 0, self.final_result
        else:
            self.logger.error("Manager received illegal message type")
            raise ErrorManagerMessage()
        return None

    def handle_worker_message(self, message: WorkerMessage):
        """ Handle command received from worker """
        def is_assignment_fully_completed():
            return not len(self.workers)
        if isinstance(message, WorkerStateMessage):
            state, result = message.payload
            if state == WorkerStateMessage.WORKER_STATE_DONE:
                self.logger.debug(f"Worker {message.actor_id} is done")
                self.logger.debug(f"Stopping worker {message.actor_id}")
                # ==> Stopping the worker and freeing resources
                self.final_result = self.final_result | result
                self.workers[message.actor_id].stop()
                self.workers.pop(message.actor_id)

            if is_assignment_fully_completed():
                self.logger.debug("Last actor finished!")
        else:
            self.logger.error("Manager received illegal message status")
            raise ErrorWorkerMessage

    def handle_manager_message(self, message: ManagerMessage):
        """ Handle command received from HQ """
        if isinstance(message, ManagerHireMessage):
            self.logger.debug(f"New hired workers!")
            self.workers = message.workers

        elif isinstance(message, ManagerStartMessage):
            assignments = message.payload
            self.logger.debug(f"We got an assignment!")
            self.propagate_tasks(assignments=assignments)

        else:
            self.logger.error("Manager received illegal message status")
            raise ErrorStateMessage()

    def propagate_tasks(self, assignments):
        """ The actual propagation of the assignment into workers """
        raise NotImplementedError
