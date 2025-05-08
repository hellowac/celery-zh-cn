.. _guide-workers:

===============
Workers 指南
===============


Workers Guide


.. _worker-starting:

启动 worker
===================

Starting the worker

.. tab:: 中文

    .. admonition:: 守护进程化（Daemonizing）

        你可能希望使用守护进程工具将 worker 以后台进程的方式启动。
        请参阅 :ref:`daemonizing`，了解如何使用常见的服务管理器将 worker 启动为守护进程。

    你也可以通过以下命令在前台启动 worker：

    .. code-block:: console

        $ celery -A proj worker -l INFO

    要查看完整的命令行选项列表，请参阅 :mod:`~celery.bin.worker`，或直接运行：

    .. code-block:: console

        $ celery worker --help

    你可以在同一台机器上启动多个 worker，但请确保通过 :option:`--hostname <celery worker --hostname>` 参数为每个 worker 指定唯一的节点名：

    .. code-block:: console

        $ celery -A proj worker --loglevel=INFO --concurrency=10 -n worker1@%h
        $ celery -A proj worker --loglevel=INFO --concurrency=10 -n worker2@%h
        $ celery -A proj worker --loglevel=INFO --concurrency=10 -n worker3@%h

    ``hostname`` 参数支持以下变量展开：

    - ``%h``：主机名，包含域名。
    - ``%n``：仅主机名。
    - ``%d``：仅域名。

    假设当前主机名为 *george.example.com*，这些变量将被展开为：

    +----------+----------------+------------------------------+
    | 变量     | 模板           | 展开结果                     |
    +----------+----------------+------------------------------+
    | ``%h``   | ``worker1@%h`` | *worker1@george.example.com* |
    +----------+----------------+------------------------------+
    | ``%n``   | ``worker1@%n`` | *worker1@george*             |
    +----------+----------------+------------------------------+
    | ``%d``   | ``worker1@%d`` | *worker1@example.com*        |
    +----------+----------------+------------------------------+

    .. admonition:: 针对 :pypi:`supervisor` 用户的注意事项

        ``%`` 符号必须通过添加第二个 ``%`` 进行转义： `%%h`。

.. tab:: 英文

    .. admonition:: Daemonizing

        You probably want to use a daemonization tool to start
        the worker in the background. See :ref:`daemonizing` for help
        starting the worker as a daemon using popular service managers.

    You can start the worker in the foreground by executing the command:

    .. code-block:: console

        $ celery -A proj worker -l INFO

    For a full list of available command-line options see
    :mod:`~celery.bin.worker`, or simply do:

    .. code-block:: console

        $ celery worker --help

    You can start multiple workers on the same machine, but
    be sure to name each individual worker by specifying a
    node name with the :option:`--hostname <celery worker --hostname>` argument:

    .. code-block:: console

        $ celery -A proj worker --loglevel=INFO --concurrency=10 -n worker1@%h
        $ celery -A proj worker --loglevel=INFO --concurrency=10 -n worker2@%h
        $ celery -A proj worker --loglevel=INFO --concurrency=10 -n worker3@%h

    The ``hostname`` argument can expand the following variables:

    - ``%h``:  Hostname, including domain name.
    - ``%n``:  Hostname only.
    - ``%d``:  Domain name only.

    If the current hostname is *george.example.com*, these will expand to:

    +----------+----------------+------------------------------+
    | Variable | Template       | Result                       |
    +----------+----------------+------------------------------+
    | ``%h``   | ``worker1@%h`` | *worker1@george.example.com* |
    +----------+----------------+------------------------------+
    | ``%n``   | ``worker1@%n`` | *worker1@george*             |
    +----------+----------------+------------------------------+
    | ``%d``   | ``worker1@%d`` | *worker1@example.com*        |
    +----------+----------------+------------------------------+

    .. admonition:: Note for :pypi:`supervisor` users

        The ``%`` sign must be escaped by adding a second one: `%%h`.

.. _worker-stopping:

停止 worker
===================

Stopping the worker

.. tab:: 中文

    建议使用 :sig:`TERM` 信号来关闭 worker。

    当关闭被触发时，worker 会在实际退出前完成所有正在执行的任务。如果这些任务很重要，你应该等待它们完成后再执行进一步操作，例如发送 :sig:`KILL` 信号这类激进的命令。

    如果 worker 在合理时间内无法关闭（例如陷入死循环等），可以使用 :sig:`KILL` 信号强制终止它；但请注意，此时正在执行的任务将会丢失（即除非这些任务设置了 :attr:`~@Task.acks_late` 选项）。

    此外，由于进程无法拦截 :sig:`KILL` 信号，worker 将无法回收其子进程；你需要手动执行清理。以下命令通常可以完成这项工作：

    .. code-block:: console

        $ pkill -9 -f 'celery worker'

    如果你的系统中没有 :command:`pkill` 命令，也可以使用稍长一点的替代方式：

    .. code-block:: console

        $ ps auxww | awk '/celery worker/ {print $2}' | xargs kill -9

    .. versionchanged:: 5.2
        在 Linux 系统上，Celery 现在支持在 worker 终止后向所有子进程发送 :sig:`KILL` 信号。
        这是通过 ``prctl(2)`` 的 `PR_SET_PDEATHSIG` 选项实现的。

.. tab:: 英文

    Shutdown should be accomplished using the :sig:`TERM` signal.

    When shutdown is initiated the worker will finish all currently executing
    tasks before it actually terminates. If these tasks are important, you should
    wait for it to finish before doing anything drastic, like sending the :sig:`KILL`
    signal.

    If the worker won't shutdown after considerate time, for being
    stuck in an infinite-loop or similar, you can use the :sig:`KILL` signal to
    force terminate the worker: but be aware that currently executing tasks will
    be lost (i.e., unless the tasks have the :attr:`~@Task.acks_late`
    option set).

    Also as processes can't override the :sig:`KILL` signal, the worker will
    not be able to reap its children; make sure to do so manually. This
    command usually does the trick:

    .. code-block:: console

        $ pkill -9 -f 'celery worker'

    If you don't have the :command:`pkill` command on your system, you can use the slightly
    longer version:

    .. code-block:: console

        $ ps auxww | awk '/celery worker/ {print $2}' | xargs kill -9

    .. versionchanged:: 5.2
        On Linux systems, Celery now supports sending :sig:`KILL` signal to all child processes
        after worker termination. This is done via `PR_SET_PDEATHSIG` option of ``prctl(2)``.

.. _worker_shutdown:

关闭 worker
---------------

Worker Shutdown

.. tab:: 中文

    我们将使用 *Warm（温）、Soft（软）、Cold（冷）、Hard（硬）* 这几个术语来描述 worker 关闭的不同阶段。
    当收到 :sig:`TERM` 或 :sig:`QUIT` 信号时，worker 会启动关闭流程。
    在关闭流程中，:sig:`INT` （Ctrl-C）信号同样会被处理，并始终触发下一个关闭阶段。

.. tab:: 英文

    We will use the terms *Warm, Soft, Cold, Hard* to describe the different stages of worker shutdown.
    The worker will initiate the shutdown process when it receives the :sig:`TERM` or :sig:`QUIT` signal.
    The :sig:`INT` (Ctrl-C) signal is also handled during the shutdown process and always triggers the 
    next stage of the shutdown process.

.. _worker-warm-shutdown:

热关闭
~~~~~~~~~~~~~

Warm Shutdown

.. tab:: 中文

    当 worker 收到 :sig:`TERM` 信号时，会启动一次温关闭（warm shutdown）。
    worker 会在终止之前完成当前正在执行的所有任务。
    第一次收到 :sig:`INT` （Ctrl-C）信号时，也会启动一次温关闭。

    温关闭会停止调用 :func:`WorkController.start() <celery.worker.worker.WorkController.start>`，
    并调用 :func:`WorkController.stop() <celery.worker.worker.WorkController.stop>`。

    - 在温关闭阶段，收到的后续 :sig:`TERM` 信号将被忽略。
    - 下一次收到 :sig:`INT` 信号将触发关闭流程的下一个阶段。


.. tab:: 英文

    When the worker receives the :sig:`TERM` signal, it will initiate a warm shutdown. The worker will
    finish all currently executing tasks before it actually terminates. The first time the worker receives
    the :sig:`INT` (Ctrl-C) signal, it will initiate a warm shutdown as well.

    The warm shutdown will stop the call to :func:`WorkController.start() <celery.worker.worker.WorkController.start>`
    and will call :func:`WorkController.stop() <celery.worker.worker.WorkController.stop>`.

    - Additional :sig:`TERM` signals will be ignored during the warm shutdown process.
    - The next :sig:`INT` signal will trigger the next stage of the shutdown process.

.. _worker-cold-shutdown:

.. _worker-REMAP_SIGTERM:

冷关闭
~~~~~~~~~~~~~

Cold Shutdown

.. tab:: 中文

    冷关机（Cold shutdown）在 worker 收到 :sig:`QUIT` 信号时触发。此时 worker 会立即停止所有正在执行的任务并终止进程。

    .. note::

        如果环境变量 ``REMAP_SIGTERM`` 被设置为 ``SIGQUIT``，那么当 worker 收到 :sig:`TERM` 信号时也将会触发冷关机，而非温关机。

    冷关机会停止对 :func:`WorkController.start() <celery.worker.worker.WorkController.start>` 的调用，并改为调用 :func:`WorkController.terminate() <celery.worker.worker.WorkController.terminate>`。

    如果温关机已经开始，切换到冷关机时将运行一个名为 ``on_cold_shutdown`` 的信号处理器，用于从主进程中取消所有正在执行的任务，并可能触发 :ref:`worker-soft-shutdown`。

.. tab:: 英文

    Cold shutdown is initiated when the worker receives the :sig:`QUIT` signal. The worker will stop
    all currently executing tasks and terminate immediately.

    .. note::

        If the environment variable ``REMAP_SIGTERM`` is set to ``SIGQUIT``, the worker will also initiate
        a cold shutdown when it receives the :sig:`TERM` signal instead of a warm shutdown.

    The cold shutdown will stop the call to :func:`WorkController.start() <celery.worker.worker.WorkController.start>`
    and will call :func:`WorkController.terminate() <celery.worker.worker.WorkController.terminate>`.

    If the warm shutdown already started, the transition to cold shutdown will run a signal handler ``on_cold_shutdown``
    to cancel all currently executing tasks from the MainProcess and potentially trigger the :ref:`worker-soft-shutdown`.

.. _worker-soft-shutdown:

软关闭
~~~~~~~~~~~~~

Soft Shutdown

.. tab:: 中文

    .. versionadded:: 5.5

    软关机（Soft shutdown）是一种有时间限制的温关机，发生在冷关机之前。worker 会允许所有当前正在执行的任务在 :setting:`worker_soft_shutdown_timeout` 指定的秒数内完成，然后才终止进程。如果时间限制到达，worker 将启动冷关机并取消所有正在执行的任务。如果在软关机期间收到 :sig:`QUIT` 信号，worker 会取消所有任务，但仍会等待设定的时间限制结束后再终止，从而以更优雅的方式完成冷关机。

    为了兼容旧有行为，软关机默认是禁用的。要启用软关机，需将 :setting:`worker_soft_shutdown_timeout` 设置为一个正的浮点数。当没有任务正在运行时，软关机会被跳过。若希望在空闲状态下也强制执行软关机，还需启用 :setting:`worker_enable_soft_shutdown_on_idle` 设置。

    .. warning::

        如果 worker 当前没有运行任务，但有 ETA 任务被保留，除非启用了 :setting:`worker_enable_soft_shutdown_on_idle`，软关机不会被触发，这可能导致冷关机期间任务丢失。使用 ETA 任务时，建议启用空闲时软关机功能。可根据实际部署情况尝试不同的 :setting:`worker_soft_shutdown_timeout` 配置值，以最大程度减少任务丢失风险。

    例如，当设置 ``worker_soft_shutdown_timeout=3`` 时，worker 会允许最多 3 秒的时间让正在执行的任务完成。如果时间到了，则执行冷关机并取消所有任务。

    .. code-block:: console

        [INFO/MainProcess] Task myapp.long_running_task[6f748357-b2c7-456a-95de-f05c00504042] received
        [WARNING/ForkPoolWorker-8] long_running_task is running, sleeping 1/2000s
        [WARNING/ForkPoolWorker-8] long_running_task is running, sleeping 2/2000s
        [WARNING/ForkPoolWorker-8] long_running_task is running, sleeping 3/2000s
        ^C
        worker: Hitting Ctrl+C again will initiate cold shutdown, terminating all running tasks!

        worker: Warm shutdown (MainProcess)
        [WARNING/ForkPoolWorker-8] long_running_task is running, sleeping 4/2000s
        [WARNING/ForkPoolWorker-8] long_running_task is running, sleeping 5/2000s
        [WARNING/ForkPoolWorker-8] long_running_task is running, sleeping 6/2000s
        ^C
        worker: Hitting Ctrl+C again will terminate all running tasks!
        [WARNING/MainProcess] Initiating Soft Shutdown, terminating in 3 seconds
        [WARNING/ForkPoolWorker-8] long_running_task is running, sleeping 7/2000s
        [WARNING/ForkPoolWorker-8] long_running_task is running, sleeping 8/2000s
        [WARNING/ForkPoolWorker-8] long_running_task is running, sleeping 9/2000s
        [WARNING/MainProcess] Restoring 1 unacknowledged message(s)

    - 下一次 :sig:`QUIT` 信号将在软关机中取消仍在运行的任务，但 worker 仍会等待时间限制结束才终止。
    - 第二次（或之后的） :sig:`QUIT` 或 :sig:`INT` 信号将会触发下一阶段的关机流程。

.. tab:: 英文

    .. versionadded:: 5.5

    Soft shutdown is a time limited warm shutdown, initiated just before the cold shutdown. The worker will
    allow :setting:`worker_soft_shutdown_timeout` seconds for all currently executing tasks to finish before
    it terminates. If the time limit is reached, the worker will initiate a cold shutdown and cancel all currently
    executing tasks. If the :sig:`QUIT` signal is received during the soft shutdown, the worker will cancel all
    currently executing tasks but still wait for the time limit to finish before terminating, giving a chance for
    the worker to perform the cold shutdown a little more gracefully.

    The soft shutdown is disabled by default to maintain backward compatibility with the :ref:`worker-cold-shutdown`
    behavior. To enable the soft shutdown, set :setting:`worker_soft_shutdown_timeout` to a positive float value.
    The soft shutdown will be skipped if there are no tasks running. To force the soft shutdown, *also* enable the
    :setting:`worker_enable_soft_shutdown_on_idle` setting.

    .. warning::

        If the worker is not running any task but has ETA tasks reserved, the soft shutdown will not be initiated
        unless the :setting:`worker_enable_soft_shutdown_on_idle` setting is enabled, which may lead to task loss
        during the cold shutdown. When using ETA tasks, it is recommended to enable the soft shutdown on idle.
        Experiment which :setting:`worker_soft_shutdown_timeout` value works best for your setup to reduce the risk
        of task loss to a minimum.

    For example, when setting ``worker_soft_shutdown_timeout=3``, the worker will allow 3 seconds for all currently
    executing tasks to finish before it terminates. If the time limit is reached, the worker will initiate a cold shutdown
    and cancel all currently executing tasks.

    .. code-block:: console

        [INFO/MainProcess] Task myapp.long_running_task[6f748357-b2c7-456a-95de-f05c00504042] received
        [WARNING/ForkPoolWorker-8] long_running_task is running, sleeping 1/2000s
        [WARNING/ForkPoolWorker-8] long_running_task is running, sleeping 2/2000s
        [WARNING/ForkPoolWorker-8] long_running_task is running, sleeping 3/2000s
        ^C
        worker: Hitting Ctrl+C again will initiate cold shutdown, terminating all running tasks!

        worker: Warm shutdown (MainProcess)
        [WARNING/ForkPoolWorker-8] long_running_task is running, sleeping 4/2000s
        [WARNING/ForkPoolWorker-8] long_running_task is running, sleeping 5/2000s
        [WARNING/ForkPoolWorker-8] long_running_task is running, sleeping 6/2000s
        ^C
        worker: Hitting Ctrl+C again will terminate all running tasks!
        [WARNING/MainProcess] Initiating Soft Shutdown, terminating in 3 seconds
        [WARNING/ForkPoolWorker-8] long_running_task is running, sleeping 7/2000s
        [WARNING/ForkPoolWorker-8] long_running_task is running, sleeping 8/2000s
        [WARNING/ForkPoolWorker-8] long_running_task is running, sleeping 9/2000s
        [WARNING/MainProcess] Restoring 1 unacknowledged message(s)

    - The next :sig:`QUIT` signal will cancel the tasks that are still running in the soft shutdown, but the worker
      will still wait for the time limit to finish before terminating.
    - The next (2nd) :sig:`QUIT` or :sig:`INT` signal will trigger the next stage of the shutdown process.

.. _worker-hard-shutdown:

硬关闭
~~~~~~~~~~~~~

Hard Shutdown

.. tab:: 中文

    .. versionadded:: 5.5

    硬关机（Hard shutdown）主要用于本地开发或调试场景，允许通过重复发送 :sig:`INT` （Ctrl-C）信号强制 worker 立即终止。worker 会立即停止所有正在执行的任务，并在主进程中抛出 :exc:`@WorkerTerminate` 异常来退出。

    例如，注意以下日志中的 ``^C`` 表示用户通过 :sig:`INT` 信号手动推进关机阶段：

    .. code-block:: console

        [INFO/MainProcess] Task myapp.long_running_task[7235ac16-543d-4fd5-a9e1-2d2bb8ab630a] received
        [WARNING/ForkPoolWorker-8] long_running_task is running, sleeping 1/2000s
        [WARNING/ForkPoolWorker-8] long_running_task is running, sleeping 2/2000s
        ^C
        worker: Hitting Ctrl+C again will initiate cold shutdown, terminating all running tasks!

        worker: Warm shutdown (MainProcess)
        [WARNING/ForkPoolWorker-8] long_running_task is running, sleeping 3/2000s
        [WARNING/ForkPoolWorker-8] long_running_task is running, sleeping 4/2000s
        ^C
        worker: Hitting Ctrl+C again will terminate all running tasks!
        [WARNING/MainProcess] Initiating Soft Shutdown, terminating in 10 seconds
        [WARNING/ForkPoolWorker-8] long_running_task is running, sleeping 5/2000s
        [WARNING/ForkPoolWorker-8] long_running_task is running, sleeping 6/2000s
        ^C
        Waiting gracefully for cold shutdown to complete...

        worker: Cold shutdown (MainProcess)
        ^C[WARNING/MainProcess] Restoring 1 unacknowledged message(s)

    .. warning::

        日志中 ``Restoring 1 unacknowledged message(s)`` 的信息可能具有误导性，因为在硬关机后并不能保证这些消息会被恢复。相较而言，:ref:`worker-soft-shutdown` 可以在温关机与冷关机之间提供一个时间窗口，从而显著提升关机过程的优雅性。

.. tab:: 英文

    .. versionadded:: 5.5

    Hard shutdown is mostly for local or debug purposes, allowing to spam the :sig:`INT` (Ctrl-C) signal
    to force the worker to terminate immediately. The worker will stop all currently executing tasks and
    terminate immediately by raising a :exc:`@WorkerTerminate` exception in the MainProcess.

    For example, notice the ``^C`` in the logs below (using the :sig:`INT` signal to move from stage to stage):

    .. code-block:: console

        [INFO/MainProcess] Task myapp.long_running_task[7235ac16-543d-4fd5-a9e1-2d2bb8ab630a] received
        [WARNING/ForkPoolWorker-8] long_running_task is running, sleeping 1/2000s
        [WARNING/ForkPoolWorker-8] long_running_task is running, sleeping 2/2000s
        ^C
        worker: Hitting Ctrl+C again will initiate cold shutdown, terminating all running tasks!

        worker: Warm shutdown (MainProcess)
        [WARNING/ForkPoolWorker-8] long_running_task is running, sleeping 3/2000s
        [WARNING/ForkPoolWorker-8] long_running_task is running, sleeping 4/2000s
        ^C
        worker: Hitting Ctrl+C again will terminate all running tasks!
        [WARNING/MainProcess] Initiating Soft Shutdown, terminating in 10 seconds
        [WARNING/ForkPoolWorker-8] long_running_task is running, sleeping 5/2000s
        [WARNING/ForkPoolWorker-8] long_running_task is running, sleeping 6/2000s
        ^C
        Waiting gracefully for cold shutdown to complete...

        worker: Cold shutdown (MainProcess)
        ^C[WARNING/MainProcess] Restoring 1 unacknowledged message(s)

    .. warning::

        The log ``Restoring 1 unacknowledged message(s)`` is misleading as it is not guaranteed that the message
        will be restored after a hard shutdown. The :ref:`worker-soft-shutdown` allows adding a time window just between
        the warm and the cold shutdown that improves the gracefulness of the shutdown process.

.. _worker-restarting:

重启 worker
=====================

Restarting the worker

.. tab:: 中文

    若要重启 worker，应先发送 `TERM` 信号终止原有进程，再启动新实例。开发环境下建议使用 `celery multi` 管理 worker：

    .. code-block:: console

        $ celery multi start 1 -A proj -l INFO -c4 --pidfile=/var/run/celery/%n.pid
        $ celery multi restart 1 --pidfile=/var/run/celery/%n.pid

    对于生产部署，建议使用初始化脚本或进程管理工具（见 :ref:`daemonizing` ）。

    除了停止再启动外，还可以使用 :sig:`HUP` 信号直接重启 worker。需要注意的是，此方式由 worker 自行负责重启，可能不稳定，因此不建议在生产环境中使用：

    .. code-block:: console

        $ kill -HUP $pid

    .. note::

        只有当 worker 在后台以守护进程（daemon）方式运行（即无控制终端）时， :sig:`HUP` 重启才有效。

        macOS 平台因系统限制，禁用了 :sig:`HUP` 信号的处理。

.. tab:: 英文

    To restart the worker you should send the `TERM` signal and start a new
    instance. The easiest way to manage workers for development
    is by using `celery multi`:

    .. code-block:: console

        $ celery multi start 1 -A proj -l INFO -c4 --pidfile=/var/run/celery/%n.pid
        $ celery multi restart 1 --pidfile=/var/run/celery/%n.pid

    For production deployments you should be using init-scripts or a process
    supervision system (see :ref:`daemonizing`).

    Other than stopping, then starting the worker to restart, you can also
    restart the worker using the :sig:`HUP` signal. Note that the worker
    will be responsible for restarting itself so this is prone to problems and
    isn't recommended in production:

    .. code-block:: console

        $ kill -HUP $pid

    .. note::

        Restarting by :sig:`HUP` only works if the worker is running
        in the background as a daemon (it doesn't have a controlling
        terminal).

        :sig:`HUP` is disabled on macOS because of a limitation on
        that platform.

与broker服务器连接丢失时自动重新连接
====================================================

Automatic re-connection on connection loss to broker

.. tab:: 中文

    .. versionadded:: 5.3

    除非将 :setting:`broker_connection_retry_on_startup` 设置为 False，
    Celery 会在首次连接中断后自动尝试重新连接到 broker。
    而 :setting:`broker_connection_retry` 控制后续连接中断时是否自动重试重新连接。

    .. versionadded:: 5.1

    如果将 :setting:`worker_cancel_long_running_tasks_on_connection_loss` 设置为 True，
    Celery 也会取消所有当前正在运行的长时间运行任务。

    .. versionadded:: 5.3

    由于消息中间件无法追踪连接丢失前已取出的任务数量，
    Celery 会将预取计数（prefetch count）减少为当前正在运行的任务数量乘以
    :setting:`worker_prefetch_multiplier` 的结果。
    该预取计数将在每次完成一个连接丢失前启动的任务后，逐步恢复至允许的最大值。

    此特性默认启用，可通过将 :setting:`worker_enable_prefetch_count_reduction` 设置为 False 来禁用。

.. tab:: 英文

    .. versionadded:: 5.3

    Unless :setting:`broker_connection_retry_on_startup` is set to False,
    Celery will automatically retry reconnecting to the broker after the first
    connection loss. :setting:`broker_connection_retry` controls whether to automatically
    retry reconnecting to the broker for subsequent reconnects.

    .. versionadded:: 5.1

    If :setting:`worker_cancel_long_running_tasks_on_connection_loss` is set to True,
    Celery will also cancel any long running task that is currently running.

    .. versionadded:: 5.3

    Since the message broker does not track how many tasks were already fetched before
    the connection was lost, Celery will reduce the prefetch count by the number of
    tasks that are currently running multiplied by :setting:`worker_prefetch_multiplier`.
    The prefetch count will be gradually restored to the maximum allowed after
    each time a task that was running before the connection was lost is complete.

    This feature is enabled by default, but can be disabled by setting False
    to :setting:`worker_enable_prefetch_count_reduction`.

.. _worker-process-signals:

进程信号
===============

Process Signals

.. tab:: 中文

    Worker 的主进程会覆盖以下信号处理行为：

    +--------------+--------------------------------------------------+
    | :sig:`TERM`  | 温关（warm shutdown），等待任务完成后退出。         |
    +--------------+--------------------------------------------------+
    | :sig:`QUIT`  | 冷关（cold shutdown），尽快终止。                   |
    +--------------+--------------------------------------------------+
    | :sig:`USR1`  | 打印所有活跃线程的堆栈跟踪。                        |
    +--------------+--------------------------------------------------+
    | :sig:`USR2`  | 远程调试，参见 :mod:`celery.contrib.rdb`。         |
    +--------------+--------------------------------------------------+

.. tab:: 英文

    The worker's main process overrides the following signals:

    +--------------+-------------------------------------------------+
    | :sig:`TERM`  | Warm shutdown, wait for tasks to complete.      |
    +--------------+-------------------------------------------------+
    | :sig:`QUIT`  | Cold shutdown, terminate ASAP                   |
    +--------------+-------------------------------------------------+
    | :sig:`USR1`  | Dump traceback for all active threads.          |
    +--------------+-------------------------------------------------+
    | :sig:`USR2`  | Remote debug, see :mod:`celery.contrib.rdb`.    |
    +--------------+-------------------------------------------------+

.. _worker-files:

文件路径中的变量
=======================

Variables in file paths

.. tab:: 中文

    :option:`--logfile <celery worker --logfile>`、:option:`--pidfile <celery worker --pidfile>` 和
    :option:`--statedb <celery worker --statedb>` 等参数的文件路径可以包含变量占位符，
    Worker 会在运行时对其进行展开：

.. tab:: 英文

    The file path arguments for :option:`--logfile <celery worker --logfile>`,
    :option:`--pidfile <celery worker --pidfile>`, and
    :option:`--statedb <celery worker --statedb>` can contain variables that the
    worker will expand:

节点名称替换
----------------------

Node name replacements

.. tab:: 中文

    - ``%p``：完整节点名（node name）。
    - ``%h``：主机名（包含域名）。
    - ``%n``：主机名（不包含域名）。
    - ``%d``：域名部分。
    - ``%i``：Prefork 池中子进程索引，主进程为 0。
    - ``%I``：带分隔符的子进程索引。

    例如，当前主机名为 ``george@foo.example.com`` 时，将展开为：

    - ``--logfile=%p.log`` -> :file:`george@foo.example.com.log`
    - ``--logfile=%h.log`` -> :file:`foo.example.com.log`
    - ``--logfile=%n.log`` -> :file:`george.log`
    - ``--logfile=%d.log`` -> :file:`example.com.log`

.. tab:: 英文

    - ``%p``:  Full node name.
    - ``%h``:  Hostname, including domain name.
    - ``%n``:  Hostname only.
    - ``%d``:  Domain name only.
    - ``%i``:  Prefork pool process index or 0 if MainProcess.
    - ``%I``:  Prefork pool process index with separator.

    For example, if the current hostname is ``george@foo.example.com`` then
    these will expand to:

    - ``--logfile=%p.log`` -> :file:`george@foo.example.com.log`
    - ``--logfile=%h.log`` -> :file:`foo.example.com.log`
    - ``--logfile=%n.log`` -> :file:`george.log`
    - ``--logfile=%d.log`` -> :file:`example.com.log`

.. _worker-files-process-index:

Prefork 池进程索引
--------------------------

Prefork pool process index

.. tab:: 中文

    Prefork 子进程索引相关的占位符，会根据具体要打开该文件的进程展开为不同的文件名。
    
    这可用于为每个子进程指定独立的日志文件。
    
    需要注意的是：即使进程退出，或启用了 autoscale、``maxtasksperchild``、执行时间限制等机制，
    索引号也会保持在进程数限制内。换言之，该数字表示的是“进程索引”而非进程数量或进程 ID。
    
    * ``%i`` - 池中子进程索引，主进程为 0。
    
      例如：使用 ``-n worker1@example.com -c2 -f %n-%i.log`` 时，会生成三个日志文件：
    
      - :file:`worker1-0.log` （主进程）
      - :file:`worker1-1.log` （子进程 1）
      - :file:`worker1-2.log` （子进程 2）
    
    * ``%I`` - 带分隔符的池中子进程索引。
    
      例如：使用 ``-n worker1@example.com -c2 -f %n%I.log`` 时，会生成三个日志文件：
    
      - :file:`worker1.log` （主进程）
      - :file:`worker1-1.log` （子进程 1）
      - :file:`worker1-2.log` （子进程 2）

.. tab:: 英文

    The prefork pool process index specifiers will expand into a different
    filename depending on the process that'll eventually need to open the file.
    
    This can be used to specify one log file per child process.
    
    Note that the numbers will stay within the process limit even if processes
    exit or if autoscale/``maxtasksperchild``/time limits are used.  That is, the number
    is the *process index* not the process count or pid.
    
    * ``%i`` - Pool process index or 0 if MainProcess.
    
      Where ``-n worker1@example.com -c2 -f %n-%i.log`` will result in
      three log files:
      
      - :file:`worker1-0.log` (main process)
      - :file:`worker1-1.log` (pool process 1)
      - :file:`worker1-2.log` (pool process 2)
    
    * ``%I`` - Pool process index with separator.
    
      Where ``-n worker1@example.com -c2 -f %n%I.log`` will result in
      three log files:
      
      - :file:`worker1.log` (main process)
      - :file:`worker1-1.log` (pool process 1)
      - :file:`worker1-2.log` (pool process 2)

.. _worker-concurrency:

并发
===========

Concurrency

.. tab:: 中文

    默认情况下，Celery 使用多进程（multiprocessing）机制来并发执行任务，
    但你也可以使用 :ref:`Eventlet <concurrency-eventlet>`。
    工作进程/线程的数量可以通过 :option:`--concurrency <celery worker --concurrency>` 参数进行设置，
    默认值为机器上可用的 CPU 数量。

    .. admonition:: 进程数量（multiprocessing/prefork 池）

        通常来说，进程数量越多性能越好，但当数量达到某个临界点后，
        增加进程数反而会导致性能下降。
        有一些证据表明，运行多个 Worker 实例有时比只运行一个 Worker 更高效。
        例如，运行 3 个 Worker，每个都有 10 个池进程。
        你需要自行尝试以找到最适合你场景的配置，
        因为这会受到应用类型、工作负载、任务运行时间以及其他因素的影响。

.. tab:: 英文

    By default multiprocessing is used to perform concurrent execution of tasks,
    but you can also use :ref:`Eventlet <concurrency-eventlet>`. The number
    of worker processes/threads can be changed using the
    :option:`--concurrency <celery worker --concurrency>` argument and defaults
    to the number of CPUs available on the machine.

    .. admonition:: Number of processes (multiprocessing/prefork pool)

        More pool processes are usually better, but there's a cut-off point where
        adding more pool processes affects performance in negative ways.
        There's even some evidence to support that having multiple worker
        instances running, may perform better than having a single worker.
        For example 3 workers with 10 pool processes each. You need to experiment
        to find the numbers that works best for you, as this varies based on
        application, work load, task run times and other factors.

.. _worker-remote-control:

远程控制
==============

Remote control

.. tab:: 中文

    .. versionadded:: 2.0

    .. sidebar:: ``celery`` 命令

        :program:`celery` 程序用于从命令行执行远程控制指令。
        它支持下列所有命令。详情请参见 :ref:`monitoring-control`。

    :pool 支持: *prefork, eventlet, gevent, thread*, 阻塞型: *solo* （参见注释）
    :broker 支持: *amqp, redis*

    Worker 支持通过高优先级的广播消息队列进行远程控制。
    这些命令可以发送给所有 Worker，也可以只发送给指定的 Worker 列表。

    命令也可以请求回应。客户端可等待并收集这些回应。
    由于系统中没有中央服务可用来判断当前集群中有多少个 Worker，
    因此也无法准确预估将收到多少回应。
    为此，客户端提供了一个可配置的超时时间，即等待回应到达的时间上限（以秒为单位），
    默认值为 1 秒。
    如果在截止时间内 Worker 没有回应，这并不一定意味着该 Worker 没有响应，
    或者更糟糕的是已经挂掉，
    可能仅仅是因为网络延迟，或该 Worker 在处理命令时比较慢，因此应根据情况调整超时时间。

    除了超时时间，客户端还可以设置最多等待多少个回应。
    如果指定了目标 Worker，这一限制将默认为目标主机数。

    .. note::

        ``solo`` 类型的池也支持远程控制命令，
        但如果某个任务正在执行，任何待处理的控制命令都会被阻塞。
        因此当 Worker 比较繁忙时， ``solo`` 的远程控制用途会受到限制。
        此时应在客户端中提高等待回应的超时时间。

.. tab:: 英文

    .. versionadded:: 2.0

    .. sidebar:: The ``celery`` command

        The :program:`celery` program is used to execute remote control
        commands from the command-line. It supports all of the commands
        listed below. See :ref:`monitoring-control` for more information.

    :pool support: *prefork, eventlet, gevent, thread*, blocking:*solo* (see note)
    :broker support: *amqp, redis*

    Workers have the ability to be remote controlled using a high-priority
    broadcast message queue. The commands can be directed to all, or a specific
    list of workers.

    Commands can also have replies. The client can then wait for and collect
    those replies. Since there's no central authority to know how many
    workers are available in the cluster, there's also no way to estimate
    how many workers may send a reply, so the client has a configurable
    timeout — the deadline in seconds for replies to arrive in. This timeout
    defaults to one second. If the worker doesn't reply within the deadline
    it doesn't necessarily mean the worker didn't reply, or worse is dead, but
    may simply be caused by network latency or the worker being slow at processing
    commands, so adjust the timeout accordingly.

    In addition to timeouts, the client can specify the maximum number
    of replies to wait for. If a destination is specified, this limit is set
    to the number of destination hosts.

    .. note::

        The ``solo`` pool supports remote control commands,
        but any task executing will block any waiting control command,
        so it is of limited use if the worker is very busy. In that
        case you must increase the timeout waiting for replies in the client.

.. _worker-broadcast-fun:

:meth:`~@control.broadcast` 函数
----------------------------------------------------

The :meth:`~@control.broadcast` function

.. tab:: 中文

    以下是客户端用于向 Worker 发送指令的函数。
    某些远程控制命令也提供了更高级的接口，
    这些接口在内部会调用 :meth:`~@control.broadcast`，例如
    :meth:`~@control.rate_limit` 和 :meth:`~@control.ping`。

    以下为发送 :control:`rate_limit` 命令和参数的示例：

    .. code-block:: pycon

        >>> app.control.broadcast('rate_limit',
        ...                          arguments={'task_name': 'myapp.mytask',
        ...                                     'rate_limit': '200/m'})

    此操作将异步发送命令，并不会等待回应。
    若希望获取回应，可使用 `reply` 参数：

    .. code-block:: pycon

        >>> app.control.broadcast('rate_limit', {
        ...     'task_name': 'myapp.mytask', 'rate_limit': '200/m'}, reply=True)
        [{'worker1.example.com': 'New rate limit set successfully'},
        {'worker2.example.com': 'New rate limit set successfully'},
        {'worker3.example.com': 'New rate limit set successfully'}]

    通过 `destination` 参数可以指定命令接收的 Worker 列表：

    .. code-block:: pycon

        >>> app.control.broadcast('rate_limit', {
        ...     'task_name': 'myapp.mytask',
        ...     'rate_limit': '200/m'}, reply=True,
        ...                             destination=['worker1@example.com'])
        [{'worker1.example.com': 'New rate limit set successfully'}]

    当然，使用高级接口来设置速率限制更为方便，
    但也存在一些只能通过 :meth:`~@control.broadcast` 发送的命令。


.. tab:: 英文

    This is the client function used to send commands to the workers.
    Some remote control commands also have higher-level interfaces using
    :meth:`~@control.broadcast` in the background, like
    :meth:`~@control.rate_limit`, and :meth:`~@control.ping`.

    Sending the :control:`rate_limit` command and keyword arguments:

    .. code-block:: pycon

        >>> app.control.broadcast('rate_limit',
        ...                          arguments={'task_name': 'myapp.mytask',
        ...                                     'rate_limit': '200/m'})

    This will send the command asynchronously, without waiting for a reply.
    To request a reply you have to use the `reply` argument:

    .. code-block:: pycon

        >>> app.control.broadcast('rate_limit', {
        ...     'task_name': 'myapp.mytask', 'rate_limit': '200/m'}, reply=True)
        [{'worker1.example.com': 'New rate limit set successfully'},
        {'worker2.example.com': 'New rate limit set successfully'},
        {'worker3.example.com': 'New rate limit set successfully'}]

    Using the `destination` argument you can specify a list of workers
    to receive the command:

    .. code-block:: pycon

        >>> app.control.broadcast('rate_limit', {
        ...     'task_name': 'myapp.mytask',
        ...     'rate_limit': '200/m'}, reply=True,
        ...                             destination=['worker1@example.com'])
        [{'worker1.example.com': 'New rate limit set successfully'}]


    Of course, using the higher-level interface to set rate limits is much
    more convenient, but there are commands that can only be requested
    using :meth:`~@control.broadcast`.

命令
========

Commands

.. control:: revoke

``revoke``: 撤销任务
--------------------------

``revoke``: Revoking tasks

.. tab:: 中文

    :pool 支持: 全部， `terminate` 选项仅在 prefork、eventlet 和 gevent 中受支持  
    :broker 支持: *amqp, redis*  
    :command: :program:`celery -A proj control revoke <task_id>`

    所有 Worker 节点都会保留被撤销任务（revoked task）的任务 ID 信息，
    这些信息可能存储在内存中，也可能持久化在磁盘上（参见 :ref:`worker-persistent-revokes`）。

    .. note::

        可通过环境变量 ``CELERY_WORKER_REVOKES_MAX`` 设置内存中最多保留的被撤销任务数量，
        默认值为 50000。当超过此上限后，这些撤销信息将保留 10800 秒（即 3 小时）后过期。
        该过期时间可通过 ``CELERY_WORKER_REVOKE_EXPIRES`` 环境变量进行修改。

        成功任务的内存限制也可通过 ``CELERY_WORKER_SUCCESSFUL_MAX`` 和
        ``CELERY_WORKER_SUCCESSFUL_EXPIRES`` 两个环境变量设置，默认值分别为 1000 和 10800。

    当 Worker 收到撤销请求时，它将跳过该任务的执行，
    但不会中止一个已经在执行中的任务，除非设置了 `terminate` 选项。

    .. note::

        `terminate` 选项是管理员处理卡住任务的最后手段。
        它并不是终止任务本身，而是终止执行该任务的进程。
        而且该进程在收到信号时可能已经开始处理其他任务，
        因此 **绝不能通过编程方式调用此选项** 。

    如果启用了 `terminate`，Worker 将终止处理该任务的子进程。
    默认发送的信号为 `TERM`，你可以通过 `signal` 参数自定义信号类型。
    信号名称应为 Python 标准库 :mod:`signal` 模块中定义的信号的大写名称。

    撤销任务的同时也会对其进行标记撤销（revoked）。

    **示例**

    .. code-block:: pycon

        >>> result.revoke()

        >>> AsyncResult(id).revoke()

        >>> app.control.revoke('d9078da5-9915-40a0-bfa1-392c7bde42ed')

        >>> app.control.revoke('d9078da5-9915-40a0-bfa1-392c7bde42ed',
        ...                    terminate=True)

        >>> app.control.revoke('d9078da5-9915-40a0-bfa1-392c7bde42ed',
        ...                    terminate=True, signal='SIGKILL')

.. tab:: 英文

    :pool support: all, terminate only supported by prefork, eventlet and gevent
    :broker support: *amqp, redis*
    :command: :program:`celery -A proj control revoke <task_id>`

    All worker nodes keeps a memory of revoked task ids, either in-memory or
    persistent on disk (see :ref:`worker-persistent-revokes`).

    .. note::

        The maximum number of revoked tasks to keep in memory can be
        specified using the ``CELERY_WORKER_REVOKES_MAX`` environment
        variable, which defaults to 50000. When the limit has been exceeded,
        the revokes will be active for 10800 seconds (3 hours) before being
        expired. This value can be changed using the
        ``CELERY_WORKER_REVOKE_EXPIRES`` environment variable.

        Memory limits can also be set for successful tasks through the
        ``CELERY_WORKER_SUCCESSFUL_MAX`` and
        ``CELERY_WORKER_SUCCESSFUL_EXPIRES`` environment variables, and
        default to 1000 and 10800 respectively.

    When a worker receives a revoke request it will skip executing
    the task, but it won't terminate an already executing task unless
    the `terminate` option is set.

    .. note::

        The terminate option is a last resort for administrators when
        a task is stuck. It's not for terminating the task,
        it's for terminating the process that's executing the task, and that
        process may have already started processing another task at the point
        when the signal is sent, so for this reason you must never call this
        programmatically.

    If `terminate` is set the worker child process processing the task
    will be terminated. The default signal sent is `TERM`, but you can
    specify this using the `signal` argument. Signal can be the uppercase name
    of any signal defined in the :mod:`signal` module in the Python Standard
    Library.

    Terminating a task also revokes it.

    **Example**

    .. code-block:: pycon

        >>> result.revoke()

        >>> AsyncResult(id).revoke()

        >>> app.control.revoke('d9078da5-9915-40a0-bfa1-392c7bde42ed')

        >>> app.control.revoke('d9078da5-9915-40a0-bfa1-392c7bde42ed',
        ...                    terminate=True)

        >>> app.control.revoke('d9078da5-9915-40a0-bfa1-392c7bde42ed',
        ...                    terminate=True, signal='SIGKILL')


撤销多个任务
-----------------------

Revoking multiple tasks

.. tab:: 中文

    .. versionadded:: 3.1

    `revoke` 方法也支持传入一个任务 ID 列表参数，从而一次性撤销多个任务。

    **示例**

    .. code-block:: pycon

        >>> app.control.revoke([
        ...    '7993b0aa-1f0b-4780-9af0-c47c0858b3f2',
        ...    'f565793e-b041-4b2b-9ca4-dca22762a55d',
        ...    'd9d35e03-2997-42d0-a13e-64a66b88a618',
        ])

    自 3.1 版本起， ``GroupResult.revoke`` 方法也利用了此机制。

.. tab:: 英文

    .. versionadded:: 3.1


    The revoke method also accepts a list argument, where it will revoke
    several tasks at once.

    **Example**

    .. code-block:: pycon

        >>> app.control.revoke([
        ...    '7993b0aa-1f0b-4780-9af0-c47c0858b3f2',
        ...    'f565793e-b041-4b2b-9ca4-dca22762a55d',
        ...    'd9d35e03-2997-42d0-a13e-64a66b88a618',
        ])


    The ``GroupResult.revoke`` method takes advantage of this since
    version 3.1.

.. _worker-persistent-revokes:

持久性撤销
------------------

Persistent revokes

.. tab:: 中文

    任务撤销通过向所有 Worker 广播一条消息来实现，
    Worker 接收到消息后会将被撤销的任务添加到内存中的撤销列表中。
    当新的 Worker 启动时，它会与集群中其他 Worker 同步撤销任务列表。

    撤销任务列表保存在内存中，因此如果所有 Worker 都重启，该列表也会丢失。
    如果你希望在 Worker 重启后仍然保留撤销记录，可以通过 :program:`celery worker`
    命令的 `--statedb` 参数将其保存到文件中：

    .. code-block:: console

        $ celery -A proj worker -l INFO --statedb=/var/run/celery/worker.state

    如果你使用 :program:`celery multi`，则应为每个 Worker 实例创建独立的文件，
    可以使用 `%n` 占位符来引用当前节点的名称：

    .. code-block:: console

        celery multi start 2 -l INFO --statedb=/var/run/celery/%n.state

    参见 :ref:`worker-files`

    注意，任务撤销功能依赖于远程控制命令的正常工作。
    目前远程控制命令仅支持 RabbitMQ（amqp）和 Redis。


.. tab:: 英文

    Revoking tasks works by sending a broadcast message to all the workers,
    the workers then keep a list of revoked tasks in memory. When a worker starts
    up it will synchronize revoked tasks with other workers in the cluster.

    The list of revoked tasks is in-memory so if all workers restart the list
    of revoked ids will also vanish. If you want to preserve this list between
    restarts you need to specify a file for these to be stored in by using the `--statedb`
    argument to :program:`celery worker`:

    .. code-block:: console

        $ celery -A proj worker -l INFO --statedb=/var/run/celery/worker.state

    or if you use :program:`celery multi` you want to create one file per
    worker instance so use the `%n` format to expand the current node
    name:

    .. code-block:: console

        celery multi start 2 -l INFO --statedb=/var/run/celery/%n.state


    See also :ref:`worker-files`

    Note that remote control commands must be working for revokes to work.
    Remote control commands are only supported by the RabbitMQ (amqp) and Redis
    at this point.

.. control:: revoke_by_stamped_headers

``revoke_by_stamped_headers``: 通过标记的标头撤销任务
----------------------------------------------------------------------

``revoke_by_stamped_headers``: Revoking tasks by their stamped headers

.. tab:: 中文

    :pool 支持: 全部， `terminate` 选项仅在 prefork 和 eventlet 中受支持  
    :broker 支持: *amqp, redis*  
    :command: :program:`celery -A proj control revoke_by_stamped_headers <header=value>`

    该命令与 :meth:`~@control.revoke` 类似，但不是指定任务 ID，
    而是通过指定一组键值对形式的 stamped header，
    所有匹配这些键值对的 stamped header 的任务都将被撤销。

    .. warning::

        撤销的 stamped header 映射在 Worker 重启后不会持久保留，
        所以如果你重启了 Worker，这些映射将会丢失，需要重新设置。

    .. warning::

        如果你的 Worker 并发度很高，并启用了 terminate 选项，
        此命令可能性能较差，因为它需要遍历所有运行中的任务来查找具有指定 stamped header 的任务。

    **示例**

    .. code-block:: pycon

        >>> app.control.revoke_by_stamped_headers({'header': 'value'})

        >>> app.control.revoke_by_stamped_headers({'header': 'value'}, terminate=True)

        >>> app.control.revoke_by_stamped_headers({'header': 'value'}, terminate=True, signal='SIGKILL')

.. tab:: 英文

    :pool support: all, terminate only supported by prefork and eventlet
    :broker support: *amqp, redis*
    :command: :program:`celery -A proj control revoke_by_stamped_headers <header=value>`

    This command is similar to :meth:`~@control.revoke`, but instead of
    specifying the task id(s), you specify the stamped header(s) as key-value pair(s),
    and each task that has a stamped header matching the key-value pair(s) will be revoked.

    .. warning::

        The revoked headers mapping is not persistent across restarts, so if you
        restart the workers, the revoked headers will be lost and need to be
        mapped again.

    .. warning::

        This command may perform poorly if your worker pool concurrency is high
        and terminate is enabled, since it will have to iterate over all the running
        tasks to find the ones with the specified stamped header.

    **Example**

    .. code-block:: pycon

        >>> app.control.revoke_by_stamped_headers({'header': 'value'})

        >>> app.control.revoke_by_stamped_headers({'header': 'value'}, terminate=True)

        >>> app.control.revoke_by_stamped_headers({'header': 'value'}, terminate=True, signal='SIGKILL')


通过标记的标头撤销多个任务
------------------------------------------

Revoking multiple tasks by stamped headers

.. tab:: 中文

    .. versionadded:: 5.3

    ``revoke_by_stamped_headers`` 方法也支持传入一个列表参数，
    可同时根据多个 header 或多个值进行任务撤销。

    **示例**

    .. code-block:: pycon

        >>> app.control.revoke_by_stamped_headers({
        ...    'header_A': 'value_1',
        ...    'header_B': ['value_2', 'value_3'],
        })

    上述示例将撤销所有带有 stamped header ``header_A`` 且值为 ``value_1`` 的任务，
    以及所有带有 stamped header ``header_B`` 且值为 ``value_2`` 或 ``value_3`` 的任务。

    **命令行示例**

    .. code-block:: console

        $ celery -A proj control revoke_by_stamped_headers stamped_header_key_A=stamped_header_value_1 stamped_header_key_B=stamped_header_value_2

        $ celery -A proj control revoke_by_stamped_headers stamped_header_key_A=stamped_header_value_1 stamped_header_key_B=stamped_header_value_2 --terminate

        $ celery -A proj control revoke_by_stamped_headers stamped_header_key_A=stamped_header_value_1 stamped_header_key_B=stamped_header_value_2 --terminate --signal=SIGKILL

.. tab:: 英文

    .. versionadded:: 5.3

    The ``revoke_by_stamped_headers`` method also accepts a list argument, where it will revoke
    by several headers or several values.

    **Example**

    .. code-block:: pycon

        >> app.control.revoke_by_stamped_headers({
        ...    'header_A': 'value_1',
        ...    'header_B': ['value_2', 'value_3'],
        })

    This will revoke all of the tasks that have a stamped header ``header_A`` with value ``value_1``,
    and all of the tasks that have a stamped header ``header_B`` with values ``value_2`` or ``value_3``.

    **CLI Example**

    .. code-block:: console

        $ celery -A proj control revoke_by_stamped_headers stamped_header_key_A=stamped_header_value_1 stamped_header_key_B=stamped_header_value_2

        $ celery -A proj control revoke_by_stamped_headers stamped_header_key_A=stamped_header_value_1 stamped_header_key_B=stamped_header_value_2 --terminate

        $ celery -A proj control revoke_by_stamped_headers stamped_header_key_A=stamped_header_value_1 stamped_header_key_B=stamped_header_value_2 --terminate --signal=SIGKILL

.. _worker-time-limits:

时间限制
===========

Time Limits

.. tab:: 中文

    .. versionadded:: 2.0

    :pool 支持: *prefork/gevent（见下文说明）*

    .. admonition:: Soft，还是 hard？

        时间限制由两个值控制：`soft` 和 `hard`。
        soft 时间限制允许任务捕获异常进行清理；
        而 hard 限制无法被捕获，直接强制终止任务。

    单个任务有可能会无限期运行，如果有许多任务都在等待某个永远不会发生的事件，
    那么就会导致 Worker 被阻塞，无法处理新的任务。
    防止此类情况的最佳做法是启用任务的时间限制。

    时间限制（`--time-limit`）用于设置任务允许的最长期限（单位：秒），
    超过该时间后执行任务的进程将被终止并由新进程取代。
    你也可以启用 soft 时间限制（`--soft-time-limit`），
    它会抛出一个异常，任务可以在此异常中进行清理，然后再被硬性终止：

    .. code-block:: python

        from myapp import app
        from celery.exceptions import SoftTimeLimitExceeded

        @app.task
        def mytask():
            try:
                do_work()
            except SoftTimeLimitExceeded:
                clean_up_in_a_hurry()

    你也可以使用 :setting:`task_time_limit` /
    :setting:`task_soft_time_limit` 设置来配置时间限制。
    此外，也可以在客户端使用 ``AsyncResult.get()`` 函数的 ``timeout`` 参数设置超时。

    .. note::

        时间限制目前不适用于不支持 :sig:`SIGUSR1` 信号的平台。

    .. note::

        gevent 池不支持 soft 时间限制；
        另外，如果任务处于阻塞状态，它也不会强制执行 hard 时间限制。


.. tab:: 英文

    .. versionadded:: 2.0

    :pool support: *prefork/gevent (see note below)*

    .. admonition:: Soft, or hard?

        The time limit is set in two values, `soft` and `hard`.
        The soft time limit allows the task to catch an exception
        to clean up before it is killed: the hard timeout isn't catch-able
        and force terminates the task.

    A single task can potentially run forever, if you have lots of tasks
    waiting for some event that'll never happen you'll block the worker
    from processing new tasks indefinitely. The best way to defend against
    this scenario happening is enabling time limits.

    The time limit (`--time-limit`) is the maximum number of seconds a task
    may run before the process executing it is terminated and replaced by a
    new process. You can also enable a soft time limit (`--soft-time-limit`),
    this raises an exception the task can catch to clean up before the hard
    time limit kills it:

    .. code-block:: python

        from myapp import app
        from celery.exceptions import SoftTimeLimitExceeded

        @app.task
        def mytask():
            try:
                do_work()
            except SoftTimeLimitExceeded:
                clean_up_in_a_hurry()

    Time limits can also be set using the :setting:`task_time_limit` /
    :setting:`task_soft_time_limit` settings. You can also specify time
    limits for client side operation using ``timeout`` argument of
    ``AsyncResult.get()`` function.

    .. note::

        Time limits don't currently work on platforms that don't support
        the :sig:`SIGUSR1` signal.

    .. note::

        The gevent pool does not implement soft time limits. Additionally,
        it will not enforce the hard time limit if the task is blocking.


在运行时更改时间限制
--------------------------------

Changing time limits at run-time

.. tab:: 中文

    .. versionadded:: 2.3

    :broker 支持: *amqp, redis*

    有一个远程控制命令允许你动态修改任务的 soft 和 hard 时间限制 —— 名为 ``time_limit``。

    例如，将任务 ``tasks.crawl_the_web`` 的 soft 时间限制设置为 1 分钟，
    hard 时间限制设置为 2 分钟：

    .. code-block:: pycon

        >>> app.control.time_limit('tasks.crawl_the_web',
        ...                        soft=60, hard=120, reply=True)
        [{'worker1.example.com': {'ok': 'time limits set successfully'}}]

.. tab:: 英文

    .. versionadded:: 2.3

    :broker support: *amqp, redis*

    There's a remote control command that enables you to change both soft
    and hard time limits for a task — named ``time_limit``.

    Example changing the time limit for the ``tasks.crawl_the_web`` task
    to have a soft time limit of one minute, and a hard time limit of
    two minutes:

    .. code-block:: pycon

        >>> app.control.time_limit('tasks.crawl_the_web',
                                soft=60, hard=120, reply=True)
        [{'worker1.example.com': {'ok': 'time limits set successfully'}}]

    Only tasks that starts executing after the time limit change will be affected.

.. _worker-rate-limits:

速率限制
===========

Rate Limits

.. control:: rate_limit

在运行时更改速率限制
--------------------------------

Changing rate-limits at run-time

.. tab:: 中文

    只有在该时间限制变更之后开始执行的任务才会受到影响。

    另一个示例是修改任务 `myapp.mytask` 的速率限制，使其最多每分钟执行 200 次：

    .. code-block:: pycon

        >>> app.control.rate_limit('myapp.mytask', '200/m')

    上述示例未指定目标 Worker，因此该更改会影响集群中的所有 Worker 实例。
    如果你只希望更改某些特定的 Worker，可以添加 ``destination`` 参数：

    .. code-block:: pycon

        >>> app.control.rate_limit('myapp.mytask', '200/m',
        ...            destination=['celery@worker1.example.com'])

    .. warning::

        如果 Worker 启用了 :setting:`worker_disable_rate_limits` 设置，
        则此命令将不会生效。

.. tab:: 英文

    Example changing the rate limit for the `myapp.mytask` task to execute
    at most 200 tasks of that type every minute:

    .. code-block:: pycon

        >>> app.control.rate_limit('myapp.mytask', '200/m')

    The above doesn't specify a destination, so the change request will affect
    all worker instances in the cluster. If you only want to affect a specific
    list of workers you can include the ``destination`` argument:

    .. code-block:: pycon

        >>> app.control.rate_limit('myapp.mytask', '200/m',
        ...            destination=['celery@worker1.example.com'])

    .. warning::

        This won't affect workers with the
        :setting:`worker_disable_rate_limits` setting enabled.

.. _worker-max-tasks-per-child:

每个子进程的最大任务数设置
===========================

Max tasks per child setting

.. tab:: 中文

    .. versionadded:: 2.0

    :pool 支持: *prefork*

    通过此选项，你可以配置单个 Worker 进程在被替换前最多可执行的任务数。

    这在某些情况下非常有用，例如你使用了某些闭源的 C 扩展，
    并且它们存在你无法控制的内存泄漏问题。

    该选项可以通过 Worker 命令行参数
    :option:`--max-tasks-per-child <celery worker --max-tasks-per-child>` 设置，
    也可以通过配置项 :setting:`worker_max_tasks_per_child` 设置。


.. tab:: 英文

    .. versionadded:: 2.0

    :pool support: *prefork*

    With this option you can configure the maximum number of tasks
    a worker can execute before it's replaced by a new process.

    This is useful if you have memory leaks you have no control over
    for example from closed source C extensions.

    The option can be set using the workers
    :option:`--max-tasks-per-child <celery worker --max-tasks-per-child>` argument
    or using the :setting:`worker_max_tasks_per_child` setting.

.. _worker-max-memory-per-child:

每个子进程的最大内存设置
============================

Max memory per child setting

.. tab:: 中文

    .. versionadded:: 4.0

    :pool 支持: *prefork*

    通过此选项，你可以设置 Worker 在驻留内存（resident memory）使用达到指定上限后被新进程替换。

    这在你无法控制内存泄漏的情况下非常有用，例如使用了闭源的 C 扩展。

    该选项可以通过 Worker 命令行参数
    :option:`--max-memory-per-child <celery worker --max-memory-per-child>` 设置，
    也可以通过配置项 :setting:`worker_max_memory_per_child` 设置。

.. tab:: 英文

    .. versionadded:: 4.0

    :pool support: *prefork*

    With this option you can configure the maximum amount of resident
    memory a worker can execute before it's replaced by a new process.

    This is useful if you have memory leaks you have no control over
    for example from closed source C extensions.

    The option can be set using the workers
    :option:`--max-memory-per-child <celery worker --max-memory-per-child>` argument
    or using the :setting:`worker_max_memory_per_child` setting.

.. _worker-autoscaling:

自动扩缩
===========

Autoscaling

.. tab:: 中文

    .. versionadded:: 2.2

    :pool 支持: *prefork*, *gevent*

    *autoscaler* （自动伸缩器）组件用于根据负载动态调整 Worker 池的大小：

    - 当有任务要处理时，autoscaler 会增加更多的池进程；
    - 当负载降低时，它会开始减少池进程的数量。

    可以使用 :option:`--autoscale <celery worker --autoscale>` 选项启用 autoscaler，
    该选项需要两个数字：最大和最小池进程数：

    .. code-block:: text

            --autoscale=AUTOSCALE
                通过指定 max_concurrency,min_concurrency 来启用自动伸缩。例如：
                --autoscale=10,3 （始终保持至少 3 个进程，如有需要可扩展至最多 10 个）

    你还可以通过继承 :class:`~celery.worker.autoscale.Autoscaler` 来自定义 autoscaler 行为。
    可以使用的指标包括系统负载平均值、可用内存大小等。
    你可以通过配置项 :setting:`worker_autoscaler` 指定自定义 autoscaler。

.. tab:: 英文

    .. versionadded:: 2.2

    :pool support: *prefork*, *gevent*

    The *autoscaler* component is used to dynamically resize the pool
    based on load:

    - The autoscaler adds more pool processes when there is work to do,
    - and starts removing processes when the workload is low.

    It's enabled by the :option:`--autoscale <celery worker --autoscale>` option,
    which needs two numbers: the maximum and minimum number of pool processes:

    .. code-block:: text

            --autoscale=AUTOSCALE
                Enable autoscaling by providing
                max_concurrency,min_concurrency.  Example:
                --autoscale=10,3 (always keep 3 processes, but grow to
                10 if necessary).

    You can also define your own rules for the autoscaler by subclassing
    :class:`~celery.worker.autoscale.Autoscaler`.
    Some ideas for metrics include load average or the amount of memory available.
    You can specify a custom autoscaler with the :setting:`worker_autoscaler` setting.

.. _worker-queues:

队列
======

Queues

.. tab:: 中文

    一个 Worker 实例可以消费任意数量的队列。
    默认情况下，它会消费 :setting:`task_queues` 设置中定义的所有队列（如果未定义则默认使用名为 ``celery`` 的队列）。

    你可以在启动时使用 :option:`-Q <celery worker -Q>` 选项传入用逗号分隔的队列列表，指定要消费的队列：

    .. code-block:: console

        $ celery -A proj worker -l INFO -Q foo,bar,baz

    如果队列名称在 :setting:`task_queues` 中有定义，将使用该定义的配置；
    如果未定义，Celery 将根据 :setting:`task_create_missing_queues` 设置自动为你创建新队列。

    你也可以在运行时通过远程控制命令 :control:`add_consumer` 和 :control:`cancel_consumer`
    来动态添加或移除消费的队列。

.. tab:: 英文

    A worker instance can consume from any number of queues.
    By default it will consume from all queues defined in the
    :setting:`task_queues` setting (that if not specified falls back to the
    default queue named ``celery``).

    You can specify what queues to consume from at start-up, by giving a comma
    separated list of queues to the :option:`-Q <celery worker -Q>` option:

    .. code-block:: console

        $ celery -A proj worker -l INFO -Q foo,bar,baz

    If the queue name is defined in :setting:`task_queues` it will use that
    configuration, but if it's not defined in the list of queues Celery will
    automatically generate a new queue for you (depending on the
    :setting:`task_create_missing_queues` option).

    You can also tell the worker to start and stop consuming from a queue at
    run-time using the remote control commands :control:`add_consumer` and
    :control:`cancel_consumer`.

.. control:: add_consumer

队列：添加消费者
------------------------

Queues: Adding consumers

.. tab:: 中文

    :control:`add_consumer` 控制命令会通知一个或多个 Worker 开始消费某个队列。该操作是幂等的。

    要让集群中所有 Worker 开始消费名为 ``foo`` 的队列，可以使用 :program:`celery control` 命令：

    .. code-block:: console

        $ celery -A proj control add_consumer foo
        -> worker1.local: OK
            started consuming from u'foo'

    如果只希望某个特定 Worker 执行此操作，可以使用
    :option:`--destination <celery control --destination>` 参数：

    .. code-block:: console

        $ celery -A proj control add_consumer foo -d celery@worker1.local

    同样的操作也可以通过 :meth:`@control.add_consumer` 方法动态完成：

    .. code-block:: pycon

        >>> app.control.add_consumer('foo', reply=True)
        [{u'worker1.local': {u'ok': u"already consuming from u'foo'"}}]

        >>> app.control.add_consumer('foo', reply=True,
        ...                          destination=['worker1@example.com'])
        [{u'worker1.local': {u'ok': u"already consuming from u'foo'"}}]

    以上示例展示的是基于自动队列配置的用法，
    如果你需要更细粒度的控制，也可以自定义 exchange、routing_key 甚至其他选项：

    .. code-block:: pycon

        >>> app.control.add_consumer(
        ...     queue='baz',
        ...     exchange='ex',
        ...     exchange_type='topic',
        ...     routing_key='media.*',
        ...     options={
        ...         'queue_durable': False,
        ...         'exchange_durable': False,
        ...     },
        ...     reply=True,
        ...     destination=['w1@example.com', 'w2@example.com'])


.. tab:: 英文

    The :control:`add_consumer` control command will tell one or more workers
    to start consuming from a queue. This operation is idempotent.

    To tell all workers in the cluster to start consuming from a queue
    named "``foo``" you can use the :program:`celery control` program:

    .. code-block:: console

        $ celery -A proj control add_consumer foo
        -> worker1.local: OK
            started consuming from u'foo'

    If you want to specify a specific worker you can use the
    :option:`--destination <celery control --destination>` argument:

    .. code-block:: console

        $ celery -A proj control add_consumer foo -d celery@worker1.local

    The same can be accomplished dynamically using the :meth:`@control.add_consumer` method:

    .. code-block:: pycon

        >>> app.control.add_consumer('foo', reply=True)
        [{u'worker1.local': {u'ok': u"already consuming from u'foo'"}}]

        >>> app.control.add_consumer('foo', reply=True,
        ...                          destination=['worker1@example.com'])
        [{u'worker1.local': {u'ok': u"already consuming from u'foo'"}}]


    By now we've only shown examples using automatic queues,
    If you need more control you can also specify the exchange, routing_key and
    even other options:

    .. code-block:: pycon

        >>> app.control.add_consumer(
        ...     queue='baz',
        ...     exchange='ex',
        ...     exchange_type='topic',
        ...     routing_key='media.*',
        ...     options={
        ...         'queue_durable': False,
        ...         'exchange_durable': False,
        ...     },
        ...     reply=True,
        ...     destination=['w1@example.com', 'w2@example.com'])


.. control:: cancel_consumer

队列：取消消费者
---------------------------

Queues: Canceling consumers

.. tab:: 中文

    你可以使用 :control:`cancel_consumer` 控制命令，通过队列名称取消一个消费者（consumer）。

    如果你想强制集群中所有 Worker 停止消费某个队列，可以使用 :program:`celery control` 命令：

    .. code-block:: console

        $ celery -A proj control cancel_consumer foo

    你还可以使用 :option:`--destination <celery control --destination>` 参数，
    指定一个或多个 Worker 来执行该命令：

    .. code-block:: console

        $ celery -A proj control cancel_consumer foo -d celery@worker1.local

    你也可以通过编程方式调用 :meth:`@control.cancel_consumer` 方法取消队列消费：

    .. code-block:: console

        >>> app.control.cancel_consumer('foo', reply=True)
        [{u'worker1.local': {u'ok': u"no longer consuming from u'foo'"}}]

.. tab:: 英文

    You can cancel a consumer by queue name using the :control:`cancel_consumer`
    control command.

    To force all workers in the cluster to cancel consuming from a queue
    you can use the :program:`celery control` program:

    .. code-block:: console

        $ celery -A proj control cancel_consumer foo

    The :option:`--destination <celery control --destination>` argument can be
    used to specify a worker, or a list of workers, to act on the command:

    .. code-block:: console

        $ celery -A proj control cancel_consumer foo -d celery@worker1.local


    You can also cancel consumers programmatically using the
    :meth:`@control.cancel_consumer` method:

    .. code-block:: console

        >>> app.control.cancel_consumer('foo', reply=True)
        [{u'worker1.local': {u'ok': u"no longer consuming from u'foo'"}}]

.. control:: active_queues

队列：活动队列列表
-----------------------------

Queues: List of active queues

.. tab:: 中文

    你可以使用 :control:`active_queues` 控制命令获取某个 Worker 当前正在消费的队列列表：

    .. code-block:: console

        $ celery -A proj inspect active_queues
        [...]

    与其他远程控制命令一样，你也可以使用
    :option:`--destination <celery inspect --destination>` 参数来指定哪些 Worker 应当响应该请求：

    .. code-block:: console

        $ celery -A proj inspect active_queues -d celery@worker1.local
        [...]

    你还可以通过编程方式调用
    :meth:`~celery.app.control.Inspect.active_queues` 方法实现相同的功能：

    .. code-block:: pycon

        >>> app.control.inspect().active_queues()
        [...]

        >>> app.control.inspect(['worker1.local']).active_queues()
        [...]

.. tab:: 英文

    You can get a list of queues that a worker consumes from by using
    the :control:`active_queues` control command:

    .. code-block:: console

        $ celery -A proj inspect active_queues
        [...]

    Like all other remote control commands this also supports the
    :option:`--destination <celery inspect --destination>` argument used
    to specify the workers that should reply to the request:

    .. code-block:: console

        $ celery -A proj inspect active_queues -d celery@worker1.local
        [...]


    This can also be done programmatically by using the
    :meth:`~celery.app.control.Inspect.active_queues` method:

    .. code-block:: pycon

        >>> app.control.inspect().active_queues()
        [...]

        >>> app.control.inspect(['worker1.local']).active_queues()
        [...]

.. _worker-inspect:

审查 worker 
==================

Inspecting workers

.. tab:: 中文

    :class:`@control.inspect` 类可用于检查正在运行的 Worker 状态。
    它的底层使用的是远程控制命令。

    你也可以使用 ``celery`` 命令来检查 Worker 状态，
    其支持的命令与 :class:`@control` 接口相同。

    .. code-block:: pycon

        >>> # 检查所有节点。
        >>> i = app.control.inspect()

        >>> # 指定多个节点进行检查。
        >>> i = app.control.inspect(['worker1.example.com',
                                    'worker2.example.com'])

        >>> # 指定单个节点进行检查。
        >>> i = app.control.inspect('worker1.example.com')

.. tab:: 英文

    :class:`@control.inspect` lets you inspect running workers. It
    uses remote control commands under the hood.

    You can also use the ``celery`` command to inspect workers,
    and it supports the same commands as the :class:`@control` interface.

    .. code-block:: pycon

        >>> # Inspect all nodes.
        >>> i = app.control.inspect()

        >>> # Specify multiple nodes to inspect.
        >>> i = app.control.inspect(['worker1.example.com',
                                    'worker2.example.com'])

        >>> # Specify a single node to inspect.
        >>> i = app.control.inspect('worker1.example.com')

.. _worker-inspect-registered-tasks:

已注册队列的转储
------------------------

Dump of registered tasks

.. tab:: 中文

    你可以使用 :meth:`~celery.app.control.Inspect.registered` 方法获取 Worker 中已注册任务的列表：

    .. code-block:: pycon

        >>> i.registered()
        [{'worker1.example.com': ['tasks.add',
                                'tasks.sleeptask']}]

.. tab:: 英文

    You can get a list of tasks registered in the worker using the
    :meth:`~celery.app.control.Inspect.registered`:

    .. code-block:: pycon

        >>> i.registered()
        [{'worker1.example.com': ['tasks.add',
                                'tasks.sleeptask']}]

.. _worker-inspect-active-tasks:

当前正在执行的任务的转储
---------------------------------

Dump of currently executing tasks

.. tab:: 中文

    你可以使用 :meth:`~celery.app.control.Inspect.active` 方法获取当前正在执行的任务列表：

    .. code-block:: pycon

        >>> i.active()
        [{'worker1.example.com':
            [{'name': 'tasks.sleeptask',
            'id': '32666e9b-809c-41fa-8e93-5ae0c80afbbf',
            'args': '(8,)',
            'kwargs': '{}'}]}]

.. tab:: 英文

    You can get a list of active tasks using
    :meth:`~celery.app.control.Inspect.active`:

    .. code-block:: pycon

        >>> i.active()
        [{'worker1.example.com':
            [{'name': 'tasks.sleeptask',
            'id': '32666e9b-809c-41fa-8e93-5ae0c80afbbf',
            'args': '(8,)',
            'kwargs': '{}'}]}]

.. _worker-inspect-eta-schedule:

转储计划 (ETA) 任务
-----------------------------

Dump of scheduled (ETA) tasks

.. tab:: 中文

    你可以使用 :meth:`~celery.app.control.Inspect.scheduled` 方法获取等待调度的任务列表：

    .. code-block:: pycon

        >>> i.scheduled()
        [{'worker1.example.com':
            [{'eta': '2010-06-07 09:07:52', 'priority': 0,
            'request': {
                'name': 'tasks.sleeptask',
                'id': '1a7980ea-8b19-413e-91d2-0b74f3844c4d',
                'args': '[1]',
                'kwargs': '{}'}},
            {'eta': '2010-06-07 09:07:53', 'priority': 0,
            'request': {
                'name': 'tasks.sleeptask',
                'id': '49661b9a-aa22-4120-94b7-9ee8031d219d',
                'args': '[2]',
                'kwargs': '{}'}}]}]

    .. note::

        这些任务是带有 ETA/countdown 参数的任务，而不是周期性任务。

.. tab:: 英文

    You can get a list of tasks waiting to be scheduled by using
    :meth:`~celery.app.control.Inspect.scheduled`:

    .. code-block:: pycon

        >>> i.scheduled()
        [{'worker1.example.com':
            [{'eta': '2010-06-07 09:07:52', 'priority': 0,
            'request': {
                'name': 'tasks.sleeptask',
                'id': '1a7980ea-8b19-413e-91d2-0b74f3844c4d',
                'args': '[1]',
                'kwargs': '{}'}},
            {'eta': '2010-06-07 09:07:53', 'priority': 0,
            'request': {
                'name': 'tasks.sleeptask',
                'id': '49661b9a-aa22-4120-94b7-9ee8031d219d',
                'args': '[2]',
                'kwargs': '{}'}}]}]

    .. note::

        These are tasks with an ETA/countdown argument, not periodic tasks.

.. _worker-inspect-reserved:

转储预留任务
----------------------

Dump of reserved tasks

.. tab:: 中文

    保留任务（reserved tasks）是指已被接收但尚未执行的任务。

    你可以使用 :meth:`~celery.app.control.Inspect.reserved` 方法获取这些任务的列表：

    .. code-block:: pycon

        >>> i.reserved()
        [{'worker1.example.com':
            [{'name': 'tasks.sleeptask',
            'id': '32666e9b-809c-41fa-8e93-5ae0c80afbbf',
            'args': '(8,)',
            'kwargs': '{}'}]}]

.. tab:: 英文

    Reserved tasks are tasks that have been received, but are still waiting to be
    executed.

    You can get a list of these using
    :meth:`~celery.app.control.Inspect.reserved`:

    .. code-block:: pycon

        >>> i.reserved()
        [{'worker1.example.com':
            [{'name': 'tasks.sleeptask',
            'id': '32666e9b-809c-41fa-8e93-5ae0c80afbbf',
            'args': '(8,)',
            'kwargs': '{}'}]}]


.. _worker-statistics:

统计信息
----------

Statistics

.. tab:: 中文

    远程控制命令 ``inspect stats`` （或方法 :meth:`~celery.app.control.Inspect.stats`）可返回大量关于 Worker 的统计信息（有用的或无用的）：

    .. code-block:: console

        $ celery -A proj inspect stats

    关于该命令的输出详情，请参阅 :meth:`~celery.app.control.Inspect.stats` 的参考文档。

.. tab:: 英文

    The remote control command ``inspect stats`` (or
    :meth:`~celery.app.control.Inspect.stats`) will give you a long list of useful (or not
    so useful) statistics about the worker:

    .. code-block:: console

        $ celery -A proj inspect stats

    For the output details, consult the reference documentation of :meth:`~celery.app.control.Inspect.stats`.

附加命令
===================

Additional Commands

.. control:: shutdown

远程关闭
---------------

Remote shutdown

.. tab:: 中文

    以下命令可优雅地远程关闭 Worker：

    .. code-block:: pycon

        >>> app.control.broadcast('shutdown') # 关闭所有 Worker
        >>> app.control.broadcast('shutdown', destination='worker1@example.com')

.. tab:: 英文

    This command will gracefully shut down the worker remotely:

    .. code-block:: pycon

        >>> app.control.broadcast('shutdown') # shutdown all workers
        >>> app.control.broadcast('shutdown', destination='worker1@example.com')

.. control:: ping

Ping
----

.. tab:: 中文

    以下命令用于请求所有存活的 Worker 返回 ping 响应。
    Worker 会回复字符串 'pong'，仅此而已。
    该方法默认超时时间为 1 秒，你也可以自定义超时：

    .. code-block:: pycon

        >>> app.control.ping(timeout=0.5)
        [{'worker1.example.com': 'pong'},
        {'worker2.example.com': 'pong'},
        {'worker3.example.com': 'pong'}]

    :meth:`~@control.ping` 也支持 `destination` 参数，
    因此你可以指定要发送 ping 的 Worker：

    .. code-block:: pycon

        >>> ping(['worker2.example.com', 'worker3.example.com'])
        [{'worker2.example.com': 'pong'},
        {'worker3.example.com': 'pong'}]


.. tab:: 英文

    This command requests a ping from alive workers.
    The workers reply with the string 'pong', and that's just about it.
    It will use the default one second timeout for replies unless you specify
    a custom timeout:

    .. code-block:: pycon

        >>> app.control.ping(timeout=0.5)
        [{'worker1.example.com': 'pong'},
        {'worker2.example.com': 'pong'},
        {'worker3.example.com': 'pong'}]

    :meth:`~@control.ping` also supports the `destination` argument,
    so you can specify the workers to ping:

    .. code-block:: pycon

        >>> ping(['worker2.example.com', 'worker3.example.com'])
        [{'worker2.example.com': 'pong'},
        {'worker3.example.com': 'pong'}]

.. _worker-enable-events:

.. control:: enable_events
.. control:: disable_events

启用/禁用事件
---------------------

Enable/disable events

.. tab:: 中文

    你可以使用 `enable_events` 和 `disable_events` 命令来启用/禁用事件。这对于使用 :program:`celery events`/:program:`celerymon` 临时监控 Worker 非常有用。

    .. code-block:: pycon

        >>> app.control.enable_events()
        >>> app.control.disable_events()

.. tab:: 英文

    You can enable/disable events by using the `enable_events`,
    `disable_events` commands. This is useful to temporarily monitor
    a worker using :program:`celery events`/:program:`celerymon`.

    .. code-block:: pycon

        >>> app.control.enable_events()
        >>> app.control.disable_events()

.. _worker-custom-control-commands:

编写您自己的远程控制命令
========================================

Writing your own remote control commands

.. tab:: 中文

    远程控制命令有两种类型：
    
    - Inspect 命令
    
      不会有副作用，通常只是返回 Worker 中找到的一些值，比如当前已注册任务的列表、正在执行的任务列表等。
    
    - Control 命令
    
      会有副作用，比如添加一个新的队列供消费。

    远程控制命令会在控制面板中注册，并且接受一个参数：当前的
    :class:`!celery.worker.control.ControlDispatch` 实例。
    从这里你可以访问活动的
    :class:`~celery.worker.consumer.Consumer`，如果需要的话。

    下面是一个控制命令的例子，用于增加任务的预取计数：

    .. code-block:: python

        from celery.worker.control import control_command

        @control_command(
            args=[('n', int)],
            signature='[N=1]',  # <- 用于命令行帮助。
        )
        def increase_prefetch_count(state, n=1):
            state.consumer.qos.increment_eventually(n)
            return {'ok': 'prefetch count incremented'}

    确保将此代码添加到一个被 Worker 导入的模块中：
    这个模块可以与定义 Celery 应用程序的模块相同，或者你可以
    将该模块添加到 :setting:`imports` 设置中。

    重新启动 Worker，以便注册控制命令，现在你可以使用 :program:`celery control` 工具调用你的命令：

    .. code-block:: console

        $ celery -A proj control increase_prefetch_count 3

    你还可以将动作添加到 :program:`celery inspect` 程序中，
    例如一个读取当前预取计数的命令：

    .. code-block:: python

        from celery.worker.control import inspect_command

        @inspect_command()
        def current_prefetch_count(state):
            return {'prefetch_count': state.consumer.qos.value}


    重新启动 Worker 后，你现在可以使用 :program:`celery inspect` 程序查询此值：

    .. code-block:: console

        $ celery -A proj inspect current_prefetch_count


.. tab:: 英文

    There are two types of remote control commands:
    
    - Inspect command
    
      Does not have side effects, will usually just return some value
      found in the worker, like the list of currently registered tasks,
      the list of active tasks, etc.
    
    - Control command
    
      Performs side effects, like adding a new queue to consume from.
    
    Remote control commands are registered in the control panel and
    they take a single argument: the current
    :class:`!celery.worker.control.ControlDispatch` instance.
    From there you have access to the active
    :class:`~celery.worker.consumer.Consumer` if needed.
    
    Here's an example control command that increments the task prefetch count:
    
    .. code-block:: python
    
        from celery.worker.control import control_command
    
        @control_command(
            args=[('n', int)],
            signature='[N=1]',  # <- used for help on the command-line.
        )
        def increase_prefetch_count(state, n=1):
            state.consumer.qos.increment_eventually(n)
            return {'ok': 'prefetch count incremented'}
    
    Make sure you add this code to a module that is imported by the worker:
    this could be the same module as where your Celery app is defined, or you
    can add the module to the :setting:`imports` setting.
    
    Restart the worker so that the control command is registered, and now you
    can call your command using the :program:`celery control` utility:
    
    .. code-block:: console
    
        $ celery -A proj control increase_prefetch_count 3
    
    You can also add actions to the :program:`celery inspect` program,
    for example one that reads the current prefetch count:
    
    .. code-block:: python
    
        from celery.worker.control import inspect_command
    
        @inspect_command()
        def current_prefetch_count(state):
            return {'prefetch_count': state.consumer.qos.value}
    
    
    After restarting the worker you can now query this value using the
    :program:`celery inspect` program:
    
    .. code-block:: console
    
        $ celery -A proj inspect current_prefetch_count
    