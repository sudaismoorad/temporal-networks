# Temporal-Networks:

# Table of Contents

- [Description](#description)
- [Requirement](#requirement)
- [How to use it](#how-to-use-it)
  - [Simple Temporal Networks](#simple-temporal-network)
  - [Simple Temporal Networks with Uncertainty](#simple-temporal-network-with-uncertainty)
- [Extra Information](#extra-information)
- [TODO](#todo)

## Description

A temporal network is a data structure for representing and reasoning about time, especially constraints on activities.  
Different kinds of temporal networks have different kinds of features (e.g., some can accommodate actions with uncertain durations,
while others can accommodate actions that generate information in real time). This project will involve implementing algorithms from
the literature on Temporal Networks with the aim of empirically evaluating them in reproducible ways.

## Requirement

Python3 support is needed for the module to work:

- You will also need the matplotlib and networkx modules. To install them simply use the following commands:

```
pip3 install matplotlib
pip3 install networkx
```

## How to use it

There is currently support for two types of temporal networks (more to be added in the future):

- Simple Temporal Networks
- Simple Temporal Networks with Uncertainty

### Simple Temporal Network

The STN class creates a Simple Temporal Network with the following algorithms:

#### Algorithms we implemented

1. Visualizing STNs: Calling the vizualize method in the STN class creates a matplotlib plot of
   the STN. To vizualize an STN simply call the method like this:
   ```
   stn.visualize()
   ```
2. Consistency checking: Does an STN have a solution?
3. Generating or incrementally updating solutions for STNs
4. All-pairs, shortest-paths algorithms for STNs
5. Algorithms associated with real-time execution of STNs (“dispatchability”)
6. Generation of random STNs to support empirical evaluation
7. Different kinds of “path-consistency” algorithms for STNs

All algorithms can be accessed by importing the stn_algorithms module as follows:
```
from stn_algorithms import *
# (add examples here)
```

#### Algorithms on STNs

1. Floyd-Warshall, Bellman-Ford, Dijkstra, Johnson's
2. Dispatchability algorithm (Tsamardinos & Morris, 1998)
3. Path Consistency (Dechter et al., 1991; Chleq, 1995; Planken, 2013)
4. Incrementally updating solutions (Ramalingam, 1995)

### Simple Temporal Network with Uncertainty

The STNU creates a Simple Temporal Network with Uncertainty with the following algorithms:

#### Algorithms we implemented

1. Visualizing STNUs: Calling the vizualize method in the STN class creates a matplotlib plot of
   the STNU
2. Generating “chordal” (a.k.a., “triangulated”) graphs for STNs
3. Dynamic controllability-checking algorithms for STNUs

#### Algorithms on STNUs

1. DC-checking algorithms for STNUs (Morris, 2014; Cairo et al., 2018)

## TODO

1. Add support for other types of temporal networks, e.g., CSTNU's, Hyper Temporal Networks etc.
2. Random generation of temporal networks
