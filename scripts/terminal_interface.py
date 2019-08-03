#!/usr/bin/env python

import curses

import rospy
from long_term_deployment.msg import AgentDescription, Task
from long_term_deployment.srv import GetRegisteredAgents, QueueTask, QueueTaskList, AgentStatusList


class TerminalInterface(object):

    def __init__(self):
        rospy.wait_for_service('/task_server/get_agents')
        self.agents_proxy = rospy.ServiceProxy('/task_server/get_agents', GetRegisteredAgents)
        rospy.wait_for_service('/task_server/get_queued_tasks')
        self.queued_tasks_proxy = rospy.ServiceProxy('/task_server/get_queued_tasks', QueueTaskList)
        rospy.wait_for_service('/task_server/get_agents_status')
        self.active_tasks_proxy = rospy.ServiceProxy('/task_server/get_agents_status', AgentStatusList)
        rospy.wait_for_service('/task_server/queue_task')
        self.queue_active_task_proxy = rospy.ServiceProxy('/task_server/queue_task', QueueTask)
        rospy.wait_for_service('/task_server/start_continuous_task')
        self.start_continuous_task_proxy = rospy.ServiceProxy('/task_server/start_continuous_task', QueueTask)
        rospy.wait_for_service('/task_server/stop_continuous_task')
        self.stop_continuous_task_proxy = rospy.ServiceProxy('/task_server/stop_continuous_task', QueueTask)

    def process_input(self, key):
        if key == '0':
            self.queue_active_task_proxy(Task(
                '',
                'long_term_deployment',
                'test_task',
                ['5'],
                False), AgentDescription('erratic', 'erratic'))
        elif key == '1':
            self.start_continuous_task_proxy(Task(
                '',
                'navigation_tasks',
                'navigate_on_map',
                ['graf'],
                False), AgentDescription('erratic', 'erratic'))
        elif key == '2':
            self.stop_continuous_task_proxy(Task(
                '',
                'navigation_tasks',
                'navigate_on_map',
                ['graf'],
                False), AgentDescription('erratic', 'erratic'))
        elif key == '3':
            self.start_continuous_task_proxy(Task(
                '',
                'navigation_tasks',
                'build_new_map',
                ['new_maze'],
                False), AgentDescription('erratic', 'erratic'))
        elif key == '4':
            self.stop_continuous_task_proxy(Task(
                '',
                'navigation_tasks',
                'build_new_map',
                ['new_maze'],
                False), AgentDescription('erratic', 'erratic'))
        elif key == '5':
            self.start_continuous_task_proxy(Task(
                '',
                'navigation_tasks',
                'explore_map',
                [],
                True), AgentDescription('erratic', 'erratic'))
        elif key == '6':
            self.stop_continuous_task_proxy(Task(
                '',
                'navigation_tasks',
                'explore_map',
                [],
                False), AgentDescription('erratic', 'erratic'))
        elif key == '7':
            self.queue_active_task_proxy(Task(
                '',
                'navigation_tasks',
                'go_to_pose',
                ['5.0', '5.0', '0.0'],
                False), AgentDescription('erratic', 'erratic'))
        elif key == '8':
            self.queue_active_task_proxy(Task(
                '',
                'navigation_tasks',
                'go_to_pose',
                ['2.0', '2.0', '0.0'],
                False), AgentDescription('erratic', 'erratic'))
        elif key == '9':
            self.start_continuous_task_proxy(Task(
                '',
                'monitoring_tasks',
                'record_wifi',
                ['test_file'],
                True), AgentDescription('erratic', 'erratic'))
        elif key == '/':
            self.stop_continuous_task_proxy(Task(
                '',
                'monitoring_tasks',
                'record_wifi',
                ['test_file'],
                True), AgentDescription('erratic', 'erratic'))
        elif key == 'z':
            self.start_continuous_task_proxy(Task(
                '',
                'long_term_deployment',
                'schedule_executor',
                [],
                False), AgentDescription('fetch', 'fetch'))

    def update_screen(self, stdscr):
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Declaration of strings
        statusbarstr = "Press 'q' to exit | STATUS BAR"

        stdscr.addstr(2, 0, '-' * (width - 1))
        stdscr.addstr(int(height // 2), 0, '-' * (width - 1))
        stdscr.addstr(int(height // 2) + 1, 0, 'Press "0" to queue "test_task"')
        stdscr.addstr(int(height // 2) + 2, 0, 'Press "1" to start navigation on erratic agent')
        stdscr.addstr(int(height // 2) + 3, 0, 'Press "2" to stop navigation on erratic agent')
        stdscr.addstr(int(height // 2) + 4, 0, 'Press "3" to start building a map on erratic agent')
        stdscr.addstr(int(height // 2) + 5, 0, 'Press "4" to stop building a map on erratic agent')
        stdscr.addstr(int(height // 2) + 6, 0, 'Press "5" to start frontier exploration on erratic agent')
        stdscr.addstr(int(height // 2) + 7, 0, 'Press "6" to stop frontier exploration on erratic agent')
        stdscr.addstr(int(height // 2) + 8, 0, 'Press "7" to go to 5,5 on map')
        stdscr.addstr(int(height // 2) + 9, 0, 'Press "8" to go to 2,2 on map')
        stdscr.addstr(int(height // 2) + 10, 0, 'Press "9" to start recording wifi levels')
        stdscr.addstr(int(height // 2) + 11, 0, 'Press "/" to stop recording wifi levels')

        for i in range(1, int(height // 2)):
            stdscr.addstr(i, 15, '|')
            stdscr.addstr(i, 39, '|')
            stdscr.addstr(i, 59, '|')

        stdscr.addstr(1, 3, 'Agent')
        stdscr.addstr(1, 22, 'Active task')
        stdscr.addstr(1, 41, 'Continuous tasks')
        stdscr.addstr(1, 68, 'Task Queue')

        for i, agent in enumerate(self.agents):
            stdscr.addstr(i + 3, 2, agent)

            active_task = self.agent_tasks[agent]['active_task']
            if active_task is None:
                stdscr.addstr(i + 3, 22, 'Inactive')
            else:
                stdscr.addstr(i + 3, 22, active_task)

            stdscr.addstr(i + 3, 41, str(self.agent_tasks[agent]['background_tasks']))

        for i, task in enumerate(self.queued_tasks):
            stdscr.addstr(i + 3, 62, task)

        # Rendering some text
        whstr = 'Width: {}, Height: {}'.format(width, height)
        stdscr.addstr(0, 0, whstr, curses.color_pair(1))

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height - 1, 0, statusbarstr)
        stdscr.addstr(height - 1, len(statusbarstr), ' ' * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Refresh the screen
        stdscr.refresh()


    def draw_menu(self, stdscr):
        curses.raw()
        curses.cbreak()
        stdscr.nodelay(True)
    
        # Clear and refresh the screen for a blank canvas
        stdscr.clear()
        stdscr.refresh()
    
        # Start colors in curses
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
        # Loop where k is the last character pressed
        k = None
        r = rospy.Rate(10)
        while k != 'q' and not rospy.is_shutdown():
            k = None
            tmp = stdscr.getch()  # non blocking now
            if tmp != -1 and 0 <= tmp <= 255:
                k = chr(tmp)
    
            # Initialization
            self.agents = [a.agent_name for a in self.agents_proxy().agents]
            self.queued_tasks = ['{}/{}'.format(t.package_name, t.launchfile_name)
                            for t in self.queued_tasks_proxy().tasks]
            self.agent_tasks = {}
            for a in self.active_tasks_proxy().agent_statuses:
                self.agent_tasks[a.agent.agent_name] = {
                    'active_task': a.active_task.launchfile_name,
                    'background_tasks': [t.launchfile_name for t in a.background_tasks],
                }
    
            self.process_input(k)
    
            self.update_screen(stdscr)
            r.sleep()


if __name__ == '__main__':
    rospy.init_node('server_terminal')
    node = TerminalInterface()
    curses.wrapper(node.draw_menu)

# self.s1 = rospy.Service('{}/register_agent'.format(name), RegisterAgent, self.handle_register_agent)
