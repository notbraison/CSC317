import math
import heapq

from location import Location
from distance import Distance
from typing import Dict, Set, Tuple, Union
from stack import Stack
from location_names import location_names

locations: Dict[str, Location] = {}
for location_name in location_names:
    locations[location_name.value] = Location(location_name.value)


def unvisit_locations():
    for name, location in locations.items():
        location.visited = False


romania: Dict[Location, Set[Distance]] = {
    location_names.ARAD.value: set([
        Distance(75, locations[location_names.ZERIND.value]),
        Distance(140, locations[location_names.SIBIU.value]),
        Distance(118, locations[location_names.TIMISOARA.value])
    ]),
    location_names.BUCHAREST.value: set([
        Distance(85, locations[location_names.URZICENI.value]),
        Distance(90, locations[location_names.GIURGIU.value]),
        Distance(101, locations[location_names.PITESTI.value]),
        Distance(211, locations[location_names.FARAGAS.value])
    ]),
    location_names.CRAIOVA.value: set([
        Distance(120, locations[location_names.DOBRETA.value]),
        Distance(138, locations[location_names.PITESTI.value]),
        Distance(146, locations[location_names.RIMNICU_VILCEA.value]),
    ]),
    location_names.DOBRETA.value: set([
        Distance(75, locations[location_names.MEHADIA.value]),
        Distance(120, locations[location_names.CRAIOVA.value]),
        Distance(75, locations[location_names.ZERIND.value]),
    ]),
    location_names.EFORIE.value: set([
        Distance(86, locations[location_names.HIRSOVA.value]),
    ]),
    location_names.FARAGAS.value: set([
        Distance(99, locations[location_names.SIBIU.value]),
        Distance(211, locations[location_names.BUCHAREST.value]),
    ]),
    location_names.GIURGIU.value: set([
        Distance(90, locations[location_names.BUCHAREST.value]),
    ]),
    location_names.HIRSOVA.value: set([
        Distance(98, locations[location_names.URZICENI.value]),
        Distance(86, locations[location_names.EFORIE.value]),
    ]),
    location_names.IASI.value: set([
        Distance(87, locations[location_names.NEAMT.value]),
        Distance(92, locations[location_names.VASLUI.value]),
    ]),
    location_names.LUGOJ.value: set([
        Distance(111, locations[location_names.TIMISOARA.value]),
        Distance(70, locations[location_names.MEHADIA.value]),
    ]),
    location_names.MEHADIA.value: set([
        Distance(70, locations[location_names.LUGOJ.value]),
        Distance(75, locations[location_names.DOBRETA.value]),
    ]),
    location_names.NEAMT.value: set([
        Distance(87, locations[location_names.IASI.value]),
    ]),
    location_names.ORADEA.value: set([
        Distance(71, locations[location_names.ZERIND.value]),
        Distance(151, locations[location_names.SIBIU.value]),
    ]),
    location_names.PITESTI.value: set([
        Distance(97, locations[location_names.RIMNICU_VILCEA.value]),
        Distance(101, locations[location_names.BUCHAREST.value]),
        Distance(138, locations[location_names.CRAIOVA.value]),
    ]),
    location_names.RIMNICU_VILCEA.value: set([
        Distance(80, locations[location_names.SIBIU.value]),
        Distance(97, locations[location_names.PITESTI.value]),
        Distance(146, locations[location_names.CRAIOVA.value]),
    ]),
    location_names.SIBIU.value: set([
        Distance(80, locations[location_names.RIMNICU_VILCEA.value]),
        Distance(99, locations[location_names.FARAGAS.value]),
        Distance(151, locations[location_names.ORADEA.value]),
        Distance(140, locations[location_names.ARAD.value]),
    ]),
    location_names.TIMISOARA.value: set([
        Distance(118, locations[location_names.ARAD.value]),
        Distance(111, locations[location_names.LUGOJ.value]),
    ]),
    location_names.URZICENI.value: set([
        Distance(85, locations[location_names.BUCHAREST.value]),
        Distance(98, locations[location_names.HIRSOVA.value]),
        Distance(142, locations[location_names.VASLUI.value]),
    ]),
    location_names.VASLUI.value: set([
        Distance(92, locations[location_names.IASI.value]),
        Distance(142, locations[location_names.URZICENI.value]),
    ]),
    location_names.ZERIND.value: set([
        Distance(71, locations[location_names.ORADEA.value]),
        Distance(75, locations[location_names.ARAD.value]),
    ]),
}


def dfs(current_location_name: str):
    # Start with location specified in parameter
    current_location: Location = locations[current_location_name]
    if not current_location:
        print(f"'{current_location_name}' is not a valid location")
    # Add necessary data structures
    visited = set()
    to_visit = Stack[Distance]()
    # Add start location to visited list and flag it as visited
    current_location.visited = True
    visited.add(current_location.name)

    # Add the neighbours to the stack
    neighbours = romania[current_location_name]
    for neighbour in neighbours:
        to_visit.push(neighbour)

    # print(to_visit.pop().destination)
    while not to_visit.isEmpty():
        # Pop from stack and flag it visited, and append it to list
        current_location = to_visit.pop().destination
        # print(f"{current_location.name} is being visited")
        current_location.visited = True
        visited.add(current_location.name)

        # Get neighbours of current node
        neighbours = romania[current_location.name]

        for neighbour in neighbours:
            # Only add locations not visited
            if not neighbour.destination.visited:
                to_visit.push(neighbour)

    # Unvisit nodes to allow for another traversal
    unvisit_locations()

    # Convert to list to allow for sorting
    visited = list(visited)
    visited.sort()
    return visited


def dijkstra(start: str):
    shortest_paths: Dict[str, Tuple[int, Union(Location | None)]] = dict()
    # Generate the shortest paths data structure
    for location_name in location_names:
        # If the name of the start location is same, then set path to zero
        # else, set path to infinity
        if start == location_name.value:
            shortest_paths[start] = (0, locations[start].name)
        else:
            shortest_paths[location_name.value] = (math.inf, None)

    priority_queue = []

    heapq.heappush(priority_queue, (0, start))

    while len(priority_queue) != 0:
        current = heapq.heappop(priority_queue)
        current_location_name = current[1]
        if locations[current_location_name].visited:
            continue

        for neighbour in romania[current_location_name]:
            cumulative_distance = shortest_paths[current_location_name][0] + neighbour.distance
            if cumulative_distance < shortest_paths[neighbour.destination.name][0]:
                shortest_paths[neighbour.destination.name] = (cumulative_distance, locations[current_location_name].name)
                heapq.heappush(priority_queue, (shortest_paths[neighbour.destination.name][0], neighbour.destination.name))
    return shortest_paths


def travel(start: str, end: str):
    shortest_paths = dijkstra(start)

    locations = []
    # Add end first
    locations.append(end)
    current = shortest_paths[end][1]

    # To handle the case of someone putting the same start and end
    if start == end:
        return [start]

    # Add onto list the intermediate paths
    while current != start:
        locations.append(current)
        current = shortest_paths[current][1]

    # Add start last
    locations.append(start)

    # Reverse since list is in reverse
    locations.reverse()

    return {
        "path": locations,
        "distance": shortest_paths[end][0]
    }


print("DFS")
print("---")
print(dfs(location_names.ARAD.value))
print("DIJKSTRA")
print("--------")
print(dijkstra(location_names.ARAD.value))
print("SHORTEST PATH")
print("-------------")
print(travel(location_names.ARAD.value, location_names.HIRSOVA.value))
