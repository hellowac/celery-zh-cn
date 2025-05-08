.. _guide-debugging:

======================================
调试
======================================

Debugging

.. _tut-remote_debug:

远程调试任务（使用 pdb）
====================================

Debugging Tasks Remotely (using pdb)

基础知识
------------

Basics

.. tab:: 中文

    :mod:`celery.contrib.rdb` 是 :mod:`pdb` 的一个扩展版本，支持对无法访问终端的进程进行远程调试。

    使用示例：

    .. code-block:: python

        from celery import task
        from celery.contrib import rdb

        @task()
        def add(x, y):
            result = x + y
            rdb.set_trace()  # <- 设置断点
            return result

    :func:`~celery.contrib.rdb.set_trace` 会在当前位置设置一个断点，
    并创建一个套接字（socket），你可以通过 telnet 连接该端口，从而远程调试你的任务。

    调试器可能会被多个进程同时启动，因此不会使用固定端口，而是从一个基础端口（默认 6900）开始搜索可用端口。
    可以通过设置环境变量 :envvar:`CELERY_RDB_PORT` 来更改基础端口。

    默认情况下，调试器只允许本地主机访问；
    如需从外部访问，需设置环境变量 :envvar:`CELERY_RDB_HOST`。

    当 worker 执行到断点时，会记录如下日志信息：

    .. code-block:: text

        [INFO/MainProcess] Received task:
            tasks.add[d7261c71-4962-47e5-b342-2448bedd20e8]
        [WARNING/PoolWorker-1] Remote Debugger:6900:
            Please telnet 127.0.0.1 6900.  Type `exit` in session to continue.
        [2011-01-18 14:25:44,119: WARNING/PoolWorker-1] Remote Debugger:6900:
            Waiting for client...

    连接指定端口后，你将进入一个 `pdb` shell：

    .. code-block:: console

        $ telnet localhost 6900
        Connected to localhost.
        Escape character is '^]'.
        > /opt/devel/demoapp/tasks.py(128)add()
        -> return result
        (Pdb)

    输入 ``help`` 可以查看可用命令列表。
    如果你之前没有使用过 `pdb`，建议阅读 `Python Debugger Manual`_。

    以下是一个调试示例：读取变量 ``result`` 的值、修改它，并继续任务执行：

    .. code-block:: text

        (Pdb) result
        4
        (Pdb) result = 'hello from rdb'
        (Pdb) continue
        Connection closed by foreign host.

    我们“破坏性”修改的结果可以在 worker 日志中看到：

    .. code-block:: text

        [2011-01-18 14:35:36,599: INFO/MainProcess] Task
            tasks.add[d7261c71-4962-47e5-b342-2448bedd20e8] succeeded
            in 61.481s: 'hello from rdb'

.. tab:: 英文

    :mod:`celery.contrib.rdb` is an extended version of :mod:`pdb` that
    enables remote debugging of processes that doesn't have terminal
    access.

    Example usage:

    .. code-block:: python

        from celery import task
        from celery.contrib import rdb

        @task()
        def add(x, y):
            result = x + y
            rdb.set_trace()  # <- set break-point
            return result


    :func:`~celery.contrib.rdb.set_trace` sets a break-point at the current
    location and creates a socket you can telnet into to remotely debug
    your task.

    The debugger may be started by multiple processes at the same time,
    so rather than using a fixed port the debugger will search for an
    available port, starting from the base port (6900 by default).
    The base port can be changed using the environment variable
    :envvar:`CELERY_RDB_PORT`.

    By default the debugger will only be available from the local host,
    to enable access from the outside you have to set the environment
    variable :envvar:`CELERY_RDB_HOST`.

    When the worker encounters your break-point it'll log the following
    information:

    .. code-block:: text

        [INFO/MainProcess] Received task:
            tasks.add[d7261c71-4962-47e5-b342-2448bedd20e8]
        [WARNING/PoolWorker-1] Remote Debugger:6900:
            Please telnet 127.0.0.1 6900.  Type `exit` in session to continue.
        [2011-01-18 14:25:44,119: WARNING/PoolWorker-1] Remote Debugger:6900:
            Waiting for client...

    If you telnet the port specified you'll be presented
    with a `pdb` shell:

    .. code-block:: console

        $ telnet localhost 6900
        Connected to localhost.
        Escape character is '^]'.
        > /opt/devel/demoapp/tasks.py(128)add()
        -> return result
        (Pdb)

    Enter ``help`` to get a list of available commands,
    It may be a good idea to read the `Python Debugger Manual`_ if
    you have never used `pdb` before.

    To demonstrate, we'll read the value of the ``result`` variable,
    change it and continue execution of the task:

    .. code-block:: text

        (Pdb) result
        4
        (Pdb) result = 'hello from rdb'
        (Pdb) continue
        Connection closed by foreign host.

    The result of our vandalism can be seen in the worker logs:

    .. code-block:: text

        [2011-01-18 14:35:36,599: INFO/MainProcess] Task
            tasks.add[d7261c71-4962-47e5-b342-2448bedd20e8] succeeded
            in 61.481s: 'hello from rdb'

.. _`Python Debugger Manual`: http://docs.python.org/library/pdb.html


技巧
----

Tips

.. _breakpoint_signal:

启用断点信号
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Enabling the break-point signal

.. tab:: 中文

    如果设置了环境变量 :envvar:`CELERY_RDBSIG`，则在接收到 `SIGUSR2` 信号时，worker 将自动打开一个 rdb 会话。
    此行为适用于主进程和 worker 子进程。

    例如以下方式启动 worker：

    .. code-block:: console

        $ CELERY_RDBSIG=1 celery worker -l INFO

    随后你可以通过如下命令向任意一个 worker 进程发送信号以触发 rdb 会话：

    .. code-block:: console

        $ kill -USR2 <pid>

.. tab:: 英文

    If the environment variable :envvar:`CELERY_RDBSIG` is set, the worker
    will open up an rdb instance whenever the `SIGUSR2` signal is sent.
    This is the case for both main and worker processes.

    For example starting the worker with:

    .. code-block:: console

        $ CELERY_RDBSIG=1 celery worker -l INFO

    You can start an rdb session for any of the worker processes by executing:

    .. code-block:: console

        $ kill -USR2 <pid>
