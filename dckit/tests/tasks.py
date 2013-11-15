import unittest
from dckit import DCKit
from dckit.tasks.task import Task, TaskState
from dckit.tasks.movement_task import MovementTask
from dckit.drivers.ideal import IdealDrone


class TaskTest(unittest.TestCase):
    def setUp(self):
        self.dckit = DCKit()

    def tearDown(self):
        pass

    def test_evaluate(self):
        drone = IdealDrone("Drone 1")
        self.dckit.addDrone(drone)

        task = Task("Maintask")

        subtask1 = MovementTask("subtask1", (1, 1, 1))

        task.addSubtask(subtask1)

        self.dckit.addTask(task)
        self.dckit._main_loop()

        self.assertEqual(subtask1.state, TaskState.COMPLETE, "Subtask complete")
        self.assertEqual(task.state, TaskState.COMPLETE, "Task complete")

    def test_evaluate2(self):
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

        self.dckit._main_loop()

if __name__ == "__main__":
    unittest.main()
