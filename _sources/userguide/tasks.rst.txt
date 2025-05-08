.. _guide-tasks:

=====================================================================
任务/Tasks
=====================================================================

Tasks
    
.. tab:: 中文
    
    任务是 Celery 应用的构建模块。
    
    任务是一个类，可以由任何可调用对象创建。它同时扮演双重角色：
    既定义了调用任务时发生的行为（发送消息），也定义了 worker 接收到该消息后发生的行为。
    
    每个任务类都有一个唯一的名称，该名称会在消息中被引用，
    以便 worker 能够找到要执行的正确函数。
    
    任务消息在被 worker :term:`确认 <acknowledged>` 之前不会从队列中移除。
    worker 可以提前预留多个消息，即使 worker 被杀死（如电源故障或其他原因），
    消息也会被重新投递给另一个 worker。
    
    理想情况下，任务函数应具备 :term:`幂等性 <idempotent>`：即
    即使以相同参数调用多次，也不会产生非预期的副作用。
    由于 worker 无法检测你的任务是否幂等，默认行为是在任务执行前
    立即确认消息，以避免已经开始执行的任务被再次执行。
    
    如果你的任务是幂等的，可以设置 :attr:`~Task.acks_late` 选项，
    使 worker 在任务返回 *之后* 再确认消息。另见 FAQ 条目 :ref:`faq-acks_late-vs-retry`。
    
    请注意，即使启用了 :attr:`~Task.acks_late`，如果执行任务的子进程终止
    （无论是任务调用了 :func:`sys.exit`，还是收到信号），worker 仍然会确认该消息。
    此行为是有意为之，原因如下：
    
    #. 我们不希望重新执行那些导致内核发送 :sig:`SIGSEGV` （段错误）或类似信号的任务。
    #. 我们假设系统管理员主动杀死任务，是不希望它自动重启。
    #. 占用大量内存的任务可能会触发内核的 OOM 杀手（Out-Of-Memory Killer），
       同样的情况可能再次发生。
    #. 若任务在重新投递时总是失败，可能会造成高频消息循环，进而拖垮系统。
    
    如果你确实希望在上述情形下重新投递任务，可以考虑启用
    :setting:`task_reject_on_worker_lost` 配置项。
    
    .. warning::
    
        阻塞任务若无限期运行，最终可能导致 worker 实例无法处理其他任务。
    
        如果你的任务涉及 I/O 操作，务必为这些操作添加超时，
        比如使用 :pypi:`requests` 库进行 Web 请求时添加超时参数：
    
        .. code-block:: python
    
            connect_timeout, read_timeout = 5.0, 30.0
            response = requests.get(URL, timeout=(connect_timeout, read_timeout))
    
        :ref:`时间限制 <worker-time-limits>` 是确保所有任务及时返回的便捷手段，
        但时间限制触发时会强制杀死进程，因此应仅用于那些尚未配置手动超时的场景。
    
        在早期版本中，默认的 prefork 池调度器对长时间运行的任务不太友好，
        因此如果你有运行数分钟或数小时的任务，建议在启动 :program:`celery worker` 时
        启用命令行选项 :option:`-Ofair <celery worker -O>`。
        不过，从 4.0 版本起，-Ofair 已成为默认调度策略。
        参见 :ref:`optimizing-prefetch-limit` 以获取更多信息，
        若需获得最佳性能，建议将长任务与短任务路由到专用的 worker 上
        （参见 :ref:`routing-automatic`）。
    
        如果你的 worker 出现挂起现象，请先调查哪些任务正在运行再提交问题，
        因为挂起通常是某些任务在执行网络操作时阻塞所致。


.. tab:: 英文

    Tasks are the building blocks of Celery applications.
    
    A task is a class that can be created out of any callable. It performs
    dual roles in that it defines both what happens when a task is
    called (sends a message), and what happens when a worker receives that message.
    
    Every task class has a unique name, and this name is referenced in messages
    so the worker can find the right function to execute.
    
    A task message is not removed from the queue
    until that message has been :term:`acknowledged` by a worker. A worker can reserve
    many messages in advance and even if the worker is killed -- by power failure
    or some other reason -- the message will be redelivered to another worker.
    
    Ideally task functions should be :term:`idempotent`: meaning
    the function won't cause unintended effects even if called
    multiple times with the same arguments.
    Since the worker cannot detect if your tasks are idempotent, the default
    behavior is to acknowledge the message in advance, just before it's executed,
    so that a task invocation that already started is never executed again.
    
    If your task is idempotent you can set the :attr:`~Task.acks_late` option
    to have the worker acknowledge the message *after* the task returns
    instead. See also the FAQ entry :ref:`faq-acks_late-vs-retry`.
    
    Note that the worker will acknowledge the message if the child process executing
    the task is terminated (either by the task calling :func:`sys.exit`, or by signal)
    even when :attr:`~Task.acks_late` is enabled.  This behavior is intentional
    as...
    
    #. We don't want to rerun tasks that forces the kernel to send
       a :sig:`SIGSEGV` (segmentation fault) or similar signals to the process.
    #. We assume that a system administrator deliberately killing the task
       does not want it to automatically restart.
    #. A task that allocates too much memory is in danger of triggering the kernel
       OOM killer, the same may happen again.
    #. A task that always fails when redelivered may cause a high-frequency
       message loop taking down the system.
    
    If you really want a task to be redelivered in these scenarios you should
    consider enabling the :setting:`task_reject_on_worker_lost` setting.
    
    .. warning::
    
        A task that blocks indefinitely may eventually stop the worker instance
        from doing any other work.
    
        If your task does I/O then make sure you add timeouts to these operations,
        like adding a timeout to a web request using the :pypi:`requests` library:
    
        .. code-block:: python
    
            connect_timeout, read_timeout = 5.0, 30.0
            response = requests.get(URL, timeout=(connect_timeout, read_timeout))
    
        :ref:`Time limits <worker-time-limits>` are convenient for making sure all
        tasks return in a timely manner, but a time limit event will actually kill
        the process by force so only use them to detect cases where you haven't
        used manual timeouts yet.
    
        In previous versions, the default prefork pool scheduler was not friendly
        to long-running tasks, so if you had tasks that ran for minutes/hours, it
        was advised to enable the :option:`-Ofair <celery worker -O>` command-line
        argument to the :program:`celery worker`. However, as of version 4.0,
        -Ofair is now the default scheduling strategy. See :ref:`optimizing-prefetch-limit`
        for more information, and for the best performance route long-running and
        short-running tasks to dedicated workers (:ref:`routing-automatic`).
    
        If your worker hangs then please investigate what tasks are running
        before submitting an issue, as most likely the hanging is caused
        by one or more tasks hanging on a network operation.

.. _task-basics:

基础知识
======

Basics

.. tab:: 中文

    你可以使用 :meth:`@task` 装饰器轻松地将任何可调用对象创建为一个任务：

    .. code-block:: python

        from .models import User

        @app.task
        def create_user(username, password):
            User.objects.create(username=username, password=password)

    任务还可以设置多个 :ref:`选项 <task-options>`，
    这些选项可以作为参数传递给装饰器：

    .. code-block:: python

        @app.task(serializer='json')
        def create_user(username, password):
            User.objects.create(username=username, password=password)

.. tab:: 英文

    You can easily create a task from any callable by using
    the :meth:`@task` decorator:

    .. code-block:: python

        from .models import User

        @app.task
        def create_user(username, password):
            User.objects.create(username=username, password=password)


    There are also many :ref:`options <task-options>` that can be set for the task,
    these can be specified as arguments to the decorator:

    .. code-block:: python

        @app.task(serializer='json')
        def create_user(username, password):
            User.objects.create(username=username, password=password)


如何导入任务装饰器？
-----------------------------------

How do I import the task decorator?

.. tab:: 中文

    任务装饰器是在你的 :class:`@Celery` 应用实例上可用的，
    如果你还不了解它，请先阅读 :ref:`first-steps`。

    如果你在使用 Django（参见 :ref:`django-first-steps`），
    或者你是一个库的作者，那你很可能会想使用 :func:`@shared_task` 装饰器：

    .. code-block:: python

        from celery import shared_task

        @shared_task
        def add(x, y):
            return x + y

.. tab:: 英文

    The task decorator is available on your :class:`@Celery` application instance,
    if you don't know what this is then please read :ref:`first-steps`.

    If you're using Django (see :ref:`django-first-steps`), or you're the author
    of a library then you probably want to use the :func:`@shared_task` decorator:

    .. code-block:: python

        from celery import shared_task

        @shared_task
        def add(x, y):
            return x + y

多个装饰器
-------------------

Multiple decorators

.. tab:: 中文

    当你将多个装饰器与任务装饰器组合使用时，
    必须确保 ``task`` 装饰器是最后应用的
    （奇怪的是，在 Python 中这意味着它必须出现在列表的最上方）：

    .. code-block:: python

        @app.task
        @decorator2
        @decorator1
        def add(x, y):
            return x + y

.. tab:: 英文

    When using multiple decorators in combination with the task
    decorator you must make sure that the `task`
    decorator is applied last (oddly, in Python this means it must
    be first in the list):

    .. code-block:: python

        @app.task
        @decorator2
        @decorator1
        def add(x, y):
            return x + y

绑定任务
-----------

Bound tasks

.. tab:: 中文

    一个任务被绑定（bound）意味着该任务的第一个参数
    将始终是任务实例本身（ ``self`` ），
    就像 Python 中绑定方法的行为一样：

    .. code-block:: python

        logger = get_task_logger(__name__)

        @app.task(bind=True)
        def add(self, x, y):
            logger.info(self.request.id)

    绑定任务在执行重试（通过 :meth:`Task.retry() <@Task.retry>`）、
    访问当前任务请求信息，以及你为自定义任务基类添加其他功能时是必须的。

.. tab:: 英文

    A task being bound means the first argument to the task will always
    be the task instance (``self``), just like Python bound methods:

    .. code-block:: python

        logger = get_task_logger(__name__)

        @app.task(bind=True)
        def add(self, x, y):
            logger.info(self.request.id)

    Bound tasks are needed for retries (using :meth:`Task.retry() <@Task.retry>`),
    for accessing information about the current task request, and for any
    additional functionality you add to custom task base classes.

任务继承
----------------

Task inheritance

.. tab:: 中文

    ``base`` 参数用于指定任务所继承的基类：

    .. code-block:: python

        import celery

        class MyTask(celery.Task):

            def on_failure(self, exc, task_id, args, kwargs, einfo):
                print('{0!r} failed: {1!r}'.format(task_id, exc))

        @app.task(base=MyTask)
        def add(x, y):
            raise KeyError()

.. tab:: 英文

    The ``base`` argument to the task decorator specifies the base class of the task:

    .. code-block:: python

        import celery

        class MyTask(celery.Task):

            def on_failure(self, exc, task_id, args, kwargs, einfo):
                print('{0!r} failed: {1!r}'.format(task_id, exc))

        @app.task(base=MyTask)
        def add(x, y):
            raise KeyError()

.. _task-names:

名称
=====

Names

.. tab:: 中文

    每个任务都必须拥有一个唯一的名称。
    
    如果没有显式指定名称，任务装饰器会自动为你生成一个名称，
    该名称基于以下两个因素：1）定义任务的模块名，2）任务函数的名称。
    
    显式指定任务名称的示例：
    
    .. code-block:: pycon
    
        >>> @app.task(name='sum-of-two-numbers')
        >>> def add(x, y):
        ...     return x + y
    
        >>> add.name
        'sum-of-two-numbers'
    
    一个推荐的最佳实践是使用模块名作为命名空间，
    这样可以避免任务名称在多个模块之间发生冲突：
    
    .. code-block:: pycon
    
        >>> @app.task(name='tasks.add')
        >>> def add(x, y):
        ...     return x + y
    
    你可以通过查看任务的 ``.name`` 属性来获取它的名称：
    
    .. code-block:: pycon
    
        >>> add.name
        'tasks.add'
    
    这里指定的名称（``tasks.add``）恰好是任务定义在名为
    :file:`tasks.py` 的模块中时会自动生成的名称：
    
    :file:`tasks.py`:
    
    .. code-block:: python
    
        @app.task
        def add(x, y):
            return x + y
    
    .. code-block:: pycon
    
        >>> from tasks import add
        >>> add.name
        'tasks.add'
    
    .. note::
    
       你可以在 worker 中使用 `inspect` 命令查看所有已注册任务的名称。
       参见用户指南中 :ref:`monitoring-control` 部分的 `inspect registered` 命令。

.. tab:: 英文

    Every task must have a unique name.
    
    If no explicit name is provided the task decorator will generate one for you,
    and this name will be based on 1) the module the task is defined in, and 2)
    the name of the task function.
    
    Example setting explicit name:
    
    .. code-block:: pycon
    
        >>> @app.task(name='sum-of-two-numbers')
        >>> def add(x, y):
        ...     return x + y
    
        >>> add.name
        'sum-of-two-numbers'
    
    A best practice is to use the module name as a name-space,
    this way names won't collide if there's already a task with that name
    defined in another module.
    
    .. code-block:: pycon
    
        >>> @app.task(name='tasks.add')
        >>> def add(x, y):
        ...     return x + y
    
    You can tell the name of the task by investigating its ``.name`` attribute:
    
    .. code-block:: pycon
    
        >>> add.name
        'tasks.add'
    
    The name we specified here (``tasks.add``) is exactly the name that would've
    been automatically generated for us if the task was defined in a module
    named :file:`tasks.py`:
    
    :file:`tasks.py`:
    
    .. code-block:: python
    
        @app.task
        def add(x, y):
            return x + y
    
    .. code-block:: pycon
    
        >>> from tasks import add
        >>> add.name
        'tasks.add'
    
    .. note::
    
       You can use the `inspect` command in a worker to view the names of
       all registered tasks. See the `inspect registered` command in the
       :ref:`monitoring-control` section of the User Guide.

.. _task-name-generator-info:

更改自动命名行为
--------------------------------------

Changing the automatic naming behavior

    .. versionadded:: 4.0

.. tab:: 中文

    在某些情况下，默认的自动命名方式并不适用。
    设想你有许多任务分别定义在多个模块中::
    
        project/
               /__init__.py
               /celery.py
               /moduleA/
                       /__init__.py
                       /tasks.py
               /moduleB/
                       /__init__.py
                       /tasks.py
    
    使用默认自动命名时，每个任务会生成如下名称：
    `moduleA.tasks.taskA`、`moduleA.tasks.taskB`、`moduleB.tasks.test`，等等。
    你可能不希望所有任务名称中都包含 `tasks`。
    如上所述，你可以显式为所有任务指定名称，
    或者你也可以通过重写 :meth:`@gen_task_name` 来更改自动命名行为。
    继续以上示例，`celery.py` 中可能包含：
    
    .. code-block:: python
    
        from celery import Celery
    
        class MyCelery(Celery):
    
            def gen_task_name(self, name, module):
                if module.endswith('.tasks'):
                    module = module[:-6]
                return super().gen_task_name(name, module)
    
        app = MyCelery('main')
    
    这样，每个任务将拥有名称如 `moduleA.taskA`、`moduleA.taskB` 和 `moduleB.test`。
    
    .. warning::
    
        请确保你的 :meth:`@gen_task_name` 是纯函数：
        即对于相同的输入，必须始终返回相同的输出。

.. tab:: 英文
    
    There are some cases when the default automatic naming isn't suitable.
    Consider having many tasks within many different modules::
    
        project/
               /__init__.py
               /celery.py
               /moduleA/
                       /__init__.py
                       /tasks.py
               /moduleB/
                       /__init__.py
                       /tasks.py
    
    Using the default automatic naming, each task will have a generated name
    like `moduleA.tasks.taskA`, `moduleA.tasks.taskB`, `moduleB.tasks.test`,
    and so on. You may want to get rid of having `tasks` in all task names.
    As pointed above, you can explicitly give names for all tasks, or you
    can change the automatic naming behavior by overriding
    :meth:`@gen_task_name`. Continuing with the example, `celery.py`
    may contain:
    
    .. code-block:: python
    
        from celery import Celery
    
        class MyCelery(Celery):
    
            def gen_task_name(self, name, module):
                if module.endswith('.tasks'):
                    module = module[:-6]
                return super().gen_task_name(name, module)
    
        app = MyCelery('main')
    
    So each task will have a name like `moduleA.taskA`, `moduleA.taskB` and
    `moduleB.test`.
    
    .. warning::
    
        Make sure that your :meth:`@gen_task_name` is a pure function: meaning
        that for the same input it must always return the same output.

.. _task-request-info:

任务请求
============

Task Request

.. tab:: 中文

    :attr:`Task.request <@Task.request>` 包含与当前执行的任务相关的信息与状态。
    
    该请求对象定义了以下属性：
    
    :id: 当前执行任务的唯一 ID。
    
    :group: 如果任务属于某个 :ref:`group <canvas-group>`，则为该组的唯一 ID。
    
    :chord: 如果任务是某个 chord 的一部分（处于 header 中），则为该 chord 的唯一 ID。
    
    :correlation_id: 用于去重等用途的自定义 ID。
    
    :args: 位置参数。
    
    :kwargs: 关键字参数。
    
    :origin: 发送该任务的主机名。
    
    :retries: 当前任务已重试的次数，整数，初始值为 `0`。
    
    :is_eager: 若任务是在客户端本地执行而非由 worker 执行，则为 :const:`True`。
    
    :eta: 任务的原始 ETA（若有）。为 UTC 时间（受 :setting:`enable_utc` 设置影响）。
    
    :expires: 任务的原始过期时间（若有）。为 UTC 时间（受 :setting:`enable_utc` 设置影响）。
    
    :hostname: 正在执行该任务的 worker 实例的节点名称。
    
    :delivery_info: 其他消息投递信息。为一个映射，包含用于投递该任务的 exchange 和 routing key。
                    例如 :meth:`Task.retry() <@Task.retry>` 使用该信息将任务重新发送到相同的队列。
                    该字典中的键是否可用取决于所使用的消息代理。
    
    :reply-to: 回复应发送到的队列名称（例如用于 RPC 结果后端）。
    
    :called_directly: 如果任务不是由 worker 执行的，此标志将被设置为 True。
    
    :timelimit: 当前任务的 ``(soft, hard)`` 时间限制（如果有）。
    
    :callbacks: 任务成功返回时要调用的签名（signature）列表。
    
    :errbacks: 任务失败时要调用的签名列表。
    
    :utc: 若调用者启用了 UTC，则为 True（参见 :setting:`enable_utc`）。
    
    .. versionadded:: 3.1
    
    :headers: 附带此任务消息发送的消息头映射（可能为 :const:`None`）。
    
    :reply_to: 要将回复发送到的位置（队列名称）。
    
    :correlation_id: 通常与任务 ID 相同，在 amqp 中常用于追踪回复对应的请求。
    
    .. versionadded:: 4.0
    
    :root_id: 当前任务所属工作流中的第一个任务的唯一 ID（如果存在）。
    
    :parent_id: 调用当前任务的父任务的唯一 ID（如果存在）。
    
    :chain: 构成任务链的任务列表（反转顺序，如果存在）。
            该列表中的最后一个元素是当前任务完成后要接着执行的任务。
            如果使用的是任务协议的第一版，链式任务将存在于 ``request.callbacks`` 中。
    
    .. versionadded:: 5.2
    
    :properties: 接收该任务消息时附带的消息属性映射（可能为 :const:`None` 或 :const:`{}`）
    
    :replaced_task_nesting: 当前任务被替换的嵌套层级数（如果有，可能为 :const:`0`）


.. tab:: 英文

    :attr:`Task.request <@Task.request>` contains information and state
    related to the currently executing task.
    
    The request defines the following attributes:
    
    :id: The unique id of the executing task.
    
    :group: The unique id of the task's :ref:`group <canvas-group>`, if this task is a member.
    
    :chord: The unique id of the chord this task belongs to (if the task
            is part of the header).
    
    :correlation_id: Custom ID used for things like de-duplication.
    
    :args: Positional arguments.
    
    :kwargs: Keyword arguments.
    
    :origin: Name of host that sent this task.
    
    :retries: How many times the current task has been retried.
              An integer starting at `0`.
    
    :is_eager: Set to :const:`True` if the task is executed locally in
               the client, not by a worker.
    
    :eta: The original ETA of the task (if any).
          This is in UTC time (depending on the :setting:`enable_utc`
          setting).
    
    :expires: The original expiry time of the task (if any).
              This is in UTC time (depending on the :setting:`enable_utc`
              setting).
    
    :hostname: Node name of the worker instance executing the task.
    
    :delivery_info: Additional message delivery information. This is a mapping
                    containing the exchange and routing key used to deliver this
                    task. Used by for example :meth:`Task.retry() <@Task.retry>`
                    to resend the task to the same destination queue.
                    Availability of keys in this dict depends on the
                    message broker used.
    
    :reply-to: Name of queue to send replies back to (used with RPC result
               backend for example).
    
    :called_directly: This flag is set to true if the task wasn't
                      executed by the worker.
    
    :timelimit: A tuple of the current ``(soft, hard)`` time limits active for
                this task (if any).
    
    :callbacks: A list of signatures to be called if this task returns successfully.
    
    :errbacks: A list of signatures to be called if this task fails.
    
    :utc: Set to true the caller has UTC enabled (:setting:`enable_utc`).
    
    
    .. versionadded:: 3.1
    
    :headers:  Mapping of message headers sent with this task message
               (may be :const:`None`).
    
    :reply_to:  Where to send reply to (queue name).
    
    :correlation_id: Usually the same as the task id, often used in amqp
                     to keep track of what a reply is for.
    
    .. versionadded:: 4.0
    
    :root_id: The unique id of the first task in the workflow this task
              is part of (if any).
    
    :parent_id: The unique id of the task that called this task (if any).
    
    :chain: Reversed list of tasks that form a chain (if any).
            The last item in this list will be the next task to succeed the
            current task.  If using version one of the task protocol the chain
            tasks will be in ``request.callbacks`` instead.
    
    .. versionadded:: 5.2
    
    :properties: Mapping of message properties received with this task message
                 (may be :const:`None` or :const:`{}`)
    
    :replaced_task_nesting: How many times the task was replaced, if at all.
                            (may be :const:`0`)

示例
-------

Example

.. tab:: 中文

    一个访问上下文信息的任务示例如下：

    .. code-block:: python

        @app.task(bind=True)
        def dump_context(self, x, y):
            print('Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.format(
                    self.request))

    `bind` 参数表示该函数将成为一个“绑定方法”，因此你可以访问任务类型实例上的属性和方法。

.. tab:: 英文

    An example task accessing information in the context is:

    .. code-block:: python

        @app.task(bind=True)
        def dump_context(self, x, y):
            print('Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.format(
                    self.request))


    The ``bind`` argument means that the function will be a "bound method" so
    that you can access attributes and methods on the task type instance.

.. _task-logging:

日志记录
=======

Logging

.. tab:: 中文

    Worker 会自动为你配置日志记录，当然你也可以手动配置。

    Celery 提供了一个名为 "celery.task" 的特殊日志记录器，你可以继承该日志记录器来自动在日志中包含任务名和唯一 ID。

    最佳实践是在模块顶部为所有任务创建一个通用日志记录器：

    .. code-block:: python

        from celery.utils.log import get_task_logger

        logger = get_task_logger(__name__)

        @app.task
        def add(x, y):
            logger.info('Adding {0} + {1}'.format(x, y))
            return x + y

    Celery 使用的是标准的 Python 日志库，相关文档可参见 :mod:`这里 <logging>`。

    你也可以使用 :func:`print`，因为写入标准输出/错误的内容会被重定向到日志系统（你可以禁用此行为，参见  :setting:`worker_redirect_stdouts`）。

    .. note::

        如果你在任务或任务模块中创建日志记录器实例，worker 不会更新输出重定向设置。

        如果你希望将 ``sys.stdout`` 和 ``sys.stderr`` 重定向到自定义日志记录器，你需要手动启用，例如：

        .. code-block:: python

            import sys

            logger = get_task_logger(__name__)

            @app.task(bind=True)
            def add(self, x, y):
                old_outs = sys.stdout, sys.stderr
                rlevel = self.app.conf.worker_redirect_stdouts_level
                try:
                    self.app.log.redirect_stdouts_to_logger(logger, rlevel)
                    print('Adding {0} + {1}'.format(x, y))
                    return x + y
                finally:
                    sys.stdout, sys.stderr = old_outs

    .. note::

        如果你需要的某个 Celery 日志记录器没有输出日志，应该检查该记录器是否正确传播（propagate）。以下示例启用了 "celery.app.trace"，以便输出 "succeeded in" 之类的日志：

        .. code-block:: python

            import celery
            import logging

            @celery.signals.after_setup_logger.connect
            def on_after_setup_logger(**kwargs):
                logger = logging.getLogger('celery')
                logger.propagate = True
                logger = logging.getLogger('celery.app.trace')
                logger.propagate = True

    .. note::

        如果你希望完全禁用 Celery 的日志配置，可以使用 :signal:`setup_logging` 信号：

        .. code-block:: python

            import celery

            @celery.signals.setup_logging.connect
            def on_setup_logging(**kwargs):
                pass

.. tab:: 英文

    The worker will automatically set up logging for you, or you can
    configure logging manually.

    A special logger is available named "celery.task", you can inherit
    from this logger to automatically get the task name and unique id as part
    of the logs.

    The best practice is to create a common logger
    for all of your tasks at the top of your module:

    .. code-block:: python

        from celery.utils.log import get_task_logger

        logger = get_task_logger(__name__)

        @app.task
        def add(x, y):
            logger.info('Adding {0} + {1}'.format(x, y))
            return x + y

    Celery uses the standard Python logger library,
    and the documentation can be found :mod:`here <logging>`.

    You can also use :func:`print`, as anything written to standard
    out/-err will be redirected to the logging system (you can disable this,
    see :setting:`worker_redirect_stdouts`).

    .. note::

        The worker won't update the redirection if you create a logger instance
        somewhere in your task or task module.

        If you want to redirect ``sys.stdout`` and ``sys.stderr`` to a custom
        logger you have to enable this manually, for example:

        .. code-block:: python

            import sys

            logger = get_task_logger(__name__)

            @app.task(bind=True)
            def add(self, x, y):
                old_outs = sys.stdout, sys.stderr
                rlevel = self.app.conf.worker_redirect_stdouts_level
                try:
                    self.app.log.redirect_stdouts_to_logger(logger, rlevel)
                    print('Adding {0} + {1}'.format(x, y))
                    return x + y
                finally:
                    sys.stdout, sys.stderr = old_outs


    .. note::

        If a specific Celery logger you need is not emitting logs, you should
        check that the logger is propagating properly. In this example
        "celery.app.trace" is enabled so that "succeeded in" logs are emitted:

        .. code-block:: python


            import celery
            import logging

            @celery.signals.after_setup_logger.connect
            def on_after_setup_logger(**kwargs):
                logger = logging.getLogger('celery')
                logger.propagate = True
                logger = logging.getLogger('celery.app.trace')
                logger.propagate = True


    .. note::

        If you want to completely disable Celery logging configuration,
        use the :signal:`setup_logging` signal:

        .. code-block:: python

            import celery

            @celery.signals.setup_logging.connect
            def on_setup_logging(**kwargs):
                pass


.. _task-argument-checking:

参数检查
-----------------

Argument checking

.. tab:: 中文

    .. versionadded:: 4.0

    Celery 在你调用任务时会验证传入的参数，就像 Python 调用普通函数一样：

    .. code-block:: pycon

        >>> @app.task
        ... def add(x, y):
        ...     return x + y

        # 使用两个参数调用任务是可行的：
        >>> add.delay(8, 8)
        <AsyncResult: f59d71ca-1549-43e0-be41-4e8821a83c0c>

        # 仅使用一个参数调用任务则会报错：
        >>> add.delay(8)
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "celery/app/task.py", line 376, in delay
            return self.apply_async(args, kwargs)
        File "celery/app/task.py", line 485, in apply_async
            check_arguments(*(args or ()), **(kwargs or {}))
        TypeError: add() takes exactly 2 arguments (1 given)

    你可以通过将任务的 :attr:`~@Task.typing` 属性设置为 :const:`False` 来禁用参数检查：

    .. code-block:: pycon

        >>> @app.task(typing=False)
        ... def add(x, y):
        ...     return x + y

        # 在本地调用有效，但当 worker 接收到任务时会报错。
        >>> add.delay(8)
        <AsyncResult: f59d71ca-1549-43e0-be41-4e8821a83c0c>

.. tab:: 英文

    .. versionadded:: 4.0

    Celery will verify the arguments passed when you call the task, just
    like Python does when calling a normal function:

    .. code-block:: pycon

        >>> @app.task
        ... def add(x, y):
        ...     return x + y

        # Calling the task with two arguments works:
        >>> add.delay(8, 8)
        <AsyncResult: f59d71ca-1549-43e0-be41-4e8821a83c0c>

        # Calling the task with only one argument fails:
        >>> add.delay(8)
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "celery/app/task.py", line 376, in delay
            return self.apply_async(args, kwargs)
        File "celery/app/task.py", line 485, in apply_async
            check_arguments(*(args or ()), **(kwargs or {}))
        TypeError: add() takes exactly 2 arguments (1 given)

    You can disable the argument checking for any task by setting its
    :attr:`~@Task.typing` attribute to :const:`False`:

    .. code-block:: pycon

        >>> @app.task(typing=False)
        ... def add(x, y):
        ...     return x + y

        # Works locally, but the worker receiving the task will raise an error.
        >>> add.delay(8)
        <AsyncResult: f59d71ca-1549-43e0-be41-4e8821a83c0c>

.. _task-hiding-sensitive-information:

在参数中隐藏敏感信息
-----------------------------------------

Hiding sensitive information in arguments

.. tab:: 中文

    .. versionadded:: 4.0

    当使用 :setting:`task_protocol` 为 2 或更高版本时（自 4.0 起默认），你可以通过 `argsrepr` 和 `kwargsrepr` 调用参数来自定义在日志和监控事件中位置参数和关键字参数的显示方式：

    .. code-block:: pycon

        >>> add.apply_async((2, 3), argsrepr='(<secret-x>, <secret-y>)')

        >>> charge.s(account, card='1234 5678 1234 5678').set(
        ...     kwargsrepr=repr({'card': '**** **** **** 5678'})
        ... ).delay()

    .. warning::

        如果有人能够从消息代理（broker）读取任务消息，或以其他方式拦截消息，那么敏感信息仍然是可访问的。

        因此，如果你的消息中包含敏感信息，建议对其进行加密；以信用卡号为例，实际号码应加密存储在安全存储中，并在任务中检索并解密。

.. tab:: 英文

    .. versionadded:: 4.0

    When using :setting:`task_protocol` 2 or higher (default since 4.0), you can
    override how positional arguments and keyword arguments are represented in logs
    and monitoring events using the ``argsrepr`` and ``kwargsrepr`` calling
    arguments:

    .. code-block:: pycon

        >>> add.apply_async((2, 3), argsrepr='(<secret-x>, <secret-y>)')

        >>> charge.s(account, card='1234 5678 1234 5678').set(
        ...     kwargsrepr=repr({'card': '**** **** **** 5678'})
        ... ).delay()


    .. warning::

        Sensitive information will still be accessible to anyone able
        to read your task message from the broker, or otherwise able intercept it.

        For this reason you should probably encrypt your message if it contains
        sensitive information, or in this example with a credit card number
        the actual number could be stored encrypted in a secure store that you retrieve
        and decrypt in the task itself.

.. _task-retry:

重试
========

Retrying

.. tab:: 中文

    可以使用 :meth:`Task.retry() <@Task.retry>` 方法重新执行任务，例如在遇到可恢复的错误时。
    
    调用 `retry` 时会发送一条新消息，使用相同的 task-id，并确保该消息被投递到与原始任务相同的队列中。
    
    任务重试也会被记录为一种任务状态，因此你可以通过结果实例跟踪任务进度（参见 :ref:`task-states`）。
    
    下面是一个使用 `retry` 的示例：
    
    .. code-block:: python
    
        @app.task(bind=True)
        def send_twitter_status(self, oauth, tweet):
            try:
                twitter = Twitter(oauth)
                twitter.update_status(tweet)
            except (Twitter.FailWhaleError, Twitter.LoginError) as exc:
                raise self.retry(exc=exc)
    
    .. note::
    
        :meth:`Task.retry() <@Task.retry>` 的调用会抛出一个异常，因此其后的代码不会被执行。该异常为 :exc:`~@Retry`，它不会被视为错误，而是一个“半谓词”，表示该任务应被重试，以便在启用了结果后端时记录正确的状态。
    
        这是正常行为，除非将 ``throw`` 参数设置为 :const:`False`，否则总会发生此行为。
    
    `task` 装饰器中的 `bind` 参数会使任务获得对 `self` （任务类型实例）的访问权限。
    
    `exc` 参数用于传递异常信息，该信息会被用于日志记录和存储任务结果。
    异常及其回溯信息将在任务状态中可用（如果启用了结果后端）。
    
    如果任务定义了 `max_retries` 值，在超过最大重试次数时会重新抛出当前异常，但在以下两种情况下不会抛出原始异常：
    
    * 未提供 `exc` 参数：
    
      在这种情况下，将抛出 :exc:`~@MaxRetriesExceededError` 异常。
    
    * 当前没有异常可用：
    
      如果没有原始异常可以重新抛出，则会使用 `exc` 参数作为替代，例如：
    
      .. code-block:: python
        
          self.retry(exc=Twitter.LoginError())
    
      将会抛出提供的 `exc` 参数所指定的异常。

.. tab:: 英文

    :meth:`Task.retry() <@Task.retry>` can be used to re-execute the task,
    for example in the event of recoverable errors.

    When you call ``retry`` it'll send a new message, using the same
    task-id, and it'll take care to make sure the message is delivered
    to the same queue as the originating task.

    When a task is retried this is also recorded as a task state,
    so that you can track the progress of the task using the result
    instance (see :ref:`task-states`).

    Here's an example using ``retry``:

    .. code-block:: python

        @app.task(bind=True)
        def send_twitter_status(self, oauth, tweet):
            try:
                twitter = Twitter(oauth)
                twitter.update_status(tweet)
            except (Twitter.FailWhaleError, Twitter.LoginError) as exc:
                raise self.retry(exc=exc)

    .. note::

        The :meth:`Task.retry() <@Task.retry>` call will raise an exception so any
        code after the retry won't be reached. This is the :exc:`~@Retry`
        exception, it isn't handled as an error but rather as a semi-predicate
        to signify to the worker that the task is to be retried,
        so that it can store the correct state when a result backend is enabled.

        This is normal operation and always happens unless the
        ``throw`` argument to retry is set to :const:`False`.

    The bind argument to the task decorator will give access to ``self`` (the
    task type instance).

    The ``exc`` argument is used to pass exception information that's
    used in logs, and when storing task results.
    Both the exception and the traceback will
    be available in the task state (if a result backend is enabled).

    If the task has a ``max_retries`` value the current exception
    will be re-raised if the max number of retries has been exceeded,
    but this won't happen if:

    - An ``exc`` argument wasn't given.

      In this case the :exc:`~@MaxRetriesExceededError`
      exception will be raised.

    - There's no current exception

      If there's no original exception to re-raise the ``exc``
      argument will be used instead, so:

      .. code-block:: python

          self.retry(exc=Twitter.LoginError())

      will raise the ``exc`` argument given.

.. _task-retry-custom-delay:

使用自定义重试延迟
--------------------------

Using a custom retry delay

.. tab:: 中文

    当任务被重试时，可以在重试前等待一段时间，默认的延迟时间由 :attr:`~@Task.default_retry_delay` 属性定义。默认值为 3 分钟。请注意，该值的单位为秒（int 或 float）。

    你也可以通过在调用 :meth:`~@Task.retry` 时传入 `countdown` 参数来覆盖默认值。

    .. code-block:: python

        @app.task(bind=True, default_retry_delay=30 * 60)  # 30 分钟后重试。
        def add(self, x, y):
            try:
                something_raising()
            except Exception as exc:
                # 覆盖默认延迟时间，设置为 1 分钟后重试
                raise self.retry(exc=exc, countdown=60)
.. tab:: 英文

    When a task is to be retried, it can wait for a given amount of time
    before doing so, and the default delay is defined by the
    :attr:`~@Task.default_retry_delay`
    attribute. By default this is set to 3 minutes. Note that the
    unit for setting the delay is in seconds (int or float).

    You can also provide the `countdown` argument to :meth:`~@Task.retry` to
    override this default.

    .. code-block:: python

        @app.task(bind=True, default_retry_delay=30 * 60)  # retry in 30 minutes.
        def add(self, x, y):
            try:
                something_raising()
            except Exception as exc:
                # overrides the default delay to retry after 1 minute
                raise self.retry(exc=exc, countdown=60)

.. _task-autoretry:

已知异常的自动重试
------------------------------------

Automatic retry for known exceptions

.. tab:: 中文

    有时候你可能希望在遇到某个特定异常时自动重试任务。
    
    幸运的是，你可以通过 :meth:`@task` 装饰器中的 `autoretry_for` 参数告诉 Celery 自动重试任务：
    
    .. code-block:: python
    
        from twitter.exceptions import FailWhaleError
    
        @app.task(autoretry_for=(FailWhaleError,))
        def refresh_timeline(user):
            return twitter.refresh_timeline(user)
    
    如果你希望为内部的 :meth:`~@Task.retry` 调用指定自定义参数，可以通过 :meth:`@task` 装饰器传递 `retry_kwargs` 参数：
    
    .. code-block:: python
    
        @app.task(autoretry_for=(FailWhaleError,),
                retry_kwargs={'max_retries': 5})
        def refresh_timeline(user):
            return twitter.refresh_timeline(user)
    
    这是一种替代手动处理异常的方法。上述示例等价于将任务主体包裹在 :keyword:`try` ... :keyword:`except` 语句中：
    
    .. code-block:: python
    
        @app.task
        def refresh_timeline(user):
            try:
                twitter.refresh_timeline(user)
            except FailWhaleError as exc:
                raise refresh_timeline.retry(exc=exc, max_retries=5)
    
    如果你希望在任意错误发生时都自动重试，可以这样写：
    
    .. code-block:: python
    
        @app.task(autoretry_for=(Exception,))
        def x():
            ...
    
    .. versionadded:: 4.2
    
    如果你的任务依赖其他服务，例如向某个 API 发送请求，那么使用 `指数退避机制 <https://en.wikipedia.org/wiki/Exponential_backoff>`_ 是个不错的选择，可以避免请求过多压垮服务。幸运的是，Celery 的自动重试机制对此提供了良好支持。只需指定 :attr:`~Task.retry_backoff` 参数即可，例如：
    
    .. code-block:: python
    
        from requests.exceptions import RequestException
    
        @app.task(autoretry_for=(RequestException,), retry_backoff=True)
        def x():
            ...
    
    默认情况下，该指数退避机制还会引入随机抖动（jitter_），以避免所有任务同时运行。最大的退避延迟默认设置为 10 分钟。你可以根据下方文档说明对这些行为进行自定义。
    
    .. versionadded:: 4.4
    
    你也可以在基于类的任务中设置 `autoretry_for`、 `max_retries`、 `retry_backoff`、 `retry_backoff_max` 和 `retry_jitter` 等选项：
    
    .. code-block:: python
    
        class BaseTaskWithRetry(Task):
            autoretry_for = (TypeError,)
            max_retries = 5
            retry_backoff = True
            retry_backoff_max = 700
            retry_jitter = False
    
    .. attribute:: Task.autoretry_for
    
        异常类组成的列表或元组。如果任务在执行期间抛出了这些异常之一，则会自动重试。
        默认情况下，不会对任何异常进行自动重试。
    
    .. attribute:: Task.max_retries
    
        一个整数。表示放弃前的最大重试次数。设置为 ``None`` 表示无限重试。
        默认值为 ``3``。
    
    .. attribute:: Task.retry_backoff
    
        布尔值或整数。如果设置为 ``True``，自动重试将遵循 `指数退避机制`_ 的规则。
        第一次重试延迟 1 秒，第二次延迟 2 秒，第三次延迟 4 秒，第四次延迟 8 秒，以此类推。
        （但该延迟值可能会受到 :attr:`~Task.retry_jitter` 启用时的影响。）
        如果设置为一个整数，则该值将作为延迟因子使用。例如，若设为 ``3``，第一次重试延迟 3 秒，第二次为 6 秒，第三次为 12 秒，第四次为 24 秒，依此类推。
        默认值为 ``False``，即不启用重试延迟。
    
    .. attribute:: Task.retry_backoff_max
    
        一个整数。如果启用了 ``retry_backoff``，则该选项用于设置任务自动重试之间的最大延迟时间（单位：秒）。
        默认值为 ``600`` （即 10 分钟）。
    
    .. attribute:: Task.retry_jitter
    
        布尔值。`抖动（jitter） <https://en.wikipedia.org/wiki/Jitter>`_ 用于在指数退避延迟中引入随机性，以避免队列中的所有任务同时被调度执行。
        如果设置为 ``True``，则由 :attr:`~Task.retry_backoff` 计算出的延迟值将被视为最大值，实际延迟时间将在 0 到该最大值之间随机选取。
        默认值为 ``True``。
    
    .. versionadded:: 5.3.0
    
    .. attribute:: Task.dont_autoretry_for
    
        异常类组成的列表或元组。指定的异常将不会触发自动重试。
        这允许你从 `autoretry_for <Task.autoretry_for>`:attr: 中排除某些不希望自动重试的异常。
    
.. tab:: 英文

    .. versionadded:: 4.0

    Sometimes you just want to retry a task whenever a particular exception
    is raised.
    
    Fortunately, you can tell Celery to automatically retry a task using
    `autoretry_for` argument in the :meth:`@task` decorator:
    
    .. code-block:: python
    
        from twitter.exceptions import FailWhaleError
    
        @app.task(autoretry_for=(FailWhaleError,))
        def refresh_timeline(user):
            return twitter.refresh_timeline(user)
    
    If you want to specify custom arguments for an internal :meth:`~@Task.retry`
    call, pass `retry_kwargs` argument to :meth:`@task` decorator:
    
    .. code-block:: python
    
        @app.task(autoretry_for=(FailWhaleError,),
                  retry_kwargs={'max_retries': 5})
        def refresh_timeline(user):
            return twitter.refresh_timeline(user)
    
    This is provided as an alternative to manually handling the exceptions,
    and the example above will do the same as wrapping the task body
    in a :keyword:`try` ... :keyword:`except` statement:
    
    .. code-block:: python
    
        @app.task
        def refresh_timeline(user):
            try:
                twitter.refresh_timeline(user)
            except FailWhaleError as exc:
                raise refresh_timeline.retry(exc=exc, max_retries=5)
    
    If you want to automatically retry on any error, simply use:
    
    .. code-block:: python
    
        @app.task(autoretry_for=(Exception,))
        def x():
            ...
    
    .. versionadded:: 4.2
    
    If your tasks depend on another service, like making a request to an API,
    then it's a good idea to use `exponential backoff`_ to avoid overwhelming the
    service with your requests. Fortunately, Celery's automatic retry support
    makes it easy. Just specify the :attr:`~Task.retry_backoff` argument, like this:
    
    .. code-block:: python
    
        from requests.exceptions import RequestException
    
        @app.task(autoretry_for=(RequestException,), retry_backoff=True)
        def x():
            ...
    
    By default, this exponential backoff will also introduce random jitter_ to
    avoid having all the tasks run at the same moment. It will also cap the
    maximum backoff delay to 10 minutes. All these settings can be customized
    via options documented below.
    
    .. versionadded:: 4.4
    
    You can also set `autoretry_for`, `max_retries`, `retry_backoff`, `retry_backoff_max` and `retry_jitter` options in class-based tasks:
    
    .. code-block:: python
    
        class BaseTaskWithRetry(Task):
            autoretry_for = (TypeError,)
            max_retries = 5
            retry_backoff = True
            retry_backoff_max = 700
            retry_jitter = False
    
    .. attribute:: Task.autoretry_for
       :no-index:
    
        A list/tuple of exception classes. If any of these exceptions are raised
        during the execution of the task, the task will automatically be retried.
        By default, no exceptions will be autoretried.
    
    .. attribute:: Task.max_retries
       :no-index:
    
        A number. Maximum number of retries before giving up. A value of ``None``
        means task will retry forever. By default, this option is set to ``3``.
    
    .. attribute:: Task.retry_backoff
       :no-index:
    
        A boolean, or a number. If this option is set to ``True``, autoretries
        will be delayed following the rules of `exponential backoff`_. The first
        retry will have a delay of 1 second, the second retry will have a delay
        of 2 seconds, the third will delay 4 seconds, the fourth will delay 8
        seconds, and so on. (However, this delay value is modified by
        :attr:`~Task.retry_jitter`, if it is enabled.)
        If this option is set to a number, it is used as a
        delay factor. For example, if this option is set to ``3``, the first retry
        will delay 3 seconds, the second will delay 6 seconds, the third will
        delay 12 seconds, the fourth will delay 24 seconds, and so on. By default,
        this option is set to ``False``, and autoretries will not be delayed.
    
    .. attribute:: Task.retry_backoff_max
       :no-index:
    
        A number. If ``retry_backoff`` is enabled, this option will set a maximum
        delay in seconds between task autoretries. By default, this option is set to ``600``,
        which is 10 minutes.
    
    .. attribute:: Task.retry_jitter
       :no-index:
    
        A boolean. `Jitter`_ is used to introduce randomness into
        exponential backoff delays, to prevent all tasks in the queue from being
        executed simultaneously. If this option is set to ``True``, the delay
        value calculated by :attr:`~Task.retry_backoff` is treated as a maximum,
        and the actual delay value will be a random number between zero and that
        maximum. By default, this option is set to ``True``.
    
    .. versionadded:: 5.3.0
    
    .. attribute:: Task.dont_autoretry_for
       :no-index:
    
        A list/tuple of exception classes.  These exceptions won't be autoretried.
    	This allows to exclude some exceptions that match `autoretry_for
    	<Task.autoretry_for>`:attr: but for which you don't want a retry.
    
.. _task-pydantic:
    
使用 Pydantic 进行参数验证
=================================

Argument validation with Pydantic

.. tab:: 中文

    .. versionadded:: 5.5.0
    
    你可以通过传入 ``pydantic=True`` 来使用 Pydantic_ 对参数进行校验与转换，
    以及基于类型提示对返回结果进行序列化。
    
    .. NOTE::
    
       参数校验仅涵盖任务端的参数和返回值。你在使用 ``delay()`` 或 ``apply_async()`` 
       调用任务时仍需自行序列化参数。
    
    例如：
    
    .. code-block:: python
    
        from pydantic import BaseModel
    
        class ArgModel(BaseModel):
            value: int
    
        class ReturnModel(BaseModel):
            value: str
    
        @app.task(pydantic=True)
        def x(arg: ArgModel) -> ReturnModel:
            # 使用 Pydantic 模型进行类型提示的参数会被自动转换
            assert isinstance(arg, ArgModel)
    
            # 返回的模型会被自动转换为字典
            return ReturnModel(value=f"example: {arg.value}")
    
    随后，你可以使用一个符合模型的字典调用该任务，并获得经 ``BaseModel.model_dump()`` 
    序列化后的返回结果：
    
    .. code-block:: python
    
        >>> result = x.delay({'value': 1})
        >>> result.get(timeout=1)
        {'value': 'example: 1'}

.. tab:: 英文

    .. versionadded:: 5.5.0

    You can use Pydantic_ to validate and convert arguments as well as serializing
    results based on typehints by passing ``pydantic=True``.

    .. NOTE::

        Argument validation only covers arguments/return values on the task side. You still have
        serialize arguments yourself when invoking a task with ``delay()`` or ``apply_async()``.

    For example:

    .. code-block:: python

        from pydantic import BaseModel

        class ArgModel(BaseModel):
            value: int

        class ReturnModel(BaseModel):
            value: str

        @app.task(pydantic=True)
        def x(arg: ArgModel) -> ReturnModel:
            # args/kwargs type hinted as Pydantic model will be converted
            assert isinstance(arg, ArgModel)

            # The returned model will be converted to a dict automatically
            return ReturnModel(value=f"example: {arg.value}")

    The task can then be called using a dict matching the model, and you'll receive
    the returned model "dumped" (serialized using ``BaseModel.model_dump()``):

    .. code-block:: python

        >>> result = x.delay({'value': 1})
        >>> result.get(timeout=1)
        {'value': 'example: 1'}

联合类型、泛型参数
----------------------------------

Union types, arguments to generics

.. tab:: 中文

    联合类型（例如 ``Union[SomeModel, OtherModel]``）或用于泛型的参数类型（例如
    ``list[SomeModel]``） **不** 受支持。

    如果你希望支持列表或类似类型，建议使用 ``pydantic.RootModel``。

.. tab:: 英文

    Union types (e.g. ``Union[SomeModel, OtherModel]``) or arguments to generics (e.g.
    ``list[SomeModel]``) are **not** supported.

    In case you want to support a list or similar types, it is recommended to use
    ``pydantic.RootModel``.


可选参数/返回值
---------------------------------

Optional parameters/return values

.. tab:: 中文

    可选参数和可选返回值也会被正确处理。例如，给定如下任务：

    .. code-block:: python

        from typing import Optional

        # 模型与上方相同

        @app.task(pydantic=True)
        def x(arg: Optional[ArgModel] = None) -> Optional[ReturnModel]:
            if arg is None:
                return None
            return ReturnModel(value=f"example: {arg.value}")

    你将会获得如下行为：

    .. code-block:: python

        >>> result = x.delay()
        >>> result.get(timeout=1) is None
        True
        >>> result = x.delay({'value': 1})
        >>> result.get(timeout=1)
        {'value': 'example: 1'}


.. tab:: 英文

    Optional parameters or return values are also handled properly. For example, given this task:

    .. code-block:: python

        from typing import Optional

        # models are the same as above

        @app.task(pydantic=True)
        def x(arg: Optional[ArgModel] = None) -> Optional[ReturnModel]:
            if arg is None:
                return None
            return ReturnModel(value=f"example: {arg.value}")

    You'll get the following behavior:

    .. code-block:: python

        >>> result = x.delay()
        >>> result.get(timeout=1) is None
        True
        >>> result = x.delay({'value': 1})
        >>> result.get(timeout=1)
        {'value': 'example: 1'}

返回值处理
---------------------

Return value handling

.. tab:: 中文

    只有当返回的模型实例与注解完全匹配时，返回值才会被序列化。如果你返回的是一个不同类型的模型实例，它将 *不会* 被序列化。 ``mypy`` 应该能够捕捉到这类错误，因此你应当据此修正类型提示。

.. tab:: 英文

    Return values will only be serialized if the returned model matches the annotation. If you pass a
    model instance of a different type, it will *not* be serialized. ``mypy`` should already catch such
    errors and you should fix your typehints then.


Pydantic 参数
-------------------

Pydantic parameters

.. tab:: 中文

    还有一些额外的选项可以影响 Pydantic 的行为：
    
    .. attribute:: Task.pydantic_strict
    
       默认情况下， `strict mode <https://docs.pydantic.dev/dev/concepts/strict_mode/>`_
       是关闭的。你可以传入 ``True`` 以启用严格的模型校验。
    
    .. attribute:: Task.pydantic_context
    
       在 Pydantic 模型校验过程中传入 `额外的校验上下文
       <https://docs.pydantic.dev/dev/concepts/validators/#validation-context>`_。
       默认情况下，上下文中已经包含了应用对象（ ``celery_app`` ）和任务名称（ ``celery_task_name`` ）。
    
    .. attribute:: Task.pydantic_dump_kwargs
    
       在序列化结果时，将这些额外参数传递给 ``dump_kwargs()``。默认情况下，仅传入 ``mode='json'``。

.. tab:: 英文

    There are a few more options influencing Pydantic behavior:
    
    .. attribute:: Task.pydantic_strict
       :no-index:
    
       By default, `strict mode <https://docs.pydantic.dev/dev/concepts/strict_mode/>`_
       is disabled. You can pass ``True`` to enable strict model validation.
    
    .. attribute:: Task.pydantic_context
       :no-index:
    
       Pass `additional validation context
       <https://docs.pydantic.dev/dev/concepts/validators/#validation-context>`_ during
       Pydantic model validation. The context already includes the application object as
       ``celery_app`` and the task name as ``celery_task_name`` by default.
    
    .. attribute:: Task.pydantic_dump_kwargs
       :no-index:
    
       When serializing a result, pass these additional arguments to ``dump_kwargs()``.
       By default, only ``mode='json'`` is passed.


.. _task-options:

选项列表
===============

List of Options

.. tab:: 中文

    任务装饰器可以接受多个选项，用以改变任务的行为。例如，你可以使用 :attr:`rate_limit` 选项来设置任务的速率限制。

    传递给任务装饰器的任意关键字参数，实际上都会被设为最终任务类的属性，以下是内置属性的列表。

.. tab:: 英文

    The task decorator can take a number of options that change the way
    the task behaves, for example you can set the rate limit for a task
    using the :attr:`rate_limit` option.

    Any keyword argument passed to the task decorator will actually be set
    as an attribute of the resulting task class, and this is a list
    of the built-in attributes.

.. _task-general-options:

常规
-------

General

.. tab:: 中文

    .. attribute:: Task.name
    
        任务的注册名称。
    
        你可以手动设置该名称，或者默认会使用模块名和类名自动生成。
    
        另见 :ref:`task-names`。
    
    .. attribute:: Task.request
    
        如果任务正在被执行，该属性将包含当前请求的信息。该信息使用线程本地存储。
    
        参见 :ref:`task-request-info`。
    
    .. attribute:: Task.max_retries
    
        仅在任务调用 ``self.retry`` 或装饰器使用了 :ref:`autoretry_for <task-autoretry>` 参数时适用。
    
        表示在放弃之前最多允许重试的次数。
        如果重试次数超过此值，则会引发 :exc:`~@MaxRetriesExceededError` 异常。
    
        .. note::
    
            必须手动调用 :meth:`~@Task.retry`，
            它不会在异常发生时自动重试。
    
        默认值为 ``3``。
        若设置为 :const:`None`，则表示禁用重试限制，任务将无限重试直到成功。
    
    .. attribute:: Task.throws
    
        一个可选的异常类型元组，表示这些错误类型不应视为真正的错误。
    
        属于该列表中的错误仍会被报告为任务失败（发送到结果后端），
        但 worker 不会将其记录为错误，也不会包含 traceback。
    
        示例：
    
        .. code-block:: python
    
            @task(throws=(KeyError, HttpNotFound)):
            def get_foo():
                something()
    
        错误类型行为如下：
    
        - 预期错误（出现在 ``Task.throws`` 中）
    
            使用 ``INFO`` 等级记录日志，不包含 traceback。
    
        - 未预期错误
    
            使用 ``ERROR`` 等级记录日志，并包含 traceback。
    
    .. attribute:: Task.default_retry_delay
    
        重试前的默认等待时间（以秒为单位）。可以是 :class:`int` 或 :class:`float`。
        默认值为三分钟。
    
    .. attribute:: Task.rate_limit
    
        设置该任务类型的速率限制（即在特定时间段内允许运行的任务数量）。
        即使启用了速率限制，任务仍然会完成，只是可能会被延迟启动。
    
        如果设置为 :const:`None`，则不启用速率限制。
        如果设置为整数或浮点数，则被解释为「每秒任务数」。
    
        可通过附加 `"/s"`、`"/m"` 或 `"/h"` 来指定速率单位为秒、分钟或小时。
        任务将在指定时间范围内均匀分布。
    
        示例： `"100/m"` （每分钟最多 100 个任务）。这将强制两个任务之间至少间隔 600 毫秒。
    
        默认值取自 :setting:`task_default_rate_limit` 设置项：
        若未设置，则默认不启用任务速率限制。
    
        注意，该限制是 *每个 worker 实例* 的限制，而非全局限制。
        若需实施全局速率限制（例如 API 请求的最大频率），应限制任务到特定队列中。
    
    .. attribute:: Task.time_limit
    
        该任务的强制时间限制（以秒为单位）。
        若未设置，则使用 worker 的默认值。
    
    .. attribute:: Task.soft_time_limit
    
        该任务的软性时间限制。
        若未设置，则使用 worker 的默认值。
    
    .. attribute:: Task.ignore_result
    
        不存储任务状态。请注意，这意味着你无法使用
        :class:`~celery.result.AsyncResult` 来检查任务是否完成，
        或获取其返回值。
    
        注意：禁用任务结果存储会影响某些功能的使用。
        更多详情请查阅 Canvas 文档。
    
    .. attribute:: Task.store_errors_even_if_ignored
    
        若设置为 :const:`True`，即使任务配置为忽略结果，错误也会被记录。
    
    .. attribute:: Task.serializer
    
        指定默认使用的序列化方法（字符串形式）。默认为 :setting:`task_serializer` 设置项的值。
        可选值包括 `pickle`、`json`、`yaml`，或使用
        :mod:`kombu.serialization.registry` 注册的自定义序列化方法。
    
        更多信息请参见 :ref:`calling-serializers`。
    
    .. attribute:: Task.compression
    
        指定默认使用的压缩方案（字符串形式）。
    
        默认为 :setting:`task_compression` 设置项的值。
        可选值包括 `gzip`、`bzip2`，或使用 :mod:`kombu.compression` 注册的自定义压缩方法。
    
        更多信息请参见 :ref:`calling-compression`。
    
    .. attribute:: Task.backend
    
        指定该任务使用的结果存储后端。应为 `celery.backends` 中某个后端类的实例。
        默认使用 `app.backend`，由 :setting:`result_backend` 设置项定义。
    
    .. attribute:: Task.acks_late
    
        若设置为 :const:`True`，该任务的消息将在任务执行**之后**被确认；
        而默认行为是在任务开始执行前确认消息。
    
        注意：这意味着如果 worker 在执行中崩溃，任务可能会被多次执行。
        因此确保你的任务是 :term:`idempotent` 的至关重要。
    
        全局默认值可通过 :setting:`task_acks_late` 设置项覆盖。
    
    .. _task-track-started:
    
    .. attribute:: Task.track_started
    
        若设置为 :const:`True`，任务在被 worker 执行时会报告其状态为 "started"。
        默认值为 :const:`False`，即任务状态仅包括 pending、finished 或 waiting-to-retry。
        对于长时间运行的任务，该状态有助于报告当前运行的任务。
    
        执行该任务的 worker 的主机名与进程 ID 会包含在状态元数据中（如：`result.info['pid']`）。
    
        全局默认值可通过 :setting:`task_track_started` 设置项覆盖。
    
    .. seealso::
    
        :class:`~@Task` 的 API 参考文档。

.. tab:: 英文

    .. attribute:: Task.name
       :no-index:
    
        The name the task is registered as.
    
        You can set this name manually, or a name will be
        automatically generated using the module and class name.
    
        See also :ref:`task-names`.
    
    .. attribute:: Task.request
       :no-index:
    
        If the task is being executed this will contain information
        about the current request. Thread local storage is used.
    
        See :ref:`task-request-info`.
    
    .. attribute:: Task.max_retries
       :no-index:
    
        Only applies if the task calls ``self.retry`` or if the task is decorated
        with the :ref:`autoretry_for <task-autoretry>` argument.
    
        The maximum number of attempted retries before giving up.
        If the number of retries exceeds this value a :exc:`~@MaxRetriesExceededError`
        exception will be raised.
    
        .. note::
    
            You have to call :meth:`~@Task.retry`
            manually, as it won't automatically retry on exception..
    
        The default is ``3``.
        A value of :const:`None` will disable the retry limit and the
        task will retry forever until it succeeds.
    
    .. attribute:: Task.throws
       :no-index:
    
        Optional tuple of expected error classes that shouldn't be regarded
        as an actual error.
    
        Errors in this list will be reported as a failure to the result backend,
        but the worker won't log the event as an error, and no traceback will
        be included.
    
        Example:
    
        .. code-block:: python
    
            @task(throws=(KeyError, HttpNotFound)):
            def get_foo():
                something()
    
        Error types:
    
        - Expected errors (in ``Task.throws``)
    
            Logged with severity ``INFO``, traceback excluded.
    
        - Unexpected errors
    
            Logged with severity ``ERROR``, with traceback included.
    
    .. attribute:: Task.default_retry_delay
       :no-index:
    
        Default time in seconds before a retry of the task
        should be executed. Can be either :class:`int` or :class:`float`.
        Default is a three minute delay.
    
    .. attribute:: Task.rate_limit
       :no-index:
    
        Set the rate limit for this task type (limits the number of tasks
        that can be run in a given time frame). Tasks will still complete when
        a rate limit is in effect, but it may take some time before it's allowed to
        start.
    
        If this is :const:`None` no rate limit is in effect.
        If it is an integer or float, it is interpreted as "tasks per second".
    
        The rate limits can be specified in seconds, minutes or hours
        by appending `"/s"`, `"/m"` or `"/h"` to the value. Tasks will be evenly
        distributed over the specified time frame.
    
        Example: `"100/m"` (hundred tasks a minute). This will enforce a minimum
        delay of 600ms between starting two tasks on the same worker instance.
    
        Default is the :setting:`task_default_rate_limit` setting:
        if not specified means rate limiting for tasks is disabled by default.
    
        Note that this is a *per worker instance* rate limit, and not a global
        rate limit. To enforce a global rate limit (e.g., for an API with a
        maximum number of  requests per second), you must restrict to a given
        queue.
    
    .. attribute:: Task.time_limit
       :no-index:
    
        The hard time limit, in seconds, for this task.
        When not set the workers default is used.
    
    .. attribute:: Task.soft_time_limit
       :no-index:
    
        The soft time limit for this task.
        When not set the workers default is used.
    
    .. attribute:: Task.ignore_result
       :no-index:
    
        Don't store task state. Note that this means you can't use
        :class:`~celery.result.AsyncResult` to check if the task is ready,
        or get its return value.
    
        Note: Certain features will not work if task results are disabled.
        For more details check the Canvas documentation.
    
    .. attribute:: Task.store_errors_even_if_ignored
       :no-index:
    
        If :const:`True`, errors will be stored even if the task is configured
        to ignore results.
    
    .. attribute:: Task.serializer
       :no-index:
    
        A string identifying the default serialization
        method to use. Defaults to the :setting:`task_serializer`
        setting. Can be `pickle`, `json`, `yaml`, or any custom
        serialization methods that have been registered with
        :mod:`kombu.serialization.registry`.
    
        Please see :ref:`calling-serializers` for more information.
    
    .. attribute:: Task.compression
       :no-index:
    
        A string identifying the default compression scheme to use.
    
        Defaults to the :setting:`task_compression` setting.
        Can be `gzip`, or `bzip2`, or any custom compression schemes
        that have been registered with the :mod:`kombu.compression` registry.
    
        Please see :ref:`calling-compression` for more information.
    
    .. attribute:: Task.backend
       :no-index:
    
        The result store backend to use for this task. An instance of one of the
        backend classes in `celery.backends`. Defaults to `app.backend`,
        defined by the :setting:`result_backend` setting.
    
    .. attribute:: Task.acks_late
       :no-index:
    
        If set to :const:`True` messages for this task will be acknowledged
        **after** the task has been executed, not *just before* (the default
        behavior).
    
        Note: This means the task may be executed multiple times should the worker
        crash in the middle of execution.  Make sure your tasks are
        :term:`idempotent`.
    
        The global default can be overridden by the :setting:`task_acks_late`
        setting.
    
    .. attribute:: Task.track_started
       :no-index:
    
        If :const:`True` the task will report its status as "started"
        when the task is executed by a worker.
        The default value is :const:`False` as the normal behavior is to not
        report that level of granularity. Tasks are either pending, finished,
        or waiting to be retried. Having a "started" status can be useful for
        when there are long running tasks and there's a need to report what
        task is currently running.
    
        The host name and process id of the worker executing the task
        will be available in the state meta-data (e.g., `result.info['pid']`)
    
        The global default can be overridden by the
        :setting:`task_track_started` setting.
    
    
    .. seealso::
    
        The API reference for :class:`~@Task`.

.. _task-states:

状态
======

States

.. tab:: 中文

    Celery 可以跟踪任务的当前状态。状态信息中还包含了
    成功任务的返回结果，或者失败任务的异常与回溯（traceback）信息。

    Celery 提供了多种 *结果后端* （result backend）供选择，
    每种后端都有其各自的优缺点（参见 :ref:`task-result-backends`）。

    在任务的生命周期中，它将经历多个可能的状态变迁，
    且每个状态都可以附加任意的元数据（meta-data）。
    当任务进入一个新的状态时，之前的状态将被遗忘，
    但某些状态变迁可以被推断出来（例如，
    如果一个任务当前处于 :state:`FAILED` 状态，
    可以推断出它之前曾处于 :state:`STARTED` 状态）。

    同时，Celery 还定义了一些状态集合，
    比如 :state:`FAILURE_STATES` 集合和 :state:`READY_STATES` 集合。

    客户端可以通过判断任务状态是否属于这些集合来决定后续行为，
    例如，是否需要重新抛出异常（如果任务状态属于 :state:`PROPAGATE_STATES`），
    或者是否可以缓存该任务状态（如果任务已准备就绪，则可以缓存）。

    此外，你也可以定义 :ref:`custom-states` 来扩展状态管理。

.. tab:: 英文

    Celery can keep track of the tasks current state. The state also contains the
    result of a successful task, or the exception and traceback information of a
    failed task.

    There are several *result backends* to choose from, and they all have
    different strengths and weaknesses (see :ref:`task-result-backends`).

    During its lifetime a task will transition through several possible states,
    and each state may have arbitrary meta-data attached to it. When a task
    moves into a new state the previous state is
    forgotten about, but some transitions can be deduced, (e.g., a task now
    in the :state:`FAILED` state, is implied to have been in the
    :state:`STARTED` state at some point).

    There are also sets of states, like the set of
    :state:`FAILURE_STATES`, and the set of :state:`READY_STATES`.

    The client uses the membership of these sets to decide whether
    the exception should be re-raised (:state:`PROPAGATE_STATES`), or whether
    the state can be cached (it can if the task is ready).

    You can also define :ref:`custom-states`.

.. _task-result-backends:

结果后端
---------------

Result Backends

.. tab:: 中文

    如果你希望跟踪任务或需要获取返回值，那么 Celery 必须将状态存储或发送到某个地方，以便之后能够检索。
    Celery 提供了多种内置的结果后端供选择：SQLAlchemy/Django ORM、Memcached、RabbitMQ/QPid（``rpc``）和 Redis —— 当然你也可以自定义自己的后端。

    没有任何一个后端能在所有使用场景中都表现良好。
    你应当了解每种后端的优缺点，并根据自己的需求选择最合适的方案。

    .. warning::

        后端在存储和传输结果时会占用资源。为了确保资源能够及时释放，
        你必须在调用任务之后，对每一个返回的 :class:`~@AsyncResult` 实例，
        最终调用一次 :meth:`~@AsyncResult.get` 或 :meth:`~@AsyncResult.forget` 方法。

    .. seealso::

        :ref:`conf-result-backend`

.. tab:: 英文

    If you want to keep track of tasks or need the return values, then Celery
    must store or send the states somewhere so that they can be retrieved later.
    There are several built-in result backends to choose from: SQLAlchemy/Django ORM,
    Memcached, RabbitMQ/QPid (``rpc``), and Redis -- or you can define your own.
    
    No backend works well for every use case.
    You should read about the strengths and weaknesses of each backend, and choose
    the most appropriate for your needs.
    
    .. warning::
    
        Backends use resources to store and transmit results. To ensure
        that resources are released, you must eventually call
        :meth:`~@AsyncResult.get` or :meth:`~@AsyncResult.forget` on
        EVERY :class:`~@AsyncResult` instance returned after calling
        a task.
    
    .. seealso::
    
        :ref:`conf-result-backend`

RPC 结果后端 (RabbitMQ/QPid)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

RPC Result Backend (RabbitMQ/QPid)

.. tab:: 中文

    RPC 结果后端（ ``rpc://`` ）比较特殊，因为它实际上并不 *存储* 状态，
    而是将其作为消息发送出去。这一点非常重要，因为它意味着：

    - 一个结果 *只能被检索一次*。
    - *只能由发起该任务的客户端* 进行检索。

    两个不同的进程无法同时等待同一个结果。

    尽管有这些限制，如果你需要实时接收状态变更信息，RPC 后端依然是一个非常优秀的选择。
    使用消息传递机制意味着客户端无需轮询即可接收新状态。

    默认情况下，消息是瞬时（非持久化）的，因此如果代理（broker）重启，结果将会丢失。
    你可以通过设置 :setting:`result_persistent` 来配置后端发送持久化消息。

.. tab:: 英文

    The RPC result backend (`rpc://`) is special as it doesn't actually *store*
    the states, but rather sends them as messages. This is an important difference as it
    means that a result *can only be retrieved once*, and *only by the client
    that initiated the task*. Two different processes can't wait for the same result.

    Even with that limitation, it is an excellent choice if you need to receive
    state changes in real-time. Using messaging means the client doesn't have to
    poll for new states.

    The messages are transient (non-persistent) by default, so the results will
    disappear if the broker restarts. You can configure the result backend to send
    persistent messages using the :setting:`result_persistent` setting.

数据库结果后端
~~~~~~~~~~~~~~~~~~~~~~~

Database Result Backend

.. tab:: 中文

    将状态存储在数据库中对许多人来说非常方便，特别是当已有数据库基础设施（例如 Web 应用）时，
    但这种方式也存在一些局限性：
    
    * 轮询数据库以获取新状态的代价很高，因此你应当增加操作的轮询间隔，比如在调用 `result.get()` 时。
    
    * 有些数据库的默认事务隔离级别并不适合用于轮询数据表以检测变化。
    
      以 MySQL 为例，其默认的事务隔离级别是 `REPEATABLE-READ`：
      这意味着在当前事务提交之前，该事务无法看到其他事务所做的更改。
    
      因此，推荐将事务隔离级别修改为 `READ-COMMITTED`。


.. tab:: 英文

    Keeping state in the database can be convenient for many, especially for
    web applications with a database already in place, but it also comes with
    limitations.
    
    * Polling the database for new states is expensive, and so you should
      increase the polling intervals of operations, such as `result.get()`.
    
    * Some databases use a default transaction isolation level that
      isn't suitable for polling tables for changes.
    
      In MySQL the default transaction isolation level is `REPEATABLE-READ`:
      meaning the transaction won't see changes made by other transactions until
      the current transaction is committed.
    
      Changing that to the `READ-COMMITTED` isolation level is recommended.

.. _task-builtin-states:

内置状态
---------------

Built-in States

.. state:: PENDING

PENDING
~~~~~~~

.. tab:: 中文

    任务正在等待执行或未知.
    任何未知的任务 ID 都暗示处于待处理状态.

.. tab:: 英文

    Task is waiting for execution or unknown.
    Any task id that's not known is implied to be in the pending state.

.. state:: STARTED

STARTED
~~~~~~~

.. tab:: 中文

    任务已开始.
    默认情况下不报告，要启用请参阅 :attr:`@Task.track_started` 。

    :meta-data: 执行任务的工作进程的 `pid` 和 `hostname` 。

.. tab:: 英文

    Task has been started.
    Not reported by default, to enable please see :attr:`@Task.track_started`.

    :meta-data: `pid` and `hostname` of the worker process executing the task.

.. state:: SUCCESS

SUCCESS
~~~~~~~

.. tab:: 中文

    任务已成功执行。

    :meta-data: `result` 包含任务的返回值。
    :propagates: Yes
    :ready: Yes

.. tab:: 英文

    Task has been successfully executed.

    :meta-data: `result` contains the return value of the task.
    :propagates: Yes
    :ready: Yes

.. state:: FAILURE

FAILURE
~~~~~~~

.. tab:: 中文

    任务执行失败.

    :meta-data: `result` 包含发生的异常， `traceback` 包含引发异常时堆栈的回溯。
    :propagates: Yes

.. tab:: 英文

    Task execution resulted in failure.

    :meta-data: `result` contains the exception occurred, and `traceback` contains the backtrace of the stack at the point when the exception was raised.
    :propagates: Yes

.. state:: RETRY

RETRY
~~~~~

.. tab:: 中文

    任务正在重试.

    :meta-data: `result` 包含导致重试的异常， `traceback` 包含引发异常时堆栈的回溯。
    :propagates: No

.. tab:: 英文

    Task is being retried.

    :meta-data: `result` contains the exception that caused the retry, and `traceback` contains the backtrace of the stack at the point when the exceptions was raised.
    :propagates: No

.. state:: REVOKED

REVOKED
~~~~~~~

.. tab:: 中文

    任务已被撤销.

    :propagates: Yes

.. tab:: 英文

    Task has been revoked.

    :propagates: Yes

.. _custom-states:

自定义状态
-------------

Custom states

.. tab:: 中文

    你可以轻松地定义自己的任务状态，只需要一个唯一的名称即可。
    状态名通常是一个大写字符串。例如，你可以参考 :mod:`可中止任务 <~celery.contrib.abortable>` ，
    其中定义了一个自定义的 :state:`ABORTED` 状态。

    使用 :meth:`~@Task.update_state` 方法可以更新任务的状态：

    .. code-block:: python

        @app.task(bind=True)
        def upload_files(self, filenames):
            for i, file in enumerate(filenames):
                if not self.request.called_directly:
                    self.update_state(state='PROGRESS',
                        meta={'current': i, 'total': len(filenames)})

    在上面的例子中，我创建了状态 `"PROGRESS"`，
    用于告知了解此状态的应用程序当前任务正在进行中，
    并通过 `current` 和 `total` 这两个计数值来表示任务的进度。
    例如，可以基于这些元数据来创建进度条显示。

.. tab:: 英文

    You can easily define your own states, all you need is a unique name.
    The name of the state is usually an uppercase string. As an example
    you could have a look at the :mod:`abortable tasks <~celery.contrib.abortable>`
    which defines a custom :state:`ABORTED` state.

    Use :meth:`~@Task.update_state` to update a task's state:.

    .. code-block:: python

        @app.task(bind=True)
        def upload_files(self, filenames):
            for i, file in enumerate(filenames):
                if not self.request.called_directly:
                    self.update_state(state='PROGRESS',
                        meta={'current': i, 'total': len(filenames)})


    Here I created the state `"PROGRESS"`, telling any application
    aware of this state that the task is currently in progress, and also where
    it is in the process by having `current` and `total` counts as part of the
    state meta-data. This can then be used to create progress bars for example.

.. _pickling_exceptions:

创建可 pickle 的异常
------------------------------

Creating pickleable exceptions

.. tab:: 中文

    一个鲜为人知的 Python 事实是：异常要能被 `pickle` 模块序列化，必须遵循一些简单的规则。

    如果任务抛出了无法被 pickle 序列化的异常，那么在使用 Pickle 作为序列化器时，任务将无法正常工作。

    为了确保异常对象可以被 pickle 正确序列化，
    异常类 *必须* 在其 ``.args`` 属性中保存创建实例时的原始参数。
    最简单的方式就是在自定义异常的构造函数中调用 ``Exception.__init__`` 方法。

    下面是一些可以正常工作的示例，以及一个错误示例：

    .. code-block:: python

        # 正确示例：
        class HttpError(Exception):
            pass

        # 错误示例：
        class HttpError(Exception):

            def __init__(self, status_code):
                self.status_code = status_code

        # 正确示例：
        class HttpError(Exception):

            def __init__(self, status_code):
                self.status_code = status_code
                Exception.__init__(self, status_code)  # <-- 必须调用

    因此，规则总结如下：
    如果异常类支持自定义参数 ``*args``，
    则必须在构造函数中调用 ``Exception.__init__(self, *args)``。

    需要注意的是：
    目前对于 *关键字参数（keyword arguments）* 并没有特别的支持，
    因此如果希望在反序列化（unpickle）时保留关键字参数，
    必须将它们作为普通的位置参数（args）传递：

    .. code-block:: python

        class HttpError(Exception):

            def __init__(self, status_code, headers=None, body=None):
                self.status_code = status_code
                self.headers = headers
                self.body = body

                super(HttpError, self).__init__(status_code, headers, body)


.. tab:: 英文

    A rarely known Python fact is that exceptions must conform to some
    simple rules to support being serialized by the pickle module.

    Tasks that raise exceptions that aren't pickleable won't work
    properly when Pickle is used as the serializer.

    To make sure that your exceptions are pickleable the exception
    *MUST* provide the original arguments it was instantiated
    with in its ``.args`` attribute. The simplest way
    to ensure this is to have the exception call ``Exception.__init__``.

    Let's look at some examples that work, and one that doesn't:

    .. code-block:: python


        # OK:
        class HttpError(Exception):
            pass

        # BAD:
        class HttpError(Exception):

            def __init__(self, status_code):
                self.status_code = status_code

        # OK:
        class HttpError(Exception):

            def __init__(self, status_code):
                self.status_code = status_code
                Exception.__init__(self, status_code)  # <-- REQUIRED


    So the rule is:
    For any exception that supports custom arguments ``*args``,
    ``Exception.__init__(self, *args)`` must be used.

    There's no special support for *keyword arguments*, so if you
    want to preserve keyword arguments when the exception is unpickled
    you have to pass them as regular args:

    .. code-block:: python

        class HttpError(Exception):

            def __init__(self, status_code, headers=None, body=None):
                self.status_code = status_code
                self.headers = headers
                self.body = body

                super(HttpError, self).__init__(status_code, headers, body)

.. _task-semipredicates:

任务半谓词
==============

Semipredicates

.. tab:: 中文

    worker 将任务包装在一个跟踪函数中，用于记录任务的最终状态。可以使用多种异常来通知此函数，以改变其处理任务返回的方式。

    .. admonition:: 译注: Semipredicates
       :class: toggle

       在 Celery 的上下文中，"task semipredicates" 是一个相对专业的术语，其翻译需要结合技术语义和中文表达习惯。以下是针对该术语的详细解析和推荐译法：

       ----

       1. **术语解析**

       - **Semipredicate（半谓词）**：

         - **计算机科学中的原意**：指既返回结果又返回状态（如成功/失败）的函数，例如 C 语言的 ``fopen()`` 在失败时返回 ``NULL`` 同时设置 ``errno``。

         - **在 Celery 中的延伸**：可能指任务（task）在执行时既产生返回值，又隐含状态信息（如 ``SUCCESS``、``FAILURE`` 或重试状态）。

       - **Task Semipredicates**：

         - 指 Celery 任务设计中同时承载业务逻辑结果和自身执行状态的特性，例如：

           .. code-block:: python
    
                @app.task(bind=True)
                def my_task(self, x, y):
                    try:
                        return x / y  # 业务结果
                    except ZeroDivisionError:
                        self.retry(countdown=60)  # 状态控制

       ----

       2. **推荐翻译方案**

       根据上下文可选择以下译法：

       .. list-table::
          
          * - 英文术语
            - 推荐中文翻译
            - 适用场景
          * - Task Semipredicates
            - 任务半谓词
            - 强调技术实现（学术/底层文档）
          * - 
            - 任务状态复合体
            - 强调状态与结果的结合（设计文档）
          * - 
            - 双态任务
            - 简洁表达（非正式场合）

       ----

       3. **使用示例**

       **(1) 技术文档中的翻译**

       原文：

           Celery tasks act as semipredicates, returning both computed values and their own execution status.

       译文：

           Celery 任务作为任务半谓词，既返回计算结果，又携带自身执行状态。

       **(2) 设计文档中的翻译**

       原文：

           The semipredicate nature of tasks allows for robust error handling.

       译文：

           任务的状态复合体特性使其支持健壮的错误处理。

       ----

       4. **注意事项**

       - **一致性**：在同一个项目中保持术语翻译统一。

       - **注释说明**：首次出现时可添加英文原词和简要解释，例如：

       任务半谓词（Task Semipredicates，指同时返回结果和状态的任务）

       - **受众适配**：面向开发者可直接用英文术语，面向非技术读者建议意译。

       ----

       5. **相关术语对照表**

       .. list-table::
          
          * - 英文术语
            - 中文翻译
          * - Task
            - 任务
          * - Predicate Function
            - 谓词函数
          * - Stateful Task
            - 有状态任务
          * - Idempotent Task
            - 幂等任务

       通过以上方式，可以准确传达 "task semipredicates" 在 Celery 中的技术内涵。


.. tab:: 英文

    The worker wraps the task in a tracing function that records the final state of the task. There are a number of exceptions that can be used to signal this function to change how it treats the return of the task.

.. _task-semipred-ignore:

忽略
------

Ignore

.. tab:: 中文

    任务可以抛出 :exc:`~@Ignore` 异常以强制 Worker 忽略该任务。
    这意味着任务的状态不会被记录，但消息仍会被确认（从队列中移除）。

    这可用于实现自定义的类似撤销（revoke）的功能，或者手动存储任务结果。

    示例：将撤销的任务保存在 Redis 的集合中：

    .. code-block:: python

        from celery.exceptions import Ignore

        @app.task(bind=True)
        def some_task(self):
            if redis.ismember('tasks.revoked', self.request.id):
                raise Ignore()

    示例：手动存储任务结果：

    .. code-block:: python

        from celery import states
        from celery.exceptions import Ignore

        @app.task(bind=True)
        def get_tweets(self, user):
            timeline = twitter.get_timeline(user)
            if not self.request.called_directly:
                self.update_state(state=states.SUCCESS, meta=timeline)
            raise Ignore()

.. tab:: 英文

    The task may raise :exc:`~@Ignore` to force the worker to ignore the
    task. This means that no state will be recorded for the task, but the
    message is still acknowledged (removed from queue).

    This can be used if you want to implement custom revoke-like
    functionality, or manually store the result of a task.

    Example keeping revoked tasks in a Redis set:

    .. code-block:: python

        from celery.exceptions import Ignore

        @app.task(bind=True)
        def some_task(self):
            if redis.ismember('tasks.revoked', self.request.id):
                raise Ignore()

    Example that stores results manually:

    .. code-block:: python

        from celery import states
        from celery.exceptions import Ignore

        @app.task(bind=True)
        def get_tweets(self, user):
            timeline = twitter.get_timeline(user)
            if not self.request.called_directly:
                self.update_state(state=states.SUCCESS, meta=timeline)
            raise Ignore()

.. _task-semipred-reject:

拒绝
------

Reject

.. tab:: 中文

    任务可以抛出 :exc:`~@Reject` 异常，以使用 AMQP 的 ``basic_reject`` 方法拒绝任务消息。
    除非启用了 :attr:`Task.acks_late`，否则此操作不会产生任何效果。

    拒绝一条消息的效果与确认（ack）类似，但某些消息代理还可能实现了其他功能可供利用。
    例如，RabbitMQ 支持 `死信交换器（Dead Letter Exchanges） <Dead Letter Exchanges>`_ 的概念，
    可以将队列配置为使用一个死信交换器，拒绝的消息会被重新投递到该交换器。

    拒绝还可以用于重新排队消息，但请务必谨慎使用，因为这可能很容易导致无限的消息循环。

    示例：当任务导致内存溢出时使用 reject：

    .. code-block:: python

        import errno
        from celery.exceptions import Reject

        @app.task(bind=True, acks_late=True)
        def render_scene(self, path):
            file = get_file(path)
            try:
                renderer.render_scene(file)

            # 如果文件太大无法载入内存，
            # 则拒绝该任务，使其被投递到死信交换器，
            # 以便我们手动检查具体情况。
            except MemoryError as exc:
                raise Reject(exc, requeue=False)
            except OSError as exc:
                if exc.errno == errno.ENOMEM:
                    raise Reject(exc, requeue=False)

            # 对于其他错误，10 秒后重试。
            except Exception as exc:
                raise self.retry(exc, countdown=10)

    示例：重新排队消息：

    .. code-block:: python

        from celery.exceptions import Reject

        @app.task(bind=True, acks_late=True)
        def requeues(self):
            if not self.request.delivery_info['redelivered']:
                raise Reject('no reason', requeue=True)
            print('received two times')

    有关 ``basic_reject`` 方法的更多信息，请参阅所使用消息代理的文档。


.. tab:: 英文

    The task may raise :exc:`~@Reject` to reject the task message using
    AMQPs ``basic_reject`` method. This won't have any effect unless
    :attr:`Task.acks_late` is enabled.

    Rejecting a message has the same effect as acking it, but some
    brokers may implement additional functionality that can be used.
    For example RabbitMQ supports the concept of `Dead Letter Exchanges`_
    where a queue can be configured to use a dead letter exchange that rejected
    messages are redelivered to.

    Reject can also be used to re-queue messages, but please be very careful
    when using this as it can easily result in an infinite message loop.

    Example using reject when a task causes an out of memory condition:

    .. code-block:: python

        import errno
        from celery.exceptions import Reject

        @app.task(bind=True, acks_late=True)
        def render_scene(self, path):
            file = get_file(path)
            try:
                renderer.render_scene(file)

            # if the file is too big to fit in memory
            # we reject it so that it's redelivered to the dead letter exchange
            # and we can manually inspect the situation.
            except MemoryError as exc:
                raise Reject(exc, requeue=False)
            except OSError as exc:
                if exc.errno == errno.ENOMEM:
                    raise Reject(exc, requeue=False)

            # For any other error we retry after 10 seconds.
            except Exception as exc:
                raise self.retry(exc, countdown=10)

    Example re-queuing the message:

    .. code-block:: python

        from celery.exceptions import Reject

        @app.task(bind=True, acks_late=True)
        def requeues(self):
            if not self.request.delivery_info['redelivered']:
                raise Reject('no reason', requeue=True)
            print('received two times')

    Consult your broker documentation for more details about the ``basic_reject``
    method.

.. _`Dead Letter Exchanges`: http://www.rabbitmq.com/dlx.html


.. _task-semipred-retry:

重试
-----

Retry

.. tab:: 中文

    :exc:`~@Retry` 异常由 ``Task.retry`` 方法抛出，用于告知 Worker 该任务正在被重试。

.. tab:: 英文

    The :exc:`~@Retry` exception is raised by the ``Task.retry`` method
    to tell the worker that the task is being retried.

.. _task-custom-classes:

自定义任务类
===================

Custom task classes

.. tab:: 中文

    所有任务都继承自 :class:`@Task` 类。  
    :meth:`~@Task.run` 方法将作为任务的主体执行。

    例如，以下代码：

    .. code-block:: python

        @app.task
        def add(x, y):
            return x + y

    其背后大致等价于如下实现：

    .. code-block:: python

        class _AddTask(app.Task):

            def run(self, x, y):
                return x + y
        add = app.tasks[_AddTask.name]

.. tab:: 英文

    All tasks inherit from the :class:`@Task` class.
    The :meth:`~@Task.run` method becomes the task body.

    As an example, the following code,

    .. code-block:: python

        @app.task
        def add(x, y):
            return x + y


    will do roughly this behind the scenes:

    .. code-block:: python

        class _AddTask(app.Task):

            def run(self, x, y):
                return x + y
        add = app.tasks[_AddTask.name]


实例化
-------------

Instantiation

.. tab:: 中文

    任务在每次请求时 **不会** 重新实例化，而是以全局实例的形式注册在任务注册表中。

    这意味着 ``__init__`` 构造函数在每个进程中只会被调用一次，并且任务类在语义上更接近于一个 Actor 模型。

    如果你定义了如下任务：

    .. code-block:: python

        from celery import Task

        class NaiveAuthenticateServer(Task):

            def __init__(self):
                self.users = {'george': 'password'}

            def run(self, username, password):
                try:
                    return self.users[username] == password
                except KeyError:
                    return False

    并且将每次请求都路由到同一个进程中执行，那么它将在请求之间保持状态。

    这对于缓存资源也很有用，例如以下用于缓存数据库连接的 Task 基类：

    .. code-block:: python

        from celery import Task

        class DatabaseTask(Task):
            _db = None

            @property
            def db(self):
                if self._db is None:
                    self._db = Database.connect()
                return self._db

.. tab:: 英文

    A task is **not** instantiated for every request, but is registered
    in the task registry as a global instance.

    This means that the ``__init__`` constructor will only be called
    once per process, and that the task class is semantically closer to an
    Actor.

    If you have a task,

    .. code-block:: python

        from celery import Task

        class NaiveAuthenticateServer(Task):

            def __init__(self):
                self.users = {'george': 'password'}

            def run(self, username, password):
                try:
                    return self.users[username] == password
                except KeyError:
                    return False

    And you route every request to the same process, then it
    will keep state between requests.

    This can also be useful to cache resources,
    For example, a base Task class that caches a database connection:

    .. code-block:: python

        from celery import Task

        class DatabaseTask(Task):
            _db = None

            @property
            def db(self):
                if self._db is None:
                    self._db = Database.connect()
                return self._db

每个任务的使用
~~~~~~~~~~~~~~

Per task usage

.. tab:: 中文

    可以像下面这样将上述基类应用于每个任务中：

    .. code-block:: python

        from celery.app import task

        @app.task(base=DatabaseTask, bind=True)
        def process_rows(self: task):
            for row in self.db.table.all():
                process_row(row)

    这样， ``process_rows`` 任务中的 ``db`` 属性在每个进程中将始终保持一致。

.. tab:: 英文

    The above can be added to each task like this:

    .. code-block:: python


        from celery.app import task

        @app.task(base=DatabaseTask, bind=True)
        def process_rows(self: task):
            for row in self.db.table.all():
                process_row(row)

    The ``db`` attribute of the ``process_rows`` task will then
    always stay the same in each process.

.. _custom-task-cls-app-wide:

App范围的使用
~~~~~~~~~~~~~~

App-wide usage

.. tab:: 中文

    你还可以通过在实例化应用时传入 ``task_cls`` 参数，指定整个 Celery 应用使用你自定义的任务类。
    该参数可以是表示任务类的 Python 路径字符串，或是类对象本身：

    .. code-block:: python

        from celery import Celery

        app = Celery('tasks', task_cls='your.module.path:DatabaseTask')

    这样，所有使用装饰器语法声明的任务都将使用你自定义的 ``DatabaseTask`` 类，并且都将具备一个 ``db`` 属性。

    默认值是 Celery 提供的类： ``'celery.app.task:Task'`` 。

.. tab:: 英文

    You can also use your custom class in your whole Celery app by passing it as
    the ``task_cls`` argument when instantiating the app. This argument should be
    either a string giving the python path to your Task class or the class itself:

    .. code-block:: python

        from celery import Celery

        app = Celery('tasks', task_cls='your.module.path:DatabaseTask')

    This will make all your tasks declared using the decorator syntax within your
    app to use your ``DatabaseTask`` class and will all have a ``db`` attribute.

    The default value is the class provided by Celery: ``'celery.app.task:Task'``.

处理程序
--------

Handlers

.. tab:: 中文

    .. method:: before_start(self, task_id, args, kwargs)

        任务在开始执行前由 Worker 调用。

        .. versionadded:: 5.2

        :param task_id: 待执行任务的唯一标识符。
        :param args: 待执行任务的原始位置参数。
        :param kwargs: 待执行任务的原始关键字参数。

        此处理器的返回值将被忽略。

    .. method:: after_return(self, status, retval, task_id, args, kwargs, einfo)

        任务返回后调用的处理器。

        :param status: 当前任务的状态。
        :param retval: 任务的返回值或异常对象。
        :param task_id: 任务的唯一标识符。
        :param args: 已返回任务的原始位置参数。
        :param kwargs: 已返回任务的原始关键字参数。

        :keyword einfo: :class:`~billiard.einfo.ExceptionInfo`
                        实例，包含 traceback（若存在）。

        此处理器的返回值将被忽略。

    .. method:: on_failure(self, exc, task_id, args, kwargs, einfo)

        当任务失败时由 Worker 调用。

        :param exc: 任务抛出的异常。
        :param task_id: 失败任务的唯一标识符。
        :param args: 失败任务的原始位置参数。
        :param kwargs: 失败任务的原始关键字参数。

        :keyword einfo: :class:`~billiard.einfo.ExceptionInfo`
                        实例，包含 traceback。

        此处理器的返回值将被忽略。

    .. method:: on_retry(self, exc, task_id, args, kwargs, einfo)

        当任务即将重试时由 Worker 调用。

        :param exc: 传递给 :meth:`~@Task.retry` 的异常。
        :param task_id: 被重试任务的唯一标识符。
        :param args: 被重试任务的原始位置参数。
        :param kwargs: 被重试任务的原始关键字参数。

        :keyword einfo: :class:`~billiard.einfo.ExceptionInfo`
                        实例，包含 traceback。

        此处理器的返回值将被忽略。

    .. method:: on_success(self, retval, task_id, args, kwargs)

        当任务成功执行时由 Worker 调用。

        :param retval: 任务的返回值。
        :param task_id: 已执行任务的唯一标识符。
        :param args: 已执行任务的原始位置参数。
        :param kwargs: 已执行任务的原始关键字参数。

        此处理器的返回值将被忽略。


.. tab:: 英文

    .. method:: before_start(self, task_id, args, kwargs)
       :no-index:

       Run by the worker before the task starts executing.

       .. versionadded:: 5.2

       :param task_id: Unique id of the task to execute.
       :param args: Original arguments for the task to execute.
       :param kwargs: Original keyword arguments for the task to execute.

       The return value of this handler is ignored.

    .. method:: after_return(self, status, retval, task_id, args, kwargs, einfo)
       :no-index:

       Handler called after the task returns.

       :param status: Current task state.
       :param retval: Task return value/exception.
       :param task_id: Unique id of the task.
       :param args: Original arguments for the task that returned.
       :param kwargs: Original keyword arguments for the task
                   that returned.

       :keyword einfo: :class:`~billiard.einfo.ExceptionInfo`
                       instance, containing the traceback (if any).

       The return value of this handler is ignored.

    .. method:: on_failure(self, exc, task_id, args, kwargs, einfo)
       :no-index:

       This is run by the worker when the task fails.

       :param exc: The exception raised by the task.
       :param task_id: Unique id of the failed task.
       :param args: Original arguments for the task that failed.
       :param kwargs: Original keyword arguments for the task
                       that failed.

       :keyword einfo: :class:`~billiard.einfo.ExceptionInfo`
                          instance, containing the traceback.

       The return value of this handler is ignored.

    .. method:: on_retry(self, exc, task_id, args, kwargs, einfo)
       :no-index:

       This is run by the worker when the task is to be retried.

       :param exc: The exception sent to :meth:`~@Task.retry`.
       :param task_id: Unique id of the retried task.
       :param args: Original arguments for the retried task.
       :param kwargs: Original keyword arguments for the retried task.

       :keyword einfo: :class:`~billiard.einfo.ExceptionInfo`
                       instance, containing the traceback.

       The return value of this handler is ignored.

    .. method:: on_success(self, retval, task_id, args, kwargs)
       :no-index:

       Run by the worker if the task executes successfully.

       :param retval: The return value of the task.
       :param task_id: Unique id of the executed task.
       :param args: Original arguments for the executed task.
       :param kwargs: Original keyword arguments for the executed task.

       The return value of this handler is ignored.

.. _task-requests-and-custom-requests:

请求和自定义请求
----------------------------

Requests and custom requests

.. tab:: 中文

    在收到执行任务的消息时， `worker <guide-workers>`:ref: 会创建一个
    `request <celery.worker.request.Request>`:class: 来表示这种需求。

    自定义任务类可以通过更改属性 `celery.app.task.Task.Request`:attr:
    来重写使用的请求类。你可以直接分配自定义请求类本身，或者
    它的完全限定名称。

    请求有多个职责。自定义请求类应覆盖所有这些职责——它们负责实际
    执行和跟踪任务。我们强烈推荐继承 `celery.worker.request.Request`:class:。

    当使用 `pre-forking worker <worker-concurrency>`:ref: 时，`~celery.worker.request.Request.on_timeout`:meth: 和
    `~celery.worker.request.Request.on_failure`:meth: 方法将在主工作进程中执行。
    应用程序可以利用这一功能来检测 `celery.app.task.Task.on_failure`:meth:
    未检测到的失败。

    例如，以下自定义请求类会检测并记录硬时间限制和其他失败。

    .. code-block:: python

        import logging
        from celery import Task
        from celery.worker.request import Request

        logger = logging.getLogger('my.package')

        class MyRequest(Request):
            '一个最小的自定义请求，用于记录失败和硬时间限制。'

            def on_timeout(self, soft, timeout):
                super(MyRequest, self).on_timeout(soft, timeout)
                if not soft:
                    logger.warning(
                        '任务 %s 强制执行了硬超时',
                        self.task.name
                    )

            def on_failure(self, exc_info, send_failed_event=True, return_ok=False):
                super().on_failure(
                    exc_info,
                    send_failed_event=send_failed_event,
                    return_ok=return_ok
                )
                logger.warning(
                    '任务 %s 检测到失败',
                    self.task.name
                )

        class MyTask(Task):
            Request = MyRequest  # 你可以使用 FQN 'my.package:MyRequest'

        @app.task(base=MyTask)
        def some_longrunning_task():
            # 发挥你的想象力

.. tab:: 英文

    Upon receiving a message to run a task, the `worker <guide-workers>`:ref:
    creates a `request <celery.worker.request.Request>`:class: to represent such
    demand.

    Custom task classes may override which request class to use by changing the
    attribute `celery.app.task.Task.Request`:attr:.  You may either assign the
    custom request class itself, or its fully qualified name.

    The request has several responsibilities.  Custom request classes should cover
    them all -- they are responsible to actually run and trace the task.  We
    strongly recommend to inherit from `celery.worker.request.Request`:class:.

    When using the `pre-forking worker <worker-concurrency>`:ref:, the methods
    `~celery.worker.request.Request.on_timeout`:meth: and
    `~celery.worker.request.Request.on_failure`:meth: are executed in the main
    worker process.  An application may leverage such facility to detect failures
    which are not detected using `celery.app.task.Task.on_failure`:meth:.

    As an example, the following custom request detects and logs hard time
    limits, and other failures.

    .. code-block:: python

        import logging
        from celery import Task
        from celery.worker.request import Request

        logger = logging.getLogger('my.package')

        class MyRequest(Request):
            'A minimal custom request to log failures and hard time limits.'

            def on_timeout(self, soft, timeout):
                super(MyRequest, self).on_timeout(soft, timeout)
                if not soft:
                    logger.warning(
                        'A hard timeout was enforced for task %s',
                        self.task.name
                    )

            def on_failure(self, exc_info, send_failed_event=True, return_ok=False):
                super().on_failure(
                    exc_info,
                    send_failed_event=send_failed_event,
                    return_ok=return_ok
                )
                logger.warning(
                    'Failure detected for task %s',
                    self.task.name
                )

        class MyTask(Task):
            Request = MyRequest  # you can use a FQN 'my.package:MyRequest'

        @app.task(base=MyTask)
        def some_longrunning_task():
            # use your imagination


.. _task-how-they-work:

工作原理
============

How it works

.. tab:: 中文

    以下是技术细节。虽然这部分内容不是你必须了解的，但你可能会感兴趣。

    所有定义的任务都会列在一个注册表中。注册表包含任务名称和对应的任务类的列表。
    你可以自己检查这个注册表：

    .. code-block:: pycon

        >>> from proj.celery import app
        >>> app.tasks
        {'celery.chord_unlock':
            <@task: celery.chord_unlock>,
        'celery.backend_cleanup':
            <@task: celery.backend_cleanup>,
        'celery.chord':
            <@task: celery.chord>}

    这是 Celery 内置任务的列表。请注意，只有在定义任务的模块被导入时，
    这些任务才会被注册。

    默认加载器会导入 :setting:`imports` 配置项中列出的所有模块。

    :meth:`@task` 装饰器负责将你的任务注册到应用程序的任务注册表中。

    当任务被发送时，实际上并不会发送函数代码，只会发送任务名称以便执行。
    当 Worker 收到消息时，它可以在任务注册表中查找该名称，找到执行代码。

    这意味着你的 Worker 应该始终与客户端使用相同的软件版本。这是一个缺点，
    但替代方案是一个尚未解决的技术挑战。

.. tab:: 英文

    Here come the technical details. This part isn't something you need to know,
    but you may be interested.

    All defined tasks are listed in a registry. The registry contains
    a list of task names and their task classes. You can investigate this registry
    yourself:

    .. code-block:: pycon

        >>> from proj.celery import app
        >>> app.tasks
        {'celery.chord_unlock':
            <@task: celery.chord_unlock>,
        'celery.backend_cleanup':
            <@task: celery.backend_cleanup>,
        'celery.chord':
            <@task: celery.chord>}

    This is the list of tasks built into Celery. Note that tasks
    will only be registered when the module they're defined in is imported.

    The default loader imports any modules listed in the
    :setting:`imports` setting.

    The :meth:`@task` decorator is responsible for registering your task
    in the applications task registry.

    When tasks are sent, no actual function code is sent with it, just the name
    of the task to execute. When the worker then receives the message it can look
    up the name in its task registry to find the execution code.

    This means that your workers should always be updated with the same software
    as the client. This is a drawback, but the alternative is a technical
    challenge that's yet to be solved.

.. _task-best-practices:

技巧和最佳实践
=======================

Tips and Best Practices

.. _task-ignore_results:

忽略不需要的结果
-----------------------------

Ignore results you don't want

.. tab:: 中文

    如果你不关心任务的结果，务必设置 :attr:`~@Task.ignore_result` 选项，
    因为存储结果会浪费时间和资源。

    .. code-block:: python

        @app.task(ignore_result=True)
        def mytask():
            something()

    也可以使用 :setting:`task_ignore_result` 配置项全局禁用结果存储。

    .. versionadded::4.2

    通过在调用 ``apply_async`` 时传递 ``ignore_result`` 布尔参数，可以在每次执行时启用/禁用结果存储。

    .. code-block:: python

        @app.task
        def mytask(x, y):
            return x + y

        # 不会存储结果
        result = mytask.apply_async((1, 2), ignore_result=True)
        print(result.get()) # -> None

        # 会存储结果
        result = mytask.apply_async((1, 2), ignore_result=False)
        print(result.get()) # -> 3

    默认情况下，当配置了结果后端时，任务会*不忽略结果*（``ignore_result=False``）。

    选项优先级顺序如下：

    1. 全局 :setting:`task_ignore_result`
    2. :attr:`~@Task.ignore_result` 选项
    3. 任务执行选项 ``ignore_result``

.. tab:: 英文

    If you don't care about the results of a task, be sure to set the
    :attr:`~@Task.ignore_result` option, as storing results
    wastes time and resources.

    .. code-block:: python

        @app.task(ignore_result=True)
        def mytask():
            something()

    Results can even be disabled globally using the :setting:`task_ignore_result`
    setting.

    .. versionadded::4.2

    Results can be enabled/disabled on a per-execution basis, by passing the ``ignore_result`` boolean parameter,
    when calling ``apply_async``.

    .. code-block:: python

        @app.task
        def mytask(x, y):
            return x + y

        # No result will be stored
        result = mytask.apply_async((1, 2), ignore_result=True)
        print(result.get()) # -> None

        # Result will be stored
        result = mytask.apply_async((1, 2), ignore_result=False)
        print(result.get()) # -> 3

    By default tasks will *not ignore results* (``ignore_result=False``) when a result backend is configured.


    The option precedence order is the following:

    1. Global :setting:`task_ignore_result`
    2. :attr:`~@Task.ignore_result` option
    3. Task execution option ``ignore_result``

更多优化技巧
----------------------

More optimization tips

.. tab:: 中文

    您可以在 :ref:`优化指南 <guide-optimizing>` 中找到更多优化技巧。

.. tab:: 英文

    You find additional optimization tips in the :ref:`Optimizing Guide <guide-optimizing>`.

.. _task-synchronous-subtasks:

避免启动同步子任务
------------------------------------

Avoid launching synchronous subtasks

.. tab:: 中文

    让一个任务等待另一个任务的结果是非常低效的，
    如果工作进程池耗尽，甚至可能导致死锁。

    相反，应该使你的设计异步化，例如使用 *回调*。

    **不推荐的做法**：

    .. code-block:: python

        @app.task
        def update_page_info(url):
            page = fetch_page.delay(url).get()
            info = parse_page.delay(page).get()
            store_page_info.delay(url, info)

        @app.task
        def fetch_page(url):
            return myhttplib.get(url)

        @app.task
        def parse_page(page):
            return myparser.parse_document(page)

        @app.task
        def store_page_info(url, info):
            return PageInfo.objects.create(url, info)


    **推荐的做法**：

    .. code-block:: python

        def update_page_info(url):
            # fetch_page -> parse_page -> store_page
            chain = fetch_page.s(url) | parse_page.s() | store_page_info.s(url)
            chain()

        @app.task()
        def fetch_page(url):
            return myhttplib.get(url)

        @app.task()
        def parse_page(page):
            return myparser.parse_document(page)

        @app.task(ignore_result=True)
        def store_page_info(info, url):
            PageInfo.objects.create(url=url, info=info)


    在这里，我通过将不同的 :func:`~celery.signature` 任务链接起来创建了任务链。
    你可以在 :ref:`designing-workflows` 中阅读有关任务链和其他强大构造的信息。

    默认情况下，Celery 不允许在任务内同步运行子任务，
    但在极少数或极端情况下，你可能需要这样做。
    **警告**：
    启用子任务同步执行不推荐！

    .. code-block:: python

        @app.task
        def update_page_info(url):
            page = fetch_page.delay(url).get(disable_sync_subtasks=False)
            info = parse_page.delay(page).get(disable_sync_subtasks=False)
            store_page_info.delay(url, info)

        @app.task
        def fetch_page(url):
            return myhttplib.get(url)

        @app.task
        def parse_page(page):
            return myparser.parse_document(page)

        @app.task
        def store_page_info(url, info):
            return PageInfo.objects.create(url, info)

.. tab:: 英文

    Having a task wait for the result of another task is really inefficient,
    and may even cause a deadlock if the worker pool is exhausted.

    Make your design asynchronous instead, for example by using *callbacks*.

    **Bad**:

    .. code-block:: python

        @app.task
        def update_page_info(url):
            page = fetch_page.delay(url).get()
            info = parse_page.delay(page).get()
            store_page_info.delay(url, info)

        @app.task
        def fetch_page(url):
            return myhttplib.get(url)

        @app.task
        def parse_page(page):
            return myparser.parse_document(page)

        @app.task
        def store_page_info(url, info):
            return PageInfo.objects.create(url, info)


    **Good**:

    .. code-block:: python

        def update_page_info(url):
            # fetch_page -> parse_page -> store_page
            chain = fetch_page.s(url) | parse_page.s() | store_page_info.s(url)
            chain()

        @app.task()
        def fetch_page(url):
            return myhttplib.get(url)

        @app.task()
        def parse_page(page):
            return myparser.parse_document(page)

        @app.task(ignore_result=True)
        def store_page_info(info, url):
            PageInfo.objects.create(url=url, info=info)


    Here I instead created a chain of tasks by linking together
    different :func:`~celery.signature`'s.
    You can read about chains and other powerful constructs
    at :ref:`designing-workflows`.

    By default Celery will not allow you to run subtasks synchronously within a task,
    but in rare or extreme cases you might need to do so.
    **WARNING**:
    enabling subtasks to run synchronously is not recommended!

    .. code-block:: python

        @app.task
        def update_page_info(url):
            page = fetch_page.delay(url).get(disable_sync_subtasks=False)
            info = parse_page.delay(page).get(disable_sync_subtasks=False)
            store_page_info.delay(url, info)

        @app.task
        def fetch_page(url):
            return myhttplib.get(url)

        @app.task
        def parse_page(page):
            return myparser.parse_document(page)

        @app.task
        def store_page_info(url, info):
            return PageInfo.objects.create(url, info)


.. _task-performance-and-strategies:

性能和策略
==========================

Performance and Strategies

.. _task-granularity:

粒度
-----------

Granularity

.. tab:: 中文

    任务粒度是每个子任务所需的计算量。
    通常来说，将问题拆分成许多小任务比将其拆分成少数几个长时间运行的任务要好。

    使用较小的任务，你可以并行处理更多的任务，并且这些任务的运行时间不会长到阻塞工作进程，进而影响其它等待任务的处理。

    然而，执行任务确实会有开销。需要发送消息，数据可能不在本地等等。所以，如果任务过于细粒度，添加的开销可能会消除任何潜在的好处。

    .. seealso::

        《 `并发的艺术 <Art of Concurrency>`_ 》一书专门讨论了任务粒度这一主题 [AOC1]_ 。

.. tab:: 英文

    The task granularity is the amount of computation needed by each subtask.
    In general it is better to split the problem up into many small tasks rather
    than have a few long running tasks.

    With smaller tasks you can process more tasks in parallel and the tasks
    won't run long enough to block the worker from processing other waiting tasks.

    However, executing a task does have overhead. A message needs to be sent, data
    may not be local, etc. So if the tasks are too fine-grained the
    overhead added probably removes any benefit.

    .. seealso::

        The book `Art of Concurrency`_ has a section dedicated to the topic
        of task granularity [AOC1]_.

.. _`Art of Concurrency`: http://oreilly.com/catalog/9780596521547

.. [AOC1] Breshears, Clay. Section 2.2.1, "The Art of Concurrency".
   O'Reilly Media, Inc. May 15, 2009. ISBN-13 978-0-596-52153-0.

.. _task-data-locality:

数据本地性
-------------

Data locality

.. tab:: 中文

    处理任务的工作进程应该尽可能接近数据。最好的情况是数据存在内存中，最坏的情况是需要从另一个大陆进行完全传输。

    如果数据距离较远，可以尝试在该位置运行另一个工作进程，或者如果不可能的话，可以缓存经常使用的数据，或者预加载你知道将会使用的数据。

    在工作进程之间共享数据的最简单方法是使用分布式缓存系统，比如 `memcached`_。

    .. seealso::

        Jim Gray 的论文 `分布式计算经济 <Distributed Computing Economics>`_ 是关于数据本地化主题的极好介绍。

.. tab:: 英文

    The worker processing the task should be as close to the data as
    possible. The best would be to have a copy in memory, the worst would be a
    full transfer from another continent.

    If the data is far away, you could try to run another worker at location, or
    if that's not possible - cache often used data, or preload data you know
    is going to be used.

    The easiest way to share data between workers is to use a distributed cache
    system, like `memcached`_.

    .. seealso::

        The paper `Distributed Computing Economics`_ by Jim Gray is an excellent
        introduction to the topic of data locality.

.. _`Distributed Computing Economics`:
    http://research.microsoft.com/pubs/70001/tr-2003-24.pdf

.. _`memcached`: http://memcached.org/

.. _task-state:

状态
-----

State

.. tab:: 中文

    由于 Celery 是一个分布式系统，你无法知道任务将在哪个进程或机器上执行。你甚至无法知道任务是否会及时运行。

    古老的异步格言告诉我们：“确认世界的状态是任务的责任”。这意味着，世界观可能在任务请求之后发生变化，因此任务有责任确保世界是应该有的样子；如果你有一个重新索引搜索引擎的任务，并且该搜索引擎应该每隔最多 5 分钟才重新索引一次，那么它必须由任务来确认，而不是调用者。

    另一个问题是 Django 模型对象。它们不应该作为任务的参数传递。通常最好在任务运行时重新从数据库中获取对象，因为使用旧数据可能会导致竞争条件。

    设想以下场景，你有一篇文章和一个任务，该任务自动扩展其中的一些缩写：

    .. code-block:: python

        class Article(models.Model):
            title = models.CharField()
            body = models.TextField()

        @app.task
        def expand_abbreviations(article):
            article.body.replace('MyCorp', 'My Corporation')
            article.save()

    首先，一个作者创建并保存了一篇文章，然后该作者点击按钮，启动了缩写扩展任务：

    .. code-block:: pycon

        >>> article = Article.objects.get(id=102)
        >>> expand_abbreviations.delay(article)

    现在，队列非常忙碌，因此任务将在 2 分钟后才执行。
    与此同时，另一个作者对文章进行了修改，因此，当任务最终执行时，文章的正文被恢复到了旧版本，因为任务参数中的文章正文是旧的。

    解决竞争条件很容易，只需改用文章的 ID，并在任务体内重新获取文章：

    .. code-block:: python

        @app.task
        def expand_abbreviations(article_id):
            article = Article.objects.get(id=article_id)
            article.body.replace('MyCorp', 'My Corporation')
            article.save()

    .. code-block:: pycon

        >>> expand_abbreviations.delay(article_id)

    这种方法甚至可能带来性能上的好处，因为发送大消息可能非常昂贵。

.. tab:: 英文

    Since Celery is a distributed system, you can't know which process, or
    on what machine the task will be executed. You can't even know if the task will
    run in a timely manner.

    The ancient async sayings tells us that “asserting the world is the
    responsibility of the task”. What this means is that the world view may
    have changed since the task was requested, so the task is responsible for
    making sure the world is how it should be;  If you have a task
    that re-indexes a search engine, and the search engine should only be
    re-indexed at maximum every 5 minutes, then it must be the tasks
    responsibility to assert that, not the callers.

    Another gotcha is Django model objects. They shouldn't be passed on as
    arguments to tasks. It's almost always better to re-fetch the object from
    the database when the task is running instead,  as using old data may lead
    to race conditions.

    Imagine the following scenario where you have an article and a task
    that automatically expands some abbreviations in it:

    .. code-block:: python

        class Article(models.Model):
            title = models.CharField()
            body = models.TextField()

        @app.task
        def expand_abbreviations(article):
            article.body.replace('MyCorp', 'My Corporation')
            article.save()

    First, an author creates an article and saves it, then the author
    clicks on a button that initiates the abbreviation task:

    .. code-block:: pycon

        >>> article = Article.objects.get(id=102)
        >>> expand_abbreviations.delay(article)

    Now, the queue is very busy, so the task won't be run for another 2 minutes.
    In the meantime another author makes changes to the article, so
    when the task is finally run, the body of the article is reverted to the old
    version because the task had the old body in its argument.

    Fixing the race condition is easy, just use the article id instead, and
    re-fetch the article in the task body:

    .. code-block:: python

        @app.task
        def expand_abbreviations(article_id):
            article = Article.objects.get(id=article_id)
            article.body.replace('MyCorp', 'My Corporation')
            article.save()

    .. code-block:: pycon

        >>> expand_abbreviations.delay(article_id)

    There might even be performance benefits to this approach, as sending large
    messages may be expensive.

.. _task-database-transactions:

数据库事务
---------------------

Database transactions

.. tab:: 中文

    我们来看另一个例子：

    .. code-block:: python

        from django.db import transaction
        from django.http import HttpResponseRedirect

        @transaction.atomic
        def create_article(request):
            article = Article.objects.create()
            expand_abbreviations.delay(article.pk)
            return HttpResponseRedirect('/articles/')

    这是一个 Django 视图，它在数据库中创建了一个文章对象，
    然后将主键传递给任务。它使用了 `transaction.atomic` 装饰器，当视图返回时，事务会被提交，或者如果视图抛出异常，事务会被回滚。

    这里有一个竞争条件，因为事务是原子的。这意味着文章对象在视图函数返回响应之前不会持久化到数据库。如果异步任务在事务提交之前开始执行，它可能会尝试在文章对象不存在时查询该对象。为了解决这个问题，我们需要确保在触发任务之前提交事务。

    解决方法是使用 :meth:`~celery.contrib.django.task.DjangoTask.delay_on_commit`：

    .. code-block:: python

        from django.db import transaction
        from django.http import HttpResponseRedirect

        @transaction.atomic
        def create_article(request):
            article = Article.objects.create()
            expand_abbreviations.delay_on_commit(article.pk)
            return HttpResponseRedirect('/articles/')

    该方法在 Celery 5.4 中添加。它是一个快捷方式，使用 Django 的 ``on_commit`` 回调，在所有事务成功提交后启动你的 Celery 任务。

.. tab:: 英文

    Let's have a look at another example:
    
    .. code-block:: python
    
        from django.db import transaction
        from django.http import HttpResponseRedirect
    
        @transaction.atomic
        def create_article(request):
            article = Article.objects.create()
            expand_abbreviations.delay(article.pk)
            return HttpResponseRedirect('/articles/')
    
    This is a Django view creating an article object in the database,
    then passing the primary key to a task. It uses the `transaction.atomic`
    decorator, that will commit the transaction when the view returns, or
    roll back if the view raises an exception.
    
    There is a race condition because transactions are atomic. This means the article object is not persisted to the database until after the view function returns a response. If the asynchronous task starts executing before the transaction is committed, it may attempt to query the article object before it exists. To prevent this, we need to ensure that the transaction is committed before triggering the task.
    
    The solution is to use :meth:`~celery.contrib.django.task.DjangoTask.delay_on_commit` instead：
    
    .. code-block:: python
    
        from django.db import transaction
        from django.http import HttpResponseRedirect
    
        @transaction.atomic
        def create_article(request):
            article = Article.objects.create()
            expand_abbreviations.delay_on_commit(article.pk)
            return HttpResponseRedirect('/articles/')
    
    This method was added in Celery 5.4. It's a shortcut that uses Django's
    ``on_commit`` callback to launch your Celery task once all transactions
    have been committed successfully.

使用 Celery 5.4 及以下版本
~~~~~~~~~~~~~~~~

With Celery <5.4

.. tab:: 中文

    如果你使用的是较旧版本的 Celery，可以直接使用 Django 的回调来复制这种行为，如下所示：

    .. code-block:: python

        import functools
        from django.db import transaction
        from django.http import HttpResponseRedirect

        @transaction.atomic
        def create_article(request):
            article = Article.objects.create()
            transaction.on_commit(
                functools.partial(expand_abbreviations.delay, article.pk)
            )
            return HttpResponseRedirect('/articles/')

    .. note::

        ``on_commit`` 在 Django 1.9 及以上版本中可用。如果你使用的是更早版本，则可以通过 `django-transaction-hooks`_ 库来添加对其的支持。

.. tab:: 英文

    If you're using an older version of Celery, you can replicate this behaviour
    using the Django callback directly as follows:

    .. code-block:: python

        import functools
        from django.db import transaction
        from django.http import HttpResponseRedirect

        @transaction.atomic
        def create_article(request):
            article = Article.objects.create()
            transaction.on_commit(
                functools.partial(expand_abbreviations.delay, article.pk)
            )
            return HttpResponseRedirect('/articles/')

    .. note::

        ``on_commit`` is available in Django 1.9 and above, if you are using a
        version prior to that then the `django-transaction-hooks`_ library
        adds support for this.

.. _`django-transaction-hooks`: https://github.com/carljm/django-transaction-hooks

.. _task-example:

示例
=======

Example

.. tab:: 中文

    让我们看一个实际的例子：一个博客，评论需要进行垃圾邮件过滤。当评论被创建时，垃圾邮件过滤器在后台运行，因此用户无需等待其完成。

    我有一个 Django 博客应用，允许对博客文章进行评论。下面是我为这个应用描述的部分模型、视图和任务。

.. tab:: 英文

    Let's take a real world example: a blog where comments posted need to be
    filtered for spam. When the comment is created, the spam filter runs in the
    background, so the user doesn't have to wait for it to finish.

    I have a Django blog application allowing comments
    on blog posts. I'll describe parts of the models/views and tasks for this
    application.

``blog/models.py``
------------------

.. tab:: 中文

    评论模型如下所示：

    .. code-block:: python

        from django.db import models
        from django.utils.translation import ugettext_lazy as _


        class Comment(models.Model):
            name = models.CharField(_('name'), max_length=64)
            email_address = models.EmailField(_('email address'))
            homepage = models.URLField(_('home page'),
                                    blank=True, verify_exists=False)
            comment = models.TextField(_('comment'))
            pub_date = models.DateTimeField(_('Published date'),
                                            editable=False, auto_add_now=True)
            is_spam = models.BooleanField(_('spam?'),
                                        default=False, editable=False)

            class Meta:
                verbose_name = _('comment')
                verbose_name_plural = _('comments')


    在发表评论的视图中，我首先将评论写入数据库，然后在后台启动垃圾邮件过滤任务。

.. tab:: 英文

    The comment model looks like this:

    .. code-block:: python

        from django.db import models
        from django.utils.translation import ugettext_lazy as _


        class Comment(models.Model):
            name = models.CharField(_('name'), max_length=64)
            email_address = models.EmailField(_('email address'))
            homepage = models.URLField(_('home page'),
                                    blank=True, verify_exists=False)
            comment = models.TextField(_('comment'))
            pub_date = models.DateTimeField(_('Published date'),
                                            editable=False, auto_add_now=True)
            is_spam = models.BooleanField(_('spam?'),
                                        default=False, editable=False)

            class Meta:
                verbose_name = _('comment')
                verbose_name_plural = _('comments')


    In the view where the comment is posted, I first write the comment
    to the database, then I launch the spam filter task in the background.

.. _task-example-blog-views:

``blog/views.py``
-----------------

.. tab:: 中文

    .. code-block:: python

        from django import forms
        from django.http import HttpResponseRedirect
        from django.template.context import RequestContext
        from django.shortcuts import get_object_or_404, render_to_response

        from blog import tasks
        from blog.models import Comment


        class CommentForm(forms.ModelForm):

            class Meta:
                model = Comment


        def add_comment(request, slug, template_name='comments/create.html'):
            post = get_object_or_404(Entry, slug=slug)
            remote_addr = request.META.get('REMOTE_ADDR')

            if request.method == 'post':
                form = CommentForm(request.POST, request.FILES)
                if form.is_valid():
                    comment = form.save()
                    # 异步检查垃圾邮件。
                    tasks.spam_filter.delay(comment_id=comment.id,
                                            remote_addr=remote_addr)
                    return HttpResponseRedirect(post.get_absolute_url())
            else:
                form = CommentForm()

            context = RequestContext(request, {'form': form})
            return render_to_response(template_name, context_instance=context)


    为了过滤评论中的垃圾邮件，我使用了 `Akismet`_ ，这是一个用于过滤 `Wordpress` 免费博客平台中发布评论的垃圾邮件服务。 `Akismet`_ 对个人使用是免费的，但商业使用需要付费。你需要注册该服务以获得 API 密钥。

    为了调用 `Akismet`_ 的 API，我使用了 `Michael Foord`_ 编写的 `akismet.py`_ 库。

.. tab:: 英文

    .. code-block:: python

        from django import forms
        from django.http import HttpResponseRedirect
        from django.template.context import RequestContext
        from django.shortcuts import get_object_or_404, render_to_response

        from blog import tasks
        from blog.models import Comment


        class CommentForm(forms.ModelForm):

            class Meta:
                model = Comment


        def add_comment(request, slug, template_name='comments/create.html'):
            post = get_object_or_404(Entry, slug=slug)
            remote_addr = request.META.get('REMOTE_ADDR')

            if request.method == 'post':
                form = CommentForm(request.POST, request.FILES)
                if form.is_valid():
                    comment = form.save()
                    # Check spam asynchronously.
                    tasks.spam_filter.delay(comment_id=comment.id,
                                            remote_addr=remote_addr)
                    return HttpResponseRedirect(post.get_absolute_url())
            else:
                form = CommentForm()

            context = RequestContext(request, {'form': form})
            return render_to_response(template_name, context_instance=context)


    To filter spam in comments I use `Akismet`_, the service
    used to filter spam in comments posted to the free blog platform
    `Wordpress`. `Akismet`_ is free for personal use, but for commercial use you
    need to pay. You have to sign up to their service to get an API key.

    To make API calls to `Akismet`_ I use the `akismet.py`_ library written by
    `Michael Foord`_.

.. _task-example-blog-tasks:

``blog/tasks.py``
-----------------

.. code-block:: python

    from celery import Celery

    from akismet import Akismet

    from django.core.exceptions import ImproperlyConfigured
    from django.contrib.sites.models import Site

    from blog.models import Comment


    app = Celery(broker='amqp://')


    @app.task
    def spam_filter(comment_id, remote_addr=None):
        logger = spam_filter.get_logger()
        logger.info('Running spam filter for comment %s', comment_id)

        comment = Comment.objects.get(pk=comment_id)
        current_domain = Site.objects.get_current().domain
        akismet = Akismet(settings.AKISMET_KEY, 'http://{0}'.format(domain))
        if not akismet.verify_key():
            raise ImproperlyConfigured('Invalid AKISMET_KEY')


        is_spam = akismet.comment_check(user_ip=remote_addr,
                            comment_content=comment.comment,
                            comment_author=comment.name,
                            comment_author_email=comment.email_address)
        if is_spam:
            comment.is_spam = True
            comment.save()

        return is_spam

.. _`Akismet`: http://akismet.com/faq/
.. _`akismet.py`: http://www.voidspace.org.uk/downloads/akismet.py
.. _`Michael Foord`: http://www.voidspace.org.uk/
.. _`exponential backoff`: https://en.wikipedia.org/wiki/Exponential_backoff
.. _`jitter`: https://en.wikipedia.org/wiki/Jitter
.. _`Pydantic`: https://docs.pydantic.dev/
