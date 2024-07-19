import pykka

from Logger import Logger
from Exceptions import *
from Messages import *
import pykka


class WorkerActor(pykka.ThreadingActor):
    WORKER_IDLE = 1
    WORKER_EXEC = 2

    def __init__(self, worker_id, supervisor, logger_title, logger_severity=None):
        super().__init__()
        self.logger = Logger(title=logger_title, severity=logger_severity)
        self.logger.debug(f"Initializing Worker {worker_id}")
        self.state = WorkerActor.WORKER_IDLE
        self.supervisor = supervisor
        self.worker_id = worker_id

    def on_failure(self, exception_type, exception_value, traceback) -> None:
        self.logger.error(f"Worker.on_failure({exception_type}, {exception_value}, {traceback}")

    def on_stop(self) -> None:
        self.state = WorkerActor.WORKER_IDLE
        return None

    def on_receive(self, message):
        self.logger.debug("Worker received message!")
        if isinstance(message, WorkerTaskMessage):
            if message.actor_id == self.worker_id:
                if message.payload:
                    result = self.do_action(message.payload)
                    self.report_done(result)
        else:
            self.logger.error("Worker received illegal message status")
            raise ErrorWorkerMessage()

    def report_done(self, result):
        self.logger.debug(f"Worker {self.worker_id} reporting completion")
        self.state = WorkerActor.WORKER_IDLE
        self.supervisor.tell(WorkerStateMessage(worker_id=self.worker_id,
                                                state=WorkerStateMessage.WORKER_STATE_DONE,
                                                result=result))

    def do_action(self, assignment):
        raise NotImplementedError
