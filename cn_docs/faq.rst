.. _faq:

============================
常见问题
============================

Frequently Asked Questions


.. _faq-general:

常见
=======

General

.. _faq-when-to-use:

What kinds of things should I use Celery for?
---------------------------------------------

What kinds of things should I use Celery for?

.. tab:: 中文

    **答：** `Queue everything and delight everyone`_ 是一篇很好的文章，
    描述了为什么在 Web 环境中要使用队列。

    以下是一些常见的使用场景：

    * 在后台运行任务。例如，为了尽快完成 Web 请求，然后逐步更新用户页面。这样即使真正的处理需要一些时间，也会给用户带来性能良好、响应迅速的印象。

    * 在 Web 请求完成后再运行某些任务。

    * 通过异步执行并使用重试机制，确保某件事最终会完成。

    * 定期调度任务。

    在某种程度上还包括：

    * 分布式计算。

    * 并行执行。

.. tab:: 英文

    **Answer:** `Queue everything and delight everyone`_ is a good article
    describing why you'd use a queue in a web context.

    These are some common use cases:

    * Running something in the background. For example, to finish the web request
      as soon as possible, then update the users page incrementally.
      This gives the user the impression of good performance and "snappiness", even
      though the real work might actually take some time.

    * Running something after the web request has finished.

    * Making sure something is done, by executing it asynchronously and using
    retries.

    * Scheduling periodic work.

    And to some degree:

    * Distributed computing.

    * Parallel execution.

.. _`Queue everything and delight everyone`: https://decafbad.com/blog/2008/07/04/queue-everything-and-delight-everyone

.. _faq-misconceptions:

误解
==============

Misconceptions

.. _faq-loc:

Celery 真的由 50,000 行代码组成吗？
---------------------------------------------------

Does Celery really consist of 50.000 lines of code?

.. tab:: 中文

    **答：** 不，这样的大数字在多个地方都有报告。

    截至目前的代码行数如下：

        - 核心代码：7,141 行。
        - 测试代码：14,209 行。
        - 后端、contrib、兼容性工具等：9,032 行。

    代码行数并不是一个有用的度量标准，
    即使 Celery 包含了 5 万行代码，你也无法从这个数字得出任何结论。

.. tab:: 英文

    **Answer:** No, this and similarly large numbers have
    been reported at various locations.

    The numbers as of this writing are:

        - core: 7,141 lines of code.
        - tests: 14,209 lines.
        - backends, contrib, compat utilities: 9,032 lines.

    Lines of code isn't a useful metric, so
    even if Celery did consist of 50k lines of code you wouldn't
    be able to draw any conclusions from such a number.

Celery 依赖项多吗？
-----------------------------------

Does Celery have many dependencies?

.. tab:: 中文

    一个常见的批评是 Celery 使用了过多的依赖项。  
    这种担忧的合理性很难理解，尤其是考虑到代码重用已成为现代软件开发中对抗复杂性的既定方式，
    而且由于 pip 和 PyPI 等软件包管理器的存在，安装和维护依赖项的成本现在已经非常低，几乎可以忽略不计。

    Celery 在发展过程中已经替换了若干依赖项，当前的依赖列表如下：

.. tab:: 英文

    A common criticism is that Celery uses too many dependencies.
    The rationale behind such a fear is hard to imagine, especially considering
    code reuse as the established way to combat complexity in modern software
    development, and that the cost of adding dependencies is very low now
    that package managers like pip and PyPI makes the hassle of installing
    and maintaining dependencies a thing of the past.

    Celery has replaced several dependencies along the way, and
    the current list of dependencies are:

celery
~~~~~~

celery

.. tab:: 中文

    - :pypi:`kombu`

      Kombu 是 Celery 生态系统的一部分，是用于发送和接收消息的库。
      它也是支持多种消息代理的关键所在。
      Kombu 同样被 OpenStack 项目和许多其他项目所使用，验证了将其从 Celery 代码库中独立出来的选择是正确的。

    - :pypi:`billiard`

      Billiard 是 Python `multiprocessing` 模块的一个分支，包含了许多性能和稳定性的改进。
      我们的最终目标是将这些改进回合并到 Python 官方代码中。

      它还用于兼容不自带 `multiprocessing` 模块的旧版本 Python。

.. tab:: 英文

    - :pypi:`kombu`

      Kombu is part of the Celery ecosystem and is the library used
      to send and receive messages. It's also the library that enables
      us to support many different message brokers. It's also used by the
      OpenStack project, and many others, validating the choice to separate
      it from the Celery code-base.

    - :pypi:`billiard`

      Billiard is a fork of the Python multiprocessing module containing
      many performance and stability improvements. It's an eventual goal
      that these improvements will be merged back into Python one day.

      It's also used for compatibility with older Python versions
      that don't come with the multiprocessing module.

kombu
~~~~~

kombu

.. tab:: 中文

    Kombu 依赖以下软件包：

    - :pypi:`amqp`

      底层的纯 Python AMQP 客户端实现。由于 AMQP 是默认的代理协议，因此这是一个自然的依赖项。

    .. note::

        为了便于处理常见配置的依赖项，Celery 定义了多个“捆绑包”（bundle package），
        参见 :ref:`bundles`。


.. tab:: 英文

    Kombu depends on the following packages:

    - :pypi:`amqp`

      The underlying pure-Python amqp client implementation. AMQP being the default
      broker this is a natural dependency.

    .. note::

        To handle the dependencies for popular configuration
        choices Celery defines a number of "bundle" packages,
        see :ref:`bundles`.


.. _faq-heavyweight:

Celery 是重量级的吗？
-----------------------

Is Celery heavy-weight?

.. tab:: 中文

    Celery 在内存占用和性能方面带来的开销都非常小。

    但请注意，默认配置并未针对时间或空间进行优化，
    详情请参见 :ref:`guide-optimizing` 指南。

.. tab:: 英文

    Celery poses very little overhead both in memory footprint and
    performance.

    But please note that the default configuration isn't optimized for time nor
    space, see the :ref:`guide-optimizing` guide for more information.

.. _faq-serialization-is-a-choice:

Celery 依赖于 pickle 吗？
------------------------------

Is Celery dependent on pickle?

.. tab:: 中文

    **回答：** 不，Celery 可以支持任何序列化方案。

    我们内置支持 JSON、YAML、Pickle 和 msgpack。  
    每个任务都关联一个内容类型，因此你甚至可以让一个任务使用 Pickle，另一个使用 JSON。

    默认的序列化格式过去是 Pickle，但从 4.0 版本开始，默认已改为 JSON。  
    如果你需要将复杂的 Python 对象作为任务参数发送，可以使用 Pickle 作为序列化格式，
    但请参考 :ref:`security-serializers` 中的相关安全说明。

    如果你需要与其他语言通信，应使用适合该目的的序列化格式，也就是说，基本上除了 Pickle 以外的任何格式。

    你可以设置一个全局默认序列化器、特定任务的默认序列化器，甚至是在发送某个任务实例时使用的序列化器。

.. tab:: 英文

    **Answer:** No, Celery can support any serialization scheme.

    We have built-in support for JSON, YAML, Pickle, and msgpack.
    Every task is associated with a content type, so you can even send one task using pickle,
    another using JSON.

    The default serialization support used to be pickle, but since 4.0 the default
    is now JSON.  If you require sending complex Python objects as task arguments,
    you can use pickle as the serialization format, but see notes in
    :ref:`security-serializers`.

    If you need to communicate with other languages you should use
    a serialization format suited to that task, which pretty much means any
    serializer that's not pickle.

    You can set a global default serializer, the default serializer for a
    particular Task, or even what serializer to use when sending a single task
    instance.

.. _faq-is-celery-for-django-only:

Celery 只适用于 Django 吗？
--------------------------

Is Celery for Django only?

.. tab:: 中文

    **回答：** 不，Celery 可以配合任何框架使用，无论是 Web 框架还是其他类型框架。

.. tab:: 英文

    **Answer:** No, you can use Celery with any framework, web or otherwise.

.. _faq-is-celery-for-rabbitmq-only:

我必须使用 AMQP/RabbitMQ 吗？
-------------------------------

Do I have to use AMQP/RabbitMQ?

.. tab:: 中文

    **回答：** 不，虽然推荐使用 RabbitMQ，但你也可以使用 Redis、SQS 或 Qpid。

    参见 :ref:`brokers` 了解更多信息。

    使用 Redis 作为 broker 的性能不如 AMQP broker，  
    但将 RabbitMQ 用作消息代理、Redis 用作结果存储的组合是很常见的做法。  
    如果你对可靠性有严格要求，建议使用 RabbitMQ 或其他 AMQP broker。  
    一些传输方案采用轮询机制，因此可能会消耗更多资源。  
    但如果由于某些原因你无法使用 AMQP，完全可以使用这些替代方案。  
    它们在大多数用例中都能良好运行。需要注意的是，以上讨论并非 Celery 特有；
    如果你之前使用 Redis/数据库作为队列没有问题，现在也应该不会有问题。  
    如果将来有需要，你随时可以升级。

.. tab:: 英文

    **Answer**: No, although using RabbitMQ is recommended you can also
    use Redis, SQS, or Qpid.

    See :ref:`brokers` for more information.

    Redis as a broker won't perform as well as
    an AMQP broker, but the combination RabbitMQ as broker and Redis as a result
    store is commonly used. If you have strict reliability requirements you're
    encouraged to use RabbitMQ or another AMQP broker. Some transports also use
    polling, so they're likely to consume more resources. However, if you for
    some reason aren't able to use AMQP, feel free to use these alternatives.
    They will probably work fine for most use cases, and note that the above
    points are not specific to Celery; If using Redis/database as a queue worked
    fine for you before, it probably will now. You can always upgrade later
    if you need to.

.. _faq-is-celery-multilingual:

Celery 支持多种语言吗？
-----------------------

Is Celery multilingual?

.. tab:: 中文

    **回答：** 可以。

    :mod:`~celery.bin.worker` 是用 Python 编写的 Celery Worker 实现。
    如果某个语言有 AMQP 客户端，那么在该语言中创建一个 Worker 所需的工作并不多。
    一个 Celery Worker 本质上就是一个连接到消息代理以处理消息的程序。

    此外，还有一种更独立于语言的方式，那就是使用 REST 任务。
    任务不再是函数，而是 URL。
    有了这个信息，你甚至可以创建简单的 Web 服务器来预加载代码：
    只需暴露一个执行操作的端点，并创建一个任务来对该端点发起 HTTP 请求即可。

    你也可以使用 `Flower <https://flower.readthedocs.io>`_ 提供的 `REST API <https://flower.readthedocs.io/en/latest/api.html#post--api-task-async-apply-(.+)>`_ 来调用任务。

    
.. tab:: 英文

    **Answer:** Yes.

    :mod:`~celery.bin.worker` is an implementation of Celery in Python. If the
    language has an AMQP client, there shouldn't be much work to create a worker
    in your language. A Celery worker is just a program connecting to the broker
    to process messages.

    Also, there's another way to be language-independent, and that's to use REST
    tasks, instead of your tasks being functions, they're URLs. With this
    information you can even create simple web servers that enable preloading of
    code. Simply expose an endpoint that performs an operation, and create a task
    that just performs an HTTP request to that endpoint.

    You can also use `Flower's <https://flower.readthedocs.io>`_ `REST API <https://flower.readthedocs.io/en/latest/api.html#post--api-task-async-apply-(.+)>`_ to invoke tasks.

.. _faq-troubleshooting:

故障排除
===============

Troubleshooting

.. _faq-mysql-deadlocks:

MySQL 抛出死锁错误，我该怎么办？
-------------------------------------------------

MySQL is throwing deadlock errors, what can I do?

.. tab:: 中文

    **回答：** MySQL 的默认隔离级别是 `REPEATABLE-READ`，  
    如果你不需要这么高的隔离性，可以将其设置为 `READ-COMMITTED`。  
    你可以通过在 :file:`my.cnf` 中添加以下内容来实现这一设置::

        [mysqld]
        transaction-isolation = READ-COMMITTED

    关于 InnoDB 的事务模型的更多信息，请参阅 MySQL 用户手册中的 `MySQL - The InnoDB Transaction Model and Locking`_。

    （感谢 Honza Kral 和 Anton Tsigularov 提供该方案）

.. tab:: 英文

    **Answer:** MySQL has default isolation level set to `REPEATABLE-READ`,
    if you don't really need that, set it to `READ-COMMITTED`.
    You can do that by adding the following to your :file:`my.cnf`::

        [mysqld]
        transaction-isolation = READ-COMMITTED

    For more information about InnoDB’s transaction model see `MySQL - The InnoDB
    Transaction Model and Locking`_ in the MySQL user manual.

    (Thanks to Honza Kral and Anton Tsigularov for this solution)

.. _`MySQL - The InnoDB Transaction Model and Locking`: https://dev.mysql.com/doc/refman/5.1/en/innodb-transaction-model.html

.. _faq-worker-hanging:

工作线程什么都没做，只是挂了
---------------------------------------------

The worker isn't doing anything, just hanging

.. tab:: 中文

    **回答：** 请参见 `MySQL is throwing deadlock errors, what can I do?`_，或  
    `Why is Task.delay/apply\*/the worker just hanging?`_。

.. tab:: 英文

    **Answer:** See `MySQL is throwing deadlock errors, what can I do?`_,
    or `Why is Task.delay/apply\*/the worker just hanging?`_.

.. _faq-results-unreliable:

任务结果无法可靠返回
--------------------------------------

Task results aren't reliably returning

.. tab:: 中文

    **回答：** 如果你使用数据库后端来存储结果，特别是使用 MySQL，  
    请参见 `MySQL is throwing deadlock errors, what can I do?`_。

.. tab:: 英文

    **Answer:** If you're using the database backend for results, and in particular
    using MySQL, see `MySQL is throwing deadlock errors, what can I do?`_.

.. _faq-publish-hanging:

为什么 Task.delay/apply\*/ 工作线程挂了？
--------------------------------------------------

Why is Task.delay/apply\*/the worker just hanging?

.. tab:: 中文

    **回答：** 某些 AMQP 客户端存在一个 bug，当它无法验证当前用户身份、密码错误，  
    或用户没有访问指定虚拟主机的权限时，可能会导致挂起。  
    请务必检查你的消息代理日志（RabbitMQ 的日志通常位于大多数系统的 :file:`/var/log/rabbitmq/rabbit.log`），  
    通常会包含描述问题原因的消息。

.. tab:: 英文

    **Answer:** There's a bug in some AMQP clients that'll make it hang if
    it's not able to authenticate the current user, the password doesn't match or
    the user doesn't have access to the virtual host specified. Be sure to check
    your broker logs (for RabbitMQ that's :file:`/var/log/rabbitmq/rabbit.log` on
    most systems), it usually contains a message describing the reason.

.. _faq-worker-on-freebsd:

它在 FreeBSD 上能正常工作吗？
------------------------

Does it work on FreeBSD?

.. tab:: 中文

    **回答：** 视情况而定；

    当使用 RabbitMQ（AMQP）或 Redis 传输时，应该可以开箱即用。

    对于其他传输方式，将使用兼容的 prefork 池，这要求系统提供可用的 POSIX 信号量实现，  
    该功能自 FreeBSD 8.x 起默认启用。对于更早版本的 FreeBSD，你需要在内核中启用 POSIX 信号量并手动重新编译 billiard。

    幸运的是，Viktor Petersson 撰写了一篇教程帮助你在 FreeBSD 上开始使用 Celery：
    http://www.playingwithwire.com/2009/10/how-to-get-celeryd-to-work-on-freebsd/

.. tab:: 英文

    **Answer:** Depends;

    When using the RabbitMQ (AMQP) and Redis transports it should work
    out of the box.

    For other transports the compatibility prefork pool is
    used and requires a working POSIX semaphore implementation,
    this is enabled in FreeBSD by default since FreeBSD 8.x.
    For older version of FreeBSD, you have to enable
    POSIX semaphores in the kernel and manually recompile billiard.

    Luckily, Viktor Petersson has written a tutorial to get you started with
    Celery on FreeBSD here:
    http://www.playingwithwire.com/2009/10/how-to-get-celeryd-to-work-on-freebsd/

.. _faq-duplicate-key-errors:

我遇到了“IntegrityError: Duplicate Key”错误。为什么？
-------------------------------------------------------

I'm having `IntegrityError: Duplicate Key` errors. Why?

.. tab:: 中文

    **回答：** 请参见 `MySQL is throwing deadlock errors, what can I do?`_。  
    感谢 :github_user:`@howsthedotcom` 提供建议。
    
.. tab:: 英文--

    **Answer:** See `MySQL is throwing deadlock errors, what can I do?`_.
    Thanks to :github_user:`@howsthedotcom`.

.. _faq-worker-stops-processing:

为什么我的任务没有被处理？
------------------------------

Why aren't my tasks processed?

.. tab:: 中文

    **回答：** 使用 RabbitMQ 时，你可以通过以下命令查看当前有多少个消费者在接收任务：

    .. code-block:: console

        $ rabbitmqctl list_queues -p <myvhost> name messages consumers
        Listing queues ...
        celery     2891    2

    上面的输出表示任务队列中还有 2891 条待处理的消息，当前有 2 个消费者正在处理。

    队列一直未清空的一个可能原因是某个过期的 worker 进程“劫持”了消息。  
    这可能是因为该 worker 没有正确关闭。

    当消息被某个 worker 接收后，broker 会等待其发送确认（ack）信号，才会标记该消息为已处理。  
    在此之前，broker 不会将该消息重新发送给其他消费者，除非当前消费者已正确关闭。

    如果遇到这种情况，你需要手动终止所有 worker 并重新启动：

    .. code-block:: console

        $ pkill 'celery worker'

        $ # - 如果系统没有 pkill，可以使用：
        $ # ps auxww | awk '/celery worker/ {print $2}' | xargs kill

    你可能需要等待一段时间直到所有 worker 执行完任务。  
    如果长时间仍处于挂起状态，可以使用强制方式终止它们：

    .. code-block:: console

        $ pkill -9 'celery worker'

        $ # - 如果系统没有 pkill，可以使用：
        $ # ps auxww | awk '/celery worker/ {print $2}' | xargs kill -9

.. tab:: 英文

    **Answer:** With RabbitMQ you can see how many consumers are currently
    receiving tasks by running the following command:

    .. code-block:: console

        $ rabbitmqctl list_queues -p <myvhost> name messages consumers
        Listing queues ...
        celery     2891    2

    This shows that there's 2891 messages waiting to be processed in the task
    queue, and there are two consumers processing them.

    One reason that the queue is never emptied could be that you have a stale
    worker process taking the messages hostage. This could happen if the worker
    wasn't properly shut down.

    When a message is received by a worker the broker waits for it to be
    acknowledged before marking the message as processed. The broker won't
    re-send that message to another consumer until the consumer is shut down
    properly.

    If you hit this problem you have to kill all workers manually and restart
    them:

    .. code-block:: console

        $ pkill 'celery worker'

        $ # - If you don't have pkill use:
        $ # ps auxww | awk '/celery worker/ {print $2}' | xargs kill

    You may have to wait a while until all workers have finished executing
    tasks. If it's still hanging after a long time you can kill them by force
    with:

    .. code-block:: console

        $ pkill -9 'celery worker'

        $ # - If you don't have pkill use:
        $ # ps auxww | awk '/celery worker/ {print $2}' | xargs kill -9

.. _faq-task-does-not-run:

为什么我的任务无法运行？
----------------------

Why won't my Task run?

.. tab:: 中文

    **答：** 可能存在语法错误，导致任务模块无法被导入。

    你可以手动执行任务，查看 Celery 是否能够运行该任务：

    .. code-block:: python

        >>> from myapp.tasks import MyPeriodicTask
        >>> MyPeriodicTask.delay()

    查看 worker 的日志文件，以确定是否能够找到任务，或者是否发生了其他错误。

.. tab:: 英文

    **Answer:** There might be syntax errors preventing the tasks module being imported.

    You can find out if Celery is able to run the task by executing the
    task manually:

    .. code-block:: python

        >>> from myapp.tasks import MyPeriodicTask
        >>> MyPeriodicTask.delay()

    Watch the workers log file to see if it's able to find the task, or if some
    other error is happening.

.. _faq-periodic-task-does-not-run:

为什么我的周期性任务无法运行？
-------------------------------

Why won't my periodic task run?

.. tab:: 中文

    **答：** 参见 `为什么我的任务无法运行？ <Why won't my Task run?>`_。

.. tab:: 英文

    **Answer:** See `Why won't my Task run?`_.

.. _faq-purge-the-queue:

如何清除所有等待中的任务？
---------------------------------

How do I purge all waiting tasks?

.. tab:: 中文

    **答：** 你可以使用 ``celery purge`` 命令清空所有配置的任务队列：

    .. code-block:: console

        $ celery -A proj purge

    或通过编程方式清空：

    .. code-block:: pycon

        >>> from proj.celery import app
        >>> app.control.purge()
        1753

    如果你只想清空特定队列中的消息，则需要使用 AMQP API 或 :program:`celery amqp` 工具：

    .. code-block:: console

        $ celery -A proj amqp queue.purge <queue name>

    数字 1753 表示删除的消息数量。

    你也可以在启动 worker 时启用
    :option:`--purge <celery worker --purge>` 选项，在 worker 启动时自动清空消息。

.. tab:: 英文

    **Answer:** You can use the ``celery purge`` command to purge
    all configured task queues:

    .. code-block:: console

        $ celery -A proj purge

    or programmatically:

    .. code-block:: pycon

        >>> from proj.celery import app
        >>> app.control.purge()
        1753

    If you only want to purge messages from a specific queue
    you have to use the AMQP API or the :program:`celery amqp` utility:

    .. code-block:: console

        $ celery -A proj amqp queue.purge <queue name>

    The number 1753 is the number of messages deleted.

    You can also start the worker with the
    :option:`--purge <celery worker --purge>` option enabled to purge messages
    when the worker starts.

.. _faq-messages-left-after-purge:

我已经清除了消息，但队列中仍然有消息？
---------------------------------------------------------------------

I've purged messages, but there are still messages left in the queue?

.. tab:: 中文

    **答：** 任务会在实际执行后才会被确认（即从队列中移除）。worker 接收到任务后到实际执行之间可能有延迟，特别是当等待执行的任务很多时。未确认的消息会一直被 worker 持有，直到与 broker（AMQP 服务器）的连接关闭。当连接关闭（例如 worker 被停止）时，这些任务会由 broker 重新投递给下一个可用的 worker（或重启后的同一个 worker），因此如果要彻底清空等待中的任务队列，必须先停止所有 worker，然后使用 :func:`celery.control.purge` 清空任务。

.. tab:: 英文

    **Answer:** Tasks are acknowledged (removed from the queue) as soon
    as they're actually executed. After the worker has received a task, it will
    take some time until it's actually executed, especially if there are a lot
    of tasks already waiting for execution. Messages that aren't acknowledged are
    held on to by the worker until it closes the connection to the broker (AMQP
    server). When that connection is closed (e.g., because the worker was stopped)
    the tasks will be re-sent by the broker to the next available worker (or the
    same worker when it has been restarted), so to properly purge the queue of
    waiting tasks you have to stop all the workers, and then purge the tasks
    using :func:`celery.control.purge`.

.. _faq-results:

结果
=======

Results

.. _faq-get-result-by-task-id:

如果我有指向任务结果的 ID，该如何获取结果？
---------------------------------------------------------------------

How do I get the result of a task if I have the ID that points there?

.. tab:: 中文

    **答：** 使用 `task.AsyncResult`：

    .. code-block:: pycon

        >>> result = my_task.AsyncResult(task_id)
        >>> result.get()

    这将返回一个 :class:`~celery.result.AsyncResult` 实例，使用当前任务的结果后端。

    如果你需要指定自定义结果后端，或者希望使用当前应用默认的后端，可以使用
    :class:`@AsyncResult`：

    .. code-block:: pycon

        >>> result = app.AsyncResult(task_id)
        >>> result.get()
    
.. tab:: 英文-

    **Answer**: Use `task.AsyncResult`:

    .. code-block:: pycon

        >>> result = my_task.AsyncResult(task_id)
        >>> result.get()

    This will give you a :class:`~celery.result.AsyncResult` instance
    using the tasks current result backend.

    If you need to specify a custom result backend, or you want to use
    the current application's default backend you can use
    :class:`@AsyncResult`:

    .. code-block:: pycon

        >>> result = app.AsyncResult(task_id)
        >>> result.get()

.. _faq-security:

安全性
========

Security

使用 `pickle` 是否存在安全隐患？
----------------------------------------

Isn't using `pickle` a security concern?

.. tab:: 中文

    **答：** 的确，自 Celery 4.0 起，默认的序列化格式为 JSON，这是为了让用户有意识地选择合适的序列化方式并关注安全问题。

    保护 broker、数据库和其他传输 pickled 数据的服务不被未授权访问是至关重要的。

    这不仅仅是 Celery 的问题，例如 Django 的缓存客户端也使用了 pickle。

    对于任务消息，可以通过设置 :setting:`task_serializer` 为 "json" 或 "yaml" 来替代 pickle。

    同样地，任务结果的序列化方式可以通过 :setting:`result_serializer` 来配置。

    关于使用格式的详细说明以及在判断使用何种格式时的查找顺序，请参见 :ref:`calling-serializers`。

.. tab:: 英文

    **Answer**: Indeed, since Celery 4.0 the default serializer is now JSON
    to make sure people are choosing serializers consciously and aware of this concern.

    It's essential that you protect against unauthorized
    access to your broker, databases and other services transmitting pickled
    data.

    Note that this isn't just something you should be aware of with Celery, for
    example also Django uses pickle for its cache client.

    For the task messages you can set the :setting:`task_serializer`
    setting to "json" or "yaml" instead of pickle.

    Similarly for task results you can set :setting:`result_serializer`.

    For more details of the formats used and the lookup order when
    checking what format to use for a task see :ref:`calling-serializers`

消息可以加密吗？
--------------------------

Can messages be encrypted?

.. tab:: 中文

    **答：** 某些 AMQP broker（包括 RabbitMQ）支持 SSL。你可以通过设置 :setting:`broker_use_ssl` 来启用 SSL。

    如果你还需要为消息添加额外的加密或安全机制，请联系 :ref:`mailing-list` 以获取更多信息。

.. tab:: 英文

    **Answer**: Some AMQP brokers supports using SSL (including RabbitMQ).
    You can enable this using the :setting:`broker_use_ssl` setting.

    It's also possible to add additional encryption and security to messages,
    if you have a need for this then you should contact the :ref:`mailing-list`.

以 root 身份运行 `:program:`celery worker` 是否安全？
---------------------------------------------------

Is it safe to run :program:`celery worker` as root?

.. tab:: 中文

    **答：** 不可以！

    虽然我们目前尚未发现安全漏洞，但假设不存在安全问题是非常天真的，因此强烈建议以非特权用户身份运行 Celery 服务（:program:`celery worker`、:program:`celery beat`、:program:`celeryev` 等）。

.. tab:: 英文

    **Answer**: No!

    We're not currently aware of any security issues, but it would
    be incredibly naive to assume that they don't exist, so running
    the Celery services (:program:`celery worker`, :program:`celery beat`,
    :program:`celeryev`, etc) as an unprivileged user is recommended.

.. _faq-brokers:

代理
=======

Brokers

为什么 RabbitMQ 会崩溃？
-------------------------

Why is RabbitMQ crashing?

.. tab:: 中文

    **答：** 如果 RabbitMQ 内存耗尽，会导致崩溃。这个问题将在 RabbitMQ 的未来版本中修复。请参考 RabbitMQ FAQ： https://www.rabbitmq.com/faq.html#node-runs-out-of-memory

    .. note::

        该问题在 RabbitMQ 2.0 及以上版本中已被修复。新版本引入了一个新的持久化机制，能够容忍内存溢出错误。推荐 Celery 用户使用 RabbitMQ 2.1 或更高版本。

        如果你仍在运行旧版本 RabbitMQ，并遇到崩溃问题，请尽快升级！

    在旧版 RabbitMQ 中，如果 Celery 配置不当，可能导致崩溃。即便不会崩溃，也可能占用大量系统资源，因此必须注意一些常见陷阱。

    * 事件（Events）

    使用 :option:`-E <celery worker -E>` 启动 :mod:`~celery.bin.worker` 时，会发送反映 worker 内部事件的消息。

    只有在有事件监控器实时消费这些事件，或者定期清空事件队列的情况下，才应启用事件。

    * AMQP 结果后端

    当使用 AMQP 结果后端时，每个任务的结果都会以消息的形式发送。如果你没有收集这些结果，它们将持续堆积，最终可能导致 RabbitMQ 内存耗尽。

    该结果后端已被弃用，因此不应再使用。建议使用 RPC 后端用于 rpc 样式的调用，或者使用持久化后端以支持多消费者访问结果。

    结果默认在 1 天后过期。你可以通过设置 :setting:`result_expires` 配置该值。

    如果你不需要任务结果，务必设置 `ignore_result` 选项：

    .. code-block:: python

        @app.task(ignore_result=True)
        def mytask():
            pass

        class MyTask(Task):
            ignore_result = True

.. tab:: 英文

    **Answer:** RabbitMQ will crash if it runs out of memory. This will be fixed in a
    future release of RabbitMQ. please refer to the RabbitMQ FAQ:
    https://www.rabbitmq.com/faq.html#node-runs-out-of-memory

    .. note::

        This is no longer the case, RabbitMQ versions 2.0 and above
        includes a new persister, that's tolerant to out of memory
        errors. RabbitMQ 2.1 or higher is recommended for Celery.

        If you're still running an older version of RabbitMQ and experience
        crashes, then please upgrade!

    Misconfiguration of Celery can eventually lead to a crash
    on older version of RabbitMQ. Even if it doesn't crash, this
    can still consume a lot of resources, so it's
    important that you're aware of the common pitfalls.

    * Events.

    Running :mod:`~celery.bin.worker` with the :option:`-E <celery worker -E>`
    option will send messages for events happening inside of the worker.

    Events should only be enabled if you have an active monitor consuming them,
    or if you purge the event queue periodically.

    * AMQP backend results.

    When running with the AMQP result backend, every task result will be sent
    as a message. If you don't collect these results, they will build up and
    RabbitMQ will eventually run out of memory.

    This result backend is now deprecated so you shouldn't be using it.
    Use either the RPC backend for rpc-style calls, or a persistent backend
    if you need multi-consumer access to results.

    Results expire after 1 day by default. It may be a good idea
    to lower this value by configuring the :setting:`result_expires`
    setting.

    If you don't use the results for a task, make sure you set the
    `ignore_result` option:

    .. code-block:: python

        @app.task(ignore_result=True)
        def mytask():
            pass

        class MyTask(Task):
            ignore_result = True

.. _faq-use-celery-with-stomp:

我可以将 Celery 与 ActiveMQ/STOMP 一起使用吗？
-------------------------------------

Can I use Celery with ActiveMQ/STOMP?

.. tab:: 中文

    **答复**：不支持。此前在 :pypi:`Carrot`（我们早期使用的消息库）中曾提供该支持，
    但目前的消息库 :pypi:`Kombu` 并不支持该功能。

.. tab:: 英文

    **Answer**: No. It used to be supported by :pypi:`Carrot` (our old messaging library)
    but isn't currently supported in :pypi:`Kombu` (our new messaging library).

.. _faq-non-amqp-missing-features:

不使用 AMQP 代理时，哪些功能不受支持？
-------------------------------------------------------------

What features aren't supported when not using an AMQP broker?

.. tab:: 中文

    以下是使用虚拟传输（virtual transports）时不可用功能的非完整列表：

        * 远程控制命令（仅 Redis 支持）。

        * 事件监控在部分虚拟传输中可能无法正常工作。

        * `header` 和 `fanout` 类型的交换机
            （其中 `fanout` 类型由 Redis 支持）。

.. tab:: 英文

    This is an incomplete list of features not available when
    using the virtual transports:

        * Remote control commands (supported only by Redis).

        * Monitoring with events may not work in all virtual transports.

        * The `header` and `fanout` exchange types
            (`fanout` is supported by Redis).

.. _faq-tasks:

任务
=====

Tasks

.. _faq-tasks-connection-reuse:

如何在调用任务时重用相同的连接？
-------------------------------------------------------

How can I reuse the same connection when calling tasks?

.. tab:: 中文

    **答复**：参见 :setting:`broker_pool_limit` 配置项。
    自 2.5 版本起，连接池默认启用。

.. tab:: 英文

    **Answer**: See the :setting:`broker_pool_limit` setting.
    The connection pool is enabled by default since version 2.5.

.. _faq-sudo-subprocess:

:mod:`subprocess` 中的 `:command:`sudo` 返回 `:const:`None`
------------------------------------------------------------

:command:`sudo` in a :mod:`subprocess` returns :const:`None`

.. tab:: 中文

    有一个 :command:`sudo` 的配置选项会禁止无 tty 的进程使用 :command:`sudo`：

    .. code-block:: text

        Defaults requiretty

    如果你在 :file:`/etc/sudoers` 文件中配置了该选项，
    当 worker 以守护进程（daemon）方式运行时，任务将无法调用 :command:`sudo`。
    如果你希望允许此行为，请从 :file:`/etc/sudoers` 文件中移除该行。

    参见：https://timelordz.com/wiki/Apache_Sudo_Commands

.. tab:: 英文

    There's a :command:`sudo` configuration option that makes it illegal
    for process without a tty to run :command:`sudo`:

    .. code-block:: text

        Defaults requiretty

    If you have this configuration in your :file:`/etc/sudoers` file then
    tasks won't be able to call :command:`sudo` when the worker is
    running as a daemon. If you want to enable that, then you need to remove
    the line from :file:`/etc/sudoers`.

    See: http://timelordz.com/wiki/Apache_Sudo_Commands

.. _faq-deletes-unknown-tasks:

为什么工作进程无法处理队列中的任务时会将其删除？
-----------------------------------------------------------------------------

Why do workers delete tasks from the queue if they're unable to process them?

.. tab:: 中文

    **答复**：

    Worker 会拒绝未知任务、编码错误的消息以及不符合任务消息协议的消息。

    如果不进行拒绝，这些消息可能会被不断重投递，形成死循环。

    较新版本的 RabbitMQ 支持为交换机配置死信队列（dead-letter queue），
    从而将被拒绝的消息转发至该队列。

.. tab:: 英文

    **Answer**:

    The worker rejects unknown tasks, messages with encoding errors and messages
    that don't contain the proper fields (as per the task message protocol).

    If it didn't reject them they could be redelivered again and again,
    causing a loop.

    Recent versions of RabbitMQ has the ability to configure a dead-letter
    queue for exchange, so that rejected messages is moved there.

.. _faq-execute-task-by-name:

我可以通过名称调用任务吗？
--------------------------

Can I call a task by name?

.. tab:: 中文

    **答复**：可以，使用 :meth:`@send_task` 方法。

    你还可以通过 AMQP 客户端，以任务名称方式从任意语言调用任务：

    .. code-block:: python

        >>> app.send_task('tasks.add', args=[2, 2], kwargs={})
        <AsyncResult: 373550e8-b9a0-4666-bc61-ace01fa4f91d>

    如果你希望结合 ``chain``、``chord`` 或 ``group`` 使用按名称调用的任务，
    可以使用 :meth:`@Celery.signature` 方法：

    .. code-block:: python

        >>> chain(
        ...     app.signature('tasks.add', args=[2, 2], kwargs={}),
        ...     app.signature('tasks.add', args=[1, 1], kwargs={})
        ... ).apply_async()
        <AsyncResult: e9d52312-c161-46f0-9013-2713e6df812d>
    
.. tab:: 英文---

    **Answer**: Yes, use :meth:`@send_task`.

    You can also call a task by name, from any language,
    using an AMQP client:

    .. code-block:: python

        >>> app.send_task('tasks.add', args=[2, 2], kwargs={})
        <AsyncResult: 373550e8-b9a0-4666-bc61-ace01fa4f91d>

    To use ``chain``, ``chord`` or ``group`` with tasks called by name,
    use the :meth:`@Celery.signature` method:

    .. code-block:: python

        >>> chain(
        ...     app.signature('tasks.add', args=[2, 2], kwargs={}),
        ...     app.signature('tasks.add', args=[1, 1], kwargs={})
        ... ).apply_async()
        <AsyncResult: e9d52312-c161-46f0-9013-2713e6df812d>

.. _faq-get-current-task-id:

我可以获取当前任务的任务 ID 吗？
------------------------------------------

Can I get the task id of the current task?

.. tab:: 中文

    **答复**：可以，当前任务的 id 及其他信息可通过 task request 获取::

        @app.task(bind=True)
        def mytask(self):
            cache.set(self.request.id, "Running")

    详见 :ref:`task-request-info`。

    如果你无法获取任务实例的引用，也可以使用
    :attr:`app.current_task <@current_task>`：

    .. code-block:: python

        >>> app.current_task.request.id

    但需注意，这个任务可能是任意任务，
    包括被 worker 执行的任务、由该任务调用的子任务，或以 eager 模式执行的任务。

    若希望获取当前 worker 实际正在处理的任务，请使用
    :attr:`app.current_worker_task <@current_worker_task>`：

    .. code-block:: python

        >>> app.current_worker_task.request.id

    .. note::

        :attr:`~@current_task` 与 :attr:`~@current_worker_task` 的值
        都可能为 :const:`None`。
    
.. tab:: 英文

    **Answer**: Yes, the current id and more is available in the task request::

        @app.task(bind=True)
        def mytask(self):
            cache.set(self.request.id, "Running")

    For more information see :ref:`task-request-info`.

    If you don't have a reference to the task instance you can use
    :attr:`app.current_task <@current_task>`:

    .. code-block:: python

        >>> app.current_task.request.id

    But note that this will be any task, be it one executed by the worker, or a
    task called directly by that task, or a task called eagerly.

    To get the current task being worked on specifically, use
    :attr:`app.current_worker_task <@current_worker_task>`:

    .. code-block:: python

        >>> app.current_worker_task.request.id

    .. note::

        Both :attr:`~@current_task`, and :attr:`~@current_worker_task` can be
        :const:`None`.

.. _faq-custom-task-ids:

我可以指定自定义的 task_id 吗？
-------------------------------

Can I specify a custom task_id?

.. tab:: 中文

    **答复**：可以，使用 :meth:`Task.apply_async` 方法中的 `task_id` 参数：

    .. code-block:: pycon

        >>> task.apply_async(args, kwargs, task_id='…')

.. tab:: 英文

    **Answer**: Yes, use the `task_id` argument to :meth:`Task.apply_async`:

    .. code-block:: pycon

        >>> task.apply_async(args, kwargs, task_id='…')


我可以对任务使用装饰器吗？
--------------------------------

Can I use decorators with tasks?

.. tab:: 中文

    **答复**：可以，但请参见 :ref:`task-basics` 侧边栏中的说明。

.. tab:: 英文

    **Answer**: Yes, but please see note in the sidebar at :ref:`task-basics`.

.. _faq-natural-task-ids:

我可以使用自然的任务 ID 吗？
---------------------------

Can I use natural task ids?

.. tab:: 中文

    **答复**：可以，但必须确保 ID 是唯一的。
    因为存在两个任务具有相同 ID 的行为是未定义的。

    虽然世界可能不会因此爆炸，但这些任务确实可能会互相覆盖其结果。

.. tab:: 英文

    **Answer**: Yes, but make sure it's unique, as the behavior
    for two tasks existing with the same id is undefined.

    The world will probably not explode, but they can
    definitely overwrite each others results.

.. _faq-task-callbacks:

我可以在某个任务完成后再运行另一个任务吗？
------------------------------------------------

Can I run a task once another task has finished?

.. tab:: 中文

    **答复**：可以，你可以在一个任务中安全地启动另一个任务。

    一个常见模式是为任务添加回调函数：

    .. code-block:: python

        from celery.utils.log import get_task_logger

        logger = get_task_logger(__name__)

        @app.task
        def add(x, y):
            return x + y

        @app.task(ignore_result=True)
        def log_result(result):
            logger.info("log_result got: %r", result)

    调用示例：

    .. code-block:: pycon

        >>> (add.s(2, 2) | log_result.s()).delay()

    更多信息参见 :doc:`userguide/canvas`。

.. tab:: 英文

    **Answer**: Yes, you can safely launch a task inside a task.

    A common pattern is to add callbacks to tasks:

    .. code-block:: python

        from celery.utils.log import get_task_logger

        logger = get_task_logger(__name__)

        @app.task
        def add(x, y):
            return x + y

        @app.task(ignore_result=True)
        def log_result(result):
            logger.info("log_result got: %r", result)

    Invocation:

    .. code-block:: pycon

        >>> (add.s(2, 2) | log_result.s()).delay()

    See :doc:`userguide/canvas` for more information.

.. _faq-cancel-task:

我可以取消正在执行的任务吗？
-------------------------------------

Can I cancel the execution of a task?

.. tab:: 中文

    **答复**：可以，使用 :meth:`result.revoke() <celery.result.AsyncResult.revoke>`：

    .. code-block:: pycon

        >>> result = add.apply_async(args=[2, 2], countdown=120)
        >>> result.revoke()

    如果你只有任务 ID，也可以这样撤销：

    .. code-block:: pycon

        >>> from proj.celery import app
        >>> app.control.revoke(task_id)

    此外也支持传入任务 ID 列表作为参数。

.. tab:: 英文

    **Answer**: Yes, Use :meth:`result.revoke() <celery.result.AsyncResult.revoke>`:

    .. code-block:: pycon

        >>> result = add.apply_async(args=[2, 2], countdown=120)
        >>> result.revoke()

    or if you only have the task id:

    .. code-block:: pycon

        >>> from proj.celery import app
        >>> app.control.revoke(task_id)


    The latter also support passing a list of task-ids as argument.

.. _faq-node-not-receiving-broadcast-commands:

为什么我的远程控制命令没有被所有工作进程接收？
--------------------------------------------------------------

Why aren't my remote control commands received by all workers?

.. tab:: 中文

    **答复**：为了接收广播式的远程控制命令，每个 worker 节点会基于其节点名（nodename）
    创建一个唯一的队列名称。

    如果多个 worker 具有相同的主机名，则控制命令将在它们之间轮询（round-robin）分发。

    为避免这种情况，你可以通过 :mod:`~celery.bin.worker` 的
    :option:`-n <celery worker -n>` 参数为每个 worker 显式设置节点名：

    .. code-block:: console

        $ celery -A proj worker -n worker1@%h
        $ celery -A proj worker -n worker2@%h

    其中 ``%h`` 会扩展为当前主机名。

.. tab:: 英文

    **Answer**: To receive broadcast remote control commands, every worker node
    creates a unique queue name, based on the nodename of the worker.

    If you have more than one worker with the same host name, the
    control commands will be received in round-robin between them.

    To work around this you can explicitly set the nodename for every worker
    using the :option:`-n <celery worker -n>` argument to
    :mod:`~celery.bin.worker`:

    .. code-block:: console

        $ celery -A proj worker -n worker1@%h
        $ celery -A proj worker -n worker2@%h

    where ``%h`` expands into the current hostname.

.. _faq-task-routing:

我可以只将某些任务发送到某些服务器吗？
-------------------------------------------

Can I send some tasks to only some servers?

.. tab:: 中文

    **答复**：可以。你可以使用不同的消息路由拓扑将任务路由到一个或多个 worker，
    一个 worker 实例也可以绑定多个队列。

    详见 :doc:`userguide/routing`。
    
.. tab:: 英文

    **Answer:** Yes, you can route tasks to one or more workers,
    using different message routing topologies, and a worker instance
    can bind to multiple queues.

    See :doc:`userguide/routing` for more information.

.. _faq-disable-prefetch:

我可以禁用任务预取吗？
-----------------------------------

Can I disable prefetching of tasks?

.. tab:: 中文

    **答复**：可能可以！AMQP 中的 “prefetch” 一词容易让人误解，
    它实际上仅用于描述任务预取的 *限制*，并不意味着真正的预取行为。

    可以禁用预取限制，但这意味着 worker 会尽可能快地消费尽可能多的任务。

    关于预取限制的讨论，以及配置 worker 每次仅保留一个任务的设置，详见：
    :ref:`optimizing-prefetch-limit`。

.. tab:: 英文

    **Answer**: Maybe! The AMQP term "prefetch" is confusing, as it's only used
    to describe the task prefetching *limit*.  There's no actual prefetching involved.

    Disabling the prefetch limits is possible, but that means the worker will
    consume as many tasks as it can, as fast as possible.

    A discussion on prefetch limits, and configuration settings for a worker
    that only reserves one task at a time is found here:
    :ref:`optimizing-prefetch-limit`.

.. _faq-change-periodic-task-interval-at-runtime:

我可以运行时更改周期性任务的执行间隔吗？
--------------------------------------------------------

Can I change the interval of a periodic task at runtime?

.. tab:: 中文

    **答复**：可以，你可以使用 Django 的数据库调度器，
    或自定义一个新的调度类，并重写
    :meth:`~celery.schedules.schedule.is_due` 方法：

    .. code-block:: python

        from celery.schedules import schedule

        class my_schedule(schedule):

            def is_due(self, last_run_at):
                return run_now, next_time_to_check

.. tab:: 英文

    **Answer**: Yes, you can use the Django database scheduler, or you can
    create a new schedule subclass and override
    :meth:`~celery.schedules.schedule.is_due`:

    .. code-block:: python

        from celery.schedules import schedule

        class my_schedule(schedule):

            def is_due(self, last_run_at):
                return run_now, next_time_to_check

.. _faq-task-priorities:

Celery 支持任务优先级吗？
------------------------------------

Does Celery support task priorities?

.. tab:: 中文

    **答复**：可以。RabbitMQ 从 3.5.0 版本起支持消息优先级，
    Redis 传输方式则是对优先级支持进行模拟。

    你也可以通过将高优先级任务路由到专用的 worker 来实现优先处理。
    在实践中，这种方式通常比消息级别的优先级更有效。
    你还可以结合速率限制和消息优先级来构建响应式系统。

.. tab:: 英文

    **Answer**: Yes, RabbitMQ supports priorities since version 3.5.0,
    and the Redis transport emulates priority support.

    You can also prioritize work by routing high priority tasks
    to different workers. In the real world this usually works better
    than per message priorities. You can use this in combination with rate
    limiting, and per message priorities to achieve a responsive system.

.. _faq-acks_late-vs-retry:

我应该使用 retry 还是 acks_late？
--------------------------------

Should I use retry or acks_late?

.. tab:: 中文

    **答复**：视情况而定。这两者并非互斥，你可能需要同时使用。

    `Task.retry` 用于重试任务，主要适用于通过 :keyword:`try` 块可以捕获的预期错误。
    这类错误不会触发 AMQP 事务： **即使任务抛出异常，消息也会被确认（acknowledged）！**

    `acks_late` 设置用于 worker 在执行任务中途崩溃时，允许任务被重新执行。
    需要注意的是，worker 崩溃是非常罕见的情况，通常属于不可恢复的错误，需要人工介入
    （如 worker 或任务代码中的 bug）。

    理想情况下，任何失败的任务都可以安全重试，但现实中往往并非如此。
    例如如下任务：

    .. code-block:: python

        @app.task
        def process_upload(filename, tmpfile):
            # 增加数据库中存储的文件计数
            increment_file_counter()
            add_file_metadata_to_db(filename, tmpfile)
            copy_file_to_destination(filename, tmpfile)

    如果在将文件复制到目标位置时发生崩溃，系统状态就会不一致。
    当然，这个例子并不致命，但你可以想象更严重的场景。
    因此，为了编程便利性，我们选择了牺牲一定的可靠性；
    但对于有需要且清楚其含义的用户，仍然可以启用 `acks_late`，
    并期望将来支持手动确认（manual acknowledgment）。

    另外，`Task.retry` 提供了 AMQP 事务不具备的一些特性：
    如重试间隔、最大重试次数等。

    因此，对于 Python 错误，请使用 `retry`；
    若你的任务是幂等的，并且需要更高的可靠性，
    可以结合使用 `acks_late`。

.. tab:: 英文

    **Answer**: Depends. It's not necessarily one or the other, you may want
    to use both.

    `Task.retry` is used to retry tasks, notably for expected errors that
    is catch-able with the :keyword:`try` block. The AMQP transaction isn't used
    for these errors: **if the task raises an exception it's still acknowledged!**

    The `acks_late` setting would be used when you need the task to be
    executed again if the worker (for some reason) crashes mid-execution.
    It's important to note that the worker isn't known to crash, and if
    it does it's usually an unrecoverable error that requires human
    intervention (bug in the worker, or task code).

    In an ideal world you could safely retry any task that's failed, but
    this is rarely the case. Imagine the following task:

    .. code-block:: python

        @app.task
        def process_upload(filename, tmpfile):
            # Increment a file count stored in a database
            increment_file_counter()
            add_file_metadata_to_db(filename, tmpfile)
            copy_file_to_destination(filename, tmpfile)

    If this crashed in the middle of copying the file to its destination
    the world would contain incomplete state. This isn't a critical
    scenario of course, but you can probably imagine something far more
    sinister. So for ease of programming we have less reliability;
    It's a good default, users who require it and know what they
    are doing can still enable acks_late (and in the future hopefully
    use manual acknowledgment).

    In addition `Task.retry` has features not available in AMQP
    transactions: delay between retries, max retries, etc.

    So use retry for Python errors, and if your task is idempotent
    combine that with `acks_late` if that level of reliability
    is required.

.. _faq-schedule-at-specific-time:

我可以安排任务在特定时间执行吗？
---------------------------------------------------

Can I schedule tasks to execute at a specific time?

.. tab:: 中文

    **答复**：可以。你可以使用 :meth:`Task.apply_async` 的 `eta` 参数。
    需要注意的是，不建议使用过远的 `eta` 时间，此类情况推荐使用
    :ref:`周期性任务 <guide-beat>`。

    详见 :ref:`calling-eta`。

.. tab:: 英文

    **Answer**: Yes. You can use the `eta` argument of :meth:`Task.apply_async`.
    Note that using distant `eta` times is not recommended, and in such case
    :ref:`periodic tasks<guide-beat>` should be preferred.

    See :ref:`calling-eta` for more details.

.. _faq-safe-worker-shutdown:

我可以安全地关闭工作进程吗？
----------------------------------

Can I safely shut down the worker?

.. tab:: 中文

    **答复**：可以，使用 :sig:`TERM` 信号。

    这将通知 worker 完成当前正在执行的所有任务，并尽快关闭。
    即使使用的是实验性的传输方式，只要 shutdown 完成，任务也不会丢失。

    **绝不应该** 使用 :sig:`KILL` 信号（即 ``kill -9``）强制终止 :mod:`~celery.bin.worker`，
    除非你已经尝试过多次使用 :sig:`TERM` 并等待了几分钟以便让其有机会正常退出。

    同时，确保你终止的是主 worker 进程，而不是其子进程。
    如果你知道某个子进程正在执行任务，并且该任务阻碍了 worker 的关闭，
    可以将 kill 信号发送给该特定子进程，但这也会导致该任务被标记为
    ``WorkerLostError`` 状态，因此该任务不会被重新执行。

    若你安装了 :pypi:`setproctitle` 模块，识别进程类型会更容易：

    .. code-block:: console

        $ pip install setproctitle

    安装该库后，你可以在 :command:`ps` 输出中看到进程类型，
    但需重启 worker 进程后此功能才会生效。

    .. seealso::

        :ref:`worker-stopping`

.. tab:: 英文

    **Answer**: Yes, use the :sig:`TERM` signal.

    This will tell the worker to finish all currently
    executing jobs and shut down as soon as possible. No tasks should be lost
    even with experimental transports as long as the shutdown completes.

    You should never stop :mod:`~celery.bin.worker` with the :sig:`KILL` signal
    (``kill -9``), unless you've tried :sig:`TERM` a few times and waited a few
    minutes to let it get a chance to shut down.

    Also make sure you kill the main worker process only, not any of its child
    processes.  You can direct a kill signal to a specific child process if
    you know the process is currently executing a task the worker shutdown
    is depending on, but this also means that a ``WorkerLostError`` state will
    be set for the task so the task won't run again.

    Identifying the type of process is easier if you have installed the
    :pypi:`setproctitle` module:

    .. code-block:: console

        $ pip install setproctitle

    With this library installed you'll be able to see the type of process in
    :command:`ps` listings, but the worker must be restarted for this to take effect.

    .. seealso::

        :ref:`worker-stopping`

.. _faq-daemonizing:

我可以在 [platform] 上在后台运行工作进程吗？
-----------------------------------------------------

Can I run the worker in the background on [platform]?

.. tab:: 中文

    **答复**：可以，详见 :ref:`daemonizing`。

.. tab:: 英文

    **Answer**: Yes, please see :ref:`daemonizing`.

.. _faq-django:

Django
======

.. _faq-django-beat-database-tables:

“django-celery-beat”创建的数据库表有什么用途？
-----------------------------------------------------------------------------

What purpose does the database tables created by ``django-celery-beat`` have?

.. tab:: 中文

    当使用数据库支持的调度器时，周期性任务的调度信息来自 ``PeriodicTask`` 模型，
    此外还会涉及一些辅助表（如 ``IntervalSchedule``、 ``CrontabSchedule``、 ``PeriodicTasks``）。

.. tab:: 英文

    When the database-backed schedule is used the periodic task
    schedule is taken from the ``PeriodicTask`` model, there are
    also several other helper tables (``IntervalSchedule``,
    ``CrontabSchedule``, ``PeriodicTasks``).

.. _faq-django-result-database-tables:

“django-celery-results”创建的数据库表有什么用途？
--------------------------------------------------------------------------------

What purpose does the database tables created by ``django-celery-results`` have?

.. tab:: 中文

    Django 的数据库结果后端扩展需要额外的两个模型：
    ``TaskResult`` 和 ``GroupResult``。

.. tab:: 英文

    The Django database result backend extension requires
    two extra models: ``TaskResult`` and ``GroupResult``.

.. _faq-windows:

Windows
=======

.. _faq-windows-worker-embedded-beat:

Celery 支持 Windows 吗？
----------------------------------------------------------------

Does Celery support Windows?

.. tab:: 中文

    **答复**：不支持。

    自 Celery 4.x 起，因资源限制已不再支持 Windows 平台。

    不过它可能仍可工作，并且我们欢迎相关补丁提交。

.. tab:: 英文

    **Answer**: No.

    Since Celery 4.x, Windows is no longer supported due to lack of resources.

    But it may still work and we are happy to accept patches.
