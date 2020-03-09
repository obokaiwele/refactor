from enum import Enum
import copy


class City(Enum):
    SEATTLE = 1
    SAN_FRANCISCO = 2
    LAS_VEGAS = 3
    LOS_ANGELES = 4
    DENVER = 5
    MINNEAPOLIS = 6
    DALLAS = 7
    CHICAGO = 8
    WASHINGTON_DC = 9
    BOSTON = 10
    NEW_YORK = 11
    MIAMI = 12


mapping = {
    'Seattle': City.SEATTLE,
    'San Francisco': City.SAN_FRANCISCO,
    'Las Vegas': City.LAS_VEGAS,
    'Los Angeles': City.LOS_ANGELES,
    'Denver': City.DENVER,
    'Minneapolis': City.MINNEAPOLIS,
    'Dallas': City.DALLAS,
    'Chicago': City.CHICAGO,
    'Washington D.C.': City.WASHINGTON_DC,
    'Boston': City.BOSTON,
    'New York': City.NEW_YORK,
    'Miami': City.MIAMI,
}


class Network(object):
    def __init__(self, distances):
        self._distances = copy.deepcopy(distances)
        self._costs = self.one_way_costs()
        self._two_way_distances = self.two_way_distances()
        self._two_way_costs = self.two_way_costs()
        self._nodes = [city for city in City]

    def one_way_costs(self):
        costs = copy.deepcopy(self._distances)
        for k_outer, v_outer in costs.items():
            for k_inner, v_inner in v_outer.items():
                distance = costs[k_outer][k_inner]
                cost = 0
                if distance > 2000:
                    cost += 0.002 * (distance - 2000) + 0.003 * 1000 + 0.004 * 500 + 0.005 * 500
                elif distance > 1000:
                    cost += 0.003 * (distance - 1000) + 0.004 * 500 + 0.005 * 500
                elif distance > 500:
                    cost += 0.004 * (distance - 500) + 0.005 * 500
                else:
                    cost += 0.005 * distance
                costs[k_outer][k_inner] = cost
        return costs

    def two_way_distances(self):
        network = copy.deepcopy(self._distances)
        for k_outer, v_outer in self._distances.items():
            for k_inner, v_inner in v_outer.items():
                if k_inner not in network:
                    network[k_inner] = {}
                if k_inner not in network[k_inner].keys():
                    network[k_inner][k_outer] = v_inner
        return network

    def two_way_costs(self):
        network = copy.deepcopy(self._costs)
        for k_outer, v_outer in self._distances.items():
            for k_inner, v_inner in v_outer.items():
                if k_inner not in network:
                    network[k_inner] = {}
                if k_inner not in network[k_inner].keys():
                    network[k_inner][k_outer] = v_inner
        return network


    def dj(self, start_node, by_distance):
        """
        Dijkstra's algorithm for computing the minimum additive cost from a start node to all other nodes.
        :param nodes: all unique nodes
        :param costs: costs from one node to another
        :param start_node: start node
        :return: minimum additive cost from start node to all other nodes
        """
        unvisited_nodes = {node: None for node in self._nodes}
        visited_nodes = {}
        current_node = start_node
        current_cost = 0
        unvisited_nodes[current_node] = current_cost

        costs = self._two_way_costs
        if by_distance:
            costs = self._two_way_distances

        while True:
            for neighbor, cost in costs[current_node].items():
                if neighbor not in unvisited_nodes:
                    continue
                new_cost = current_cost + cost
                if unvisited_nodes[neighbor] is None or new_cost < unvisited_nodes[neighbor]:
                    unvisited_nodes[neighbor] = new_cost
            visited_nodes[current_node] = current_cost
            del unvisited_nodes[current_node]
            if not unvisited_nodes:
                break
            candidates = [node for node in unvisited_nodes.items() if node[1]]

            # we need the maximum, so sort from largest to smallest
            current_node, current_cost = sorted(candidates, key=lambda x: x[1], reverse=False)[0]
        return visited_nodes



def dj(nodes, costs, start_node):
    """
    Dijkstra's algorithm for computing the minimum additive cost from a start node to all other nodes.
    :param nodes: all unique nodes
    :param costs: costs from one node to another
    :param start_node: start node
    :return: minimum additive cost from start node to all other nodes
    """
    unvisited_nodes = {node: None for node in nodes}
    visited_nodes = {}
    current_node = start_node
    current_cost = 0
    unvisited_nodes[current_node] = current_cost
    while True:
        for neighbor, cost in costs[current_node].items():
            if neighbor not in unvisited_nodes:
                continue
            new_cost = current_cost + cost
            if unvisited_nodes[neighbor] is None or new_cost < unvisited_nodes[neighbor]:
                unvisited_nodes[neighbor] = new_cost
        visited_nodes[current_node] = current_cost
        del unvisited_nodes[current_node]
        if not unvisited_nodes:
            break
        candidates = [node for node in unvisited_nodes.items() if node[1]]

        # we need the maximum, so sort from largest to smallest
        current_node, current_cost = sorted(candidates, key=lambda x: x[1], reverse=False)[0]
    return visited_nodes


def get_key(dictionary, val):
    for key, value in dictionary.items():
        if val == value:
            return key
    return 'key does not exist'


def make_two_way(one_way):
    network = one_way.copy()
    for k_outer, v_outer in one_way.items():
        for k_inner, v_inner in v_outer.items():
            if k_inner not in network:
                network[k_inner] = {}
            if k_inner not in network[k_inner].keys():
                network[k_inner][k_outer] = v_inner
    return network


def generate_by_cost(one_way):
    for k_outer, v_outer in one_way.items():
        for k_inner, v_inner in v_outer.items():
            distance = one_way[k_outer][k_inner]
            cost = 0
            if distance > 2000:
                cost += 0.002 * (distance - 2000) + 0.003 * 1000 + 0.004 * 500 + 0.005 * 500
            elif distance > 1000:
                cost += 0.003 * (distance - 1000) + 0.004 * 500 + 0.005 * 500
            elif distance > 500:
                cost += 0.004 * (distance - 500) + 0.005 * 500
            else:
                cost += 0.005 * distance
            one_way[k_outer][k_inner] = cost
    return one_way


def get_network(by_distance=True):
    cities = {1: 'Seattle', 2: 'San Francisco', 3: 'Las Vegas', 4: 'Los Angeles', 5: 'Denver',
              6: 'Minneapolis', 7: 'Dallas', 8: 'Chicago', 9: 'Washington, D.C.', 10: 'Boston',
              11: 'New York', 12: 'Miami'}
    one_way = {1: {2: 1306, 5: 2161, 6: 2661},
               2: {3: 919, 4: 629},
               3: {4: 435, 5: 1225, 7: 1983},
               5: {6: 1483, 7: 1258},
               6: {7: 1532, 8: 661},
               7: {9: 2113, 12: 2161},
               8: {9: 1145, 10: 1613},
               9: {10: 725, 11: 383, 12: 1709},
               10: {11: 338},
               11: {12: 2145}}
    if not by_distance:
        one_way = generate_by_cost(one_way)
    two_way = make_two_way(one_way)
    return cities, two_way


def driver():
    print('\n\n')
    by_distance = input('Computing by (type 0 for distance or 1 for costs)? ')
    city_nodes, costs = get_network(by_distance=int(by_distance)==0)
    nodes = city_nodes.keys()
    start_city = input('What is the start city? ')
    start_node = get_key(city_nodes, start_city)
    paths = dj(nodes, costs, start_node)

    for k, v in paths.items():
        print(f'{start_city} : {city_nodes[k]} = {round(v, 4)}')


def main():
    distances = {
        City.SEATTLE: {
            City.SAN_FRANCISCO: 1306,
            City.DENVER: 2161,
            City.MINNEAPOLIS: 2661,
        },
        City.SAN_FRANCISCO: {
            City.LAS_VEGAS: 919,
            City.LOS_ANGELES: 629,
        },
        City.LAS_VEGAS: {
            City.LOS_ANGELES: 435,
            City.DENVER: 1225,
            City.DALLAS: 1983,
        },
        City.DENVER: {
            City.MINNEAPOLIS: 1483,
            City.DALLAS: 1258,
        },
        City.MINNEAPOLIS: {
            City.DALLAS: 1532,
            City.CHICAGO: 661,
        },
        City.DALLAS: {
            City.WASHINGTON_DC: 2113,
            City.MIAMI: 2161,
        },
        City.CHICAGO: {
            City.WASHINGTON_DC: 1145,
            City.BOSTON: 1613,
        },
        City.WASHINGTON_DC: {
            City.BOSTON: 725,
            City.NEW_YORK: 383,
            City.MIAMI: 1709,
        },
        City.BOSTON: {
            City.NEW_YORK: 338,
        },
        City.NEW_YORK: {
            City.MIAMI: 2145,
        },
    }

    print('\n\n')
    by_distance = input('Computing by (type 0 for distance or 1 for costs)? ')

    network = Network(distances)

    start_city = input('What is the start city? ')

    start_node = mapping[start_city]

    paths = network.dj(start_node, by_distance)

    for k, v in paths.items():
        print(f'{start_city} : {k.name} = {round(v, 4)}')



if __name__ == '__main__':
    # driver()
    main()
