import unittest
from dckit import DCKit
from dckit.tasks.task import Task, TaskState
from dckit.tasks.movement_task import MovementTask
from dckit.drivers.ideal import IdealDrone
from operator import eq
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TaskTest(unittest.TestCase):
    def setUp(self):
        self.dckit = DCKit()

        drone = IdealDrone("Drone 1")
        self.dckit.addDrone(drone)

    def tearDown(self):
        pass

    def test_evaluate(self):
        task = Task("Maintask")

        subtask1 = MovementTask("subtask1", (1, 1, 1))
        subtask2 = MovementTask("subtask2", (2, 2, 2))
        subtask3 = MovementTask("subtask3", (3, 3, 3))
        subtask4 = MovementTask("subtask4", (3, 3, 3))
        subtask5 = MovementTask("subtask5", (3, 3, 3))
        subtask6 = MovementTask("subtask6", (3, 3, 3))

        task.addSubtask(subtask1)
        subtask2.addSubtask(subtask3)
        subtask2.addSubtask(subtask4)
        subtask3.addSubtask(subtask5)
        subtask5.addSubtask(subtask6)
        task.addSubtask(subtask2)

        self.dckit.addTask(task)

        self.dckit._accumulateCapabilities()
        self.assertEqual(task.required_capabilities, set(['move']), "Task capability move")

        def compareState(current, expected):
            # for i, s in enumerate(expected):
            #     if current[i] != expected[i]:
            #         return False

            # return True
            return all(map(eq, current, expected))

        states = [
            [  # Before all iterations
                TaskState.READY,
                TaskState.READY,
                TaskState.READY,
                TaskState.READY,
                TaskState.READY,
                TaskState.READY,
                TaskState.READY
            ], [  # After 1st iteration
                TaskState.EXECUTING,
                TaskState.EXECUTING,
                TaskState.READY,
                TaskState.READY,
                TaskState.READY,
                TaskState.READY,
                TaskState.READY
            ], [  # After 2nd iteration
                TaskState.EXECUTING,
                TaskState.COMPLETE,
                TaskState.READY,
                TaskState.READY,
                TaskState.READY,
                TaskState.READY,
                TaskState.READY
            ], [  # After 3rd iteration
                TaskState.EXECUTING,
                TaskState.COMPLETE,
                TaskState.EXECUTING,
                TaskState.EXECUTING,
                TaskState.READY,
                TaskState.EXECUTING,
                TaskState.EXECUTING
            ], [  # After 4th iteration
                TaskState.EXECUTING,
                TaskState.COMPLETE,
                TaskState.EXECUTING,
                TaskState.EXECUTING,
                TaskState.READY,
                TaskState.EXECUTING,
                TaskState.COMPLETE
            ], [  # After 5th iteration
                TaskState.EXECUTING,
                TaskState.COMPLETE,
                TaskState.EXECUTING,
                TaskState.COMPLETE,
                TaskState.EXECUTING,
                TaskState.COMPLETE,
                TaskState.COMPLETE
            ], [  # After 6th iteration
                TaskState.EXECUTING,
                TaskState.COMPLETE,
                TaskState.EXECUTING,
                TaskState.COMPLETE,
                TaskState.COMPLETE,
                TaskState.COMPLETE,
                TaskState.COMPLETE
            ], [  # After 7th iteration
                TaskState.COMPLETE,
                TaskState.COMPLETE,
                TaskState.COMPLETE,
                TaskState.COMPLETE,
                TaskState.COMPLETE,
                TaskState.COMPLETE,
                TaskState.COMPLETE
            ]
        ]

        previous = None
        for expected in states:
            current = [
                task.state,
                subtask1.state,
                subtask2.state,
                subtask3.state,
                subtask4.state,
                subtask5.state,
                subtask6.state
            ]

            previous = current

            break_outer = False

            i = 0
            while True:
                current = [
                    task.state,
                    subtask1.state,
                    subtask2.state,
                    subtask3.state,
                    subtask4.state,
                    subtask5.state,
                    subtask6.state
                ]

                state_changed = not compareState(current, previous)
                state_expected = compareState(current, expected)

                if state_expected:
                    break

                if state_changed and not state_expected:
                    logger.info("Previous State: %s", previous)
                    logger.info("Current State: %s", current)
                    logger.info("Expected State: %s", expected)
                    self.fail("Inconsistent state encountered")
                    break_outer = True
                    break

                self.dckit._iterate(i)
                # logging.info("Iteration %u", i)
                i += 1

            # logging.info("Ran %u iterations", i)

            if break_outer:
                break

    def test_accumulate(self):
        task = Task("Maintask")

        subtask1 = Task("subtask1", (1, 1, 1))
        subtask1.required_capabilities = ["move"]
        subtask2 = Task("subtask2", (2, 2, 2))
        subtask2.required_capabilities = ["fly"]
        subtask3 = Task("subtask3", (3, 3, 3))
        subtask3.required_capabilities = ["walk"]

        subtask1.addSubtask(subtask2)
        task.addSubtask(subtask1)
        task.addSubtask(subtask3)

        self.dckit.addTask(task)

        self.dckit._accumulateCapabilities()

        acc = set(["move", "fly", "walk"])
        self.assertEqual(task.required_capabilities, acc, "Contains all child required capabilites")
        self.assertFalse("walk" in subtask1.required_capabilities, "Subtask 1 does not contain walk")
        self.assertFalse("walk" in subtask2.required_capabilities, "Subtask 2 does not contain walk")
        self.assertTrue("fly" in subtask1.required_capabilities, "Subtask 1 contains fly")

if __name__ == "__main__":
    unittest.main()
