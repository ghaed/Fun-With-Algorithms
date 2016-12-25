""" Solves the traveling salesman problem using a dynamic programming approach"""


class Graph(object):
    """ Defines a graph"""

    def __init__(self):
        """ Constructor to initialize an empty matrix representation of the graph. """
        self._a = []        # Dyamic programming 2D matrix
        self._priors = []        # Dyamic programming 2D matrix, pointing to one-before-last index k
        self._x = []        # x coordinates
        self._y = []        # y coordinates
        self.all_subsets = []        # a list of all possible sub-sets of the array
        self.n = 0          # Number of vertices, i.e. nodes. Excludes skipped nodes
        self.path = []
        self.skip_nodes_dic = {}    # Stores the coordinates of the skipped nodes in {double_node_id:(x,y)} format
                                    # Basically, insert a node with node_id = double_node_id+1 with coordinates
                                    # (x,y) after double_node in the path
        self.node_dic = {}   # Maps the used self.n nodes to self.n+self.nskip nodes
        # self.doube_nodes =[]    # List of double-nodes, i.e nodes for which the next element is merged with them

    def read_graph_from_file(self, file_name, skip_nodes_list=[]):
        """ Fills the x and y coordinates by reading the given file. Also, initializes the array self._a used
        in the Dynamic-Programming implementation of the TSP problem. Also fills the s array"""
        f = open(file_name)
        lines = f.readlines()
        line = lines[0].rstrip()
        self.n = int(line)-len(skip_nodes_list)
        print 'Ignoring the following nodes: ', skip_nodes_list
        # Construct the 2D array for TSP
        print 'Constructing 2D array'
        row_a = [1e9 for _ in range(self.n + 1)]
        row_prior = [0 for _ in range(self.n + 1)]
        progress = 0
        for y in range(2**self.n):
            if y % (2**(self.n-3)) == 0:
                progress += 12.5
                print 'Construction progress', progress, '%'
            self._a.append(row_a[:])
            self._priors.append(row_prior[:])
        # self._a = [[float("inf") for x in range(self.n + 1)] for y in range(2**self.n)]
        print 'Constructing 2D array completed'
        self._a[1][1] = 0
        self._x = [0.0]*(self.n+1)
        self._y = [0.0]*(self.n+1)
        i = 0       # node index, including skipped
        j = 0       # node index, excluding skipped
        for line in lines[1:]:
            line_strings = line.split()
            i += 1
            if i in skip_nodes_list:
                # store the information of the skipped node.
                # j denotes the index (out of self.n) of the node i was merged with
                self.skip_nodes_dic[i-1] = (float(line_strings[0]), float(line_strings[1])) # indexed by double-node's original index
                self.doube_nodes.append(i-1)
                continue
            j += 1
            self.node_dic[j] = i
            self._x[j] = float(line_strings[0])
            self._y[j] = float(line_strings[1])
        # The i_s (index of s out of 2^n) when converted to binary tells us what elements are present
        # eg: 0'b101 means that nodes 1 and 3 are present whearas node 2 is not
        # Fill all_s
        print 'Forming list of sub-arrays...'
        self.all_subsets = self.sub_sets(range(1, self.n+1))

    @staticmethod
    def sub_sets(input_set):
        """ Returns the sub-sets of a given array"""
        n = len(input_set)
        result = [[] for _ in range(2**n)]
        for i in range(2**n):
            j = i
            for k in range(n):
                if j & 0x01:
                    result[i].append(input_set[k])
                j >>= 1
        return result

    def tsp(self):
        for m in range(2, self.n + 1):  # Sweep sub-problem size
            print 'calculating TSP sub-problems of size m=', m
            subset_index = -1        # indexes the subset number in the self.all_subsets array. Will come handy later
            for s in self.all_subsets:  # Look at all sub-sets of size m that include 1
                subset_index += 1
                if not len(s) == m or 1 not in s:
                    continue
                for j in s:     # For reach sub-set s, look at each possible last path ending-point
                    if j == 1:
                        continue
                    min_len = float('inf')
                    prior = (0, 0)
                    for k in s:     # For each j, look at all possible one-before-last nodes, k
                        if k == j:
                            continue
                        # print 'updating 2D matricx: m=', m, 's=', s, 'j=', j, 'subset_index=', subset_index,
                        # 'k=', k, 'recur=', self._a[subset_index-2**(j-1)][k] + self.distance(k,j),
                        # 'min_a(before)=', min_a
                        candidate = self._a[subset_index-2**(j-1)][k] + self.distance(k, j)
                        if candidate < min_len:
                            min_len = candidate
                            prior = (subset_index-2**(j-1), k)  # Book-keeping to keep track of one-before-last node

                        # print 'min_a(after)=', min_a
                    self._a[subset_index][j] = min_len
                    self._priors[subset_index][j] = prior
                    # print self.a_string

        # Find the best-of-n last-point for the TSP
        min_len = float('inf')
        last_j = float('inf')
        for j in range(2, self.n + 1):
            candidate = self._a[2**self.n - 1][j] + self.distance(j, 1)
            if candidate < min_len:
                min_len = candidate
                last_j = j
            # result = min(result, self._a[2**self.n - 1][j] + self.distance(j, 1))

        # Back-calculate the path of the TSP
        self.path = [last_j]
        subset_index = 2**self.n - 1
        j = last_j
        for _ in range(self.n - 1):
            (subset_index, j) = self._priors[subset_index][j]
            self.path.append(self.node_dic[j])


        return min_len

    def amend_skipped_nodes(self):
        """ Amends the skipped nodes by finding the shortes possible paths. The assumption is that self.node_dic[]
        """
        paths = []
        base_path = []
        x = []
        y = []
        for node in self.path:
            base_path.append(node)
            self.x.append()
            if node in self.skip_nodes_dic.keys():
                base_path.append(node + 1)



        for i in range(2**self.nskip):
            path=


    def distance(self, i, j):
        """ Calculates the distance between two points indexed by i and j"""
        return ((self._x[i] - self._x[j])**2 + (self._y[i] - self._y[j])**2)**0.5

    @property
    def x(self):
        return self._x[1:]

    @property
    def y(self):
        return self._y[1:]

    @property
    def a(self):
        result = [[100 for _ in range(self.n)] for _ in range(2 ** self.n)]
        for i in range(2 ** self.n):
            for j in range(self.n):
                result[i][j] = self._a[i][j + 1]
        return result

    @property
    def priors(self):
        result = [[100 for _ in range(self.n)] for _ in range(2 ** self.n)]
        for i in range(2 ** self.n):
            for j in range(self.n):
                result[i][j] = self._priors[i][j + 1]
        return result

    @property
    def a_string(self):
        """ Returns a in a printable string format"""
        result = ""
        for elem in self.a:
            result += str(elem) + '\n'
        return result

    @property
    def priors_string(self):
        """ Returns a in a printable string format"""
        result = ""
        for elem in self.priors:
            result += str(elem) + '\n'
        return result

    @property
    def nskip(self):
        return len(self.skip_nodes_dic.keys())

g = Graph()
# g.read_graph_from_file('test_case_6.47.txt')
# g.read_graph_from_file('test_case_7.89.txt', skip_nodes=[4])
g.read_graph_from_file('tsp.txt', skip_nodes_list=[4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22])
# g.read_graph_from_file('tsp_simplified01.txt')
tsp_result = g.tsp()
print 'TSP length=', tsp_result
print 'prior: \n', g.priors_string
print 'a: \n', g.a_string
print 'TSP path: ', g.path