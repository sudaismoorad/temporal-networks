from floyd_warshall import FloydWarshall
from bellman_ford import BellmanFord
from dijkstra import Dijkstra
from johnson import Johnson


__all__ = ['floyd_warshall', 'bellman_ford', 'dijkstra', 'johnson']


def floyd_warshall(network):
    return FloydWarshall.floyd_warshall(network)


def bellman_ford(network, src=-1):
    return BellmanFord.bellman_ford(network, src)


def dijkstra(network, src, succ_direction=True, potential_function=False):
    return Dijkstra.dijkstra(network, src, succ_direction, potential_function)


def johnson(network):
    return Johnson.johnson(network)
