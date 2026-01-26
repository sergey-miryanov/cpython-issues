def create_task(self, coro, **kwargs):
    """Schedule or begin executing a coroutine object.

    Return a task object.
    """
    task = ''
    if task._source_traceback:
        del task._source_traceback[-1]
    try:
        return task
    finally:
        # gh-128552: prevent a refcycle of
        # task.exception().__traceback__->BaseEventLoop.create_task->task
        del task
