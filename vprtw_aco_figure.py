import matplotlib.pyplot as plt
from multiprocessing import Queue as MPQueue
import astar
import astar_neighbor


class VrptwAcoFigure:
    def __init__(self, nodes: list, path_queue: MPQueue, mode=1, astar_path=None):
        """
        :param nodes: nodes是各个结点的list，包括depot
        :param path_queue: queue用来存放工作线程计算得到的path，队列中的每一个元素都是一个path，path中存放的是各个结点的id
        """

        self.nodes = nodes
        self.figure = plt.figure(figsize=(10, 10))
        self.figure_ax = self.figure.add_subplot(1, 1, 1)
        self.path_queue = path_queue
        self._depot_color = 'k'
        self._customer_color = 'darksalmon'
        self._customer_done_color = 'yellowgreen'
        # self._line_color = 'darksalmon'
        self._line_color = ['g', 'r', 'c', 'm', 'y', 'k']
        self.mode = mode
        self.astar_path = astar_path
        self.sct_list = []

    def _draw_point(self):
        # 画出depot
        self.figure_ax.scatter([self.nodes[0].x], [self.nodes[0].y], c=self._depot_color, label='depot', s=40)

        self.figure_ax.scatter(list(node.x for node in self.nodes[1:]),
                               list(node.y for node in self.nodes[1:]), c=self._customer_color, label='customer', s=20)
        plt.pause(0.5)

    def run(self):
        if self.mode == 3:
            xlist = []
            ylist = []
            map = astar.loadMap()
            for i in range(50):
                for j in range(50):
                    if map[i, j] == 1:
                        xlist.append(i)
                        ylist.append(j)
            self.figure_ax.scatter(xlist, ylist, c='steelblue', label='block', s=150, marker='s')
        elif self.mode == 4:
            xlist = []
            ylist = []
            neighborhood_x = []
            neighborhood_y = []
            entrance_x = []
            entrance_y = []
            map = astar_neighbor.loadMap()
            for i in range(50):
                for j in range(50):
                    if map[i, j] == 1:
                        xlist.append(i)
                        ylist.append(j)
                    elif map[i, j] == 4:
                        neighborhood_x.append(i)
                        neighborhood_y.append(j)
                    elif map[i, j] == 6:
                        entrance_x.append(i)
                        entrance_y.append(j)
            self.figure_ax.scatter(xlist, ylist, c='steelblue', label='block', s=150, marker='s')
            self.figure_ax.scatter(neighborhood_x, neighborhood_y, c='green', label='block', s=150, marker='s')
            self.figure_ax.scatter(entrance_x, entrance_y, c='yellow', label='block', s=150, marker='s')

        self._draw_point()
        self.figure.show()

        while True:
            if not self.path_queue.empty():
                info = self.path_queue.get()
                while not self.path_queue.empty():
                    info = self.path_queue.get()

                path, distance, used_vehicle_num = info.get_path_info()
                if path is None:
                    print('[draw figure]: exit')
                    break

                remove_obj = []
                for line in self.figure_ax.lines:
                    if line._label == 'line':
                        remove_obj.append(line)
                for scatter in self.sct_list:
                    scatter.set_visible(False)
                for line in remove_obj:
                    self.figure_ax.lines.remove(line)
                remove_obj.clear()

                self.figure_ax.set_title('travel distance: %0.2f, number of vehicles: %d ' % (distance, used_vehicle_num))
                self._draw_line(path)
            plt.pause(1)

    def _draw_line(self, path):
        cnt = 0
        for i in range(1, len(path)):
            if self.mode == 1:
                x_list = [self.nodes[path[i - 1]].x, self.nodes[path[i]].x]
                y_list = [self.nodes[path[i - 1]].y, self.nodes[path[i]].y]
                self.figure_ax.plot(x_list, y_list, color=self._line_color[cnt], linewidth=1.5, label='line')
            elif self.mode == 2:
                x1_list = [self.nodes[path[i - 1]].x, self.nodes[path[i - 1]].x]
                y1_list = [self.nodes[path[i - 1]].y, self.nodes[path[i]].y]
                self.figure_ax.plot(x1_list, y1_list, color=self._line_color[cnt], linewidth=1.5, label='line',
                                    alpha=0.5)
                x2_list = [self.nodes[path[i - 1]].x, self.nodes[path[i]].x]
                y2_list = [self.nodes[path[i]].y, self.nodes[path[i]].y]
                self.figure_ax.plot(x2_list, y2_list, color=self._line_color[cnt], linewidth=1.5, label='line',
                                    alpha=0.3)

            elif self.mode == 3:
                x_list3 = []
                y_list3 = []
                pointlist = self.astar_path[int(self.nodes[path[i - 1]].id)][int(self.nodes[path[i]].id)]
                for j in pointlist:
                    x_list3.append(j[0])
                    y_list3.append(j[1])

                for m in range(1, len(pointlist)):
                    x_list = [x_list3[m-1], x_list3[m]]
                    y_list = [y_list3[m-1], y_list3[m]]
                    self.figure_ax.plot(x_list, y_list, color=self._line_color[cnt], linewidth=1.5, label='line',
                                        alpha=0.8)

            elif self.mode == 4:
                x_list4 = []
                y_list4 = []
                pointlist = self.astar_path[int(self.nodes[path[i - 1]].id)][int(self.nodes[path[i]].id)]
                for j in pointlist:
                    x_list4.append(j[0])
                    y_list4.append(j[1])

                for m in range(1, len(pointlist)):
                    x_list = [x_list4[m - 1], x_list4[m]]
                    y_list = [y_list4[m - 1], y_list4[m]]
                    self.figure_ax.plot(x_list, y_list, color=self._line_color[cnt], linewidth=1.5, label='line',
                                        alpha=0.8)

            if path[i] == 0:
                cnt = (cnt + 1) % len(self._line_color)
            else:
                self.sct_list.append(self.figure_ax.scatter([self.nodes[path[i]].x], [self.nodes[path[i]].y],
                                                c=self._customer_done_color, label='customer_done', s=100, marker='*'))

            plt.pause(0.2)
