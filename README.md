# SWP

Simple workpools in simple workflow. Proof-of-concept code for long running
workers in SWF.

The basic idea is to have workers that run forever and continuously heartbeat -
on a cancel request, they will wrap up work. Work will by dynamically added and
removed as needed. Workers that die or fail to heartbeat will have their work
picked up by new workers.

### Usage

1. Register workers with `register.py`

2. Start decider(s) with `decider.py`

3. Start actor(s) with `actor.py`

4. Add work with `start.py`

5. Remove work with `stop.py <workflow-uid>`

5. Alternatively to adding or removing work, workers can be converged with
   `converge.py <yaml-file>`
