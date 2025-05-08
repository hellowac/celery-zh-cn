.. _signals:

=======
信号
=======

Signals

.. tab:: 中文

    信号（Signals）允许解耦的应用程序在应用的其他部分发生某些操作时接收通知。

    Celery 内置了许多信号，您的应用程序可以通过钩入这些信号来增强某些行为。

.. tab:: 英文

    Signals allow decoupled applications to receive notifications when
    certain actions occur elsewhere in the application.

    Celery ships with many signals that your application can hook into
    to augment behavior of certain actions.

.. _signal-basics:

基础
======

Basics

.. tab:: 中文

    多种类型的事件都会触发信号，您可以连接这些信号，在其触发时执行相应操作。

    以下是连接 :signal:`after_task_publish` 信号的示例：

    .. code-block:: python

        from celery.signals import after_task_publish

        @after_task_publish.connect
        def task_sent_handler(sender=None, headers=None, body=None, **kwargs):
            # 任务信息位于 headers 中（任务消息使用协议版本 2）
            info = headers if 'task' in headers else body
            print('after_task_publish for task id {info[id]}'.format(
                info=info,
            ))

    某些信号还支持按 sender 进行过滤。例如，:signal:`after_task_publish` 信号
    使用任务名作为 sender，因此通过为
    :class:`~celery.utils.dispatch.signal.Signal.connect` 方法提供 ``sender`` 参数，
    可以让处理器仅在名称为 `"proj.tasks.add"` 的任务被发布时被调用：

    .. code-block:: python

        @after_task_publish.connect(sender='proj.tasks.add')
        def task_sent_handler(sender=None, headers=None, body=None, **kwargs):
            # 任务信息位于 headers 中（任务消息使用协议版本 2）
            info = headers if 'task' in headers else body
            print('after_task_publish for task id {info[id]}'.format(
                info=info,
            ))

    信号使用与 :mod:`django.core.dispatch` 相同的实现方式。因此，其他关键字参数（如 signal）
    默认也会传递给所有信号处理器。

    编写信号处理器的最佳实践是接受任意关键字参数（即 ``**kwargs``）。这样做可确保
    即使将来的 Celery 版本增加新参数，也不会破坏已有代码。

.. tab:: 英文

    Several kinds of events trigger signals, you can connect to these signals
    to perform actions as they trigger.

    Example connecting to the :signal:`after_task_publish` signal:

    .. code-block:: python

        from celery.signals import after_task_publish

        @after_task_publish.connect
        def task_sent_handler(sender=None, headers=None, body=None, **kwargs):
            # information about task are located in headers for task messages
            # using the task protocol version 2.
            info = headers if 'task' in headers else body
            print('after_task_publish for task id {info[id]}'.format(
                info=info,
            ))


    Some signals also have a sender you can filter by. For example the
    :signal:`after_task_publish` signal uses the task name as a sender, so by
    providing the ``sender`` argument to
    :class:`~celery.utils.dispatch.signal.Signal.connect` you can
    connect your handler to be called every time a task with name `"proj.tasks.add"`
    is published:

    .. code-block:: python

        @after_task_publish.connect(sender='proj.tasks.add')
        def task_sent_handler(sender=None, headers=None, body=None, **kwargs):
            # information about task are located in headers for task messages
            # using the task protocol version 2.
            info = headers if 'task' in headers else body
            print('after_task_publish for task id {info[id]}'.format(
                info=info,
            ))

    Signals use the same implementation as :mod:`django.core.dispatch`. As a
    result other keyword parameters (e.g., signal) are passed to all signal
    handlers by default.

    The best practice for signal handlers is to accept arbitrary keyword
    arguments (i.e., ``**kwargs``). That way new Celery versions can add additional
    arguments without breaking user code.

.. _signal-ref:

信号
=======

Signals

Task 信号
------------

Task Signals

.. signal:: before_task_publish

``before_task_publish``
~~~~~~~~~~~~~~~~~~~~~~~

.. tab:: 中文

    .. versionadded:: 3.1

    在任务被发布之前触发该信号。
    请注意，这是在发送任务的进程中执行的。

    Sender 为被发送的任务名称。

    提供的参数包括：

    * ``body``

      任务消息体。

      这是一个包含任务消息字段的映射，参见
      :ref:`message-protocol-task-v2` 和 :ref:`message-protocol-task-v1`
      获取可能定义字段的参考信息。

    * ``exchange``

      要发送到的交换机名称，或一个 :class:`~kombu.Exchange` 对象。

    * ``routing_key``

      发送消息时使用的路由键。

    * ``headers``

      应用层头部信息映射（可修改）。

    * ``properties``

      消息属性（可修改）。

    * ``declare``

      在发布消息前需声明的实体（:class:`~kombu.Exchange`、
      :class:`~kombu.Queue` 或 :class:`~kombu.binding`）列表。可修改。

    * ``retry_policy``

      重试策略映射。可为 :meth:`kombu.Connection.ensure` 方法的任意参数，亦可修改。

.. tab:: 英文

    .. versionadded:: 3.1

    Dispatched before a task is published.
    Note that this is executed in the process sending the task.

    Sender is the name of the task being sent.

    Provides arguments:

    * ``body``

      Task message body.

      This is a mapping containing the task message fields,
      see :ref:`message-protocol-task-v2`
      and :ref:`message-protocol-task-v1`
      for a reference of possible fields that can be defined.

    * ``exchange``

      Name of the exchange to send to or a :class:`~kombu.Exchange` object.

    * ``routing_key``

      Routing key to use when sending the message.

    * ``headers``

      Application headers mapping (can be modified).

    * ``properties``

      Message properties (can be modified)

    * ``declare``

      List of entities (:class:`~kombu.Exchange`,
      :class:`~kombu.Queue`, or :class:`~kombu.binding` to declare before
      publishing the message. Can be modified.

    * ``retry_policy``

      Mapping of retry options. Can be any argument to
      :meth:`kombu.Connection.ensure` and can be modified.

.. signal:: after_task_publish

``after_task_publish``
~~~~~~~~~~~~~~~~~~~~~~

.. tab:: 中文

    任务被发送到 broker 后将触发该信号。
    请注意，这是在发送任务的进程中执行的。

    Sender 为被发送的任务名称。

    提供的参数包括：

    * ``headers``

      任务消息的头部信息，参见
      :ref:`message-protocol-task-v2` 和 :ref:`message-protocol-task-v1`
      获取可能定义字段的参考信息。

    * ``body``

      任务消息体，参见
      :ref:`message-protocol-task-v2` 和 :ref:`message-protocol-task-v1`
      获取可能定义字段的参考信息。

    * ``exchange``

      所使用的交换机名称或 :class:`~kombu.Exchange` 对象。

    * ``routing_key``

      所使用的路由键。


.. tab:: 英文

    Dispatched when a task has been sent to the broker.
    Note that this is executed in the process that sent the task.

    Sender is the name of the task being sent.

    Provides arguments:

    * ``headers``

      The task message headers, see :ref:`message-protocol-task-v2`
      and :ref:`message-protocol-task-v1`
      for a reference of possible fields that can be defined.

    * ``body``

      The task message body, see :ref:`message-protocol-task-v2`
      and :ref:`message-protocol-task-v1`
      for a reference of possible fields that can be defined.

    * ``exchange``

      Name of the exchange or :class:`~kombu.Exchange` object used.

    * ``routing_key``

      Routing key used.

.. signal:: task_prerun

``task_prerun``
~~~~~~~~~~~~~~~

.. tab:: 中文

    任务执行前会触发该信号。

    Sender 为正在执行的任务对象。

    提供的参数包括：

    * ``task_id``

      将要执行的任务 ID。

    * ``task``

      正在执行的任务对象。

    * ``args``

      任务的位置参数。

    * ``kwargs``

      任务的关键字参数。

.. tab:: 英文

    Dispatched before a task is executed.

    Sender is the task object being executed.

    Provides arguments:

    * ``task_id``

      Id of the task to be executed.

    * ``task``

      The task being executed.

    * ``args``

      The tasks positional arguments.

    * ``kwargs``

      The tasks keyword arguments.

.. signal:: task_postrun

``task_postrun``
~~~~~~~~~~~~~~~~

.. tab:: 中文

    任务执行完毕后会触发该信号。

    Sender 为已执行的任务对象。

    提供的参数包括：

    * ``task_id``

      已执行任务的 ID。

    * ``task``

      已执行的任务对象。

    * ``args``

      任务的位置参数。

    * ``kwargs``

      任务的关键字参数。

    * ``retval``

      任务的返回值。

    * ``state``

      执行结果的状态名称。

.. tab:: 英文

    Dispatched after a task has been executed.

    Sender is the task object executed.

    Provides arguments:

    * ``task_id``

      Id of the task to be executed.

    * ``task``

      The task being executed.

    * ``args``

      The tasks positional arguments.

    * ``kwargs``

      The tasks keyword arguments.

    * ``retval``

      The return value of the task.

    * ``state``

      Name of the resulting state.

.. signal:: task_retry

``task_retry``
~~~~~~~~~~~~~~

.. tab:: 中文

    任务即将重试时会触发该信号。

    Sender 为任务对象。

    提供的参数包括：

    * ``request``

      当前任务请求对象。

    * ``reason``

      重试原因（通常为一个异常实例，但始终可强制转换为 :class:`str`）。

    * ``einfo``

      异常的详细信息，包括 traceback
      （一个 :class:`billiard.einfo.ExceptionInfo` 对象）。

.. tab:: 英文

    Dispatched when a task will be retried.

    Sender is the task object.

    Provides arguments:

    * ``request``

      The current task request.

    * ``reason``

      Reason for retry (usually an exception instance, but can always be
      coerced to :class:`str`).

    * ``einfo``

      Detailed exception information, including traceback
      (a :class:`billiard.einfo.ExceptionInfo` object).


.. signal:: task_success

``task_success``
~~~~~~~~~~~~~~~~

.. tab:: 中文

    任务执行成功后会触发该信号。

    Sender 为已执行的任务对象。

    提供的参数包括：

    * ``result``
    
      任务的返回值。

.. tab:: 英文

    Dispatched when a task succeeds.

    Sender is the task object executed.

    Provides arguments

    * ``result``
    
      Return value of the task.

.. signal:: task_failure

``task_failure``
~~~~~~~~~~~~~~~~

.. tab:: 中文

    任务执行失败后会触发该信号。

    Sender 为已执行的任务对象。

    提供的参数包括：

    * ``task_id``

      任务 ID。

    * ``exception``

      抛出的异常实例。

    * ``args``

      调用任务时使用的位置参数。

    * ``kwargs``

      调用任务时使用的关键字参数。

    * ``traceback``

      异常的堆栈跟踪对象。

    * ``einfo``

      一个 :class:`billiard.einfo.ExceptionInfo` 实例。


.. tab:: 英文

    Dispatched when a task fails.
    
    Sender is the task object executed.
    
    Provides arguments:
    
    * ``task_id``
    
      Id of the task.
    
    * ``exception``
    
      Exception instance raised.
    
    * ``args``
    
      Positional arguments the task was called with.
    
    * ``kwargs``
    
      Keyword arguments the task was called with.
    
    * ``traceback``
    
      Stack trace object.
    
    * ``einfo``
    
      The :class:`billiard.einfo.ExceptionInfo` instance.
    
.. signal:: task_internal_error
    
``task_internal_error``
~~~~~~~~~~~~~~~~~~~~~~~

.. tab:: 中文

    当任务执行期间发生 Celery 内部错误时，会触发该信号。

    Sender 为已执行的任务对象。

    提供的参数包括：

    * ``task_id``

      任务的 ID。

    * ``args``

      调用任务时使用的位置参数。

    * ``kwargs``

      调用任务时使用的关键字参数。

    * ``request``

      原始请求字典。
      提供该参数是因为在异常被抛出时，``task.request`` 可能尚未准备好。

    * ``exception``

      抛出的异常实例。

    * ``traceback``

      异常的堆栈跟踪对象。

    * ``einfo``

      一个 :class:`billiard.einfo.ExceptionInfo` 实例。

.. tab:: 英文

    Dispatched when an internal Celery error occurs while executing the task.

    Sender is the task object executed.

    Provides arguments:

    * ``task_id``

      Id of the task.

    * ``args``

      Positional arguments the task was called with.

    * ``kwargs``

      Keyword arguments the task was called with.

    * ``request``

      The original request dictionary.
      This is provided as the ``task.request`` may not be ready by the time
      the exception is raised.

    * ``exception``

      Exception instance raised.

    * ``traceback``

      Stack trace object.

    * ``einfo``

      The :class:`billiard.einfo.ExceptionInfo` instance.

.. signal:: task_received

``task_received``
~~~~~~~~~~~~~~~~~

.. tab:: 中文

    当任务从 broker 接收并准备好执行时，会触发该信号。

    Sender 为 consumer 对象。

    提供的参数包括：

    * ``request``

      这是一个 :class:`~celery.worker.request.Request` 实例，而不是
      ``task.request``。当使用 prefork 池时，该信号在父进程中触发，
      因此无法使用 ``task.request``，也不应该使用。请使用该对象，
      它们拥有许多相同的字段。

.. tab:: 英文

    Dispatched when a task is received from the broker and is ready for execution.

    Sender is the consumer object.

    Provides arguments:

    * ``request``

      This is a :class:`~celery.worker.request.Request` instance, and not
      ``task.request``. When using the prefork pool this signal
      is dispatched in the parent process, so ``task.request`` isn't available
      and shouldn't be used. Use this object instead, as they share many
      of the same fields.

.. signal:: task_revoked

``task_revoked``
~~~~~~~~~~~~~~~~

.. tab:: 中文

    当任务被 worker 撤销或终止时，会触发该信号。

    Sender 为被撤销或终止的任务对象。

    提供的参数包括：

    * ``request``

      这是一个 :class:`~celery.app.task.Context` 实例，而不是
      ``task.request``。当使用 prefork 池时，该信号在父进程中触发，
      因此无法使用 ``task.request``，也不应该使用。请使用该对象，
      它们拥有许多相同的字段。

    * ``terminated``

      如果任务是被终止的，则为 :const:`True`。

    * ``signum``

      用于终止任务的信号编号。如果该值为 :const:`None` 且
      ``terminated`` 为 :const:`True`，则应视为收到了 :sig:`TERM` 信号。

    * ``expired``

      如果任务已过期，则为 :const:`True`。


.. tab:: 英文

    Dispatched when a task is revoked/terminated by the worker.

    Sender is the task object revoked/terminated.

    Provides arguments:

    * ``request``

      This is a :class:`~celery.app.task.Context` instance, and not
      ``task.request``. When using the prefork pool this signal
      is dispatched in the parent process, so ``task.request`` isn't available
      and shouldn't be used. Use this object instead, as they share many
      of the same fields.

    * ``terminated``

       Set to :const:`True` if the task was terminated.

    * ``signum``

       Signal number used to terminate the task. If this is :const:`None` and
       terminated is :const:`True` then :sig:`TERM` should be assumed.

    * ``expired``

      Set to :const:`True` if the task expired.

.. signal:: task_unknown

``task_unknown``
~~~~~~~~~~~~~~~~

.. tab:: 中文

    当 worker 收到一个未注册任务的消息时，会触发该信号。

    Sender 为 worker 的 :class:`~celery.worker.consumer.Consumer` 实例。

    提供的参数包括：

    * ``name``

      未在注册表中找到的任务名称。

    * ``id``

      消息中的任务 ID。

    * ``message``

      原始消息对象。

    * ``exc``

      触发的错误。

.. tab:: 英文

    Dispatched when a worker receives a message for a task that's not registered.

    Sender is the worker :class:`~celery.worker.consumer.Consumer`.

    Provides arguments:

    * ``name``

      Name of task not found in registry.

    * ``id``

      The task id found in the message.

    * ``message``

      Raw message object.

    * ``exc``

      The error that occurred.

.. signal:: task_rejected

``task_rejected``
~~~~~~~~~~~~~~~~~

.. tab:: 中文

    当 worker 收到未知类型的消息，并尝试将其投递到某个任务队列时，会触发该信号。

    Sender 为 worker 的 :class:`~celery.worker.consumer.Consumer` 实例。

    提供的参数包括：

    * ``message``

      原始消息对象。

    * ``exc``

      触发的错误（如果有）。

.. tab:: 英文

    Dispatched when a worker receives an unknown type of message to one of its
    task queues.

    Sender is the worker :class:`~celery.worker.consumer.Consumer`.

    Provides arguments:

    * ``message``

      Raw message object.

    * ``exc``

      The error that occurred (if any).

App 信号
-----------

App Signals

.. signal:: import_modules

``import_modules``
~~~~~~~~~~~~~~~~~~

.. tab:: 中文

    当程序（如 worker、beat、shell 等）请求导入
    :setting:`include` 和 :setting:`imports` 设置中指定的模块时，会触发该信号。

    Sender 为应用实例。

.. tab:: 英文

    This signal is sent when a program (worker, beat, shell) etc, asks
    for modules in the :setting:`include` and :setting:`imports`
    settings to be imported.

    Sender is the app instance.

Worker 信号
--------------

Worker Signals

.. signal:: celeryd_after_setup

``celeryd_after_setup``
~~~~~~~~~~~~~~~~~~~~~~~

.. tab:: 中文

    该信号在 Worker 实例设置完成之后、调用 run 方法之前发送。这意味着通过 :option:`celery worker -Q` 选项启用的队列已生效，日志系统也已设置完成，等等。

    可用于添加自定义队列，这些队列将始终被消费，而不受 :option:`celery worker -Q` 选项限制。以下是一个示例，它为每个 Worker 设置了一个直连队列（direct queue），随后可以将任务路由到指定的 Worker：

    .. code-block:: python

        from celery.signals import celeryd_after_setup

        @celeryd_after_setup.connect
        def setup_direct_queue(sender, instance, **kwargs):
            queue_name = '{0}.dq'.format(sender)  # sender 是该 Worker 的节点名称（nodename）
            instance.app.amqp.queues.select_add(queue_name)

    提供的参数有：

    * ``sender``

      Worker 的节点名称。

    * ``instance``

      即将初始化的 :class:`celery.apps.worker.Worker` 实例。
      注意，此时仅设置了 :attr:`app` 与 :attr:`hostname`（节点名）属性，其余的 ``__init__`` 过程尚未执行。

    * ``conf``

      当前应用的配置对象。


.. tab:: 英文

    This signal is sent after the worker instance is set up, but before it
    calls run. This means that any queues from the :option:`celery worker -Q`
    option is enabled, logging has been set up and so on.

    It can be used to add custom queues that should always be consumed
    from, disregarding the :option:`celery worker -Q` option. Here's an example
    that sets up a direct queue for each worker, these queues can then be
    used to route a task to any specific worker:

    .. code-block:: python

        from celery.signals import celeryd_after_setup

        @celeryd_after_setup.connect
        def setup_direct_queue(sender, instance, **kwargs):
            queue_name = '{0}.dq'.format(sender)  # sender is the nodename of the worker
            instance.app.amqp.queues.select_add(queue_name)

    Provides arguments:

    * ``sender``

      Node name of the worker.

    * ``instance``

      This is the :class:`celery.apps.worker.Worker` instance to be initialized.
      Note that only the :attr:`app` and :attr:`hostname` (nodename) attributes have been
      set so far, and the rest of ``__init__`` hasn't been executed.

    * ``conf``

      The configuration of the current app.

.. signal:: celeryd_init

``celeryd_init``
~~~~~~~~~~~~~~~~

.. tab:: 中文
    
    这是 :program:`celery worker` 启动时发送的第一个信号。
    ``sender`` 是 Worker 的主机名，因此可以使用该信号进行特定 Worker 的配置：
    
    .. code-block:: python
    
        from celery.signals import celeryd_init
    
        @celeryd_init.connect(sender='worker12@example.com')
        def configure_worker12(conf=None, **kwargs):
            conf.task_default_rate_limit = '10/m'
    
    若要配置多个 Worker，可在连接时省略指定 sender：
    
    .. code-block:: python
    
        from celery.signals import celeryd_init
    
        @celeryd_init.connect
        def configure_workers(sender=None, conf=None, **kwargs):
            if sender in ('worker1@example.com', 'worker2@example.com'):
                conf.task_default_rate_limit = '10/m'
            if sender == 'worker3@example.com':
                conf.worker_prefetch_multiplier = 0
    
    提供的参数有：
    
    * ``sender``
    
      Worker 的节点名称。
    
    * ``instance``
    
      即将初始化的 :class:`celery.apps.worker.Worker` 实例。
      注意，此时仅设置了 :attr:`app` 与 :attr:`hostname`（节点名）属性，其余的 ``__init__`` 过程尚未执行。
    
    * ``conf``
    
      当前应用的配置对象。
    
    * ``options``
    
      通过命令行传递给 Worker 的选项（包括默认值）。

.. tab:: 英文

    This is the first signal sent when :program:`celery worker` starts up.
    The ``sender`` is the host name of the worker, so this signal can be used
    to setup worker specific configuration:

    .. code-block:: python

        from celery.signals import celeryd_init

        @celeryd_init.connect(sender='worker12@example.com')
        def configure_worker12(conf=None, **kwargs):
            conf.task_default_rate_limit = '10/m'

    or to set up configuration for multiple workers you can omit specifying a
    sender when you connect:

    .. code-block:: python

        from celery.signals import celeryd_init

        @celeryd_init.connect
        def configure_workers(sender=None, conf=None, **kwargs):
            if sender in ('worker1@example.com', 'worker2@example.com'):
                conf.task_default_rate_limit = '10/m'
            if sender == 'worker3@example.com':
                conf.worker_prefetch_multiplier = 0

    Provides arguments:

    * ``sender``

      Nodename of the worker.

    * ``instance``

      This is the :class:`celery.apps.worker.Worker` instance to be initialized.
      Note that only the :attr:`app` and :attr:`hostname` (nodename) attributes have been
      set so far, and the rest of ``__init__`` hasn't been executed.

    * ``conf``

      The configuration of the current app.

    * ``options``

      Options passed to the worker from command-line arguments (including
      defaults).

.. signal:: worker_init

``worker_init``
~~~~~~~~~~~~~~~

.. tab:: 中文

    在 worker 启动之前调度。

.. tab:: 英文

    Dispatched before the worker is started.

.. signal:: worker_before_create_process

``worker_before_create_process``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tab:: 中文
    
    在 prefork 模式下，新子进程创建前，在父进程中调度发送。
    可用于清理某些在 fork 时表现不佳的实例。
    
    .. code-block:: python
    
        @signals.worker_before_create_process.connect
        def clean_channels(**kwargs):
            grpc_singleton.clean_channel()

.. tab:: 英文

    Dispatched in the parent process, just before new child process is created in the prefork pool.
    It can be used to clean up instances that don't behave well when forking.

    .. code-block:: python

        @signals.worker_before_create_process.connect
        def clean_channels(**kwargs):
            grpc_singleton.clean_channel()

.. signal:: worker_ready

``worker_ready``
~~~~~~~~~~~~~~~~

.. tab:: 中文
    
    当 Worker 准备好接收任务时触发。

.. tab:: 英文

    Dispatched when the worker is ready to accept work.

.. signal:: heartbeat_sent

``heartbeat_sent``
~~~~~~~~~~~~~~~~~~

.. tab:: 中文
    
    当 Celery 向 Worker 发送心跳时触发。
    
    Sender 是 :class:`celery.worker.heartbeat.Heart` 实例。

.. tab:: 英文

    Dispatched when Celery sends a worker heartbeat.

    Sender is the :class:`celery.worker.heartbeat.Heart` instance.

.. signal:: worker_shutting_down

``worker_shutting_down``
~~~~~~~~~~~~~~~~~~~~~~~~

.. tab:: 中文
    
    当 Worker 开始关闭流程时触发。
    
    提供的参数有：
    
    * ``sig``
    
      收到的 POSIX 信号。
    
    * ``how``
    
      关闭方式，可能为 warm 或 cold。
    
    * ``exitcode``
    
      主进程退出时将使用的退出码。

.. tab:: 英文

    Dispatched when the worker begins the shutdown process.

    Provides arguments:

    * ``sig``

      The POSIX signal that was received.

    * ``how``

      The shutdown method, warm or cold.

    * ``exitcode``

      The exitcode that will be used when the main process exits.

.. signal:: worker_process_init

``worker_process_init``
~~~~~~~~~~~~~~~~~~~~~~~

.. tab:: 中文
    
    在所有进程池的子进程启动时触发。
    
    注意：绑定到该信号的处理函数不得阻塞超过 4 秒，否则该子进程会被视为启动失败并被终止。

.. tab:: 英文

    Dispatched in all pool child processes when they start.

    Note that handlers attached to this signal mustn't be blocking
    for more than 4 seconds, or the process will be killed assuming
    it failed to start.

.. signal:: worker_process_shutdown

``worker_process_shutdown``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tab:: 中文

    在所有进程池的子进程即将退出时触发。

    注意：不保证该信号一定会被发送；就像 :keyword:`finally` 代码块一样，无法保证在关闭时一定调用处理函数，且即使调用了，也可能会中断。

    提供的参数有：

    * ``pid``

      即将关闭的子进程的进程 ID。

    * ``exitcode``

      子进程退出时将使用的退出码。

.. tab:: 英文

    Dispatched in all pool child processes just before they exit.

    Note: There's no guarantee that this signal will be dispatched,
    similarly to :keyword:`finally` blocks it's impossible to guarantee that
    handlers will be called at shutdown, and if called it may be
    interrupted during.

    Provides arguments:

    * ``pid``

      The pid of the child process that's about to shutdown.

    * ``exitcode``

      The exitcode that'll be used when the child process exits.

.. signal:: worker_shutdown

``worker_shutdown``
~~~~~~~~~~~~~~~~~~~

.. tab:: 中文

    当 Worker 即将关闭时触发。


.. tab:: 英文

    Dispatched when the worker is about to shut down.

Beat 信号
------------

Beat Signals

.. signal:: beat_init

``beat_init``
~~~~~~~~~~~~~

.. tab:: 中文
    
    当 :program:`celery beat` 启动时（无论是独立运行还是内嵌运行）触发。
    
    Sender 是 :class:`celery.beat.Service` 实例。

.. tab:: 英文

    Dispatched when :program:`celery beat` starts (either standalone or embedded).

    Sender is the :class:`celery.beat.Service` instance.

.. signal:: beat_embedded_init

``beat_embedded_init``
~~~~~~~~~~~~~~~~~~~~~~

.. tab:: 中文
    
    当 :program:`celery beat` 以内嵌进程方式启动时，除了 :signal:`beat_init` 信号外还会发送此信号。
    
    Sender 是 :class:`celery.beat.Service` 实例。

.. tab:: 英文

    Dispatched in addition to the :signal:`beat_init` signal when :program:`celery
    beat` is started as an embedded process.

    Sender is the :class:`celery.beat.Service` instance.

事件信号
----------------

Eventlet Signals

.. signal:: eventlet_pool_started

``eventlet_pool_started``
~~~~~~~~~~~~~~~~~~~~~~~~~

.. tab:: 中文
    
    当 eventlet 进程池启动时发送。
    
    Sender 是 :class:`celery.concurrency.eventlet.TaskPool` 实例。

.. tab:: 英文

    Sent when the eventlet pool has been started.

    Sender is the :class:`celery.concurrency.eventlet.TaskPool` instance.

.. signal:: eventlet_pool_preshutdown

``eventlet_pool_preshutdown``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tab:: 中文
    
    当 Worker 关闭，并即将请求 eventlet 池等待剩余工作线程时发送。
    
    Sender 是 :class:`celery.concurrency.eventlet.TaskPool` 实例。

.. tab:: 英文

    Sent when the worker shutdown, just before the eventlet pool
    is requested to wait for remaining workers.

    Sender is the :class:`celery.concurrency.eventlet.TaskPool` instance.

.. signal:: eventlet_pool_postshutdown

``eventlet_pool_postshutdown``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tab:: 中文
    
    当池已完成 join 操作，Worker 即将关闭时发送。
    
    Sender 是 :class:`celery.concurrency.eventlet.TaskPool` 实例。

.. tab:: 英文

    Sent when the pool has been joined and the worker is ready to shutdown.

    Sender is the :class:`celery.concurrency.eventlet.TaskPool` instance.

.. signal:: eventlet_pool_apply

``eventlet_pool_apply``
~~~~~~~~~~~~~~~~~~~~~~~

.. tab:: 中文
    
    每当一个任务被提交到进程池时发送。
    
    Sender 是 :class:`celery.concurrency.eventlet.TaskPool` 实例。
    
    提供的参数有：
    
    * ``target``
    
      目标函数。
    
    * ``args``
    
      位置参数。
    
    * ``kwargs``
    
      关键字参数。

.. tab:: 英文

    Sent whenever a task is applied to the pool.

    Sender is the :class:`celery.concurrency.eventlet.TaskPool` instance.

    Provides arguments:

    * ``target``

      The target function.

    * ``args``

      Positional arguments.

    * ``kwargs``

      Keyword arguments.

日志信号
---------------

Logging Signals

.. signal:: setup_logging

``setup_logging``
~~~~~~~~~~~~~~~~~

.. tab:: 中文
    
    如果连接了此信号，Celery 将不会配置日志记录器，因此你可以使用此信号完全覆盖默认的日志配置。
    
    如果你只是希望在 Celery 的日志配置基础上进行增强，可以使用 :signal:`after_setup_logger` 与 :signal:`after_setup_task_logger` 信号。
    
    提供的参数有：
    
    * ``loglevel``
    
      日志对象的日志级别。
    
    * ``logfile``
    
      日志文件的文件名。
    
    * ``format``
    
      日志格式字符串。
    
    * ``colorize``
    
      指定日志消息是否使用颜色。

.. tab:: 英文

    Celery won't configure the loggers if this signal is connected,
    so you can use this to completely override the logging configuration
    with your own.

    If you'd like to augment the logging configuration setup by
    Celery then you can use the :signal:`after_setup_logger` and
    :signal:`after_setup_task_logger` signals.

    Provides arguments:

    * ``loglevel``

      The level of the logging object.

    * ``logfile``

      The name of the logfile.

    * ``format``

      The log format string.

    * ``colorize``

      Specify if log messages are colored or not.

.. signal:: after_setup_logger

``after_setup_logger``
~~~~~~~~~~~~~~~~~~~~~~

.. tab:: 中文
    
    在每个全局日志记录器（不包括任务日志记录器）设置完成后发送。
    用于增强日志配置。
    
    提供的参数有：
    
    * ``logger``
    
      日志记录器对象。
    
    * ``loglevel``
    
      日志对象的日志级别。
    
    * ``logfile``
    
      日志文件的文件名。
    
    * ``format``
    
      日志格式字符串。
    
    * ``colorize``
    
      指定日志消息是否使用颜色。

.. tab:: 英文

    Sent after the setup of every global logger (not task loggers).
    Used to augment logging configuration.

    Provides arguments:

    * ``logger``

      The logger object.

    * ``loglevel``

      The level of the logging object.

    * ``logfile``

      The name of the logfile.

    * ``format``

      The log format string.

    * ``colorize``

      Specify if log messages are colored or not.

.. signal:: after_setup_task_logger

``after_setup_task_logger``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tab:: 中文

    在每一个任务日志记录器完成设置后发送。
    用于增强日志配置。

    提供的参数有：

    * ``logger``

      日志记录器对象。

    * ``loglevel``

      日志对象的日志级别。

    * ``logfile``

      日志文件的文件名。

    * ``format``

      日志格式字符串。

    * ``colorize``

      指定日志消息是否使用颜色。


.. tab:: 英文

    Sent after the setup of every single task logger.
    Used to augment logging configuration.

    Provides arguments:

    * ``logger``

      The logger object.

    * ``loglevel``

      The level of the logging object.

    * ``logfile``

      The name of the logfile.

    * ``format``

      The log format string.

    * ``colorize``

      Specify if log messages are colored or not.

命令信号
---------------

Command signals

.. signal:: user_preload_options

``user_preload_options``
~~~~~~~~~~~~~~~~~~~~~~~~

.. tab:: 中文
    
    该信号在任何 Celery 命令行程序完成用户 preload 选项解析后发送。
    
    可用于为 :program:`celery` 主命令添加额外的命令行参数：
    
    .. code-block:: python
    
        from celery import Celery
        from celery import signals
        from celery.bin.base import Option
    
        app = Celery()
        app.user_options['preload'].add(Option(
            '--monitoring', action='store_true',
            help='Enable our external monitoring utility, blahblah',
        ))
    
        @signals.user_preload_options.connect
        def handle_preload_options(options, **kwargs):
            if options['monitoring']:
                enable_monitoring()
    
    Sender 是 :class:`~celery.bin.base.Command` 实例，其具体值取决于被调用的程序（例如，对于主命令，它将是 :class:`~celery.bin.celery.CeleryCommand` 对象）。
    
    提供的参数有：
    
    * ``app``
    
      应用实例。
    
    * ``options``
    
      已解析的用户 preload 选项的映射（包含默认值）。

.. tab:: 英文

    This signal is sent after any of the Celery command line programs
    are finished parsing the user preload options.

    It can be used to add additional command-line arguments to the
    :program:`celery` umbrella command:

    .. code-block:: python

        from celery import Celery
        from celery import signals
        from celery.bin.base import Option

        app = Celery()
        app.user_options['preload'].add(Option(
            '--monitoring', action='store_true',
            help='Enable our external monitoring utility, blahblah',
        ))

        @signals.user_preload_options.connect
        def handle_preload_options(options, **kwargs):
            if options['monitoring']:
                enable_monitoring()


    Sender is the :class:`~celery.bin.base.Command` instance, and the value depends
    on the program that was called (e.g., for the umbrella command it'll be
    a :class:`~celery.bin.celery.CeleryCommand`) object).

    Provides arguments:

    * ``app``

      The app instance.

    * ``options``

      Mapping of the parsed user preload options (with default values).

弃用信号
------------------

Deprecated Signals

.. signal:: task_sent

``task_sent``
~~~~~~~~~~~~~

.. tab:: 中文
    
    此信号已弃用，请改用 :signal:`after_task_publish`。

.. tab:: 英文

    This signal is deprecated, please use :signal:`after_task_publish` instead.
