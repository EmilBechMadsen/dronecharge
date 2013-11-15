import unittest
from dckit import DCKit
from dckit.tasks.task import Task, TaskState
from dckit.tasks.movement_task import MovementTask
from dckit.drivers.ideal import IdealDrone
import logging


logger = logging.getLogger(__name__)


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
        self.dckit._iterate(0)

        self.assertEqual(task.state, TaskState.EXECUTING, "Task Executing")
        self.assertEqual(subtask1.state, TaskState.EXECUTING, "Subtask Executing")

        self.dckit._iterate(1)
        self.assertEqual(task.state, TaskState.EXECUTING, "Task Executing")
        self.assertEqual(subtask1.state, TaskState.COMPLETE, "Subtask Complete")

        self.dckit._iterate(2)
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

        self.assertEquals(task.state, TaskState.READY, "Task Ready")
        self.assertEquals(subtask1.state, TaskState.READY, "Subtask1 Ready")
        self.assertEquals(subtask2.state, TaskState.READY, "Subtask2 Ready")
        self.assertEquals(subtask3.state, TaskState.READY, "Subtask3 Ready")
        self.assertEquals(subtask4.state, TaskState.READY, "Subtask4 Ready")
        self.assertEquals(subtask5.state, TaskState.READY, "Subtask5 Ready")
        self.assertEquals(subtask6.state, TaskState.READY, "Subtask6 Ready")
        
        self.dckit._iterate(0)
        self.assertEquals(task.state, TaskState.EXECUTING, "Task EXECUTING")
        self.assertEquals(subtask1.state, TaskState.EXECUTING, "Subtask1 EXECUTING")
        self.assertEquals(subtask2.state, TaskState.READY, "Subtask2 Ready")
        self.assertEquals(subtask3.state, TaskState.READY, "Subtask3 Ready")
        self.assertEquals(subtask4.state, TaskState.READY, "Subtask4 Ready")
        self.assertEquals(subtask5.state, TaskState.READY, "Subtask5 Ready")
        self.assertEquals(subtask6.state, TaskState.READY, "Subtask6 Ready")

        self.dckit._iterate(1)
        self.assertEquals(task.state, TaskState.EXECUTING, "Task EXECUTING")
        self.assertEquals(subtask1.state, TaskState.COMPLETE, "Subtask1 COMPLETE")
        self.assertEquals(subtask2.state, TaskState.READY, "Subtask2 READY")
        self.assertEquals(subtask3.state, TaskState.READY, "Subtask3 Ready")
        self.assertEquals(subtask4.state, TaskState.READY, "Subtask4 Ready")
        self.assertEquals(subtask5.state, TaskState.READY, "Subtask5 Ready")
        self.assertEquals(subtask6.state, TaskState.READY, "Subtask6 Ready")

        self.dckit._iterate(2)
        self.assertEquals(task.state, TaskState.EXECUTING, "Task EXECUTING")
        self.assertEquals(subtask1.state, TaskState.COMPLETE, "Subtask1 COMPLETE")
        self.assertEquals(subtask2.state, TaskState.EXECUTING, "Subtask2 EXECUTING")
        self.assertEquals(subtask3.state, TaskState.EXECUTING, "Subtask3 EXECUTING")
        self.assertEquals(subtask4.state, TaskState.READY, "Subtask4 Ready")
        self.assertEquals(subtask5.state, TaskState.EXECUTING, "Subtask5 EXECUTING")
        self.assertEquals(subtask6.state, TaskState.EXECUTING, "Subtask6 EXECUTING")

        self.dckit._iterate(3)
        self.assertEquals(task.state, TaskState.EXECUTING, "Task EXECUTING")
        self.assertEquals(subtask1.state, TaskState.COMPLETE, "Subtask1 COMPLETE")
        self.assertEquals(subtask2.state, TaskState.EXECUTING, "Subtask2 EXECUTING")
        self.assertEquals(subtask3.state, TaskState.EXECUTING, "Subtask3 EXECUTING")
        self.assertEquals(subtask4.state, TaskState.READY, "Subtask4 Ready")
        self.assertEquals(subtask5.state, TaskState.EXECUTING, "Subtask5 EXECUTING")
        self.assertEquals(subtask6.state, TaskState.COMPLETE, "Subtask6 COMPLETE")

        self.dckit._iterate(4)
        self.assertEquals(task.state, TaskState.EXECUTING, "Task EXECUTING")
        self.assertEquals(subtask1.state, TaskState.COMPLETE, "Subtask1 COMPLETE")
        self.assertEquals(subtask2.state, TaskState.EXECUTING, "Subtask2 EXECUTING")
        self.assertEquals(subtask3.state, TaskState.COMPLETE, "Subtask3 COMPLETE")
        self.assertEquals(subtask4.state, TaskState.EXECUTING, "Subtask4 EXECUTING")
        self.assertEquals(subtask5.state, TaskState.COMPLETE, "Subtask5 COMPLETE")
        self.assertEquals(subtask6.state, TaskState.COMPLETE, "Subtask6 COMPLETE")

        self.dckit._iterate(5)
        self.assertEquals(task.state, TaskState.EXECUTING, "Task EXECUTING")
        self.assertEquals(subtask1.state, TaskState.COMPLETE, "Subtask1 COMPLETE")
        self.assertEquals(subtask2.state, TaskState.EXECUTING, "Subtask2 EXECUTING")
        self.assertEquals(subtask3.state, TaskState.COMPLETE, "Subtask3 COMPLETE")
        self.assertEquals(subtask4.state, TaskState.COMPLETE, "Subtask4 COMPLETE")
        self.assertEquals(subtask5.state, TaskState.COMPLETE, "Subtask5 COMPLETE")
        self.assertEquals(subtask6.state, TaskState.COMPLETE, "Subtask6 COMPLETE")

        self.dckit._iterate(6)
        self.assertEquals(task.state, TaskState.COMPLETE, "Task COMPLETE")
        self.assertEquals(subtask1.state, TaskState.COMPLETE, "Subtask1 COMPLETE")
        self.assertEquals(subtask2.state, TaskState.COMPLETE, "Subtask2 COMPLETE")
        self.assertEquals(subtask3.state, TaskState.COMPLETE, "Subtask3 COMPLETE")
        self.assertEquals(subtask4.state, TaskState.COMPLETE, "Subtask4 COMPLETE")
        self.assertEquals(subtask5.state, TaskState.COMPLETE, "Subtask5 COMPLETE")
        self.assertEquals(subtask6.state, TaskState.COMPLETE, "Subtask6 COMPLETE")
        
if __name__ == "__main__":
    unittest.main()
