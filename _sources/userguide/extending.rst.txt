.. _guide-extending:

==========================
扩展 和 Bootsteps
==========================


Extensions and Bootsteps



.. _extending-custom-consumers:

自定义消息消费者
========================

Custom Message Consumers

.. tab:: 中文

    你可能希望嵌入自定义的 Kombu 消费者（Consumer）来手动处理消息。

    为此，Celery 提供了一个特殊的 :class:`~celery.bootstep.ConsumerStep` bootstep 类，
    你只需定义 ``get_consumers`` 方法。该方法必须返回一个 :class:`kombu.Consumer` 对象的列表，
    这些消费者将在连接建立时启动：

    .. code-block:: python

        from celery import Celery
        from celery import bootsteps
        from kombu import Consumer, Exchange, Queue

        my_queue = Queue('custom', Exchange('custom'), 'routing_key')

        app = Celery(broker='amqp://')


        class MyConsumerStep(bootsteps.ConsumerStep):

            def get_consumers(self, channel):
                return [Consumer(channel,
                                queues=[my_queue],
                                callbacks=[self.handle_message],
                                accept=['json'])]

            def handle_message(self, body, message):
                print('收到消息: {0!r}'.format(body))
                message.ack()
        app.steps['consumer'].add(MyConsumerStep)

        def send_me_a_message(who, producer=None):
            with app.producer_or_acquire(producer) as producer:
                producer.publish(
                    {'hello': who},
                    serializer='json',
                    exchange=my_queue.exchange,
                    routing_key='routing_key',
                    declare=[my_queue],
                    retry=True,
                )

        if __name__ == '__main__':
            send_me_a_message('world!')


    .. note::

        Kombu Consumer 支持两种不同的消息回调分发机制。
        第一种是 ``callbacks`` 参数，它接受一个形如 ``(body, message)`` 的回调函数列表；
        第二种是 ``on_message`` 参数，它接受一个形如 ``(message,)`` 的单个回调函数。
        后者不会自动对消息进行解码与反序列化。

        .. code-block:: python

            def get_consumers(self, channel):
                return [Consumer(channel, queues=[my_queue],
                                on_message=self.on_message)]


            def on_message(self, message):
                payload = message.decode()
                print(
                    '收到消息: {0!r} {props!r} rawlen={s}'.format(
                    payload, props=message.properties, s=len(message.body),
                ))
                message.ack()

.. tab:: 英文

    You may want to embed custom Kombu consumers to manually process your messages.

    For that purpose a special :class:`~celery.bootstep.ConsumerStep` bootstep class
    exists, where you only need to define the ``get_consumers`` method, that must
    return a list of :class:`kombu.Consumer` objects to start
    whenever the connection is established:

    .. code-block:: python

        from celery import Celery
        from celery import bootsteps
        from kombu import Consumer, Exchange, Queue

        my_queue = Queue('custom', Exchange('custom'), 'routing_key')

        app = Celery(broker='amqp://')


        class MyConsumerStep(bootsteps.ConsumerStep):

            def get_consumers(self, channel):
                return [Consumer(channel,
                                queues=[my_queue],
                                callbacks=[self.handle_message],
                                accept=['json'])]

            def handle_message(self, body, message):
                print('Received message: {0!r}'.format(body))
                message.ack()
        app.steps['consumer'].add(MyConsumerStep)

        def send_me_a_message(who, producer=None):
            with app.producer_or_acquire(producer) as producer:
                producer.publish(
                    {'hello': who},
                    serializer='json',
                    exchange=my_queue.exchange,
                    routing_key='routing_key',
                    declare=[my_queue],
                    retry=True,
                )

        if __name__ == '__main__':
            send_me_a_message('world!')


    .. note::

        Kombu Consumers can take use of two different message callback dispatching
        mechanisms. The first one is the ``callbacks`` argument that accepts
        a list of callbacks with a ``(body, message)`` signature,
        the second one is the ``on_message`` argument that takes a single
        callback with a ``(message,)`` signature. The latter won't
        automatically decode and deserialize the payload.

        .. code-block:: python

            def get_consumers(self, channel):
                return [Consumer(channel, queues=[my_queue],
                                on_message=self.on_message)]


            def on_message(self, message):
                payload = message.decode()
                print(
                    'Received message: {0!r} {props!r} rawlen={s}'.format(
                    payload, props=message.properties, s=len(message.body),
                ))
                message.ack()

.. _extending-blueprints:

蓝图
==========

Blueprints

.. tab:: 中文

    Bootsteps 是一种为 worker 添加自定义功能的机制。
    一个 bootstep 是一个自定义类，它定义了一组钩子方法，用于在 worker 启动过程的不同阶段执行自定义操作。
    每个 bootstep 都属于某个 blueprint，worker 当前定义了两个 blueprint：**Worker** 和 **Consumer**

    ----------------------------------------------------------

    **图 A：** Worker 和 Consumer blueprint 中的 Bootsteps。
    从下往上，Worker blueprint 中的第一个步骤是 Timer，
    最后一个步骤是启动 Consumer blueprint，
    该 blueprint 将建立与 broker 的连接并开始消费消息。

.. tab:: 英文


    Bootsteps is a technique to add functionality to the workers.
    A bootstep is a custom class that defines hooks to do custom actions
    at different stages in the worker. Every bootstep belongs to a blueprint,
    and the worker currently defines two blueprints: **Worker**, and **Consumer**

    ----------------------------------------------------------

    **Figure A:** Bootsteps in the Worker and Consumer blueprints. Starting
                  from the bottom up the first step in the worker blueprint
                  is the Timer, and the last step is to start the Consumer blueprint,
                  that then establishes the broker connection and starts
                  consuming messages.

.. figure:: ../images/worker_graph_full.png

----------------------------------------------------------

.. _extending-worker_blueprint:

Worker
======

Worker

.. tab:: 中文

    Worker 是第一个启动的 blueprint，它会启动主要组件，如事件循环（event loop）、
    处理进程池（processing pool）、以及用于处理 ETA 任务和其他定时事件的 Timer。

    当 worker 完全启动后，会继续启动 Consumer blueprint，
    它负责设置任务的执行方式、连接 broker，并启动消息消费者。

    :class:`~celery.worker.WorkController` 是 worker 的核心实现类，
    它包含多个方法和属性，可供自定义 bootstep 使用。

.. tab:: 英文


    The Worker is the first blueprint to start, and with it starts major components like
    the event loop, processing pool, and the timer used for ETA tasks and other
    timed events.

    When the worker is fully started it continues with the Consumer blueprint,
    that sets up how tasks are executed, connects to the broker and starts
    the message consumers.

    The :class:`~celery.worker.WorkController` is the core worker implementation,
    and contains several methods and attributes that you can use in your bootstep.

.. _extending-worker_blueprint-attributes:

属性
----------

Attributes

.. tab:: 中文

    .. _extending-worker-app:

    .. attribute:: app

        当前的 app 实例。

    .. _extending-worker-hostname:

    .. attribute:: hostname

        Worker 的节点名称（例如：`worker1@example.com`）

    .. _extending-worker-blueprint:

    .. attribute:: blueprint

        这是该 worker 的 :class:`~celery.bootsteps.Blueprint` 对象。

    .. _extending-worker-hub:

    .. attribute:: hub

        事件循环对象（:class:`~kombu.asynchronous.Hub`）。你可以使用它在事件循环中注册回调。

        仅在支持异步 I/O 的传输方式中可用（如 amqp、redis），
        此时应设置 `worker.use_eventloop` 属性。

        要在自定义的 worker bootstep 中使用该属性，你的 bootstep 必须依赖 Hub bootstep：

        .. code-block:: python

            class WorkerStep(bootsteps.StartStopStep):
                requires = {'celery.worker.components:Hub'}

    .. _extending-worker-pool:

    .. attribute:: pool

        当前使用的进程 / eventlet / gevent / 线程池。
        参见 :class:`celery.concurrency.base.BasePool`。

        要在自定义的 worker bootstep 中使用该属性，你的 bootstep 必须依赖 Pool bootstep：

        .. code-block:: python

            class WorkerStep(bootsteps.StartStopStep):
                requires = {'celery.worker.components:Pool'}

    .. _extending-worker-timer:

    .. attribute:: timer

        用于调度函数的 :class:`~kombu.asynchronous.timer.Timer` 实例。

        要在自定义的 worker bootstep 中使用该属性，你的 bootstep 必须依赖 Timer bootstep：

        .. code-block:: python

            class WorkerStep(bootsteps.StartStopStep):
                requires = {'celery.worker.components:Timer'}

    .. _extending-worker-statedb:

    .. attribute:: statedb

        用于在 worker 重启之间持久化状态的 :class:`Database <celery.worker.state.Persistent>` 实例。

        仅在启用了 ``statedb`` 参数时才会定义该属性。

        要在自定义的 worker bootstep 中使用该属性，你的 bootstep 必须依赖 ``Statedb`` bootstep：

        .. code-block:: python

            class WorkerStep(bootsteps.StartStopStep):
                requires = {'celery.worker.components:Statedb'}

    .. _extending-worker-autoscaler:

    .. attribute:: autoscaler

        用于根据需要自动增加或减少进程数的
        :class:`~celery.worker.autoscaler.Autoscaler` 实例。

        仅在启用了 ``autoscale`` 参数时才会定义该属性。

        要在自定义的 worker bootstep 中使用该属性，你的 bootstep 必须依赖 `Autoscaler` bootstep：

        .. code-block:: python

            class WorkerStep(bootsteps.StartStopStep):
                requires = ('celery.worker.autoscaler:Autoscaler',)

    .. _extending-worker-autoreloader:

    .. attribute:: autoreloader

        用于在文件系统发生变更时自动重新加载用户代码的
        :class:`~celery.worker.autoreloader.Autoreloader` 实例。

        仅在启用了 ``autoreload`` 参数时才会定义该属性。
        要在自定义的 worker bootstep 中使用该属性，你的 bootstep 必须依赖 `Autoreloader` bootstep：

        .. code-block:: python

            class WorkerStep(bootsteps.StartStopStep):
                requires = ('celery.worker.autoreloader:Autoreloader',)


.. tab:: 英文

    .. attribute:: app
        :no-index:

        The current app instance.

    .. attribute:: hostname
        :no-index:

        The workers node name (e.g., `worker1@example.com`)

    .. attribute:: blueprint
        :no-index:

        This is the worker :class:`~celery.bootsteps.Blueprint`.

    .. attribute:: hub
        :no-index:

        Event loop object (:class:`~kombu.asynchronous.Hub`). You can use
        this to register callbacks in the event loop.

        This is only supported by async I/O enabled transports (amqp, redis),
        in which case the `worker.use_eventloop` attribute should be set.

        Your worker bootstep must require the Hub bootstep to use this:

        .. code-block:: python

            class WorkerStep(bootsteps.StartStopStep):
                requires = {'celery.worker.components:Hub'}

    .. attribute:: pool
        :no-index:

        The current process/eventlet/gevent/thread pool.
        See :class:`celery.concurrency.base.BasePool`.

        Your worker bootstep must require the Pool bootstep to use this:

        .. code-block:: python

            class WorkerStep(bootsteps.StartStopStep):
                requires = {'celery.worker.components:Pool'}

    .. attribute:: timer
        :no-index:

        :class:`~kombu.asynchronous.timer.Timer` used to schedule functions.

        Your worker bootstep must require the Timer bootstep to use this:

        .. code-block:: python

            class WorkerStep(bootsteps.StartStopStep):
                requires = {'celery.worker.components:Timer'}

    .. attribute:: statedb
        :no-index:

        :class:`Database <celery.worker.state.Persistent>`` to persist state between
        worker restarts.

        This is only defined if the ``statedb`` argument is enabled.

        Your worker bootstep must require the ``Statedb`` bootstep to use this:

        .. code-block:: python

            class WorkerStep(bootsteps.StartStopStep):
                requires = {'celery.worker.components:Statedb'}

    .. attribute:: autoscaler
        :no-index:

        :class:`~celery.worker.autoscaler.Autoscaler` used to automatically grow
        and shrink the number of processes in the pool.

        This is only defined if the ``autoscale`` argument is enabled.

        Your worker bootstep must require the `Autoscaler` bootstep to use this:

        .. code-block:: python

            class WorkerStep(bootsteps.StartStopStep):
                requires = ('celery.worker.autoscaler:Autoscaler',)

    .. attribute:: autoreloader
        :no-index:

        :class:`~celery.worker.autoreloder.Autoreloader` used to automatically
        reload use code when the file-system changes.

        This is only defined if the ``autoreload`` argument is enabled.
        Your worker bootstep must require the `Autoreloader` bootstep to use this;

        .. code-block:: python

            class WorkerStep(bootsteps.StartStopStep):
                requires = ('celery.worker.autoreloader:Autoreloader',)

Worker 启动步骤示例
-----------------------

Example worker bootstep

.. tab:: 中文

    一个示例的 Worker bootstep 如下所示：

    .. code-block:: python

        from celery import bootsteps

        class ExampleWorkerStep(bootsteps.StartStopStep):
            requires = {'celery.worker.components:Pool'}

            def __init__(self, worker, **kwargs):
                print('在构造 WorkController 实例时调用')
                print('传递给 WorkController 的参数: {0!r}'.format(kwargs))

            def create(self, worker):
                # 此方法可用于将操作方法委托给实现了 ``start`` 和 ``stop`` 的其他对象。
                return self

            def start(self, worker):
                print('在 worker 启动时调用。')

            def stop(self, worker):
                print('在 worker 关闭时调用。')

            def terminate(self, worker):
                print('在 worker 终止时调用。')


    每个方法都会将当前的 ``WorkController`` 实例作为第一个参数传入。

    另一个示例使用 timer 以定期唤醒方式运行：

    .. code-block:: python

        from celery import bootsteps


        class DeadlockDetection(bootsteps.StartStopStep):
            requires = {'celery.worker.components:Timer'}

            def __init__(self, worker, deadlock_timeout=3600):
                self.timeout = deadlock_timeout
                self.requests = []
                self.tref = None

            def start(self, worker):
                # 每 30 秒运行一次。
                self.tref = worker.timer.call_repeatedly(
                    30.0, self.detect, (worker,), priority=10,
                )

            def stop(self, worker):
                if self.tref:
                    self.tref.cancel()
                    self.tref = None

            def detect(self, worker):
                # 更新活跃请求
                for req in worker.active_requests:
                    if req.time_start and time() - req.time_start > self.timeout:
                        raise SystemExit()

.. tab:: 英文


    An example Worker bootstep could be:

    .. code-block:: python

        from celery import bootsteps

        class ExampleWorkerStep(bootsteps.StartStopStep):
            requires = {'celery.worker.components:Pool'}

            def __init__(self, worker, **kwargs):
                print('Called when the WorkController instance is constructed')
                print('Arguments to WorkController: {0!r}'.format(kwargs))

            def create(self, worker):
                # this method can be used to delegate the action methods
                # to another object that implements ``start`` and ``stop``.
                return self

            def start(self, worker):
                print('Called when the worker is started.')

            def stop(self, worker):
                print('Called when the worker shuts down.')

            def terminate(self, worker):
                print('Called when the worker terminates')


    Every method is passed the current ``WorkController`` instance as the first
    argument.

    Another example could use the timer to wake up at regular intervals:

    .. code-block:: python

        from celery import bootsteps


        class DeadlockDetection(bootsteps.StartStopStep):
            requires = {'celery.worker.components:Timer'}

            def __init__(self, worker, deadlock_timeout=3600):
                self.timeout = deadlock_timeout
                self.requests = []
                self.tref = None

            def start(self, worker):
                # run every 30 seconds.
                self.tref = worker.timer.call_repeatedly(
                    30.0, self.detect, (worker,), priority=10,
                )

            def stop(self, worker):
                if self.tref:
                    self.tref.cancel()
                    self.tref = None

            def detect(self, worker):
                # update active requests
                for req in worker.active_requests:
                    if req.time_start and time() - req.time_start > self.timeout:
                        raise SystemExit()

自定义任务处理日志
------------------------------

Customizing Task Handling Logs

.. tab:: 中文

    Celery worker 会在任务生命周期的不同事件点向 Python 的日志子系统发出消息。
    你可以通过覆盖定义于 :file:`celery/app/trace.py` 中的 ``LOG_<TYPE>`` 格式字符串
    来自定义这些日志消息。

    例如：

    .. code-block:: python

        import celery.app.trace

        celery.app.trace.LOG_SUCCESS = "This is a custom message"

    所有格式字符串都使用任务名称和任务 ID 进行 ``%`` 格式化，
    其中一些还包含附加字段，如任务返回值或导致任务失败的异常对象。
    你可以像下面这样在自定义格式字符串中使用这些字段：

    .. code-block:: python

        import celery.app.trace

        celery.app.trace.LOG_REJECTED = "%(name)r 是个被诅咒的任务，我拒绝执行：%(exc)s"

.. tab:: 英文


    The Celery worker emits messages to the Python logging subsystem for various
    events throughout the lifecycle of a task.
    These messages can be customized by overriding the ``LOG_<TYPE>`` format
    strings which are defined in :file:`celery/app/trace.py`.
    For example:

    .. code-block:: python

        import celery.app.trace

        celery.app.trace.LOG_SUCCESS = "This is a custom message"

    The various format strings are all provided with the task name and ID for
    ``%`` formatting, and some of them receive extra fields like the return value
    or the exception which caused a task to fail.
    These fields can be used in custom format strings like so:

    .. code-block:: python

        import celery.app.trace

        celery.app.trace.LOG_REJECTED = "%(name)r is cursed and I won't run it: %(exc)s"

.. _extending-consumer_blueprint:

消费者
========

Consumer

.. tab:: 中文

    Consumer blueprint（消费者蓝图）用于与 broker 建立连接，并在连接断开时自动重启。
    消费者 bootstep 包括 worker 的心跳机制、远程控制命令接收器，以及任务消费者（最为关键）。

    在创建消费者 bootstep 时，必须确保你的 blueprint 支持重启。
    消费者 bootstep 还定义了一个额外的 `shutdown` 方法，该方法会在 worker 关闭时调用。

.. tab:: 英文


    The Consumer blueprint establishes a connection to the broker, and
    is restarted every time this connection is lost. Consumer bootsteps
    include the worker heartbeat, the remote control command consumer, and
    importantly, the task consumer.

    When you create consumer bootsteps you must take into account that it must
    be possible to restart your blueprint. An additional 'shutdown' method is
    defined for consumer bootsteps, this method is called when the worker is
    shutdown.

.. _extending-consumer-attributes:

属性
----------

Attributes

.. tab:: 中文

    .. _extending-consumer-app:

    .. attribute:: app

        当前的 app 实例。

    .. _extending-consumer-controller:

    .. attribute:: controller

        创建该 consumer 的父级 :class:`~@WorkController` 对象。

    .. _extending-consumer-hostname:

    .. attribute:: hostname

        worker 节点的名称（例如：`worker1@example.com`）

    .. _extending-consumer-blueprint:

    .. attribute:: blueprint

        这是 worker 的 :class:`~celery.bootsteps.Blueprint` 实例。

    .. _extending-consumer-hub:

    .. attribute:: hub

        事件循环对象（:class:`~kombu.asynchronous.Hub`）。你可以使用它在事件循环中注册回调函数。

        仅支持启用了异步 I/O 的 transport（如 amqp、redis），此时应设置 `worker.use_eventloop` 属性。

        若要使用此属性，你的 worker bootstep 必须依赖 Hub bootstep：

        .. code-block:: python

            class WorkerStep(bootsteps.StartStopStep):
                requires = {'celery.worker.components:Hub'}

    .. _extending-consumer-connection:

    .. attribute:: connection

        当前的 broker 连接（:class:`kombu.Connection`）。

        若要使用此属性，consumer bootstep 必须依赖 'Connection' bootstep：

        .. code-block:: python

            class Step(bootsteps.StartStopStep):
                requires = {'celery.worker.consumer.connection:Connection'}

    .. _extending-consumer-event_dispatcher:

    .. attribute:: event_dispatcher

        一个 :class:`@events.Dispatcher` 对象，可用于发送事件。

        若要使用此属性，consumer bootstep 必须依赖 `Events` bootstep。

        .. code-block:: python

            class Step(bootsteps.StartStopStep):
                requires = {'celery.worker.consumer.events:Events'}

    .. _extending-consumer-gossip:

    .. attribute:: gossip

        用于 worker 间广播通信的对象
        （:class:`~celery.worker.consumer.gossip.Gossip`）。

        若要使用此属性，consumer bootstep 必须依赖 `Gossip` bootstep。

        .. code-block:: python

            class RatelimitStep(bootsteps.StartStopStep):
                """基于集群中 worker 数量对任务进行速率限制。"""
                requires = {'celery.worker.consumer.gossip:Gossip'}

                def start(self, c):
                    self.c = c
                    self.c.gossip.on.node_join.add(self.on_cluster_size_change)
                    self.c.gossip.on.node_leave.add(self.on_cluster_size_change)
                    self.c.gossip.on.node_lost.add(self.on_node_lost)
                    self.tasks = [
                        self.app.tasks['proj.tasks.add']
                        self.app.tasks['proj.tasks.mul']
                    ]
                    self.last_size = None

                def on_cluster_size_change(self, worker):
                    cluster_size = len(list(self.c.gossip.state.alive_workers()))
                    if cluster_size != self.last_size:
                        for task in self.tasks:
                            task.rate_limit = 1.0 / cluster_size
                        self.c.reset_rate_limits()
                        self.last_size = cluster_size

                def on_node_lost(self, worker):
                    # 可能由于心跳响应过晚，因此需要尽快再次检查该 worker 是否恢复
                    self.c.timer.call_after(10.0, self.on_cluster_size_change)

        **回调事件**

        - ``<set> gossip.on.node_join``

            当有新节点加入集群时触发，提供一个
            :class:`~celery.events.state.Worker` 实例。

        - ``<set> gossip.on.node_leave``

            当有节点离开集群（关闭）时触发，提供一个
            :class:`~celery.events.state.Worker` 实例。

        - ``<set> gossip.on.node_lost``

            当集群中的某个 worker 未能按时发送或处理心跳时触发，提供一个
            :class:`~celery.events.state.Worker` 实例。

            这并不一定意味着 worker 真正离线，因此如果默认心跳超时不足以确认，
            可使用额外的超时机制。

    .. _extending-consumer-pool:

    .. attribute:: pool

        当前使用的进程 / eventlet / gevent / 线程池。
        参考 :class:`celery.concurrency.base.BasePool`。

    .. _extending-consumer-timer:

    .. attribute:: timer

        用于调度函数的 :class:`Timer <celery.utils.timer2.Schedule>`。

    .. _extending-consumer-heart:

    .. attribute:: heart

        负责发送 worker 事件心跳的对象
        （:class:`~celery.worker.heartbeat.Heart`）。

        若要使用此属性，consumer bootstep 必须依赖 `Heart` bootstep：

        .. code-block:: python

            class Step(bootsteps.StartStopStep):
                requires = {'celery.worker.consumer.heart:Heart'}

    .. _extending-consumer-task_consumer:

    .. attribute:: task_consumer

        用于消费任务消息的 :class:`kombu.Consumer` 对象。

        若要使用此属性，consumer bootstep 必须依赖 `Tasks` bootstep：

        .. code-block:: python

            class Step(bootsteps.StartStopStep):
                requires = {'celery.worker.consumer.tasks:Tasks'}

    .. _extending-consumer-strategies:

    .. attribute:: strategies

        每个已注册的任务类型在此映射中都有一个条目，
        映射值用于执行该类型任务的接收消息（即任务执行策略）。
        此映射由 `Tasks` bootstep 在 consumer 启动时生成：

        .. code-block:: python

            for name, task in app.tasks.items():
                strategies[name] = task.start_strategy(app, consumer)
                task.__trace__ = celery.app.trace.build_tracer(
                    name, task, loader, hostname
                )

        若要使用此属性，consumer bootstep 必须依赖 `Tasks` bootstep：

        .. code-block:: python

            class Step(bootsteps.StartStopStep):
                requires = {'celery.worker.consumer.tasks:Tasks'}

    .. _extending-consumer-task_buckets:

    .. attribute:: task_buckets

        一个 :class:`~collections.defaultdict`，用于按任务类型查找其速率限制器。
        此 dict 中的值可以是 None（表示无限制），也可以是实现了
        ``consume(tokens)`` 和 ``expected_time(tokens)`` 方法的
        :class:`~kombu.utils.limits.TokenBucket` 实例。

        `TokenBucket` 实现了 `令牌桶算法`_，但只要符合上述接口和方法定义，
        也可以使用其他算法。

    .. _extending_consumer-qos:

    .. attribute:: qos

        :class:`~kombu.common.QoS` 对象，用于修改当前任务通道的 `prefetch_count` 值：

        .. code-block:: python

            # 在下一个周期增加
            consumer.qos.increment_eventually(1)
            # 在下一个周期减少
            consumer.qos.decrement_eventually(1)
            consumer.qos.set(10)


.. tab:: 英文

    .. attribute:: app
        :no-index:

        The current app instance.

    .. attribute:: controller
        :no-index:

        The parent :class:`~@WorkController` object that created this consumer.

    .. attribute:: hostname
        :no-index:

        The workers node name (e.g., `worker1@example.com`)

    .. attribute:: blueprint
        :no-index:

        This is the worker :class:`~celery.bootsteps.Blueprint`.

    .. attribute:: hub
        :no-index:

        Event loop object (:class:`~kombu.asynchronous.Hub`). You can use
        this to register callbacks in the event loop.

        This is only supported by async I/O enabled transports (amqp, redis),
        in which case the `worker.use_eventloop` attribute should be set.

        Your worker bootstep must require the Hub bootstep to use this:

        .. code-block:: python

            class WorkerStep(bootsteps.StartStopStep):
                requires = {'celery.worker.components:Hub'}

    .. attribute:: connection
        :no-index:

        The current broker connection (:class:`kombu.Connection`).

        A consumer bootstep must require the 'Connection' bootstep
        to use this:

        .. code-block:: python

            class Step(bootsteps.StartStopStep):
                requires = {'celery.worker.consumer.connection:Connection'}

    .. attribute:: event_dispatcher
        :no-index:

        A :class:`@events.Dispatcher` object that can be used to send events.

        A consumer bootstep must require the `Events` bootstep to use this.

        .. code-block:: python

            class Step(bootsteps.StartStopStep):
                requires = {'celery.worker.consumer.events:Events'}

    .. attribute:: gossip
        :no-index:

        Worker to worker broadcast communication
        (:class:`~celery.worker.consumer.gossip.Gossip`).

        A consumer bootstep must require the `Gossip` bootstep to use this.

        .. code-block:: python

            class RatelimitStep(bootsteps.StartStopStep):
                """Rate limit tasks based on the number of workers in the
                cluster."""
                requires = {'celery.worker.consumer.gossip:Gossip'}

                def start(self, c):
                    self.c = c
                    self.c.gossip.on.node_join.add(self.on_cluster_size_change)
                    self.c.gossip.on.node_leave.add(self.on_cluster_size_change)
                    self.c.gossip.on.node_lost.add(self.on_node_lost)
                    self.tasks = [
                        self.app.tasks['proj.tasks.add']
                        self.app.tasks['proj.tasks.mul']
                    ]
                    self.last_size = None

                def on_cluster_size_change(self, worker):
                    cluster_size = len(list(self.c.gossip.state.alive_workers()))
                    if cluster_size != self.last_size:
                        for task in self.tasks:
                            task.rate_limit = 1.0 / cluster_size
                        self.c.reset_rate_limits()
                        self.last_size = cluster_size

                def on_node_lost(self, worker):
                    # may have processed heartbeat too late, so wake up soon
                    # in order to see if the worker recovered.
                    self.c.timer.call_after(10.0, self.on_cluster_size_change)

        **Callbacks**

        - ``<set> gossip.on.node_join``

            Called whenever a new node joins the cluster, providing a
            :class:`~celery.events.state.Worker` instance.

        - ``<set> gossip.on.node_leave``

            Called whenever a new node leaves the cluster (shuts down),
            providing a :class:`~celery.events.state.Worker` instance.

        - ``<set> gossip.on.node_lost``

            Called whenever heartbeat was missed for a worker instance in the
            cluster (heartbeat not received or processed in time),
            providing a :class:`~celery.events.state.Worker` instance.

            This doesn't necessarily mean the worker is actually offline, so use a time
            out mechanism if the default heartbeat timeout isn't sufficient.

    .. attribute:: pool
        :no-index:

        The current process/eventlet/gevent/thread pool.
        See :class:`celery.concurrency.base.BasePool`.

    .. attribute:: timer
        :no-index:

        :class:`Timer <celery.utils.timer2.Schedule` used to schedule functions.

    .. attribute:: heart
        :no-index:

        Responsible for sending worker event heartbeats
        (:class:`~celery.worker.heartbeat.Heart`).

        Your consumer bootstep must require the `Heart` bootstep to use this:

        .. code-block:: python

            class Step(bootsteps.StartStopStep):
                requires = {'celery.worker.consumer.heart:Heart'}

    .. attribute:: task_consumer
        :no-index:

        The :class:`kombu.Consumer` object used to consume task messages.

        Your consumer bootstep must require the `Tasks` bootstep to use this:

        .. code-block:: python

            class Step(bootsteps.StartStopStep):
                requires = {'celery.worker.consumer.tasks:Tasks'}

    .. attribute:: strategies
        :no-index:

        Every registered task type has an entry in this mapping,
        where the value is used to execute an incoming message of this task type
        (the task execution strategy). This mapping is generated by the Tasks
        bootstep when the consumer starts:

        .. code-block:: python

            for name, task in app.tasks.items():
                strategies[name] = task.start_strategy(app, consumer)
                task.__trace__ = celery.app.trace.build_tracer(
                    name, task, loader, hostname
                )

        Your consumer bootstep must require the `Tasks` bootstep to use this:

        .. code-block:: python

            class Step(bootsteps.StartStopStep):
                requires = {'celery.worker.consumer.tasks:Tasks'}

    .. attribute:: task_buckets
        :no-index:

        A :class:`~collections.defaultdict` used to look-up the rate limit for
        a task by type.
        Entries in this dict may be None (for no limit) or a
        :class:`~kombu.utils.limits.TokenBucket` instance implementing
        ``consume(tokens)`` and ``expected_time(tokens)``.

        TokenBucket implements the `token bucket algorithm`_, but any algorithm
        may be used as long as it conforms to the same interface and defines the
        two methods above.

    .. attribute:: qos
        :no-index:

        The :class:`~kombu.common.QoS` object can be used to change the
        task channels current prefetch_count value:

        .. code-block:: python

            # increment at next cycle
            consumer.qos.increment_eventually(1)
            # decrement at next cycle
            consumer.qos.decrement_eventually(1)
            consumer.qos.set(10)

.. _`token bucket algorithm`: https://en.wikipedia.org/wiki/Token_bucket

.. _`令牌桶算法`: https://en.wikipedia.org/wiki/Token_bucket


方法
-------

Methods

.. tab:: 中文

    .. method:: consumer.reset_rate_limits()

        更新所有已注册任务类型的 ``task_buckets`` 映射。

    .. method:: consumer.bucket_for_task(type, Bucket=TokenBucket)

        使用任务的 ``task.rate_limit`` 属性为任务创建速率限制桶。

    .. method:: consumer.add_task_queue(name, exchange=None, exchange_type=None,
                                        routing_key=None, **options):

        添加新的队列以进行消费。此操作将在连接重启后继续生效。

    .. method:: consumer.cancel_task_queue(name)

        停止消费指定名称的队列。此操作将在连接重启后继续生效。

    .. method:: apply_eta_task(request)

        根据 ``request.eta`` 属性调度 ETA 任务以执行。
        （:class:`~celery.worker.request.Request`）

.. tab:: 英文

    .. method:: consumer.reset_rate_limits()
        :no-index:

        Updates the ``task_buckets`` mapping for all registered task types.

    .. method:: consumer.bucket_for_task(type, Bucket=TokenBucket)
        :no-index:

        Creates rate limit bucket for a task using its ``task.rate_limit``
        attribute.

    .. method:: consumer.add_task_queue(name, exchange=None, exchange_type=None,
                                        routing_key=None, **options):
        :no-index:

        Adds new queue to consume from. This will persist on connection restart.

    .. method:: consumer.cancel_task_queue(name)
        :no-index:

        Stop consuming from queue by name. This will persist on connection
        restart.

    .. method:: apply_eta_task(request)
        :no-index:

        Schedule ETA task to execute based on the ``request.eta`` attribute.
        (:class:`~celery.worker.request.Request`)



.. _extending-bootsteps:

安装启动步骤
====================

Installing Bootsteps

.. tab:: 中文

    ``app.steps['worker']`` 和 ``app.steps['consumer']`` 可被修改以添加新的启动步骤（bootstep）：

    .. code-block:: pycon

        >>> app = Celery()
        >>> app.steps['worker'].add(MyWorkerStep)  # < 添加类，不实例化
        >>> app.steps['consumer'].add(MyConsumerStep)

        >>> app.steps['consumer'].update([StepA, StepB])

        >>> app.steps['consumer']
        {step:proj.StepB{()}, step:proj.MyConsumerStep{()}, step:proj.StepA{()}}

    步骤的顺序在此处并不重要，因为最终的执行顺序是由生成的依赖图（``Step.requires``）决定的。

    以下是一个示例步骤，用来演示如何安装 bootstep 以及它们的工作原理。这个步骤会打印一些无用的调试信息。
    它既可以作为 worker 的 bootstep，也可以作为 consumer 的 bootstep 添加：

    .. code-block:: python

        from celery import Celery
        from celery import bootsteps

        class InfoStep(bootsteps.Step):

            def __init__(self, parent, **kwargs):
                # 我们可以在这里以任意方式初始化 Worker/Consumer 对象，
                # 例如设置默认属性等。
                print('{0!r} is in init'.format(parent))

            def start(self, parent):
                # 此步骤将在所有其他 Worker/Consumer 的 bootstep 启动时一同启动。
                print('{0!r} is starting'.format(parent))

            def stop(self, parent):
                # Consumer 每次重启（例如连接丢失）以及关闭时都会调用 stop。
                # Worker 仅在关闭时调用 stop。
                print('{0!r} is stopping'.format(parent))

            def shutdown(self, parent):
                # shutdown 会在 Consumer 关闭时调用，而不会被 Worker 调用。
                print('{0!r} is shutting down'.format(parent))

            app = Celery(broker='amqp://')
            app.steps['worker'].add(InfoStep)
            app.steps['consumer'].add(InfoStep)

    使用该步骤启动 worker 时，会产生以下日志输出：

    .. code-block:: text

        <Worker: w@example.com (initializing)> is in init
        <Consumer: w@example.com (initializing)> is in init
        [2013-05-29 16:18:20,544: WARNING/MainProcess]
            <Worker: w@example.com (running)> is starting
        [2013-05-29 16:18:21,577: WARNING/MainProcess]
            <Consumer: w@example.com (running)> is starting
        <Consumer: w@example.com (closing)> is stopping
        <Worker: w@example.com (closing)> is stopping
        <Consumer: w@example.com (terminating)> is shutting down

    这些 ``print`` 语句会在 worker 初始化后被重定向到日志系统，因此 "is starting" 的日志是带有时间戳的。
    你可能会注意到在 shutdown 时不再输出这些信息，这是因为 ``stop`` 和 ``shutdown`` 方法是在 *信号处理器* 中调用的，
    而在信号处理器中使用日志系统是不安全的。

    使用 Python 的日志模块记录信息并不是 :term:`可重入 <reentrant>` 的：
    也就是说你不能在函数执行中断后再次调用它。因此你所编写的 ``stop`` 和 ``shutdown`` 方法也必须是 :term:`可重入 <reentrant>` 的。

    以 :option:`--loglevel=debug <celery worker --loglevel>` 启动 worker 会显示更多有关启动过程的信息：

    .. code-block:: text

        [2013-05-29 16:18:20,509: DEBUG/MainProcess] | Worker: Preparing bootsteps.
        [2013-05-29 16:18:20,511: DEBUG/MainProcess] | Worker: Building graph...
        <celery.apps.worker.Worker object at 0x101ad8410> is in init
        [2013-05-29 16:18:20,511: DEBUG/MainProcess] | Worker: New boot order:
            {Hub, Pool, Timer, StateDB, Autoscaler, InfoStep, Beat, Consumer}
        [2013-05-29 16:18:20,514: DEBUG/MainProcess] | Consumer: Preparing bootsteps.
        [2013-05-29 16:18:20,514: DEBUG/MainProcess] | Consumer: Building graph...
        <celery.worker.consumer.Consumer object at 0x101c2d8d0> is in init
        [2013-05-29 16:18:20,515: DEBUG/MainProcess] | Consumer: New boot order:
            {Connection, Mingle, Events, Gossip, InfoStep, Agent,
            Heart, Control, Tasks, event loop}
        [2013-05-29 16:18:20,522: DEBUG/MainProcess] | Worker: Starting Hub
        [2013-05-29 16:18:20,522: DEBUG/MainProcess] ^-- substep ok
        [2013-05-29 16:18:20,522: DEBUG/MainProcess] | Worker: Starting Pool
        [2013-05-29 16:18:20,542: DEBUG/MainProcess] ^-- substep ok
        [2013-05-29 16:18:20,543: DEBUG/MainProcess] | Worker: Starting InfoStep
        [2013-05-29 16:18:20,544: WARNING/MainProcess]
            <celery.apps.worker.Worker object at 0x101ad8410> is starting
        [2013-05-29 16:18:20,544: DEBUG/MainProcess] ^-- substep ok
        [2013-05-29 16:18:20,544: DEBUG/MainProcess] | Worker: Starting Consumer
        [2013-05-29 16:18:20,544: DEBUG/MainProcess] | Consumer: Starting Connection
        [2013-05-29 16:18:20,559: INFO/MainProcess] Connected to amqp://guest@127.0.0.1:5672//
        [2013-05-29 16:18:20,560: DEBUG/MainProcess] ^-- substep ok
        [2013-05-29 16:18:20,560: DEBUG/MainProcess] | Consumer: Starting Mingle
        [2013-05-29 16:18:20,560: INFO/MainProcess] mingle: searching for neighbors
        [2013-05-29 16:18:21,570: INFO/MainProcess] mingle: no one here
        [2013-05-29 16:18:21,570: DEBUG/MainProcess] ^-- substep ok
        [2013-05-29 16:18:21,571: DEBUG/MainProcess] | Consumer: Starting Events
        [2013-05-29 16:18:21,572: DEBUG/MainProcess] ^-- substep ok
        [2013-05-29 16:18:21,572: DEBUG/MainProcess] | Consumer: Starting Gossip
        [2013-05-29 16:18:21,577: DEBUG/MainProcess] ^-- substep ok
        [2013-05-29 16:18:21,577: DEBUG/MainProcess] | Consumer: Starting InfoStep
        [2013-05-29 16:18:21,577: WARNING/MainProcess]
            <celery.worker.consumer.Consumer object at 0x101c2d8d0> is starting
        [2013-05-29 16:18:21,578: DEBUG/MainProcess] ^-- substep ok
        [2013-05-29 16:18:21,578: DEBUG/MainProcess] | Consumer: Starting Heart
        [2013-05-29 16:18:21,579: DEBUG/MainProcess] ^-- substep ok
        [2013-05-29 16:18:21,579: DEBUG/MainProcess] | Consumer: Starting Control
        [2013-05-29 16:18:21,583: DEBUG/MainProcess] ^-- substep ok
        [2013-05-29 16:18:21,583: DEBUG/MainProcess] | Consumer: Starting Tasks
        [2013-05-29 16:18:21,606: DEBUG/MainProcess] basic.qos: prefetch_count->80
        [2013-05-29 16:18:21,606: DEBUG/MainProcess] ^-- substep ok
        [2013-05-29 16:18:21,606: DEBUG/MainProcess] | Consumer: Starting event loop
        [2013-05-29 16:18:21,608: WARNING/MainProcess] celery@example.com ready.


.. tab:: 英文

    ``app.steps['worker']`` and ``app.steps['consumer']`` can be modified
    to add new bootsteps:

    .. code-block:: pycon

        >>> app = Celery()
        >>> app.steps['worker'].add(MyWorkerStep)  # < add class, don't instantiate
        >>> app.steps['consumer'].add(MyConsumerStep)

        >>> app.steps['consumer'].update([StepA, StepB])

        >>> app.steps['consumer']
        {step:proj.StepB{()}, step:proj.MyConsumerStep{()}, step:proj.StepA{()}

    The order of steps isn't important here as the order is decided by the
    resulting dependency graph (``Step.requires``).

    To illustrate how you can install bootsteps and how they work, this is an example step that
    prints some useless debugging information.
    It can be added both as a worker and consumer bootstep:


    .. code-block:: python

        from celery import Celery
        from celery import bootsteps

        class InfoStep(bootsteps.Step):

            def __init__(self, parent, **kwargs):
                # here we can prepare the Worker/Consumer object
                # in any way we want, set attribute defaults, and so on.
                print('{0!r} is in init'.format(parent))

            def start(self, parent):
                # our step is started together with all other Worker/Consumer
                # bootsteps.
                print('{0!r} is starting'.format(parent))

            def stop(self, parent):
                # the Consumer calls stop every time the consumer is
                # restarted (i.e., connection is lost) and also at shutdown.
                # The Worker will call stop at shutdown only.
                print('{0!r} is stopping'.format(parent))

            def shutdown(self, parent):
                # shutdown is called by the Consumer at shutdown, it's not
                # called by Worker.
                print('{0!r} is shutting down'.format(parent))

            app = Celery(broker='amqp://')
            app.steps['worker'].add(InfoStep)
            app.steps['consumer'].add(InfoStep)

    Starting the worker with this step installed will give us the following
    logs:

    .. code-block:: text

        <Worker: w@example.com (initializing)> is in init
        <Consumer: w@example.com (initializing)> is in init
        [2013-05-29 16:18:20,544: WARNING/MainProcess]
            <Worker: w@example.com (running)> is starting
        [2013-05-29 16:18:21,577: WARNING/MainProcess]
            <Consumer: w@example.com (running)> is starting
        <Consumer: w@example.com (closing)> is stopping
        <Worker: w@example.com (closing)> is stopping
        <Consumer: w@example.com (terminating)> is shutting down

    The ``print`` statements will be redirected to the logging subsystem after
    the worker has been initialized, so the "is starting" lines are time-stamped.
    You may notice that this does no longer happen at shutdown, this is because
    the ``stop`` and ``shutdown`` methods are called inside a *signal handler*,
    and it's not safe to use logging inside such a handler.
    Logging with the Python logging module isn't :term:`reentrant`:
    meaning you cannot interrupt the function then
    call it again later. It's important that the ``stop`` and ``shutdown`` methods
    you write is also :term:`reentrant`.

    Starting the worker with :option:`--loglevel=debug <celery worker --loglevel>`
    will show us more information about the boot process:

    .. code-block:: text

        [2013-05-29 16:18:20,509: DEBUG/MainProcess] | Worker: Preparing bootsteps.
        [2013-05-29 16:18:20,511: DEBUG/MainProcess] | Worker: Building graph...
        <celery.apps.worker.Worker object at 0x101ad8410> is in init
        [2013-05-29 16:18:20,511: DEBUG/MainProcess] | Worker: New boot order:
            {Hub, Pool, Timer, StateDB, Autoscaler, InfoStep, Beat, Consumer}
        [2013-05-29 16:18:20,514: DEBUG/MainProcess] | Consumer: Preparing bootsteps.
        [2013-05-29 16:18:20,514: DEBUG/MainProcess] | Consumer: Building graph...
        <celery.worker.consumer.Consumer object at 0x101c2d8d0> is in init
        [2013-05-29 16:18:20,515: DEBUG/MainProcess] | Consumer: New boot order:
            {Connection, Mingle, Events, Gossip, InfoStep, Agent,
            Heart, Control, Tasks, event loop}
        [2013-05-29 16:18:20,522: DEBUG/MainProcess] | Worker: Starting Hub
        [2013-05-29 16:18:20,522: DEBUG/MainProcess] ^-- substep ok
        [2013-05-29 16:18:20,522: DEBUG/MainProcess] | Worker: Starting Pool
        [2013-05-29 16:18:20,542: DEBUG/MainProcess] ^-- substep ok
        [2013-05-29 16:18:20,543: DEBUG/MainProcess] | Worker: Starting InfoStep
        [2013-05-29 16:18:20,544: WARNING/MainProcess]
            <celery.apps.worker.Worker object at 0x101ad8410> is starting
        [2013-05-29 16:18:20,544: DEBUG/MainProcess] ^-- substep ok
        [2013-05-29 16:18:20,544: DEBUG/MainProcess] | Worker: Starting Consumer
        [2013-05-29 16:18:20,544: DEBUG/MainProcess] | Consumer: Starting Connection
        [2013-05-29 16:18:20,559: INFO/MainProcess] Connected to amqp://guest@127.0.0.1:5672//
        [2013-05-29 16:18:20,560: DEBUG/MainProcess] ^-- substep ok
        [2013-05-29 16:18:20,560: DEBUG/MainProcess] | Consumer: Starting Mingle
        [2013-05-29 16:18:20,560: INFO/MainProcess] mingle: searching for neighbors
        [2013-05-29 16:18:21,570: INFO/MainProcess] mingle: no one here
        [2013-05-29 16:18:21,570: DEBUG/MainProcess] ^-- substep ok
        [2013-05-29 16:18:21,571: DEBUG/MainProcess] | Consumer: Starting Events
        [2013-05-29 16:18:21,572: DEBUG/MainProcess] ^-- substep ok
        [2013-05-29 16:18:21,572: DEBUG/MainProcess] | Consumer: Starting Gossip
        [2013-05-29 16:18:21,577: DEBUG/MainProcess] ^-- substep ok
        [2013-05-29 16:18:21,577: DEBUG/MainProcess] | Consumer: Starting InfoStep
        [2013-05-29 16:18:21,577: WARNING/MainProcess]
            <celery.worker.consumer.Consumer object at 0x101c2d8d0> is starting
        [2013-05-29 16:18:21,578: DEBUG/MainProcess] ^-- substep ok
        [2013-05-29 16:18:21,578: DEBUG/MainProcess] | Consumer: Starting Heart
        [2013-05-29 16:18:21,579: DEBUG/MainProcess] ^-- substep ok
        [2013-05-29 16:18:21,579: DEBUG/MainProcess] | Consumer: Starting Control
        [2013-05-29 16:18:21,583: DEBUG/MainProcess] ^-- substep ok
        [2013-05-29 16:18:21,583: DEBUG/MainProcess] | Consumer: Starting Tasks
        [2013-05-29 16:18:21,606: DEBUG/MainProcess] basic.qos: prefetch_count->80
        [2013-05-29 16:18:21,606: DEBUG/MainProcess] ^-- substep ok
        [2013-05-29 16:18:21,606: DEBUG/MainProcess] | Consumer: Starting event loop
        [2013-05-29 16:18:21,608: WARNING/MainProcess] celery@example.com ready.


.. _extending-programs:

命令行程序
=====================

Command-line programs

.. _extending-commandoptions:

添加新的命令行选项
-------------------------------

Adding new command-line options

.. _extending-command-options:

特定于命令的选项
~~~~~~~~~~~~~~~~~~~~~~~~

Command-specific options

.. tab:: 中文

    你可以通过修改应用实例的 :attr:`~@user_options` 属性，为 ``worker``、 ``beat`` 和 ``events`` 命令添加额外的命令行选项。

    Celery 命令使用 :mod:`click` 模块解析命令行参数，因此要添加自定义参数，你需要将 :class:`click.Option` 实例添加到相应的选项集合中。

    以下是为 :program:`celery worker` 命令添加自定义选项的示例：

    .. code-block:: python

        from celery import Celery
        from click import Option

        app = Celery(broker='amqp://')

        app.user_options['worker'].add(Option(('--enable-my-option',),
                                            is_flag=True,
                                            help='启用自定义选项。'))

    所有 bootstep 现在都会以关键字参数的形式在 ``Bootstep.__init__`` 中接收到该参数：

    .. code-block:: python

        from celery import bootsteps

        class MyBootstep(bootsteps.Step):

            def __init__(self, parent, enable_my_option=False, **options):
                super().__init__(parent, **options)
                if enable_my_option:
                    party()

        app.steps['worker'].add(MyBootstep)

.. tab:: 英文


    You can add additional command-line options to the ``worker``, ``beat``, and
    ``events`` commands by modifying the :attr:`~@user_options` attribute of the
    application instance.

    Celery commands uses the :mod:`click` module to parse command-line
    arguments, and so to add custom arguments you need to add :class:`click.Option` instances
    to the relevant set.

    Example adding a custom option to the :program:`celery worker` command:

    .. code-block:: python

        from celery import Celery
        from click import Option

        app = Celery(broker='amqp://')

        app.user_options['worker'].add(Option(('--enable-my-option',),
                                            is_flag=True,
                                            help='Enable custom option.'))


    All bootsteps will now receive this argument as a keyword argument to
    ``Bootstep.__init__``:

    .. code-block:: python

        from celery import bootsteps

        class MyBootstep(bootsteps.Step):

            def __init__(self, parent, enable_my_option=False, **options):
                super().__init__(parent, **options)
                if enable_my_option:
                    party()

        app.steps['worker'].add(MyBootstep)

.. _extending-preload_options:

预加载选项
~~~~~~~~~~~~~~~

Preload options

.. tab:: 中文

    :program:`celery` 总控命令支持“预加载选项”（preload options）的概念。这些是会传递给所有子命令的特殊选项。

    你可以添加新的预加载选项，例如用于指定配置模板：

    .. code-block:: python

        from celery import Celery
        from celery import signals
        from click import Option

        app = Celery()

        app.user_options['preload'].add(Option(('-Z', '--template'),
                                            default='default',
                                            help='要使用的配置模板。'))

        @signals.user_preload_options.connect
        def on_preload_parsed(options, **kwargs):
            use_template(options['template'])

.. tab:: 英文


    The :program:`celery` umbrella command supports the concept of 'preload
    options'.  These are special options passed to all sub-commands.

    You can add new preload options, for example to specify a configuration
    template:

    .. code-block:: python

        from celery import Celery
        from celery import signals
        from click import Option

        app = Celery()

        app.user_options['preload'].add(Option(('-Z', '--template'),
                                            default='default',
                                            help='Configuration template to use.'))

        @signals.user_preload_options.connect
        def on_preload_parsed(options, **kwargs):
            use_template(options['template'])

.. _extending-subcommands:

添加新的 :program:`celery` 子命令
-----------------------------------------

Adding new :program:`celery` sub-commands

.. tab:: 中文

    可以通过使用 `setuptools entry-points`_ 向 :program:`celery` 总控命令添加新的子命令。

    Entry-point 是一种特殊的元数据，可添加到你的软件包的 ``setup.py`` 脚本中，安装后可以使用 :mod:`importlib` 模块从系统中读取。

    Celery 会识别 ``celery.commands`` entry-points 来安装额外的子命令，其中 entry-point 的值必须是一个有效的 click 命令。

    这正是 :pypi:`Flower` 监控扩展通过在 :file:`setup.py` 中添加 entry-point 的方式，实现添加 :program:`celery flower` 命令的方式：

    .. code-block:: python

        setup(
            name='flower',
            entry_points={
                'celery.commands': [
                'flower = flower.command:flower',
                ],
            }
        )

    命令定义由等号分隔为两部分，第一部分是子命令的名称（此处为 flower），第二部分是实现该命令的函数的完全限定符号路径：

    .. code-block:: text

        flower.command:flower

    模块路径与属性名称之间应使用冒号分隔，如上所示。

    在 :file:`flower/command.py` 模块中，命令函数可以定义如下：

    .. code-block:: python

        import click

        @click.command()
        @click.option('--port', default=8888, type=int, help='Web服务器端口')
        @click.option('--debug', is_flag=True)
        def flower(port, debug):
            print('运行自定义命令')


.. tab:: 英文

    New commands can be added to the :program:`celery` umbrella command by using
    `setuptools entry-points`_.


    Entry-points is special meta-data that can be added to your packages ``setup.py`` program,
    and then after installation, read from the system using the :mod:`importlib` module.

    Celery recognizes ``celery.commands`` entry-points to install additional
    sub-commands, where the value of the entry-point must point to a valid click
    command.

    This is how the :pypi:`Flower` monitoring extension may add the :program:`celery flower` command,
    by adding an entry-point in :file:`setup.py`:

    .. code-block:: python

        setup(
            name='flower',
            entry_points={
                'celery.commands': [
                'flower = flower.command:flower',
                ],
            }
        )

    The command definition is in two parts separated by the equal sign, where the
    first part is the name of the sub-command (flower), then the second part is
    the fully qualified symbol path to the function that implements the command:

    .. code-block:: text

        flower.command:flower

    The module path and the name of the attribute should be separated by colon
    as above.


    In the module :file:`flower/command.py`, the command function may be defined
    as the following:

    .. code-block:: python

        import click

        @click.command()
        @click.option('--port', default=8888, type=int, help='Webserver port')
        @click.option('--debug', is_flag=True)
        def flower(port, debug):
            print('Running our command')

.. _`setuptools entry-points`: http://reinout.vanrees.org/weblog/2010/01/06/zest-releaser-entry-points.html


Worker API
==========

Worker API

:class:`~kombu.asynchronous.Hub` - Worker 异步事件循环
---------------------------------------------------------------

:class:`~kombu.asynchronous.Hub` - The workers async event loop

:supported transports: amqp, redis

.. versionadded:: 3.0

.. tab:: 中文

    当使用 amqp 或 redis broker 传输方式时，worker 会使用异步 I/O。最终的目标是让所有传输方式都基于事件循环（event-loop）实现，但这还需要一段时间，因此其他传输方式仍然采用基于线程的解决方案。

    .. method:: hub.add(fd, callback, flags)


    .. method:: hub.add_reader(fd, callback, *args)

        添加在 ``fd`` 可读时调用的回调函数。

        该回调函数会持续注册，直到显式地使用 :meth:`hub.remove(fd) <hub.remove>` 移除，
        或者由于文件描述符不再有效而被自动丢弃。

        注意：任意给定的文件描述符在任意时刻只能注册一个回调函数，因此若第二次调用 ``add``，
        会移除此前为该文件描述符注册的任何回调。

        文件描述符可以是支持 ``fileno`` 方法的任何类似文件对象，或是文件描述符的整数编号（int）。

    .. method:: hub.add_writer(fd, callback, *args)

        添加在 ``fd`` 可写时调用的回调函数。
        参考上文 :meth:`hub.add_reader` 的说明。

    .. method:: hub.remove(fd)

        从事件循环中移除文件描述符 ``fd`` 的所有回调函数。

.. tab:: 英文

    The worker uses asynchronous I/O when the amqp or redis broker transports are
    used. The eventual goal is for all transports to use the event-loop, but that
    will take some time so other transports still use a threading-based solution.

    .. method:: hub.add(fd, callback, flags)
        :no-index:


    .. method:: hub.add_reader(fd, callback, *args)
        :no-index:

        Add callback to be called when ``fd`` is readable.

        The callback will stay registered until explicitly removed using
        :meth:`hub.remove(fd) <hub.remove>`, or the file descriptor is
        automatically discarded because it's no longer valid.

        Note that only one callback can be registered for any given
        file descriptor at a time, so calling ``add`` a second time will remove
        any callback that was previously registered for that file descriptor.

        A file descriptor is any file-like object that supports the ``fileno``
        method, or it can be the file descriptor number (int).

    .. method:: hub.add_writer(fd, callback, *args)
        :no-index:

        Add callback to be called when ``fd`` is writable.
        See also notes for :meth:`hub.add_reader` above.

    .. method:: hub.remove(fd)
        :no-index:

        Remove all callbacks for file descriptor ``fd`` from the loop.

计时器 - 事件调度
-------------------------

Timer - Scheduling events


.. method:: timer.call_after(secs, callback, args=(), kwargs=(),
                             priority=0)

.. method:: timer.call_repeatedly(secs, callback, args=(), kwargs=(),
                                  priority=0)

.. method:: timer.call_at(eta, callback, args=(), kwargs=(),
                          priority=0)
