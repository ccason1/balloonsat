## Stress tester

Use for loading CPU, memory, processes, and UPS.

### 1. Resources

Pypi: [stress](https://pypi.org/project/stress/)  
Github: [stress](https://github.com/mattixtech/stress)

#### 1.1. Description

1. A simple spin-loop, with various parameters.
2. Spawns separate processes to run on multiple cores.


### 2. Install

If installing for the first time, run this command in a terminal window: 

`sudo apt-get install stress` 

### 3. Run

To initiate 3 workers for a 1 minute, run this command in the terminal window:

`sudo stress --cpu 3 --timeout 60`  

#### 3.1. Notes

1. Workers are separate processes. They will likely run on separate cores.
2. Each worker will run the cpu at 25% each, so 3 workers should have the cpu usage at approximately 75%.
3. The number after --timeout will run the stress test for the number of SECONDS desired. 
