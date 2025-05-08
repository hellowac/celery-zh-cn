.. _guide-optimizing:

============
优化
============

Optimizing

简介
============

Introduction

.. tab:: 中文

    默认配置做了许多妥协。它对于任何单一的用例来说都不是最优的，但对于大多数情况来说已经足够好。

    根据具体的使用场景，可以应用优化。

    优化可以针对运行环境的不同属性进行调整，无论是任务执行所需的时间、使用的内存量，还是在高负载时的响应能力。

.. tab:: 英文

    The default configuration makes a lot of compromises. It's not optimal for
    any single case, but works well enough for most situations.

    There are optimizations that can be applied based on specific use cases.

    Optimizations can apply to different properties of the running environment,
    be it the time tasks take to execute, the amount of memory used, or
    responsiveness at times of high load.

确保操作
===================

Ensuring Operations

.. tab:: 中文

    在《Programming Pearls》一书中，Jon Bentley 提出了通过提出以下问题来进行粗略估算的概念：

        ❝ 密西西比河每天流出的水量是多少？ ❞

    这个练习 [4]_ 的目的是为了表明，系统能够及时处理的数据量是有限的。
    粗略估算可以作为提前规划这一点的手段。

    在 Celery 中；如果一个任务需要 10 分钟才能完成，
    而每分钟有 10 个新任务进入队列，那么队列将永远不会为空。
    因此，监控队列长度非常重要！

    一种方法是通过 :ref:`使用 Munin <monitoring-munin>`。
    你应该设置警报，当任何队列的大小达到不可接受的程度时通知你。
    这样，你就可以采取适当的措施，如添加新的工作节点，或撤销不必要的任务。

.. tab:: 英文

    In the book Programming Pearls, Jon Bentley presents the concept of
    back-of-the-envelope calculations by asking the question;

        ❝ How much water flows out of the Mississippi River in a day? ❞

    The point of this exercise [1]_ is to show that there's a limit
    to how much data a system can process in a timely manner.
    Back of the envelope calculations can be used as a means to plan for this
    ahead of time.

    In Celery; If a task takes 10 minutes to complete,
    and there are 10 new tasks coming in every minute, the queue will never
    be empty. This is why it's very important
    that you monitor queue lengths!

    A way to do this is by :ref:`using Munin <monitoring-munin>`.
    You should set up alerts, that'll notify you as soon as any queue has
    reached an unacceptable size. This way you can take appropriate action
    like adding new worker nodes, or revoking unnecessary tasks.

.. _`The back of the envelope`: http://books.google.com/books?id=kse_7qbWbjsC&pg=PA67

.. _optimizing-general-settings:

常规设置
================

General Settings

.. _optimizing-connection-pools:

代理连接池
-----------------------

Broker Connection Pools

.. tab:: 中文

    从版本 2.5 起，默认启用了代理连接池。

    你可以调整 :setting:`broker_pool_limit` 设置来最小化
    竞争，值应该基于使用代理连接的活动线程/绿色线程的数量。

.. tab:: 英文

    The broker connection pool is enabled by default since version 2.5.

    You can tweak the :setting:`broker_pool_limit` setting to minimize
    contention, and the value should be based on the number of
    active threads/green-threads using broker connections.

.. _optimizing-transient-queues:

使用临时队列
----------------------

Using Transient Queues

.. tab:: 中文

    Celery 创建的队列默认是持久的。这意味着
    代理会将消息写入磁盘，以确保即使代理重启，任务仍然会执行。

    但在某些情况下，丢失消息是可以接受的，因此并非所有任务都需要持久性。你可以为这些任务创建一个 *瞬态* 队列以提高性能：

    .. code-block:: python

        from kombu import Exchange, Queue

        task_queues = (
            Queue('celery', routing_key='celery'),
            Queue('transient', Exchange('transient', delivery_mode=1),
                routing_key='transient', durable=False),
        )


    或者使用 :setting:`task_routes`：

    .. code-block:: python

        task_routes = {
            'proj.tasks.add': {'queue': 'celery', 'delivery_mode': 'transient'}
        }


    ``delivery_mode`` 改变了该队列消息的投递方式。
    值为 1 表示消息不会写入磁盘，值为 2（默认）表示消息可以写入磁盘。

    要将任务定向到新的瞬态队列，你可以指定 queue 参数
    （或者使用 :setting:`task_routes` 设置）：

    .. code-block:: python

        task.apply_async(args, queue='transient')

    有关更多信息，请参见 :ref:`路由指南 <guide-routing>`。


.. tab:: 英文

    Queues created by Celery are persistent by default. This means that
    the broker will write messages to disk to ensure that the tasks will
    be executed even if the broker is restarted.

    But in some cases it's fine that the message is lost, so not all tasks
    require durability. You can create a *transient* queue for these tasks
    to improve performance:

    .. code-block:: python

        from kombu import Exchange, Queue

        task_queues = (
            Queue('celery', routing_key='celery'),
            Queue('transient', Exchange('transient', delivery_mode=1),
                routing_key='transient', durable=False),
        )


    or by using :setting:`task_routes`:

    .. code-block:: python

        task_routes = {
            'proj.tasks.add': {'queue': 'celery', 'delivery_mode': 'transient'}
        }


    The ``delivery_mode`` changes how the messages to this queue are delivered.
    A value of one means that the message won't be written to disk, and a value
    of two (default) means that the message can be written to disk.

    To direct a task to your new transient queue you can specify the queue
    argument (or use the :setting:`task_routes` setting):

    .. code-block:: python

        task.apply_async(args, queue='transient')

    For more information see the :ref:`routing guide <guide-routing>`.

.. _optimizing-worker-settings:

工作器设置
===============

Worker Settings

.. _optimizing-prefetch-limit:

预取限制
---------------

Prefetch Limits

.. tab:: 中文

    *Prefetch* 是一个源自 AMQP 的术语，常常被用户误解。

    预取限制是工人可以为自己保留的任务（消息）数量的**限制**。如果它设置为零，工人将继续消费消息，而不会考虑到可能有其他可用的工人节点能更快地处理这些消息 [5]_，或者消息甚至可能无法完全加载到内存中。

    工人的默认预取计数是 :setting:`worker_prefetch_multiplier` 设置与并发槽数量 [6]_ （进程/线程/绿色线程）相乘的结果。

    如果你有许多持续时间较长的任务，你希望将乘数值设置为 *1*：这意味着每个工人进程一次只会保留一个任务。

    然而——如果你有许多短时任务，并且吞吐量/往返延迟对你来说很重要，那么这个数字应该较大。如果消息已经被预取并且在内存中可用，工人每秒可以处理更多任务。你可能需要实验，以找到适合你的最佳值。在这种情况下，像 50 或 150 这样的值可能有意义。比如 64 或 128。

    如果你有长时任务和短时任务的组合，最好的选择是使用两个分别配置的工人节点，并根据运行时间来路由任务（参见 :ref:`guide-routing`）。

.. tab:: 英文

    *Prefetch* is a term inherited from AMQP that's often misunderstood
    by users.

    The prefetch limit is a **limit** for the number of tasks (messages) a worker
    can reserve for itself. If it is zero, the worker will keep
    consuming messages, not respecting that there may be other
    available worker nodes that may be able to process them sooner [2]_,
    or that the messages may not even fit in memory.

    The workers' default prefetch count is the
    :setting:`worker_prefetch_multiplier` setting multiplied by the number
    of concurrency slots [3]_ (processes/threads/green-threads).

    If you have many tasks with a long duration you want
    the multiplier value to be *one*: meaning it'll only reserve one
    task per worker process at a time.

    However -- If you have many short-running tasks, and throughput/round trip
    latency is important to you, this number should be large. The worker is
    able to process more tasks per second if the messages have already been
    prefetched, and is available in memory. You may have to experiment to find
    the best value that works for you. Values like 50 or 150 might make sense in
    these circumstances. Say 64, or 128.

    If you have a combination of long- and short-running tasks, the best option
    is to use two worker nodes that are configured separately, and route
    the tasks according to the run-time (see :ref:`guide-routing`).

一次保留一个任务
--------------------------

Reserve one task at a time

.. tab:: 中文

    任务消息只有在任务 :term:`acknowledged` （确认）后才会从队列中删除，因此如果工人在确认任务之前崩溃，任务可以重新投递给另一个工人（或者在恢复后重新投递给相同的工人）。

    请注意，异常被视为 Celery 中的正常操作，并将会被确认。
    确认主要用于防范那些无法通过 Python 异常系统正常处理的故障（例如电力故障、内存损坏、硬件故障、致命信号等）。
    对于正常的异常，你应该使用 task.retry() 来重试任务。

    .. seealso::

        请参阅 :ref:`faq-acks_late-vs-retry`。

    在使用默认的早期确认时，预取乘数设置为 *1* 意味着工人每个工人进程最多会保留一个额外的任务：换句话说，如果工人是通过 :option:`-c 10 <celery worker -c>` 启动的，则工人最多可能保留 20 个任务（10 个已确认的正在执行的任务和 10 个未确认的已保留任务）。

    用户经常询问是否可以禁用“预取任务”，这是可能的，但有一个条件。你可以让一个工人仅保留与工人进程数相同的任务，前提是这些任务是延迟确认的（例如对于 :option:`-c 10 <celery worker -c>`，有 10 个未确认的正在执行任务）

    为此，你需要启用 :term:`late acknowledgment` （延迟确认）。与默认行为相比，使用此选项意味着已经开始执行的任务将在发生电力故障或工人实例被突然终止时重试，因此这也意味着任务必须是 :term:`idempotent` （幂等的）。

    你可以通过以下配置选项启用此行为：

    .. code-block:: python

        task_acks_late = True
        worker_prefetch_multiplier = 1

    如果你希望在不使用 ack_late 的情况下禁用“预取任务”（因为你的任务不是幂等的），目前这是不可能的，你可以在此讨论：https://github.com/celery/celery/discussions/7106

.. tab:: 英文

    The task message is only deleted from the queue after the task is
    :term:`acknowledged`, so if the worker crashes before acknowledging the task,
    it can be redelivered to another worker (or the same after recovery).

    Note that an exception is considered normal operation in Celery and it will be acknowledged.
    Acknowledgments are really used to safeguard against failures that can not be normally
    handled by the Python exception system (i.e. power failure, memory corruption, hardware failure, fatal signal, etc.).
    For normal exceptions you should use task.retry() to retry the task.

    .. seealso::

        Notes at :ref:`faq-acks_late-vs-retry`.

    When using the default of early acknowledgment, having a prefetch multiplier setting
    of *one*, means the worker will reserve at most one extra task for every
    worker process: or in other words, if the worker is started with
    :option:`-c 10 <celery worker -c>`, the worker may reserve at most 20
    tasks (10 acknowledged tasks executing, and 10 unacknowledged reserved
    tasks) at any time.

    Often users ask if disabling "prefetching of tasks" is possible, and it is
    possible with a catch. You can have a worker only reserve as many tasks as
    there are worker processes, with the condition that they are acknowledged
    late (10 unacknowledged tasks executing for :option:`-c 10 <celery worker -c>`)

    For that, you need to enable  :term:`late acknowledgment`. Using this option over the
    default behavior means a task that's already started executing will be
    retried in the event of a power failure or the worker instance being killed
    abruptly, so this also means the task must be :term:`idempotent`

    You can enable this behavior by using the following configuration options:

    .. code-block:: python

        task_acks_late = True
        worker_prefetch_multiplier = 1

    If you want to disable "prefetching of tasks" without using ack_late (because
    your tasks are not idempotent) that's impossible right now and you can join the
    discussion here https://github.com/celery/celery/discussions/7106

内存使用情况
------------

Memory Usage

.. tab:: 中文

    如果你在预叉工人中遇到高内存使用情况，首先你需要确定问题是否也发生在 Celery 主进程中。Celery 主进程的内存使用量在启动后不应继续大幅增加。如果你看到这种情况，可能表示存在内存泄漏错误，应该向 Celery 问题追踪器报告。

    如果只有子进程的内存使用量很高，这表明任务存在问题。

    请记住，Python 进程的内存使用量有一个“高水位线”，在子进程停止之前不会将内存归还给操作系统。这意味着一个高内存使用的任务可能会永久增加子进程的内存使用，直到它被重启。解决这个问题可能需要向你的任务中添加分块逻辑，以减少内存峰值使用。

    Celery 工人有两种主要方式可以帮助减少由“高水位线”和/或子进程中的内存泄漏引起的内存使用： :setting:`worker_max_tasks_per_child` 和 :setting:`worker_max_memory_per_child` 设置。

    你必须小心不要将这些设置设置得过低，否则工人将花费大部分时间重新启动子进程，而不是处理任务。例如，如果你使用 :setting:`worker_max_tasks_per_child` 设置为 1，而你的子进程启动时间为 1 秒，那么该子进程每分钟只能处理最多 60 个任务（假设任务立即运行）。当你的任务始终超过 :setting:`worker_max_memory_per_child` 时，也会出现类似的问题。

.. tab:: 英文

    If you are experiencing high memory usage on a prefork worker, first you need
    to determine whether the issue is also happening on the Celery master
    process. The Celery master process's memory usage should not continue to
    increase drastically after start-up. If you see this happening, it may indicate
    a memory leak bug which should be reported to the Celery issue tracker.

    If only your child processes have high memory usage, this indicates an issue
    with your task.

    Keep in mind, Python process memory usage has a "high watermark" and will not
    return memory to the operating system until the child process has stopped. This
    means a single high memory usage task could permanently increase the memory
    usage of a child process until it's restarted. Fixing this may require adding
    chunking logic to your task to reduce peak memory usage.

    Celery workers have two main ways to help reduce memory usage due to the "high
    watermark" and/or memory leaks in child processes: the
    :setting:`worker_max_tasks_per_child` and :setting:`worker_max_memory_per_child`
    settings.

    You must be careful not to set these settings too low, or else your workers
    will spend most of their time restarting child processes instead of processing
    tasks. For example, if you use a :setting:`worker_max_tasks_per_child` of 1
    and your child process takes 1 second to start, then that child process would
    only be able to process a maximum of 60 tasks per minute (assuming the task ran
    instantly). A similar issue can occur when your tasks always exceed
    :setting:`worker_max_memory_per_child`.


.. rubric:: 脚注/Footnotes

.. [1] The chapter is available to read for free here:
       `The back of the envelope`_. The book is a classic text. Highly
       recommended.

.. [2] RabbitMQ and other brokers deliver messages round-robin,
       so this doesn't apply to an active system. If there's no prefetch
       limit and you restart the cluster, there will be timing delays between
       nodes starting. If there are 3 offline nodes and one active node,
       all messages will be delivered to the active node.

.. [3] This is the concurrency setting; :setting:`worker_concurrency` or the
       :option:`celery worker -c` option.

.. [4] 本章可以在此免费阅读：
       `The back of the envelope`_。这本书是经典著作，强烈推荐。

.. [5] RabbitMQ 和其他代理通过轮询方式传递消息，
       所以这不适用于活跃系统。如果没有预取限制，并且你重启了集群，
       节点启动之间将会有时间延迟。如果有 3 个离线节点和一个活跃节点，
       所有消息将会被投递到活跃节点。

.. [6] 这是并发设置； :setting:`worker_concurrency` 或者
       :option:`celery worker -c` 选项。
