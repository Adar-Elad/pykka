from Actors.ActorManager import ManagerActor
from Actors.ActorWorker import WorkerActor
from Logger import Logger
from Messages import *
import numpy as np
import time


class FindDivisorsManager(ManagerActor):
    def __init__(self, logger_severity):
        super().__init__(logger_title=self.__class__.__name__,
                         logger_severity=logger_severity)
        self.final_result = {}
        self.workers = {}

    def on_start(self) -> None:
        self.logger.debug("Manager became ready!")

    def on_stop(self) -> None:
        self.logger.debug("Manager stopping all workers!")

    def propagate_tasks(self, assignments):
        assert self.workers
        for worker_id, num in zip(range(len(self.workers)), assignments):
            self.logger.debug(f"Sending assignment: {num} to worker: {worker_id}")
            self.workers[worker_id].tell(WorkerTaskMessage(worker_id=worker_id, assignment=num))


class FindDivisorsWorker(WorkerActor):
    def __init__(self, worker_id, supervisor, logger_severity):
        super().__init__(worker_id=worker_id,
                         supervisor=supervisor,
                         logger_title=f"Worker-{worker_id}",
                         logger_severity=logger_severity)

    def do_action(self, assignment):
        divisors = []
        for i in range(2, assignment):
            if assignment % i == 0:
                divisors.append(i)
        self.logger.debug(f"The divisors for {assignment} are {divisors}")
        return {assignment: divisors}


if __name__ == "__main__":
    num_workers = 1000
    logger_severity = 3
    random_numbers = np.random.randint(1000, 100000, num_workers)

    # ==> Creating all actors
    manager_actor = FindDivisorsManager.start(logger_severity=logger_severity)
    worker_actors = {i: FindDivisorsWorker.start(worker_id=i,
                                                 supervisor=manager_actor,
                                                 logger_severity=logger_severity) for i in range(num_workers)}

    # ==> Assign workers for manager and trigger execution
    manager_actor.tell(ManagerHireMessage(manager_id=1, workers=worker_actors))
    manager_actor.tell(ManagerStartMessage(manager_id=1, assignment=random_numbers))

    # ==> Acquiring result
    status, solution = manager_actor.ask(IsDoneMessage(actor_id=1))
    while not status:
        time.sleep(1)
        status, solution = manager_actor.ask(IsDoneMessage(actor_id=1))
    print(solution)

    # ==> Tearing down the actors
    manager_actor.stop()
    for i in worker_actors:
        worker_actors[i].stop()
