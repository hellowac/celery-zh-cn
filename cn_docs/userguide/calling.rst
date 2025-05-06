.. _guide-calling:

===============
调用任务/Tasks
===============

Calling Tasks

.. _calling-basics:
    
.. _calling-cheat:

基础知识
======

Basics

.. tab:: 中文

    本文档介绍了 Celery 的统一“调用 API（Calling API）”，该 API 被任务实例和 :ref:`canvas <guide-canvas>` 使用。
    
    该 API 定义了一组标准的执行选项，并包括三个方法：
    
    - ``apply_async(args[, kwargs[, …]])``
    
      发送一个任务消息。
    
    - ``delay(*args, **kwargs)``
    
      发送任务消息的简写方式，但不支持设置执行选项。
    
    - *调用* （``__call__``）
    
      对支持调用 API 的对象进行调用（例如 ``add(2, 2)``）意味着任务不会由 worker 执行，而是直接在当前进程中执行（不会发送任务消息）。
    
    .. topic:: 快速备忘单（Quick Cheat Sheet）
    
        - ``T.delay(arg, kwarg=value)``
            使用星号参数的简写方式调用 ``.apply_async``。
            （``.delay(*args, **kwargs)`` 实际等价于 ``.apply_async(args, kwargs)``）。
    
        - ``T.apply_async((arg,), {'kwarg': value})``
    
        - ``T.apply_async(countdown=10)``
            在 10 秒后执行。
    
        - ``T.apply_async(eta=now + timedelta(seconds=10))``
            使用 ``eta`` 指定将在 10 秒后执行。
    
        - ``T.apply_async(countdown=60, expires=120)``
            在 1 分钟后执行，但将在 2 分钟后过期。
    
        - ``T.apply_async(expires=now + timedelta(days=2))``
            使用 :class:`~datetime.datetime` 设置为在 2 天后过期。

.. tab:: 英文

    This document describes Celery's uniform "Calling API"
    used by task instances and the :ref:`canvas <guide-canvas>`.
    
    The API defines a standard set of execution options, as well as three methods:
    
    - ``apply_async(args[, kwargs[, …]])``
    
      Sends a task message.
    
    - ``delay(*args, **kwargs)``
    
      Shortcut to send a task message, but doesn't support execution
      options.
    
    - *calling* (``__call__``)
    
      Applying an object supporting the calling API (e.g., ``add(2, 2)``)
      means that the task will not be executed by a worker, but in the current
      process instead (a message won't be sent).
    
    .. topic:: Quick Cheat Sheet
    
        - ``T.delay(arg, kwarg=value)``
            Star arguments shortcut to ``.apply_async``.
            (``.delay(*args, **kwargs)`` calls ``.apply_async(args, kwargs)``).
    
        - ``T.apply_async((arg,), {'kwarg': value})``
    
        - ``T.apply_async(countdown=10)``
            executes in 10 seconds from now.
    
        - ``T.apply_async(eta=now + timedelta(seconds=10))``
            executes in 10 seconds from now, specified using ``eta``
    
        - ``T.apply_async(countdown=60, expires=120)``
            executes in one minute from now, but expires after 2 minutes.
    
        - ``T.apply_async(expires=now + timedelta(days=2))``
            expires in 2 days, set using :class:`~datetime.datetime`.


示例
-------

Example

.. tab:: 中文

    :meth:`~@Task.delay` 方法十分便捷，因为它看起来就像是调用一个普通函数：

    .. code-block:: python

        task.delay(arg1, arg2, kwarg1='x', kwarg2='y')

    而如果使用 :meth:`~@Task.apply_async`，你需要这样写：

    .. code-block:: python

        task.apply_async(args=[arg1, arg2], kwargs={'kwarg1': 'x', 'kwarg2': 'y'})

    .. sidebar:: 提示

        如果当前进程中未注册该任务，可以使用 :meth:`~@send_task` 通过任务名称来调用任务。

    因此，虽然 `delay` 显然更为简洁方便，但如果你想设置额外的执行选项，就必须使用 ``apply_async``。

    本文档的其余部分将详细介绍任务执行选项。所有示例都使用一个名为 `add` 的任务，它返回两个参数的和：

    .. code-block:: python

        @app.task
        def add(x, y):
            return x + y


    .. topic:: 还有另一种方式……

        在阅读 :ref:`Canvas <guide-canvas>` 部分时你会进一步了解，:class:`~celery.signature` 是用于传递任务调用签名的对象（例如用于网络传输），并且它们也支持调用 API：

        .. code-block:: python

            task.s(arg1, arg2, kwarg1='x', kwargs2='y').apply_async()

.. tab:: 英文

    The :meth:`~@Task.delay` method is convenient as it looks like calling a regular
    function:

    .. code-block:: python

        task.delay(arg1, arg2, kwarg1='x', kwarg2='y')

    Using :meth:`~@Task.apply_async` instead you have to write:

    .. code-block:: python

        task.apply_async(args=[arg1, arg2], kwargs={'kwarg1': 'x', 'kwarg2': 'y'})

    .. sidebar:: Tip

        If the task isn't registered in the current process
        you can use :meth:`~@send_task` to call the task by name instead.


    So `delay` is clearly convenient, but if you want to set additional execution
    options you have to use ``apply_async``.

    The rest of this document will go into the task execution
    options in detail. All examples use a task
    called `add`, returning the sum of two arguments:

    .. code-block:: python

        @app.task
        def add(x, y):
            return x + y


    .. topic:: There's another way…

        You'll learn more about this later while reading about the :ref:`Canvas
        <guide-canvas>`, but :class:`~celery.signature`'s are objects used to pass around
        the signature of a task invocation, (for example to send it over the
        network), and they also support the Calling API:

        .. code-block:: python

            task.s(arg1, arg2, kwarg1='x', kwargs2='y').apply_async()

.. _calling-links:

链接（回调/错误回调）
============================

Linking (callbacks/errbacks)

.. tab:: 中文

    Celery 支持将任务链接在一起，使得一个任务可以在另一个任务之后执行。
    回调任务会以父任务的结果作为部分参数被调用：

    .. code-block:: python

        add.apply_async((2, 2), link=add.s(16))

    .. sidebar:: 什么是 ``s``？

        这里使用的 ``add.s`` 调用被称为签名（signature）。
        如果你不清楚这是什么，可以参考 :ref:`canvas guide <guide-canvas>`。
        你还可以在那里了解 :class:`~celery.chain`：一种更简单的方式来串联任务。

        实际上，``link`` 执行选项被视为一种内部原语，通常不建议直接使用，
        而是推荐使用链（chain）。

    上述示例中，第一个任务的结果（4）将被发送给一个新任务，
    该任务将之前的结果加上 16，形成表达式：
    :math:`(2 + 2) + 16 = 20`

    你还可以在任务抛出异常时执行回调（*errback*）。
    Worker 实际上不会以任务的方式调用 errback，而是会直接调用该函数，
    以便可以传递原始请求、异常对象和回溯信息。

    以下是一个错误回调的示例：

    .. code-block:: python

        @app.task
        def error_handler(request, exc, traceback):
            print('Task {0} raised exception: {1!r}\n{2!r}'.format(
                request.id, exc, traceback))

    可以使用 ``link_error`` 执行选项将其添加到任务中：

    .. code-block:: python

        add.apply_async((2, 2), link_error=error_handler.s())

    此外，``link`` 和 ``link_error`` 选项都可以使用列表形式：

    .. code-block:: python

        add.apply_async((2, 2), link=[add.s(16), other_task.s()])

    所有回调/错误回调将按顺序调用，且每个回调将以父任务的返回值
    作为部分参数执行。

    在 chord 的情况下，我们可以使用多种策略处理错误。
    更多信息请参阅 :ref:`chord error handling <chord-errors>`。

.. tab:: 英文

    Celery supports linking tasks together so that one task follows another.
    The callback task will be applied with the result of the parent task
    as a partial argument:

    .. code-block:: python

        add.apply_async((2, 2), link=add.s(16))

    .. sidebar:: What's ``s``?

        The ``add.s`` call used here is called a signature. If you
        don't know what they are you should read about them in the
        :ref:`canvas guide <guide-canvas>`.
        There you can also learn about :class:`~celery.chain`:  a simpler
        way to chain tasks together.

        In practice the ``link`` execution option is considered an internal
        primitive, and you'll probably not use it directly, but
        use chains instead.

    Here the result of the first task (4) will be sent to a new
    task that adds 16 to the previous result, forming the expression
    :math:`(2 + 2) + 16 = 20`


    You can also cause a callback to be applied if task raises an exception
    (*errback*). The worker won't actually call the errback as a task, but will
    instead call the errback function directly so that the raw request, exception
    and traceback objects can be passed to it.

    This is an example error callback:

    .. code-block:: python

        @app.task
        def error_handler(request, exc, traceback):
            print('Task {0} raised exception: {1!r}\n{2!r}'.format(
                request.id, exc, traceback))

    it can be added to the task using the ``link_error`` execution
    option:

    .. code-block:: python

        add.apply_async((2, 2), link_error=error_handler.s())


    In addition, both the ``link`` and ``link_error`` options can be expressed
    as a list:

    .. code-block:: python

        add.apply_async((2, 2), link=[add.s(16), other_task.s()])

    The callbacks/errbacks will then be called in order, and all
    callbacks will be called with the return value of the parent task
    as a partial argument.

    In the case of a chord, we can handle errors using multiple handling strategies.
    See :ref:`chord error handling <chord-errors>` for more information.

.. _calling-on-message:

消息
==========

On message

.. tab:: 中文

    Celery 支持通过设置 on_message 回调来捕获所有状态变更。
    
    例如，对于一个长时间运行的任务，可通过如下方式发送任务进度：
    
    .. code-block:: python
    
        @app.task(bind=True)
        def hello(self, a, b):
            time.sleep(1)
            self.update_state(state="PROGRESS", meta={'progress': 50})
            time.sleep(1)
            self.update_state(state="PROGRESS", meta={'progress': 90})
            time.sleep(1)
            return 'hello world: %i' % (a+b)
    
    .. code-block:: python
    
        def on_raw_message(body):
            print(body)
    
        a, b = 1, 1
        r = hello.apply_async(args=(a, b))
        print(r.get(on_message=on_raw_message, propagate=False))
    
    将输出如下内容：
    
    .. code-block:: text
    
        {'task_id': '5660d3a3-92b8-40df-8ccc-33a5d1d680d7',
         'result': {'progress': 50},
         'children': [],
         'status': 'PROGRESS',
         'traceback': None}
        {'task_id': '5660d3a3-92b8-40df-8ccc-33a5d1d680d7',
         'result': {'progress': 90},
         'children': [],
         'status': 'PROGRESS',
         'traceback': None}
        {'task_id': '5660d3a3-92b8-40df-8ccc-33a5d1d680d7',
         'result': 'hello world: 10',
         'children': [],
         'status': 'SUCCESS',
         'traceback': None}
        hello world: 10

.. tab:: 英文

    Celery supports catching all states changes by setting on_message callback.
    
    For example for long-running tasks to send task progress you can do something like this:
    
    .. code-block:: python
    
        @app.task(bind=True)
        def hello(self, a, b):
            time.sleep(1)
            self.update_state(state="PROGRESS", meta={'progress': 50})
            time.sleep(1)
            self.update_state(state="PROGRESS", meta={'progress': 90})
            time.sleep(1)
            return 'hello world: %i' % (a+b)
    
    .. code-block:: python
    
        def on_raw_message(body):
            print(body)
    
        a, b = 1, 1
        r = hello.apply_async(args=(a, b))
        print(r.get(on_message=on_raw_message, propagate=False))
    
    Will generate output like this:
    
    .. code-block:: text
    
        {'task_id': '5660d3a3-92b8-40df-8ccc-33a5d1d680d7',
         'result': {'progress': 50},
         'children': [],
         'status': 'PROGRESS',
         'traceback': None}
        {'task_id': '5660d3a3-92b8-40df-8ccc-33a5d1d680d7',
         'result': {'progress': 90},
         'children': [],
         'status': 'PROGRESS',
         'traceback': None}
        {'task_id': '5660d3a3-92b8-40df-8ccc-33a5d1d680d7',
         'result': 'hello world: 10',
         'children': [],
         'status': 'SUCCESS',
         'traceback': None}
        hello world: 10


.. _calling-eta:

预计到达时间和倒计时
=================

ETA and Countdown

.. tab:: 中文

    ETA（预计到达时间）允许你设置一个具体的日期和时间，
    作为任务最早被执行的时间点。 `countdown` 是设置 ETA 的快捷方式，
    用于指定未来几秒内执行：

    .. code-block:: pycon

        >>> result = add.apply_async((2, 2), countdown=3)
        >>> result.get()    # 至少等待 3 秒才返回
        4

    任务保证会在指定的时间 *之后* 执行，但不一定是准确时间。
    可能导致超时的原因包括队列中等待的项目过多，或网络延迟严重。
    为了确保任务按时执行，应监控队列是否拥堵。可以使用 Munin 或类似工具接收告警，
    从而采取相应措施来缓解负载。详见 :ref:`monitoring-munin`。

    `countdown` 是一个整数，而 `eta` 必须是 :class:`~datetime.datetime` 对象，
    用于指定精确的时间（支持毫秒精度和时区信息）：

    .. code-block:: pycon

        >>> from datetime import datetime, timedelta, timezone

        >>> tomorrow = datetime.now(timezone.utc) + timedelta(days=1)
        >>> add.apply_async((2, 2), eta=tomorrow)

    .. warning::

        使用 `eta` 或 `countdown` 的任务会被 worker 立即拉取，
        并在调度时间到来之前一直保留在内存中。
        如果使用这些选项调度大量未来任务，可能会在 worker 内堆积，
        显著增加内存占用。

        此外，任务在 worker 开始执行之前不会被确认（acknowledged）。
        如果使用 Redis 作为 broker，当 `countdown` 超过 `visibility_timeout`
        时，任务会被重新投递（参见 :ref:`redis-caveats`）。

        因此，**不推荐** 使用 `eta` 和 `countdown` 选项来调度远期任务。
        理想情况下应将调度时间控制在几分钟内。
        对于较长的调度需求，推荐使用基于数据库的周期性任务调度器，
        如在 Django 中使用 :pypi:`django-celery-beat`
        （参见 :ref:`beat-custom-schedulers`）。

    .. warning::

        当使用 RabbitMQ 作为消息代理，并设置超过 15 分钟的 ``countdown`` 时，
        可能会遇到 worker 被终止并抛出 :exc:`~amqp.exceptions.PreconditionFailed`
        错误的情况：

        .. code-block:: pycon

            amqp.exceptions.PreconditionFailed: (0, 0): (406) PRECONDITION_FAILED - consumer ack timed out on channel

        从 RabbitMQ 3.8.15 开始，默认的 ``consumer_timeout`` 为 15 分钟。
        在 3.8.17 版本中该值被提高到 30 分钟。
        如果消费者在此超时时间内未确认（ack）其任务交付，
        通道将被以 ``PRECONDITION_FAILED`` 错误关闭。
        详见 `Delivery Acknowledgement Timeout`_。

        要解决该问题，应在 RabbitMQ 配置文件 ``rabbitmq.conf`` 中设置
        ``consumer_timeout`` 参数，使其大于或等于你的 countdown 值。
        例如可以设置一个很大的值：
        ``consumer_timeout = 31622400000``，即 1 年（毫秒表示），
        以避免将来出现问题。


.. tab:: 英文

    The ETA (estimated time of arrival) lets you set a specific date and time that
    is the earliest time at which your task will be executed. `countdown` is
    a shortcut to set ETA by seconds into the future.

    .. code-block:: pycon

        >>> result = add.apply_async((2, 2), countdown=3)
        >>> result.get()    # this takes at least 3 seconds to return
        4

    The task is guaranteed to be executed at some time *after* the
    specified date and time, but not necessarily at that exact time.
    Possible reasons for broken deadlines may include many items waiting
    in the queue, or heavy network latency. To make sure your tasks
    are executed in a timely manner you should monitor the queue for congestion. Use
    Munin, or similar tools, to receive alerts, so appropriate action can be
    taken to ease the workload. See :ref:`monitoring-munin`.

    While `countdown` is an integer, `eta` must be a :class:`~datetime.datetime`
    object, specifying an exact date and time (including millisecond precision,
    and timezone information):

    .. code-block:: pycon

        >>> from datetime import datetime, timedelta, timezone

        >>> tomorrow = datetime.now(timezone.utc) + timedelta(days=1)
        >>> add.apply_async((2, 2), eta=tomorrow)

    .. warning::

        Tasks with `eta` or `countdown` are immediately fetched by the worker
        and until the scheduled time passes, they reside in the worker's memory.
        When using those options to schedule lots of tasks for a distant future,
        those tasks may accumulate in the worker and make a significant impact on
        the RAM usage.

        Moreover, tasks are not acknowledged until the worker starts executing
        them. If using Redis as a broker, task will get redelivered when `countdown`
        exceeds `visibility_timeout` (see :ref:`redis-caveats`).

        Therefore, using `eta` and `countdown` **is not recommended** for
        scheduling tasks for a distant future. Ideally, use values no longer
        than several minutes. For longer durations, consider using
        database-backed periodic tasks, e.g. with :pypi:`django-celery-beat` if
        using Django (see :ref:`beat-custom-schedulers`).

    .. warning::

        When using RabbitMQ as a message broker when specifying a ``countdown``
        over 15 minutes, you may encounter the problem that the worker terminates
        with an :exc:`~amqp.exceptions.PreconditionFailed` error will be raised:

        .. code-block:: pycon

            amqp.exceptions.PreconditionFailed: (0, 0): (406) PRECONDITION_FAILED - consumer ack timed out on channel

        In RabbitMQ since version 3.8.15 the default value for
        ``consumer_timeout`` is 15 minutes.
        Since version 3.8.17 it was increased to 30 minutes. If a consumer does
        not ack its delivery for more than the timeout value, its channel will be
        closed with a ``PRECONDITION_FAILED`` channel exception.
        See `Delivery Acknowledgement Timeout`_ for more information.

        To solve the problem, in RabbitMQ configuration file ``rabbitmq.conf`` you
        should specify the ``consumer_timeout`` parameter greater than or equal to
        your countdown value. For example, you can specify a very large value
        of ``consumer_timeout = 31622400000``, which is equal to 1 year
        in milliseconds, to avoid problems in the future.

.. _`Delivery Acknowledgement Timeout`: https://www.rabbitmq.com/consumers.html#acknowledgement-timeout

.. _calling-expiration:

到期时间
==========

Expiration

.. tab:: 中文

    ``expires`` 参数用于定义一个可选的过期时间，
    可以是任务发布后的秒数，或通过 :class:`~datetime.datetime` 指定的具体日期时间：

    .. code-block:: pycon

        >>> # 任务将在一分钟后过期
        >>> add.apply_async((10, 10), expires=60)

        >>> # 也支持 datetime 对象
        >>> from datetime import datetime, timedelta, timezone
        >>> add.apply_async((10, 10), kwargs,
        ...                 expires=datetime.now(timezone.utc) + timedelta(days=1))

    当 Worker 接收到一个已过期的任务时，会将其标记为 :state:`REVOKED`
    （:exc:`~@TaskRevokedError`）。

.. tab:: 英文

    The `expires` argument defines an optional expiry time,
    either as seconds after task publish, or a specific date and time using
    :class:`~datetime.datetime`:

    .. code-block:: pycon

        >>> # Task expires after one minute from now.
        >>> add.apply_async((10, 10), expires=60)

        >>> # Also supports datetime
        >>> from datetime import datetime, timedelta, timezone
        >>> add.apply_async((10, 10), kwargs,
        ...                 expires=datetime.now(timezone.utc) + timedelta(days=1))


    When a worker receives an expired task it will mark
    the task as :state:`REVOKED` (:exc:`~@TaskRevokedError`).

.. _calling-retry:

消息发送重试
=====================

Message Sending Retry

.. tab:: 中文

    Celery 在连接失败时会自动重试发送消息，并且可以对重试行为进行配置 —— 包括重试间隔、
    最大重试次数，或完全禁用重试。

    若要禁用重试，可以将 ``retry`` 执行选项设置为 :const:`False`：

    .. code-block:: python

        add.apply_async((2, 2), retry=False)

    .. topic:: 相关设置

        .. hlist::
            :columns: 2

            - :setting:`task_publish_retry`
            - :setting:`task_publish_retry_policy`

.. tab:: 英文

    Celery will automatically retry sending messages in the event of connection
    failure, and retry behavior can be configured -- like how often to retry, or a maximum
    number of retries -- or disabled all together.

    To disable retry you can set the ``retry`` execution option to :const:`False`:

    .. code-block:: python

        add.apply_async((2, 2), retry=False)

    .. topic:: Related Settings

        .. hlist::
            :columns: 2

            - :setting:`task_publish_retry`
            - :setting:`task_publish_retry_policy`

重试策略
------------

Retry Policy

.. tab:: 中文

    重试策略（retry policy）是一个映射，用于控制重试行为，
    其可包含以下键：
    
    - ``max_retries``
    
      放弃之前最多允许重试的次数；若达到该次数仍失败，则会抛出导致重试失败的异常。
    
      如果设置为 :const:`None`，则会无限次重试。
    
      默认值为重试 3 次。
    
    - ``interval_start``
    
      两次重试之间的等待时间（秒），可为浮点数或整数。默认值为 0（即首次重试立即发生）。
    
    - ``interval_step``
    
      每次连续重试时，会在之前的延迟基础上增加该值（浮点或整数）。默认值为 0.2。
    
    - ``interval_max``
    
      两次重试之间的最大等待时间（秒），可为浮点或整数。默认值为 0.2。
    
    - ``retry_errors``
    
      ``retry_errors`` 是一个异常类的元组，仅当任务抛出的异常属于其中之一时才会进行重试。
      若未指定，则忽略。默认值为 ``None``（忽略）。
    
      例如，如果你只希望对超时的任务进行重试，可以使用
      :exc:`~kombu.exceptions.TimeoutError`：
    
      .. code-block:: python
    
          from kombu.exceptions import TimeoutError
    
          add.apply_async((2, 2), retry=True, retry_policy={
              'max_retries': 3,
              'retry_errors': (TimeoutError, ),
          })
    
      .. versionadded:: 5.3
    
    例如，默认的重试策略等价于：
    
    .. code-block:: python
    
        add.apply_async((2, 2), retry=True, retry_policy={
            'max_retries': 3,
            'interval_start': 0,
            'interval_step': 0.2,
            'interval_max': 0.2,
            'retry_errors': None,
        })
    
    最大总重试时间为 0.4 秒。默认时间较短，
    是为了避免在连接故障时产生“重试风暴”，
    例如在 broker 连接中断时，大量 Web 服务器进程处于等待重试状态，
    从而阻塞其他请求的处理。
    

.. tab:: 英文

    A retry policy is a mapping that controls how retries behave,
    and can contain the following keys:
    
    - `max_retries`
    
      Maximum number of retries before giving up, in this case the
      exception that caused the retry to fail will be raised.
    
      A value of :const:`None` means it will retry forever.
    
      The default is to retry 3 times.
    
    - `interval_start`
    
      Defines the number of seconds (float or integer) to wait between
      retries. Default is 0 (the first retry will be instantaneous).
    
    - `interval_step`
    
      On each consecutive retry this number will be added to the retry
      delay (float or integer). Default is 0.2.
    
    - `interval_max`
    
      Maximum number of seconds (float or integer) to wait between
      retries. Default is 0.2.
    
    - `retry_errors`
    
      `retry_errors` is a tuple of exception classes that should be retried.
      It will be ignored if not specified. Default is None (ignored).
    
      For example, if you want to retry only tasks that were timed out, you can use
      :exc:`~kombu.exceptions.TimeoutError`:
    
      .. code-block:: python
    
          from kombu.exceptions import TimeoutError
    
          add.apply_async((2, 2), retry=True, retry_policy={
              'max_retries': 3,
              'retry_errors': (TimeoutError, ),
          })
    
      .. versionadded:: 5.3
    
    For example, the default policy correlates to:
    
    .. code-block:: python
    
        add.apply_async((2, 2), retry=True, retry_policy={
            'max_retries': 3,
            'interval_start': 0,
            'interval_step': 0.2,
            'interval_max': 0.2,
            'retry_errors': None,
        })
    
    the maximum time spent retrying will be 0.4 seconds. It's set relatively
    short by default because a connection failure could lead to a retry pile effect
    if the broker connection is down -- For example, many web server processes waiting
    to retry, blocking other incoming requests.

.. _calling-connection-errors:

连接错误处理
=========================

Connection Error Handling

.. tab:: 中文

    当你发送任务时，如果消息传输连接丢失，或无法建立连接，
    将抛出 :exc:`~kombu.exceptions.OperationalError` 错误：

    .. code-block:: pycon

        >>> from proj.tasks import add
        >>> add.delay(2, 2)
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "celery/app/task.py", line 388, in delay
                return self.apply_async(args, kwargs)
        File "celery/app/task.py", line 503, in apply_async
            **options
        File "celery/app/base.py", line 662, in send_task
            amqp.send_task_message(P, name, message, **options)
        File "celery/backends/rpc.py", line 275, in on_task_call
            maybe_declare(self.binding(producer.channel), retry=True)
        File "/opt/celery/kombu/kombu/messaging.py", line 204, in _get_channel
            channel = self._channel = channel()
        File "/opt/celery/py-amqp/amqp/connection.py", line 272, in connect
            self.transport.connect()
        File "/opt/celery/py-amqp/amqp/transport.py", line 100, in connect
            self._connect(self.host, self.port, self.connect_timeout)
        File "/opt/celery/py-amqp/amqp/transport.py", line 141, in _connect
            self.sock.connect(sa)
        kombu.exceptions.OperationalError: [Errno 61] Connection refused

    如果你启用了 :ref:`重试机制 <calling-retry>`，此错误只会在重试耗尽后抛出，
    或在禁用重试时立即抛出。

    你也可以自行处理该异常：

    .. code-block:: pycon

        >>> from celery.utils.log import get_logger
        >>> logger = get_logger(__name__)

        >>> try:
        ...     add.delay(2, 2)
        ... except add.OperationalError as exc:
        ...     logger.exception('发送任务时出错: %r', exc)

.. tab:: 英文

    When you send a task and the message transport connection is lost, or
    the connection cannot be initiated, an :exc:`~kombu.exceptions.OperationalError`
    error will be raised:

    .. code-block:: pycon

        >>> from proj.tasks import add
        >>> add.delay(2, 2)
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "celery/app/task.py", line 388, in delay
                return self.apply_async(args, kwargs)
        File "celery/app/task.py", line 503, in apply_async
            **options
        File "celery/app/base.py", line 662, in send_task
            amqp.send_task_message(P, name, message, **options)
        File "celery/backends/rpc.py", line 275, in on_task_call
            maybe_declare(self.binding(producer.channel), retry=True)
        File "/opt/celery/kombu/kombu/messaging.py", line 204, in _get_channel
            channel = self._channel = channel()
        File "/opt/celery/py-amqp/amqp/connection.py", line 272, in connect
            self.transport.connect()
        File "/opt/celery/py-amqp/amqp/transport.py", line 100, in connect
            self._connect(self.host, self.port, self.connect_timeout)
        File "/opt/celery/py-amqp/amqp/transport.py", line 141, in _connect
            self.sock.connect(sa)
        kombu.exceptions.OperationalError: [Errno 61] Connection refused

    If you have :ref:`retries <calling-retry>` enabled this will only happen after
    retries are exhausted, or when disabled immediately.

    You can handle this error too:

    .. code-block:: pycon

        >>> from celery.utils.log import get_logger
        >>> logger = get_logger(__name__)

        >>> try:
        ...     add.delay(2, 2)
        ... except add.OperationalError as exc:
        ...     logger.exception('Sending task raised: %r', exc)

.. _calling-serializers:

序列化器
===========

Serializers

.. sidebar::  安全性/Security

    .. tab:: 中文

        pickle 模块允许执行任意函数，
        请参阅 :ref:`安全指南 <guide-security>`。

        Celery 也内置了一个使用加密机制签名消息的专用序列化器。

    .. tab:: 英文

        The pickle module allows for execution of arbitrary functions,
        please see the :ref:`security guide <guide-security>`.

        Celery also comes with a special serializer that uses
        cryptography to sign your messages.

.. tab:: 中文

    客户端与 Worker 之间传输的数据必须经过序列化，
    因此 Celery 中的每条消息都带有 ``content_type`` 头，
    用于标识使用的序列化方法。

    默认的序列化器是 `JSON`，但你可以通过 :setting:`task_serializer` 设置进行更改，
    也可以针对每个任务单独设置，甚至每条消息分别设置。

    Celery 内置支持以下序列化格式：`JSON`、:mod:`pickle`、`YAML` 和 ``msgpack``，
    你也可以将自定义序列化器注册到 Kombu 的序列化器注册表中。

    .. seealso::

        Kombu 用户指南中的 :ref:`消息序列化 <kombu:guide-serialization>`。

    以下是各选项的优缺点：

    json -- JSON 在多种编程语言中都有良好支持，
        是 Python（自 2.6 起）的标准库之一，解码速度也相当快。

        JSON 的主要限制在于仅支持以下数据类型：字符串、Unicode、浮点数、布尔值、
        字典和列表。不支持 Decimals 和 日期对象。

        二进制数据会通过 Base64 编码传输，
        相比原生二进制类型的编码方式，数据体积会增加约 34%。

        不过，如果你的数据符合上述限制，且需要跨语言支持，
        那么默认的 JSON 配置是一个很好的选择。

        更多信息请参见 http://json.org。

        .. note::

            （摘自官方 Python 文档 https://docs.python.org/3.6/library/json.html）
            JSON 中的键始终为 :class:`str` 类型。当字典被转换为 JSON 后，
            所有的键都会被强制转换为字符串。
            因此，当一个字典转换为 JSON 后再反序列化回来，可能会与原始字典不等价。
            例如：``loads(dumps(x)) != x``，如果 x 含有非字符串类型的键。

    pickle -- 如果你不需要支持 Python 以外的语言，
        那么使用 pickle 编码可以支持所有内置的 Python 数据类型（类实例除外），
        在传输二进制数据时体积更小，并且处理速度略快于 JSON。

        更多信息请参阅 :mod:`pickle` 模块。

    yaml -- YAML 与 JSON 特性类似，
        但原生支持更多的数据类型（包括日期、递归引用等）。

        不过，Python 中的 YAML 库普遍比 JSON 库慢很多。

        如果你需要更丰富的数据类型，且仍需跨语言兼容性，
        那么 YAML 可能是一个更合适的选择。

        安装方式如下：

        .. code-block:: console

            $ pip install celery[yaml]

        更多信息请参见 http://yaml.org/

    msgpack -- msgpack 是一种二进制序列化格式，功能类似于 JSON。
        它具有更好的压缩能力，因此在编码和解析速度上通常优于 JSON。

        安装方式如下：

        .. code-block:: console

            $ pip install celery[msgpack]

        更多信息请参见 http://msgpack.org/

    若要使用自定义序列化器，需将其内容类型添加到 :setting:`accept_content` 配置项中。
    默认情况下，仅接受 JSON 格式；
    含有其他内容类型的任务将会被拒绝处理。

    Celery 在发送任务时会按以下优先级决定使用的序列化器：

    1. `serializer` 执行选项；
    2. :attr:`@-Task.serializer` 属性；
    3. :setting:`task_serializer` 设置项。

    示例：为某个任务调用显式指定序列化器：

    .. code-block:: pycon

        >>> add.apply_async((10, 10), serializer='json')


.. tab:: 英文

    Data transferred between clients and workers needs to be serialized,
    so every message in Celery has a ``content_type`` header that
    describes the serialization method used to encode it.

    The default serializer is `JSON`, but you can
    change this using the :setting:`task_serializer` setting,
    or for each individual task, or even per message.

    There's built-in support for `JSON`, :mod:`pickle`, `YAML`
    and ``msgpack``, and you can also add your own custom serializers by registering
    them into the Kombu serializer registry

    .. seealso::

        :ref:`Message Serialization <kombu:guide-serialization>` in the Kombu user
        guide.

    Each option has its advantages and disadvantages.

    json -- JSON is supported in many programming languages, is now
        a standard part of Python (since 2.6), and is fairly fast to decode.

        The primary disadvantage to JSON is that it limits you to the following
        data types: strings, Unicode, floats, Boolean, dictionaries, and lists.
        Decimals and dates are notably missing.

        Binary data will be transferred using Base64 encoding,
        increasing the size of the transferred data by 34% compared to an encoding
        format where native binary types are supported.

        However, if your data fits inside the above constraints and you need
        cross-language support, the default setting of JSON is probably your
        best choice.

        See http://json.org for more information.

        .. note::

            (From Python official docs https://docs.python.org/3.6/library/json.html)
            Keys in key/value pairs of JSON are always of the type :class:`str`. When
            a dictionary is converted into JSON, all the keys of the dictionary are
            coerced to strings. As a result of this, if a dictionary is converted
            into JSON and then back into a dictionary, the dictionary may not equal
            the original one. That is, ``loads(dumps(x)) != x`` if x has non-string
            keys.

    pickle -- If you have no desire to support any language other than
        Python, then using the pickle encoding will gain you the support of
        all built-in Python data types (except class instances), smaller
        messages when sending binary files, and a slight speedup over JSON
        processing.

        See :mod:`pickle` for more information.

    yaml -- YAML has many of the same characteristics as json,
        except that it natively supports more data types (including dates,
        recursive references, etc.).

        However, the Python libraries for YAML are a good bit slower than the
        libraries for JSON.

        If you need a more expressive set of data types and need to maintain
        cross-language compatibility, then YAML may be a better fit than the above.

        To use it, install Celery with:

        .. code-block:: console

            $ pip install celery[yaml]

        See http://yaml.org/ for more information.

    msgpack -- msgpack is a binary serialization format that's closer to JSON
        in features. The format compresses better, so is a faster to parse and
        encode compared to JSON.

        To use it, install Celery with:

        .. code-block:: console

            $ pip install celery[msgpack]

        See http://msgpack.org/ for more information.

    To use a custom serializer you need to add the content type to
    :setting:`accept_content`. By default, only JSON is accepted,
    and tasks containing other content headers are rejected.

    The following order is used to decide the serializer
    used when sending a task:

    1. The `serializer` execution option.
    2. The :attr:`@-Task.serializer` attribute
    3. The :setting:`task_serializer` setting.


    Example setting a custom serializer for a single task invocation:

    .. code-block:: pycon

        >>> add.apply_async((10, 10), serializer='json')

.. _calling-compression:

压缩
===========

Compression

.. tab:: 中文

    Celery 支持使用以下内建压缩方案对消息进行压缩：
    
    * `brotli`
    
      brotli 针对 Web 优化，尤其适用于小型文本文档。它在服务静态内容（如字体和 HTML 页面）时最为高效。
    
      如需使用此压缩算法，请通过以下命令安装 Celery：
    
      .. code-block:: console
    
        $ pip install celery[brotli]
    
    * `bzip2`
    
      bzip2 相较于 gzip 可生成更小的文件，但压缩和解压速度明显慢于 gzip。
    
      要使用该压缩算法，请确保你的 Python 可执行文件已启用 bzip2 支持。
    
      如果你遇到如下的 :class:`ImportError` 错误：
    
      .. code-block:: pycon
    
        >>> import bz2
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        ImportError: No module named 'bz2'
    
      这表示你需要重新编译 Python，使其包含 bzip2 支持。
    
    * `gzip`
    
      gzip 适用于需要较小内存占用的系统，非常适合内存受限的环境。它常用于生成 `.tar.gz` 后缀的文件。
    
      要使用该压缩算法，请确保你的 Python 可执行文件已启用 gzip 支持。
    
      如果你遇到如下的 :class:`ImportError` 错误：
    
      .. code-block:: pycon
    
        >>> import gzip
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        ImportError: No module named 'gzip'
    
      这表示你需要重新编译 Python，使其包含 gzip 支持。
    
    * `lzma`
    
      lzma 提供了较好的压缩比，具有快速的压缩与解压速度，但内存使用量相对较高。
    
      要使用该压缩算法，请确保你的 Python 可执行文件已启用 lzma 支持，并且 Python 版本不低于 3.3。
    
      如果你遇到如下的 :class:`ImportError` 错误：
    
      .. code-block:: pycon
    
        >>> import lzma
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        ImportError: No module named 'lzma'
    
      这表示你需要重新编译 Python，使其包含 lzma 支持。
    
      或者，你也可以通过以下命令安装回移植模块：
    
      .. code-block:: console
    
        $ pip install celery[lzma]
    
    * `zlib`
    
      zlib 是 Deflate 算法的库形式抽象，API 中既支持 gzip 文件格式，也支持轻量级的流格式。它是许多软件系统的关键组成部分——例如 Linux 内核和 Git 版本控制系统。
    
      要使用该压缩算法，请确保你的 Python 可执行文件已启用 zlib 支持。
    
      如果你遇到如下的 :class:`ImportError` 错误：
    
      .. code-block:: pycon
    
        >>> import zlib
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        ImportError: No module named 'zlib'
    
      这表示你需要重新编译 Python，使其包含 zlib 支持。
    
    * `zstd`
    
      zstd 针对实时压缩场景设计，其压缩速度与 zlib 相当甚至更优，同时提供更好的压缩比。它依赖于 Huff0 和 FSE 库提供的高速熵编码阶段。
    
      如需使用该压缩算法，请通过以下命令安装 Celery：
    
      .. code-block:: console
    
        $ pip install celery[zstd]
    
    你也可以创建自定义的压缩方案，并通过 :func:`kombu compression registry <kombu.compression.register>` 将其注册到 Kombu 压缩注册表中。
    
    发送任务时使用的压缩方案按以下顺序确定：
    
    1. `compression` 执行选项。
    2. :attr:`@-Task.compression` 属性。
    3. :setting:`task_compression` 设置项。
    
    如下是调用任务时指定压缩方式的示例：
    
    .. code-block:: pycon
    
        >>> add.apply_async((2, 2), compression='zlib')

.. tab:: 英文

    Celery can compress messages using the following builtin schemes:
    
    - `brotli`
    
      brotli is optimized for the web, in particular small text
      documents. It is most effective for serving static content
      such as fonts and html pages.
    
      To use it, install Celery with:
    
      .. code-block:: console
      
        $ pip install celery[brotli]
    
    - `bzip2`
    
      bzip2 creates smaller files than gzip, but compression and
      decompression speeds are noticeably slower than those of gzip.
      
      To use it, please ensure your Python executable was compiled
      with bzip2 support.
      
      If you get the following :class:`ImportError`:
      
      .. code-block:: pycon
      
          >>> import bz2
          Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          ImportError: No module named 'bz2'
      
      it means that you should recompile your Python version with bzip2 support.
      
    - `gzip`
    
      gzip is suitable for systems that require a small memory footprint,
      making it ideal for systems with limited memory. It is often
      used to generate files with the ".tar.gz" extension.
      
      To use it, please ensure your Python executable was compiled
      with gzip support.
      
      If you get the following :class:`ImportError`:
      
      .. code-block:: pycon
      
          >>> import gzip
          Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          ImportError: No module named 'gzip'
      
      it means that you should recompile your Python version with gzip support.
    
    - `lzma`
    
      lzma provides a good compression ratio and executes with
      fast compression and decompression speeds at the expense
      of higher memory usage.
      
      To use it, please ensure your Python executable was compiled
      with lzma support and that your Python version is 3.3 and above.
      
      If you get the following :class:`ImportError`:
      
      .. code-block:: pycon
      
          >>> import lzma
          Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          ImportError: No module named 'lzma'
      
      it means that you should recompile your Python version with lzma support.
      
      Alternatively, you can also install a backport using:
      
      .. code-block:: console
      
          $ pip install celery[lzma]
    
    - `zlib`
    
      zlib is an abstraction of the Deflate algorithm in library
      form which includes support both for the gzip file format
      and a lightweight stream format in its API. It is a crucial
      component of many software systems - Linux kernel and Git VCS just
      to name a few.
      
      To use it, please ensure your Python executable was compiled
      with zlib support.
      
      If you get the following :class:`ImportError`:
      
      .. code-block:: pycon
      
          >>> import zlib
          Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          ImportError: No module named 'zlib'
      
      it means that you should recompile your Python version with zlib support.
    
    - `zstd`
    
      zstd targets real-time compression scenarios at zlib-level
      and better compression ratios. It's backed by a very fast entropy
      stage, provided by Huff0 and FSE library.
      
      To use it, install Celery with:
      
      .. code-block:: console
      
          $ pip install celery[zstd]
    
    You can also create your own compression schemes and register
    them in the :func:`kombu compression registry <kombu.compression.register>`.
    
    The following order is used to decide the compression scheme
    used when sending a task:

    1. The `compression` execution option.
    2. The :attr:`@-Task.compression` attribute.
    3. The :setting:`task_compression` attribute.
    
    Example specifying the compression used when calling a task::
    
        >>> add.apply_async((2, 2), compression='zlib')
    
.. _calling-connections:
    
连接
===========

Connections

.. tab:: 中文

    .. admonition:: 自动连接池支持

        从 2.3 版本开始，Celery 支持自动连接池，因此你无需手动管理连接和发布者即可重用连接。

        从 2.5 版本开始，连接池默认启用。

        更多信息请参阅 :setting:`broker_pool_limit` 配置项。

    你也可以通过创建发布者手动管理连接：

    .. code-block:: python

        numbers = [(2, 2), (4, 4), (8, 8), (16, 16)]
        results = []
        with add.app.pool.acquire(block=True) as connection:
            with add.get_publisher(connection) as publisher:
                try:
                    for i, j in numbers:
                        res = add.apply_async((i, j), publisher=publisher)
                        results.append(res)
        print([res.get() for res in results])

    不过这个例子使用任务组表达会更加简洁：

    .. code-block:: pycon

        >>> from celery import group

        >>> numbers = [(2, 2), (4, 4), (8, 8), (16, 16)]
        >>> res = group(add.s(i, j) for i, j in numbers).apply_async()

        >>> res.get()
        [4, 8, 16, 32]


.. tab:: 英文

    .. admonition:: Automatic Pool Support

        Since version 2.3 there's support for automatic connection pools,
        so you don't have to manually handle connections and publishers
        to reuse connections.

        The connection pool is enabled by default since version 2.5.

        See the :setting:`broker_pool_limit` setting for more information.

    You can handle the connection manually by creating a
    publisher:

    .. code-block:: python

        numbers = [(2, 2), (4, 4), (8, 8), (16, 16)]
        results = []
        with add.app.pool.acquire(block=True) as connection:
            with add.get_publisher(connection) as publisher:
                try:
                    for i, j in numbers:
                        res = add.apply_async((i, j), publisher=publisher)
                        results.append(res)
        print([res.get() for res in results])


    Though this particular example is much better expressed as a group:

    .. code-block:: pycon

        >>> from celery import group

        >>> numbers = [(2, 2), (4, 4), (8, 8), (16, 16)]
        >>> res = group(add.s(i, j) for i, j in numbers).apply_async()

        >>> res.get()
        [4, 8, 16, 32]

.. _calling-routing:

路由选项
===============

Routing options

.. tab:: 中文

    Celery 可以将任务路由到不同的队列。

    简单的路由（名称 <-> 名称）可以通过 `queue` 选项实现::

        add.apply_async(queue='priority.high')

    然后，你可以通过 worker 的 :option:`-Q <celery worker -Q>` 参数将其绑定到 `priority.high` 队列：

    .. code-block:: console

        $ celery -A proj worker -l INFO -Q celery,priority.high

    .. seealso::

        不推荐在代码中硬编码队列名称，最佳实践是使用配置式路由（:setting:`task_routes`）。

        关于路由的更多信息，请参阅 :ref:`guide-routing`。

.. tab:: 英文

    Celery can route tasks to different queues.

    Simple routing (name <-> name) is accomplished using the ``queue`` option::

        add.apply_async(queue='priority.high')

    You can then assign workers to the ``priority.high`` queue by using
    the workers :option:`-Q <celery worker -Q>` argument:

    .. code-block:: console

        $ celery -A proj worker -l INFO -Q celery,priority.high

    .. seealso::

        Hard-coding queue names in code isn't recommended, the best practice
        is to use configuration routers (:setting:`task_routes`).

        To find out more about routing, please see :ref:`guide-routing`.

.. _calling-results:

结果选项
===============

Results options

.. tab:: 中文

    你可以通过 :setting:`task_ignore_result` 配置项，或使用 `ignore_result` 选项来启用或禁用结果存储：

    .. code-block:: pycon

        >>> result = add.apply_async((1, 2), ignore_result=True)
        >>> result.get()
        >>> None

        >>> # 不忽略结果（默认行为）

        ...

        >>> result = add.apply_async((1, 2), ignore_result=False)
        >>> result.get()
        >>> 3

    如果你希望在结果后端中存储关于任务的额外元数据，可以将 :setting:`result_extended` 设置为 `True`。

    .. seealso::

        有关任务的更多信息，请参阅 :ref:`guide-tasks`。

.. tab:: 英文

    You can enable or disable result storage using the :setting:`task_ignore_result`
    setting or by using the ``ignore_result`` option:

    .. code-block:: pycon

        >>> result = add.apply_async((1, 2), ignore_result=True)
        >>> result.get()
        None

        >>> # Do not ignore result (default)
        ...
        >>> result = add.apply_async((1, 2), ignore_result=False)
        >>> result.get()
        3

    If you'd like to store additional metadata about the task in the result backend
    set the :setting:`result_extended` setting to ``True``.

    .. seealso::

        For more information on tasks, please see :ref:`guide-tasks`.

高级选项
----------------

Advanced Options

.. tab:: 中文

    以下选项适用于希望充分利用 AMQP 路由能力的高级用户。如有兴趣，请阅读 :ref:`routing guide <guide-routing>`。
    
    * exchange
    
      要将消息发送到的交换器名称（或一个 :class:`kombu.entity.Exchange` 实例）。
    
    * routing_key
    
      用于决定路由的路由键。
    
    * priority
    
      范围为 `0` 到 `255` 的整数，其中 `255` 表示最高优先级。
    
      支持此选项的系统有：RabbitMQ、Redis（Redis 中优先级相反，`0` 表示最高）。

.. tab:: 英文

    These options are for advanced users who want to take use of
    AMQP's full routing capabilities. Interested parties may read the
    :ref:`routing guide <guide-routing>`.
    
    - exchange
    
      Name of exchange (or a :class:`kombu.entity.Exchange`) to
      send the message to.
    
    - routing_key
    
      Routing key used to determine.
    
    - priority
    
      A number between `0` and `255`, where `255` is the highest priority.
    
      Supported by: RabbitMQ, Redis (priority reversed, 0 is highest).
    