.. _next-steps:

============
下一步
============

Next Steps

.. tab:: 中文

    :ref:`first-steps` 指南故意保持简洁。在本指南中，我将更详细地演示 Celery 的功能，包括如何为你的应用程序和库添加 Celery 支持。

    本文档并未涵盖 Celery 的所有功能和最佳实践，因此建议你同时阅读 :ref:`User Guide <guide>`。

.. tab:: 英文

    The :ref:`first-steps` guide is intentionally minimal. In this guide I'll demonstrate what Celery offers in more detail, including how to add Celery support for your application and library.

    This document doesn't document all of Celery's features and best practices, so it's recommended that you also read the :ref:`User Guide <guide>`



在你的项目中使用Celery
================================

Using Celery in your Application

.. _project-layout:

我们的项目
-----------

Our Project

.. tab:: 中文

    项目布局
    
    .. code-block:: text

        src/
            proj/__init__.py
                /celery.py
                /tasks.py

.. tab:: 英文

    Project layout
    
    .. code-block:: text

        src/
            proj/__init__.py
                /celery.py
                /tasks.py

:file:`proj/celery.py`
~~~~~~~~~~~~~~~~~~~~~~

:file:`proj/celery.py`

.. tab:: 中文

    .. literalinclude:: ../../examples/next-steps/proj/celery.py
       :language: python

    在本模块中，你创建了我们的 :class:`@Celery` 实例（有时称为 *app*）。要在你的项目中使用 Celery，只需导入此实例。

    - ``broker`` 参数指定了要使用的代理的 URL。

      请参阅 :ref:`celerytut-broker` 获取更多信息。

    - ``backend`` 参数指定了要使用的结果后端。

      它用于跟踪任务的状态和结果。虽然默认情况下禁用了结果，但这里我使用了 RPC 结果后端，因为稍后我将演示如何检索结果。你可能希望为你的应用程序使用不同的后端。不同的后端有各自的优缺点。如果你不需要结果，最好禁用它们。也可以通过设置 ``@task(ignore_result=True)`` 选项来禁用个别任务的结果。

      请参阅 :ref:`celerytut-keeping-results` 获取更多信息。

    - ``include`` 参数是一个模块列表，当 worker 启动时会导入这些模块。你需要在这里添加我们的任务模块，以便 worker 能够找到我们的任务。

.. tab:: 英文

    .. literalinclude:: ../../examples/next-steps/proj/celery.py
       :language: python

    In this module you created our :class:`@Celery` instance (sometimes
    referred to as the *app*). To use Celery within your project
    you simply import this instance.

    - The ``broker`` argument specifies the URL of the broker to use.

      See :ref:`celerytut-broker` for more information.

    - The ``backend`` argument specifies the result backend to use.

      It's used to keep track of task state and results.
      While results are disabled by default I use the RPC result backend here
      because I demonstrate how retrieving results work later. You may want to use
      a different backend for your application. They all have different
      strengths and weaknesses. If you don't need results, it's better
      to disable them. Results can also be disabled for individual tasks
      by setting the ``@task(ignore_result=True)`` option.

      See :ref:`celerytut-keeping-results` for more information.

    - The ``include`` argument is a list of modules to import when
    the worker starts. You need to add our tasks module here so
    that the worker is able to find our tasks.

:file:`proj/tasks.py`
~~~~~~~~~~~~~~~~~~~~~

:file:`proj/tasks.py`

.. literalinclude:: ../../examples/next-steps/proj/tasks.py
    :language: python


启动 worker
-------------------

Starting the worker

.. tab:: 中文

    :program:`celery` 程序可以用来启动工作进程（根据示例项目的目录结构，你需要在 `proj` 目录的上一级目录中运行工作进程，该目录是 `src`）：

    .. code-block:: console

        $ celery -A proj worker -l INFO

    当工作进程启动时，你应该会看到一个横幅和一些消息：

        --------------- celery@halcyon.local v4.0 (latentcall)
        --- ***** -----
        -- ******* ---- [Configuration]
        - *** --- * --- . broker:      amqp://guest@localhost:5672//
        - ** ---------- . app:         __main__:0x1012d8590
        - ** ---------- . concurrency: 8 (processes)
        - ** ---------- . events:      OFF (enable -E to monitor this worker)
        - ** ----------
        - *** --- * --- [Queues]
        -- ******* ---- . celery:      exchange:celery(direct) binding:celery
        --- ***** -----

        [2012-06-08 16:23:51,078: WARNING/MainProcess] celery@halcyon.local 已启动。

    -- *broker* 是你在 `celery` 模块中通过 broker 参数指定的 URL。你也可以通过使用 :option:`-b <celery -b>` 选项在命令行上指定不同的 broker。

    -- *Concurrency* 是用于并发处理任务的预先生成的工作进程数量。当所有工作进程都忙于处理任务时，新的任务将需要等待其中一个任务完成后才能处理。

    默认的并发数是该机器上 CPU 的数量（包括核心数）。你可以通过 :option:`celery worker -c` 选项指定自定义的数量。没有推荐的值，因为最优数量取决于多种因素，但如果你的任务大部分是 I/O 密集型的，那么可以尝试增加并发数。实验表明，增加超过 CPU 数量的两倍通常并没有效果，反而可能导致性能下降。

    除了默认的预生成进程池，Celery 还支持使用 Eventlet、Gevent 或单线程运行（参见 :ref:`concurrency`）。

    -- *Events* 是一个选项，允许 Celery 发送监控消息（事件），用于在工作进程中发生的操作。这些可以被监控程序如 ``celery events`` 和 Flower 使用——Flower 是一个实时的 Celery 监控工具，你可以在 :ref:`Monitoring and Management guide <guide-monitoring>` 中了解更多。

    -- *Queues* 是工作进程将消费任务的队列列表。你可以告诉工作进程从多个队列中消费任务，这可以用来将消息路由到特定的工作进程，以实现服务质量、关注点分离和优先级等目的，所有这些都在 :ref:`Routing Guide <guide-routing>` 中进行了描述。

    你可以通过传入 :option:`!--help` 标志来获取完整的命令行参数列表：

    .. code-block:: console

        $ celery worker --help

    这些选项在 :ref:`Workers Guide <guide-workers>` 中有更详细的描述。

.. tab:: 英文

    The :program:`celery` program can be used to start the worker (you need to run the worker in the directory above
    `proj`, according to the example project layout the directory is `src`):

    .. code-block:: console

        $ celery -A proj worker -l INFO

    When the worker starts you should see a banner and some messages::

        --------------- celery@halcyon.local v4.0 (latentcall)
        --- ***** -----
        -- ******* ---- [Configuration]
        - *** --- * --- . broker:      amqp://guest@localhost:5672//
        - ** ---------- . app:         __main__:0x1012d8590
        - ** ---------- . concurrency: 8 (processes)
        - ** ---------- . events:      OFF (enable -E to monitor this worker)
        - ** ----------
        - *** --- * --- [Queues]
        -- ******* ---- . celery:      exchange:celery(direct) binding:celery
        --- ***** -----

        [2012-06-08 16:23:51,078: WARNING/MainProcess] celery@halcyon.local has started.

    -- The *broker* is the URL you specified in the broker argument in our ``celery``
    module. You can also specify a different broker on the command-line by using
    the :option:`-b <celery -b>` option.

    -- *Concurrency* is the number of prefork worker process used
    to process your tasks concurrently. When all of these are busy doing work,
    new tasks will have to wait for one of the tasks to finish before
    it can be processed.

    The default concurrency number is the number of CPU's on that machine
    (including cores). You can specify a custom number using
    the :option:`celery worker -c` option.
    There's no recommended value, as the optimal number depends on a number of
    factors, but if your tasks are mostly I/O-bound then you can try to increase
    it. Experimentation has shown that adding more than twice the number
    of CPU's is rarely effective, and likely to degrade performance
    instead.

    Including the default prefork pool, Celery also supports using
    Eventlet, Gevent, and running in a single thread (see :ref:`concurrency`).

    -- *Events* is an option that causes Celery to send
    monitoring messages (events) for actions occurring in the worker.
    These can be used by monitor programs like ``celery events``,
    and Flower -- the real-time Celery monitor, which you can read about in
    the :ref:`Monitoring and Management guide <guide-monitoring>`.

    -- *Queues* is the list of queues that the worker will consume
    tasks from. The worker can be told to consume from several queues
    at once, and this is used to route messages to specific workers
    as a means for Quality of Service, separation of concerns,
    and prioritization, all described in the :ref:`Routing Guide
    <guide-routing>`.

    You can get a complete list of command-line arguments
    by passing in the :option:`!--help` flag:

    .. code-block:: console

        $ celery worker --help

    These options are described in more detailed in the :ref:`Workers Guide <guide-workers>`.

停止 worker
~~~~~~~~~~~~~~~~~~~

Stopping the worker

.. tab:: 中文

    要停止 Worker，只需按下 :kbd:`Control-c` 即可。Worker 支持的信号列表详见 :ref:`Worker 指南 <guide-workers>`。

.. tab:: 英文

    To stop the worker simply hit :kbd:`Control-c`. A list of signals supported by the worker is detailed in the :ref:`Workers Guide <guide-workers>`.

在后台
~~~~~~~~~~~~~~~~~

In the background

.. tab:: 中文

    在生产环境中，你通常希望将工作进程在后台运行，详见 :ref:`daemonization tutorial <daemonizing>` 教程。

    守护进程脚本使用 :program:`celery multi` 命令来在后台启动一个或多个工作进程：

    .. code-block:: console

        $ celery multi start w1 -A proj -l INFO
        celery multi v4.0.0 (latentcall)
        > Starting nodes...
            > w1.halcyon.local: OK

    你也可以重新启动它：

    .. code-block:: console

        $ celery  multi restart w1 -A proj -l INFO
        celery multi v4.0.0 (latentcall)
        > Stopping nodes...
            > w1.halcyon.local: TERM -> 64024
        > Waiting for 1 node.....
            > w1.halcyon.local: OK
        > Restarting node w1.halcyon.local: OK
        celery multi v4.0.0 (latentcall)
        > Stopping nodes...
            > w1.halcyon.local: TERM -> 64052

    或者停止它：

    .. code-block:: console

        $ celery multi stop w1 -A proj -l INFO

    ``stop`` 命令是异步的，因此不会等待工作进程完全关闭。你可能更希望使用 ``stopwait`` 命令，它会确保所有当前正在执行的任务完成后才退出：

    .. code-block:: console

        $ celery multi stopwait w1 -A proj -l INFO

    .. note::

        :program:`celery multi` 并不会存储有关工作进程的信息，
        所以你在重新启动时需要使用与之前相同的命令行参数。
        只有停止时需要保证使用相同的 pidfile 和 logfile 参数。

    默认情况下，它会在当前目录中创建 pid 文件和日志文件。
    为了防止多个工作进程在彼此之上启动，建议你将这些文件
    放置到一个专用目录中：

    .. code-block:: console

        $ mkdir -p /var/run/celery
        $ mkdir -p /var/log/celery
        $ celery multi start w1 -A proj -l INFO --pidfile=/var/run/celery/%n.pid \
                                                --logfile=/var/log/celery/%n%I.log

    使用 multi 命令你可以启动多个工作进程，此外它还支持强大的命令行语法，用于为不同的工作进程指定不同参数，例如：

    .. code-block:: console

        $ celery multi start 10 -A proj -l INFO -Q:1-3 images,video -Q:4,5 data \
            -Q default -L:4,5 debug

    更多示例请参见 API 参考中的 :mod:`~celery.bin.multi` 模块。

.. tab:: 英文

    In production you'll want to run the worker in the background,
    described in detail in the :ref:`daemonization tutorial <daemonizing>`.

    The daemonization scripts uses the :program:`celery multi` command to
    start one or more workers in the background:

    .. code-block:: console

        $ celery multi start w1 -A proj -l INFO
        celery multi v4.0.0 (latentcall)
        > Starting nodes...
            > w1.halcyon.local: OK

    You can restart it too:

    .. code-block:: console

        $ celery  multi restart w1 -A proj -l INFO
        celery multi v4.0.0 (latentcall)
        > Stopping nodes...
            > w1.halcyon.local: TERM -> 64024
        > Waiting for 1 node.....
            > w1.halcyon.local: OK
        > Restarting node w1.halcyon.local: OK
        celery multi v4.0.0 (latentcall)
        > Stopping nodes...
            > w1.halcyon.local: TERM -> 64052

    or stop it:

    .. code-block:: console

        $ celery multi stop w1 -A proj -l INFO

    The ``stop`` command is asynchronous so it won't wait for the
    worker to shutdown. You'll probably want to use the ``stopwait`` command
    instead, which ensures that all currently executing tasks are completed
    before exiting:

    .. code-block:: console

        $ celery multi stopwait w1 -A proj -l INFO

    .. note::

        :program:`celery multi` doesn't store information about workers
        so you need to use the same command-line arguments when
        restarting. Only the same pidfile and logfile arguments must be
        used when stopping.

    By default it'll create pid and log files in the current directory.
    To protect against multiple workers launching on top of each other
    you're encouraged to put these in a dedicated directory:

    .. code-block:: console

        $ mkdir -p /var/run/celery
        $ mkdir -p /var/log/celery
        $ celery multi start w1 -A proj -l INFO --pidfile=/var/run/celery/%n.pid \
                                                --logfile=/var/log/celery/%n%I.log

    With the multi command you can start multiple workers, and there's a powerful
    command-line syntax to specify arguments for different workers too,
    for example:

    .. code-block:: console

        $ celery multi start 10 -A proj -l INFO -Q:1-3 images,video -Q:4,5 data \
            -Q default -L:4,5 debug

    For more examples see the :mod:`~celery.bin.multi` module in the API
    reference.

.. _app-argument:

关于 :option:`--app <celery --app>` 参数
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

About the :option:`--app <celery --app>` argument

.. tab:: 中文

    :option:`--app <celery --app>` 参数用于指定要使用的 Celery 应用实例，格式为 ``module.path:attribute``。

    但它也支持一种简写形式。如果只指定了包名，它会按以下顺序尝试查找 app 实例：

    使用 :option:`--app=proj <celery --app>` 时：

    1) 查找名为 ``proj.app`` 的属性，或  
    2) 查找名为 ``proj.celery`` 的属性，或  
    3) 查找模块 ``proj`` 中值为 Celery 应用的任意属性，或  

    如果以上都未找到，它会尝试查找名为 ``proj.celery`` 的子模块：

    4) 查找名为 ``proj.celery.app`` 的属性，或  
    5) 查找名为 ``proj.celery.celery`` 的属性，或  
    6) 查找模块 ``proj.celery`` 中值为 Celery 应用的任意属性。

    该查找策略模仿了文档中所推荐的实践：即对于单一模块使用 ``proj:app``，对于较大的项目则使用 ``proj.celery:app``。

.. tab:: 英文

    The :option:`--app <celery --app>` argument specifies the Celery app instance
    to use, in the form of ``module.path:attribute``
    
    But it also supports a shortcut form. If only a package name is specified,
    it'll try to search for the app instance, in the following order:
    
    With :option:`--app=proj <celery --app>`:
    
    1) an attribute named ``proj.app``, or
    2) an attribute named ``proj.celery``, or
    3) any attribute in the module ``proj`` where the value is a Celery
       application, or
    
    If none of these are found it'll try a submodule named ``proj.celery``:
    
    4) an attribute named ``proj.celery.app``, or
    5) an attribute named ``proj.celery.celery``, or
    6) Any attribute in the module ``proj.celery`` where the value is a Celery
       application.
    
    This scheme mimics the practices used in the documentation -- that is, ``proj:app`` for a single contained module, and ``proj.celery:app`` for larger projects.


.. _calling-tasks:

调用任务
=============

Calling Tasks

.. tab:: 中文

    你可以使用 :meth:`delay` 方法调用任务：

    .. code-block:: pycon

        >>> from proj.tasks import add

        >>> add.delay(2, 2)

    该方法实际上是另一个方法 :meth:`apply_async` 的星号参数快捷方式：

    .. code-block:: pycon

        >>> add.apply_async((2, 2))

    后者允许你指定执行选项，例如执行延迟时间（countdown）、发送到的队列等：

    .. code-block:: pycon

        >>> add.apply_async((2, 2), queue='lopri', countdown=10)

    上述示例中，该任务将被发送到名为 ``lopri`` 的队列，并且最早在消息发送后 10 秒被执行。

    直接调用任务将会在当前进程中执行任务，不会发送消息：

    .. code-block:: pycon

        >>> add(2, 2)
        4

    这三个方法 —— :meth:`delay`、:meth:`apply_async` 以及直接调用（``__call__``）构成了 Celery 的调用 API，该 API 同样用于生成任务签名。

    关于调用 API 的更详细说明，请参阅 :ref:`Calling User Guide <guide-calling>`。

    每次任务调用都会被赋予一个唯一标识符（UUID）—— 这就是任务 ID。

    ``delay`` 和 ``apply_async`` 方法会返回一个 :class:`~@AsyncResult` 实例，可用于追踪任务的执行状态。但为此你需要启用 :ref:`结果后端 <task-result-backends>`，以便有地方存储任务状态。

    默认情况下结果功能是禁用的，因为并没有一个适用于所有应用的结果后端；你需要权衡每种后端的缺点来选择是否启用。对于许多任务而言，保存返回值其实并不重要，因此将其默认禁用是合理的选择。此外请注意，结果后端不会用于任务或工作进程的监控：Celery 为此使用专用的事件消息（参见 :ref:`guide-monitoring`）。

    如果你已配置了结果后端，可以检索任务的返回值：

    .. code-block:: pycon

        >>> res = add.delay(2, 2)
        >>> res.get(timeout=1)
        4

    你可以通过 :attr:`id` 属性查看任务的 ID：

    .. code-block:: pycon

        >>> res.id
        d6b3aea2-fb9b-4ebc-8da4-848818db9114

    如果任务抛出异常，你也可以检查异常及其回溯信息，事实上 ``result.get()`` 默认会传播任何错误：

    .. code-block:: pycon

        >>> res = add.delay(2, '2')
        >>> res.get(timeout=1)

    .. code-block:: pytb

        Traceback (most recent call last):
            File "<stdin>", line 1, in <module>
            File "celery/result.py", line 221, in get
                return self.backend.wait_for_pending(
            File "celery/backends/asynchronous.py", line 195, in wait_for_pending
                return result.maybe_throw(callback=callback, propagate=propagate)
            File "celery/result.py", line 333, in maybe_throw
                self.throw(value, self._to_remote_traceback(tb))
            File "celery/result.py", line 326, in throw
                self.on_ready.throw(*args, **kwargs)
            File "vine/promises.py", line 244, in throw
                reraise(type(exc), exc, tb)
            File "vine/five.py", line 195, in reraise
                raise value
        TypeError: unsupported operand type(s) for +: 'int' and 'str'

    如果你不希望错误被传播，可以通过传入 ``propagate`` 参数来关闭它：

    .. code-block:: pycon

        >>> res.get(propagate=False)
        TypeError("unsupported operand type(s) for +: 'int' and 'str'")

    在这种情况下，它将返回所抛出的异常实例 —— 因此若要判断任务是否成功或失败，你需要使用结果实例上的对应方法：

    .. code-block:: pycon

        >>> res.failed()
        True

        >>> res.successful()
        False

    那它是如何判断任务是否失败的呢？这取决于任务的 *状态*：

    .. code-block:: pycon

        >>> res.state
        'FAILURE'

    一个任务在任意时刻只能处于一个状态，但它可能会经历多个状态。一个典型任务的状态流程可能如下所示::

        PENDING -> STARTED -> SUCCESS

    `STARTED` 状态是一种特殊状态，只有在启用了 :setting:`task_track_started` 设置，或任务设置了 ``@task(track_started=True)`` 时才会被记录。

    `PENDING` 状态实际上并不是一个已记录的状态，而是任何未知任务 ID 的默认状态。你可以通过下面的示例看到：

    .. code-block:: pycon

        >>> from proj.celery import app

        >>> res = app.AsyncResult('this-id-does-not-exist')
        >>> res.state
        'PENDING'

    如果任务被重试，状态流程会更复杂一些。例如某个任务重试了两次，其状态流程可能如下：

    .. code-block:: text

        PENDING -> STARTED -> RETRY -> STARTED -> RETRY -> STARTED -> SUCCESS

    关于任务状态的更多内容请参考任务用户指南中的 :ref:`task-states` 一节。

    任务调用的详细说明请参阅 :ref:`Calling Guide <guide-calling>`。

.. tab:: 英文

    You can call a task using the :meth:`delay` method:

    .. code-block:: pycon

        >>> from proj.tasks import add

        >>> add.delay(2, 2)

    This method is actually a star-argument shortcut to another method called
    :meth:`apply_async`:

    .. code-block:: pycon

        >>> add.apply_async((2, 2))

    The latter enables you to specify execution options like the time to run
    (countdown), the queue it should be sent to, and so on:

    .. code-block:: pycon

        >>> add.apply_async((2, 2), queue='lopri', countdown=10)

    In the above example the task will be sent to a queue named ``lopri`` and the
    task will execute, at the earliest, 10 seconds after the message was sent.

    Applying the task directly will execute the task in the current process,
    so that no message is sent:

    .. code-block:: pycon

        >>> add(2, 2)
        4

    These three methods - :meth:`delay`, :meth:`apply_async`, and applying
    (``__call__``), make up the Celery calling API, which is also used for
    signatures.

    A more detailed overview of the Calling API can be found in the
    :ref:`Calling User Guide <guide-calling>`.

    Every task invocation will be given a unique identifier (an UUID) -- this
    is the task id.

    The ``delay`` and ``apply_async`` methods return an :class:`~@AsyncResult`
    instance, which can be used to keep track of the tasks execution state.
    But for this you need to enable a :ref:`result backend <task-result-backends>` so that
    the state can be stored somewhere.

    Results are disabled by default because there is no result
    backend that suits every application; to choose one you need to consider
    the drawbacks of each individual backend. For many tasks
    keeping the return value isn't even very useful, so it's a sensible default to
    have. Also note that result backends aren't used for monitoring tasks and workers:
    for that Celery uses dedicated event messages (see :ref:`guide-monitoring`).

    If you have a result backend configured you can retrieve the return
    value of a task:

    .. code-block:: pycon

        >>> res = add.delay(2, 2)
        >>> res.get(timeout=1)
        4

    You can find the task's id by looking at the :attr:`id` attribute:

    .. code-block:: pycon

        >>> res.id
        d6b3aea2-fb9b-4ebc-8da4-848818db9114

    You can also inspect the exception and traceback if the task raised an
    exception, in fact ``result.get()`` will propagate any errors by default:

    .. code-block:: pycon

        >>> res = add.delay(2, '2')
        >>> res.get(timeout=1)

    .. code-block:: pytb

        Traceback (most recent call last):
            File "<stdin>", line 1, in <module>
            File "celery/result.py", line 221, in get
                return self.backend.wait_for_pending(
            File "celery/backends/asynchronous.py", line 195, in wait_for_pending
                return result.maybe_throw(callback=callback, propagate=propagate)
            File "celery/result.py", line 333, in maybe_throw
                self.throw(value, self._to_remote_traceback(tb))
            File "celery/result.py", line 326, in throw
                self.on_ready.throw(*args, **kwargs)
            File "vine/promises.py", line 244, in throw
                reraise(type(exc), exc, tb)
            File "vine/five.py", line 195, in reraise
                raise value
        TypeError: unsupported operand type(s) for +: 'int' and 'str'

    If you don't wish for the errors to propagate, you can disable that by passing ``propagate``:

    .. code-block:: pycon

        >>> res.get(propagate=False)
        TypeError("unsupported operand type(s) for +: 'int' and 'str'")

    In this case it'll return the exception instance raised instead --
    so to check whether the task succeeded or failed, you'll have to
    use the corresponding methods on the result instance:

    .. code-block:: pycon

        >>> res.failed()
        True

        >>> res.successful()
        False

    So how does it know if the task has failed or not?  It can find out by looking
    at the tasks *state*:

    .. code-block:: pycon

        >>> res.state
        'FAILURE'

    A task can only be in a single state, but it can progress through several
    states. The stages of a typical task can be::

        PENDING -> STARTED -> SUCCESS

    The started state is a special state that's only recorded if the
    :setting:`task_track_started` setting is enabled, or if the
    ``@task(track_started=True)`` option is set for the task.

    The pending state is actually not a recorded state, but rather
    the default state for any task id that's unknown: this you can see
    from this example:

    .. code-block:: pycon

        >>> from proj.celery import app

        >>> res = app.AsyncResult('this-id-does-not-exist')
        >>> res.state
        'PENDING'

    If the task is retried the stages can become even more complex.
    To demonstrate, for a task that's retried two times the stages would be:

    .. code-block:: text

        PENDING -> STARTED -> RETRY -> STARTED -> RETRY -> STARTED -> SUCCESS

    To read more about task states you should see the :ref:`task-states` section
    in the tasks user guide.

    Calling tasks is described in detail in the :ref:`Calling Guide <guide-calling>`.

.. _designing-workflows:

*Canvas*: 设计工作流
==============================

*Canvas*: Designing Work-flows

.. tab:: 中文

    你刚刚学习了如何使用任务的 ``delay`` 方法调用任务，而这通常就已经足够了。但有时你可能希望将某个任务调用的签名传递给另一个进程，或作为参数传递给另一个函数，Celery 为此引入了 *签名（signatures）* 的概念。

    签名会将任务调用的参数与执行选项打包，使其可以被传递给函数，甚至被序列化并通过网络发送。

    你可以为 ``add`` 任务创建一个包含参数 ``(2, 2)`` 且延迟 10 秒执行的签名，如下所示：

    .. code-block:: pycon

        >>> add.signature((2, 2), countdown=10)
        tasks.add(2, 2)

    也可以使用星号参数的快捷形式：

    .. code-block:: pycon

        >>> add.s(2, 2)
        tasks.add(2, 2)

.. tab:: 英文

    You just learned how to call a task using the tasks ``delay`` method,
    and this is often all you need. But sometimes you may want to pass the
    signature of a task invocation to another process or as an argument to another
    function, for which Celery uses something called *signatures*.

    A signature wraps the arguments and execution options of a single task
    invocation in such a way that it can be passed to functions or even serialized
    and sent across the wire.

    You can create a signature for the ``add`` task using the arguments ``(2, 2)``,
    and a countdown of 10 seconds like this:

    .. code-block:: pycon

        >>> add.signature((2, 2), countdown=10)
        tasks.add(2, 2)

    There's also a shortcut using star arguments:

    .. code-block:: pycon

        >>> add.s(2, 2)
        tasks.add(2, 2)

并且再次调用 API …
-----------------------------------

And there's that calling API again…

.. tab:: 中文

    签名实例同样支持调用 API，也就是说它们拥有 ``delay`` 和 ``apply_async`` 方法。

    但它们与任务直接调用的不同之处在于：签名可能已经预先指定了一些参数。比如，``add`` 任务需要两个参数，因此若签名中已指定两个参数，这将构成一个完整签名：

    .. code-block:: pycon

        >>> s1 = add.s(2, 2)
        >>> res = s1.delay()
        >>> res.get()
        4

    当然，你也可以构造不完整的签名，即所谓的 *部分签名（partials）*：

    .. code-block:: pycon

        # 不完整的部分签名：add(?, 2)
        >>> s2 = add.s(2)

    ``s2`` 现在是一个仍需要另一个参数的部分签名，可以在调用该签名时再补充参数：

    .. code-block:: pycon

        # 补全部分签名：add(8, 2)
        >>> res = s2.delay(8)
        >>> res.get()
        10

    上例中你添加了参数 8，它会被追加到已有的参数 2 前，构成完整签名 ``add(8, 2)``。

    关键字参数也可以在后续添加；这些关键字参数会与已有的参数合并，但新添加的参数具有优先权：

    .. code-block:: pycon

        >>> s3 = add.s(2, 2, debug=True)
        >>> s3.delay(debug=False)   # debug 现在是 False。

    如前所述，签名支持调用 API，这意味着你可以使用：

    - ``sig.apply_async(args=(), kwargs={}, **options)``

      调用签名，同时可以附带部分位置参数与关键字参数，也支持传递执行选项。

    - ``sig.delay(*args, **kwargs)``

      是 ``apply_async`` 的星号参数版本。传入的位置参数会被添加到签名原有的位置参数前，关键字参数会合并到签名中已有的关键字参数中（后者优先级低）。

    这一切看起来都很有用，那么你究竟可以用这些做什么呢？  
    为了理解这个问题，我们需要引入 *canvas 原语（canvas primitives）* ……

.. tab:: 英文

    Signature instances also support the calling API, meaning they
    have ``delay`` and ``apply_async`` methods.
    
    But there's a difference in that the signature may already have
    an argument signature specified. The ``add`` task takes two arguments,
    so a signature specifying two arguments would make a complete signature:
    
    .. code-block:: pycon
    
        >>> s1 = add.s(2, 2)
        >>> res = s1.delay()
        >>> res.get()
        4
    
    But, you can also make incomplete signatures to create what we call
    *partials*:
    
    .. code-block:: pycon
    
        # incomplete partial: add(?, 2)
        >>> s2 = add.s(2)
    
    ``s2`` is now a partial signature that needs another argument to be complete,
    and this can be resolved when calling the signature:
    
    .. code-block:: pycon
    
        # resolves the partial: add(8, 2)
        >>> res = s2.delay(8)
        >>> res.get()
        10
    
    Here you added the argument 8 that was prepended to the existing argument 2
    forming a complete signature of ``add(8, 2)``.
    
    Keyword arguments can also be added later; these are then merged with any
    existing keyword arguments, but with new arguments taking precedence:
    
    .. code-block:: pycon
    
        >>> s3 = add.s(2, 2, debug=True)
        >>> s3.delay(debug=False)   # debug is now False.
    
    As stated, signatures support the calling API: meaning that
    
    - ``sig.apply_async(args=(), kwargs={}, **options)``
    
        Calls the signature with optional partial arguments and partial
        keyword arguments. Also supports partial execution options.
    
    - ``sig.delay(*args, **kwargs)``
    
      Star argument version of ``apply_async``. Any arguments will be prepended
      to the arguments in the signature, and keyword arguments is merged with any
      existing keys.
    
    So this all seems very useful, but what can you actually do with these?
    To get to that I must introduce the canvas primitives…

原语
--------------

The Primitives

.. topic:: \

    .. hlist::
        :columns: 2

        - :ref:`group <canvas-group>`
        - :ref:`chain <canvas-chain>`
        - :ref:`chord <canvas-chord>`
        - :ref:`map <canvas-map>`
        - :ref:`starmap <canvas-map>`
        - :ref:`chunks <canvas-chunks>`

.. tab:: 中文

    这些原语（primitive）本身就是签名对象，因此它们可以以任意方式组合，用于构建复杂的工作流。

    .. note::

        以下示例包含结果的获取操作，因此若要尝试它们，你需要配置结果后端（result backend）。  
        上方提供的示例项目已经完成了此配置（参见传递给 :class:`~celery.Celery` 的 ``backend`` 参数）。

    让我们来看几个示例：

.. tab:: 英文

    These primitives are signature objects themselves, so they can be combined
    in any number of ways to compose complex work-flows.

    .. note::

        These examples retrieve results, so to try them out you need
        to configure a result backend. The example project
        above already does that (see the backend argument to :class:`~celery.Celery`).

    Let's look at some examples:

组式任务
~~~~~~~~

Groups

.. tab:: 中文

    一个 :class:`~celery.group` 会并行调用一组任务，并返回一个特殊的结果实例，  
    该实例允许你以组的形式检查结果，并按顺序获取返回值。

    .. code-block:: pycon

        >>> from celery import group
        >>> from proj.tasks import add

        >>> group(add.s(i, i) for i in range(10))().get()
        [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

    - 部分 group 调用（Partial group）

    .. code-block:: pycon

        >>> g = group(add.s(i) for i in range(10))
        >>> g(10).get()
        [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

.. tab:: 英文

    A :class:`~celery.group` calls a list of tasks in parallel,
    and it returns a special result instance that lets you inspect the results
    as a group, and retrieve the return values in order.

    .. code-block:: pycon

        >>> from celery import group
        >>> from proj.tasks import add

        >>> group(add.s(i, i) for i in range(10))().get()
        [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

    - Partial group

    .. code-block:: pycon

        >>> g = group(add.s(i) for i in range(10))
        >>> g(10).get()
        [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

链式任务
~~~~~~~

Chains

.. tab:: 中文

    任务可以链接在一起，使得一个任务返回后，另一个任务被调用:

    .. code-block:: pycon

        >>> from celery import chain
        >>> from proj.tasks import add, mul

        # (4 + 4) * 8
        >>> chain(add.s(4, 4) | mul.s(8))().get()
        64


    或者是部分链式任务:

    .. code-block:: pycon

        >>> # (? + 4) * 8
        >>> g = chain(add.s(4) | mul.s(8))
        >>> g(4).get()
        64


    链式任务也可以像这样书写：

    .. code-block:: pycon

        >>> (add.s(4, 4) | mul.s(8))().get()
        64

.. tab:: 英文

    Tasks can be linked together so that after one task returns the other
    is called:

    .. code-block:: pycon

        >>> from celery import chain
        >>> from proj.tasks import add, mul

        # (4 + 4) * 8
        >>> chain(add.s(4, 4) | mul.s(8))().get()
        64


    or a partial chain:

    .. code-block:: pycon

        >>> # (? + 4) * 8
        >>> g = chain(add.s(4) | mul.s(8))
        >>> g(4).get()
        64


    Chains can also be written like this:

    .. code-block:: pycon

        >>> (add.s(4, 4) | mul.s(8))().get()
        64

合集任务
~~~~~~~~~

Chords

.. tab:: 中文

    合集任务是一个带回调的任务组:

    .. code-block:: pycon

        >>> from celery import chord
        >>> from proj.tasks import add, xsum

        >>> chord((add.s(i, i) for i in range(10)), xsum.s())().get()
        90


    一个任务组链接到另一个任务时，会自动转换为合集任务：

    .. code-block:: pycon

        >>> (group(add.s(i, i) for i in range(10)) | xsum.s())().get()
        90


    由于这些原语都是签名类型，因此几乎可以随意组合，例如：

    .. code-block:: pycon

        >>> upload_document.s(file) | group(apply_filter.s() for filter in filters)

    请务必在 :ref:`Canvas <guide-canvas>` 用户指南中阅读更多关于工作流的信息。 

.. tab:: 英文

    A chord is a group with a callback:

    .. code-block:: pycon

        >>> from celery import chord
        >>> from proj.tasks import add, xsum

        >>> chord((add.s(i, i) for i in range(10)), xsum.s())().get()
        90


    A group chained to another task will be automatically converted
    to a chord:

    .. code-block:: pycon

        >>> (group(add.s(i, i) for i in range(10)) | xsum.s())().get()
        90


    Since these primitives are all of the signature type they
    can be combined almost however you want, for example:

    .. code-block:: pycon

        >>> upload_document.s(file) | group(apply_filter.s() for filter in filters)

    Be sure to read more about work-flows in the :ref:`Canvas <guide-canvas>` user
    guide.

路由
=======

Routing

.. tab:: 中文

    Celery 支持 AMQP 提供的全部路由功能，  
    同时也支持简单的路由机制，即将消息发送到具名队列中。

    通过 :setting:`task_routes` 配置项，你可以按任务名称进行路由，  
    从而将所有路由配置集中管理：

    .. code-block:: python

        app.conf.update(
            task_routes = {
                'proj.tasks.add': {'queue': 'hipri'},
            },
        )

    你也可以在运行时通过 ``apply_async`` 的 ``queue`` 参数来指定队列：

    .. code-block:: pycon

        >>> from proj.tasks import add
        >>> add.apply_async((2, 2), queue='hipri')

    然后你可以通过 :option:`celery worker -Q` 选项让某个 worker 从该队列中消费任务：

    .. code-block:: console

        $ celery -A proj worker -Q hipri

    你可以通过逗号分隔的列表指定多个队列。  
    例如，你可以让 worker 同时消费默认队列和 ``hipri`` 队列，  
    其中默认队列因历史原因被命名为 ``celery``：

    .. code-block:: console

        $ celery -A proj worker -Q hipri,celery

    队列的顺序无关紧要，worker 会给予所有队列相同的权重。

    如需了解更多关于路由的内容，包括如何充分利用 AMQP 的路由能力，  
    请参阅 :ref:`路由指南 <guide-routing>`。

.. tab:: 英文

    Celery supports all of the routing facilities provided by AMQP,
    but it also supports simple routing where messages are sent to named queues.

    The :setting:`task_routes` setting enables you to route tasks by name
    and keep everything centralized in one location:

    .. code-block:: python

        app.conf.update(
            task_routes = {
                'proj.tasks.add': {'queue': 'hipri'},
            },
        )

    You can also specify the queue at runtime
    with the ``queue`` argument to ``apply_async``:

    .. code-block:: pycon

        >>> from proj.tasks import add
        >>> add.apply_async((2, 2), queue='hipri')

    You can then make a worker consume from this queue by
    specifying the :option:`celery worker -Q` option:

    .. code-block:: console

        $ celery -A proj worker -Q hipri

    You may specify multiple queues by using a comma-separated list.
    For example, you can make the worker consume from both the default
    queue and the ``hipri`` queue, where
    the default queue is named ``celery`` for historical reasons:

    .. code-block:: console

        $ celery -A proj worker -Q hipri,celery

    The order of the queues doesn't matter as the worker will
    give equal weight to the queues.

    To learn more about routing, including taking use of the full
    power of AMQP routing, see the :ref:`Routing Guide <guide-routing>`.

远程控制
==============

Remote Control

.. tab:: 中文

    如果你使用的是 RabbitMQ（AMQP）、Redis 或 Qpid 作为 broker，  
    那么你可以在运行时对 worker 进行控制与检查。

    例如，你可以查看某个 worker 当前正在处理的任务：

    .. code-block:: console

        $ celery -A proj inspect active

    这是通过广播消息实现的，因此集群中的所有 worker 都会接收到远程控制指令。

    你也可以通过 :option:`--destination <celery inspect --destination>` 参数指定一个或多个 worker 来执行请求。  
    该参数接受一个以逗号分隔的 worker 主机名列表：

    .. code-block:: console

        $ celery -A proj inspect active --destination=celery@example.com

    如果未指定 destination，则每个 worker 都会响应请求。

    :program:`celery inspect` 命令包含的操作不会改变 worker 的任何状态；  
    它只会返回 worker 内部正在运行的情况和相关统计信息。  
    你可以通过以下方式查看所有可用的 inspect 命令：

    .. code-block:: console

        $ celery -A proj inspect --help

    另一个命令是 :program:`celery control`，该命令包含可在运行时改变 worker 行为的操作：

    .. code-block:: console

        $ celery -A proj control --help

    例如，你可以强制 worker 启用事件消息（event messages），用于监控任务和 worker：

    .. code-block:: console

        $ celery -A proj control enable_events

    启用事件后，你可以启动事件转储器（event dumper），查看 worker 正在执行的操作：

    .. code-block:: console

        $ celery -A proj events --dump

    或者你可以启动基于 curses 的图形界面：

    .. code-block:: console

        $ celery -A proj events

    当你完成监控后，可以通过以下命令再次关闭事件收集：

    .. code-block:: console

        $ celery -A proj control disable_events

    :program:`celery status` 命令同样使用远程控制指令，  
    用于显示当前集群中处于在线状态的 worker 列表：

    .. code-block:: console

        $ celery -A proj status

    你可以在 :ref:`监控指南 <guide-monitoring>` 中阅读更多关于 :program:`celery` 命令和监控的内容。

.. tab:: 英文

    If you're using RabbitMQ (AMQP), Redis, or Qpid as the broker then
    you can control and inspect the worker at runtime.

    For example you can see what tasks the worker is currently working on:

    .. code-block:: console

        $ celery -A proj inspect active

    This is implemented by using broadcast messaging, so all remote
    control commands are received by every worker in the cluster.

    You can also specify one or more workers to act on the request
    using the :option:`--destination <celery inspect --destination>` option.
    This is a comma-separated list of worker host names:

    .. code-block:: console

        $ celery -A proj inspect active --destination=celery@example.com

    If a destination isn't provided then every worker will act and reply
    to the request.

    The :program:`celery inspect` command contains commands that
    don't change anything in the worker; it only returns information
    and statistics about what's going on inside the worker.
    For a list of inspect commands you can execute:

    .. code-block:: console

        $ celery -A proj inspect --help

    Then there's the :program:`celery control` command, which contains
    commands that actually change things in the worker at runtime:

    .. code-block:: console

        $ celery -A proj control --help

    For example you can force workers to enable event messages (used
    for monitoring tasks and workers):

    .. code-block:: console

        $ celery -A proj control enable_events

    When events are enabled you can then start the event dumper
    to see what the workers are doing:

    .. code-block:: console

        $ celery -A proj events --dump

    or you can start the curses interface:

    .. code-block:: console

        $ celery -A proj events

    when you're finished monitoring you can disable events again:

    .. code-block:: console

        $ celery -A proj control disable_events

    The :program:`celery status` command also uses remote control commands
    and shows a list of online workers in the cluster:

    .. code-block:: console

        $ celery -A proj status

    You can read more about the :program:`celery` command and monitoring
    in the :ref:`Monitoring Guide <guide-monitoring>`.

时区
========

Timezone

.. tab:: 中文

    所有时间和日期在内部以及消息中都使用 UTC 时区。

    当 worker 接收到消息（例如带有倒计时参数的任务）时，  
    会将该 UTC 时间转换为本地时间。  
    如果你希望使用不同于系统默认的时区，  
    则需要通过 :setting:`timezone` 配置项进行设置：

    .. code-block:: python

        app.conf.timezone = 'Europe/London'

.. tab:: 英文

    All times and dates, internally and in messages use the UTC timezone.

    When the worker receives a message, for example with a countdown set it
    converts that UTC time to local time. If you wish to use
    a different timezone than the system timezone then you must
    configure that using the :setting:`timezone` setting:

    .. code-block:: python

        app.conf.timezone = 'Europe/London'

优化
============

Optimization

.. tab:: 中文

    默认配置并未针对吞吐量进行优化。默认情况下，  
    Celery 试图在处理大量短任务与少量长任务之间取得平衡，  
    在吞吐量与公平调度之间做出折中。

    如果你对公平调度有严格要求，  
    或希望对系统进行吞吐量优化，  
    请阅读 :ref:`优化指南 <guide-optimizing>`。

.. tab:: 英文

    The default configuration isn't optimized for throughput. By default,
    it tries to walk the middle way between many short tasks and fewer long
    tasks, a compromise between throughput and fair scheduling.

    If you have strict fair scheduling requirements, or want to optimize
    for throughput then you should read the :ref:`Optimizing Guide
    <guide-optimizing>`.

现在可以做什么?
===============

What to do now?

.. tab:: 中文

    阅读完本文档之后，建议继续阅读 :ref:`用户指南 <guide>`。

    如果你对 API 感兴趣，也可以参考 :ref:`API 参考 <apiref>`。

.. tab:: 英文

    Now that you have read this document you should continue
    to the :ref:`User Guide <guide>`.

    There's also an :ref:`API reference <apiref>` if you're so inclined.
