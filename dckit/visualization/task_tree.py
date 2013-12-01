import networkx as nx
import matplotlib.pyplot as plt
import logging
import time

logger = logging.getLogger(__name__)

class TaskVisualizer(object):
    """docstring for TaskVisualizer"""
    def __init__(self, tasks):
        super(TaskVisualizer, self).__init__()

        self.tasks = tasks
        self.should_stop = False

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        plt.ion()

        plt.show()

        self.init()

    def init(self):
        self.graph = nx.DiGraph()
        # self.graph.node_attr['color'] = 'green'

        self.walk(self.tasks[0])



    def walk(self, task):
        label = "{}".format(task.name)
        self.graph.add_node(id(task), state=task.state, label=label)
        for subtask in task.subtasks:
            self.graph.add_edge(id(task), id(subtask))
            self.walk(subtask)

    def walk_update(self, task):
        if not id(task) in self.graph.node:
            logger.info("reinitializing")
            self.init()  # New node was inserted, redraw graph.
            return False

        self.graph.node[id(task)]['state'] = task.state

        for subtask in task.subtasks:
            if not self.walk_update(subtask):
                break

        return True

    def stop(self):
        self.should_stop = True

    def visualize(self):
        self.should_stop = False

        while not self.should_stop:
            if len(self.tasks) > 0:
                self.walk_update(self.tasks[0])

            colormap = ['red', 'yellow', 'green']

            pos = nx.pygraphviz_layout(self.graph, prog='dot')
            colors = [colormap[self.graph.node[n]['state']] for n in self.graph.nodes()]
            labels = {n: self.graph.node[n]['label'] for n in self.graph.nodes()}

            self.ax.clear()
            nx.draw(self.graph, ax=self.ax, pos=pos, node_color=colors, labels=labels, node_size=2000)
            time.sleep(0.2)