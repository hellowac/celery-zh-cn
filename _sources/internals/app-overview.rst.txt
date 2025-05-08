=============================
“大实例”重构
=============================

"The Big Instance" Refactor

.. tab:: 中文

    `app` 分支是一个正在进行中的重构，目标是移除 Celery 中对全局配置的依赖。

    Celery 现在可以被实例化，并且同一进程空间中可以存在多个 Celery 实例。
    此外，大部分功能现在可以在不使用 monkey patch 的前提下进行自定义。

.. tab:: 英文

    The `app` branch is a work-in-progress to remove
    the use of a global configuration in Celery.

    Celery can now be instantiated and several
    instances of Celery may exist in the same process space.
    Also, large parts can be customized without resorting to monkey
    patching.

示例
========

Examples

.. tab:: 中文

    创建一个 Celery 实例::

        >>> from celery import Celery
        >>> app = Celery()
        >>> app.config_from_object('celeryconfig')
        >>> #app.config_from_envvar('CELERY_CONFIG_MODULE')


    创建任务：

    .. code-block:: python

        @app.task
        def add(x, y):
            return x + y


    创建自定义 Task 子类：

    .. code-block:: python

        Task = celery.create_task_cls()

        class DebugTask(Task):

            def on_failure(self, *args, **kwargs):
                import pdb
                pdb.set_trace()

        @app.task(base=DebugTask)
        def add(x, y):
            return x + y

    启动一个 worker：

    .. code-block:: python

        worker = celery.Worker(loglevel='INFO')

    访问配置信息：

    .. code-block:: python

        celery.conf.task_always_eager = True
        celery.conf['task_always_eager'] = True


    控制 worker::

        >>> celery.control.inspect().active()
        >>> celery.control.rate_limit(add.name, '100/m')
        >>> celery.control.broadcast('shutdown')
        >>> celery.control.discard_all()

    其他有用属性::

        # 建立 broker 连接
        >>> celery.broker_connection()

        # AMQP 专属功能
        >>> celery.amqp
        >>> celery.amqp.Router
        >>> celery.amqp.get_queues()
        >>> celery.amqp.get_task_consumer()

        # 加载器
        >>> celery.loader

        # 默认结果后端
        >>> celery.backend


    正如你所见，这一架构开启了更高维度的自定义能力。

.. tab:: 英文

    Creating a Celery instance::

        >>> from celery import Celery
        >>> app = Celery()
        >>> app.config_from_object('celeryconfig')
        >>> #app.config_from_envvar('CELERY_CONFIG_MODULE')


    Creating tasks:

    .. code-block:: python

        @app.task
        def add(x, y):
            return x + y


    Creating custom Task subclasses:

    .. code-block:: python

        Task = celery.create_task_cls()

        class DebugTask(Task):

            def on_failure(self, *args, **kwargs):
                import pdb
                pdb.set_trace()

        @app.task(base=DebugTask)
        def add(x, y):
            return x + y

    Starting a worker:

    .. code-block:: python

        worker = celery.Worker(loglevel='INFO')

    Getting access to the configuration:

    .. code-block:: python

        celery.conf.task_always_eager = True
        celery.conf['task_always_eager'] = True


    Controlling workers::

        >>> celery.control.inspect().active()
        >>> celery.control.rate_limit(add.name, '100/m')
        >>> celery.control.broadcast('shutdown')
        >>> celery.control.discard_all()

    Other interesting attributes::

        # Establish broker connection.
        >>> celery.broker_connection()

        # AMQP Specific features.
        >>> celery.amqp
        >>> celery.amqp.Router
        >>> celery.amqp.get_queues()
        >>> celery.amqp.get_task_consumer()

        # Loader
        >>> celery.loader

        # Default backend
        >>> celery.backend


    As you can probably see, this really opens up another
    dimension of customization abilities.

已弃用
==========

Deprecated

.. tab:: 中文

    * ``celery.task.ping``  
      ``celery.task.PingTask``

      功能逊于 ping 远程控制命令。
      将在 Celery 2.3 中移除。

.. tab:: 英文

    * ``celery.task.ping``
      ``celery.task.PingTask``

      Inferior to the ping remote control command.
      Will be removed in Celery 2.3.

别名（即将弃用）
=============================

Aliases (Pending deprecation)

.. tab:: 中文

    * ``celery.execute``  
        * ``.send_task`` -> {``app.send_task``}  
        * ``.delay_task`` -> *无替代方案*

    * ``celery.log``  
        * ``.get_default_logger`` -> {``app.log.get_default_logger``}  
        * ``.setup_logger`` -> {``app.log.setup_logger``}  
        * ``.get_task_logger`` -> {``app.log.get_task_logger``}  
        * ``.setup_task_logger`` -> {``app.log.setup_task_logger``}  
        * ``.setup_logging_subsystem`` -> {``app.log.setup_logging_subsystem``}  
        * ``.redirect_stdouts_to_logger`` -> {``app.log.redirect_stdouts_to_logger``}

    * ``celery.messaging``  
        * ``.establish_connection`` -> {``app.broker_connection``}  
        * ``.with_connection`` -> {``app.with_connection``}  
        * ``.get_consumer_set`` -> {``app.amqp.get_task_consumer``}  
        * ``.TaskPublisher`` -> {``app.amqp.TaskPublisher``}  
        * ``.TaskConsumer`` -> {``app.amqp.TaskConsumer``}  
        * ``.ConsumerSet`` -> {``app.amqp.ConsumerSet``}

    * ``celery.conf.*`` -> {``app.conf``}
        **注意**：所有配置键现在的命名方式与配置文件一致。
        所以键名 ``task_always_eager`` 现在应通过以下方式访问::

            >>> app.conf.task_always_eager

        而不是以前的方式::

            >>> from celery import conf
            >>> conf.always_eager

        * ``.get_queues`` -> {``app.amqp.get_queues``}

    * ``celery.utils.info``  
        * ``.humanize_seconds`` -> ``celery.utils.time.humanize_seconds``  
        * ``.textindent`` -> ``celery.utils.textindent``  
        * ``.get_broker_info`` -> {``app.amqp.get_broker_info``}  
        * ``.format_broker_info`` -> {``app.amqp.format_broker_info``}  
        * ``.format_queues`` -> {``app.amqp.format_queues``}


.. tab:: 英文

    * ``celery.execute``
        * ``.send_task`` -> {``app.send_task``}
        * ``.delay_task`` -> *no alternative*

    * ``celery.log``
        * ``.get_default_logger`` -> {``app.log.get_default_logger``}
        * ``.setup_logger`` -> {``app.log.setup_logger``}
        * ``.get_task_logger`` -> {``app.log.get_task_logger``}
        * ``.setup_task_logger`` -> {``app.log.setup_task_logger``}
        * ``.setup_logging_subsystem`` -> {``app.log.setup_logging_subsystem``}
        * ``.redirect_stdouts_to_logger`` -> {``app.log.redirect_stdouts_to_logger``}

    * ``celery.messaging``
        * ``.establish_connection`` -> {``app.broker_connection``}
        * ``.with_connection`` -> {``app.with_connection``}
        * ``.get_consumer_set`` -> {``app.amqp.get_task_consumer``}
        * ``.TaskPublisher`` -> {``app.amqp.TaskPublisher``}
        * ``.TaskConsumer`` -> {``app.amqp.TaskConsumer``}
        * ``.ConsumerSet`` -> {``app.amqp.ConsumerSet``}

    * ``celery.conf.*`` -> {``app.conf``}

        **NOTE**: All configuration keys are now named the same
        as in the configuration. So the key ``task_always_eager``
        is accessed as::

            >>> app.conf.task_always_eager

        instead of::

            >>> from celery import conf
            >>> conf.always_eager

        * ``.get_queues`` -> {``app.amqp.get_queues``}

    * ``celery.utils.info``
        * ``.humanize_seconds`` -> ``celery.utils.time.humanize_seconds``
        * ``.textindent`` -> ``celery.utils.textindent``
        * ``.get_broker_info`` -> {``app.amqp.get_broker_info``}
        * ``.format_broker_info`` -> {``app.amqp.format_broker_info``}
        * ``.format_queues`` -> {``app.amqp.format_queues``}

默认应用用法
=================

Default App Usage

.. tab:: 中文

    为了保持向后兼容，必须能够在不传递显式应用实例的情况下使用所有类/函数。

    这可以通过在应用实例缺失时，让所有依赖应用的对象使用 :data:`~celery.app.default_app` 来实现。

    .. code-block:: python

        from celery.app import app_or_default

        class SomeClass:

            def __init__(self, app=None):
                self.app = app_or_default(app)

    这种方法的问题在于，应用实例可能在过程中丢失，而一切看起来都正常。测试应用实例泄漏是很困难的。当启用环境变量 :envvar:`CELERY_TRACE_APP` 时， :func:`celery.app.app_or_default` 将会在每次需要回退到默认应用实例时引发异常。

.. tab:: 英文

    To be backward compatible, it must be possible
    to use all the classes/functions without passing
    an explicit app instance.

    This is achieved by having all app-dependent objects
    use :data:`~celery.app.default_app` if the app instance
    is missing.

    .. code-block:: python

        from celery.app import app_or_default

        class SomeClass:

            def __init__(self, app=None):
                self.app = app_or_default(app)

    The problem with this approach is that there's a chance
    that the app instance is lost along the way, and everything
    seems to be working normally. Testing app instance leaks
    is hard. The environment variable :envvar:`CELERY_TRACE_APP`
    can be used, when this is enabled :func:`celery.app.app_or_default`
    will raise an exception whenever it has to go back to the default app
    instance.

应用依赖关系树
-------------------

App Dependency Tree

* {``app``}
    * ``celery.loaders.base.BaseLoader``
    * ``celery.backends.base.BaseBackend``
    * {``app.TaskSet``}
        * ``celery.task.sets.TaskSet`` (``app.TaskSet``)
    * [``app.TaskSetResult``]
        * ``celery.result.TaskSetResult`` (``app.TaskSetResult``)

* {``app.AsyncResult``}
    * ``celery.result.BaseAsyncResult`` / ``celery.result.AsyncResult``

* ``celery.bin.worker.WorkerCommand``
    * ``celery.apps.worker.Worker``
        * ``celery.worker.WorkerController``
            * ``celery.worker.consumer.Consumer``
                * ``celery.worker.request.Request``
                * ``celery.events.EventDispatcher``
                * ``celery.worker.control.ControlDispatch``
                    * ``celery.worker.control.registry.Panel``
                    * ``celery.pidbox.BroadcastPublisher``
                * ``celery.pidbox.BroadcastConsumer``
            * ``celery.beat.EmbeddedService``

* ``celery.bin.events.EvCommand``
    * ``celery.events.snapshot.evcam``
        * ``celery.events.snapshot.Polaroid``
        * ``celery.events.EventReceiver``
    * ``celery.events.cursesmon.evtop``
        * ``celery.events.EventReceiver``
        * ``celery.events.cursesmon.CursesMonitor``
    * ``celery.events.dumper``
        * ``celery.events.EventReceiver``

* ``celery.bin.amqp.AMQPAdmin``

* ``celery.bin.beat.BeatCommand``
    * ``celery.apps.beat.Beat``
        * ``celery.beat.Service``
            * ``celery.beat.Scheduler``
