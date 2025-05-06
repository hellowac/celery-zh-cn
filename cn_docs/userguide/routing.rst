.. _guide-routing:

===============
路由任务/Tasks
===============

Routing Tasks

.. tab:: 中文

    .. note::

        类似“主题（topic）”与“广播（fanout）”的路由概念并非在所有传输方案中都可用，
        请参阅 :ref:`transport comparison table <kombu:transport-comparison>` 获取详细信息。

.. tab:: 英文

    .. note::

        Alternate routing concepts like topic and fanout is not
        available for all transports, please consult the
        :ref:`transport comparison table <kombu:transport-comparison>`.

.. _routing-basics:

基础知识
======

Basics

.. _routing-automatic:

自动路由
-----------------

Automatic routing

.. tab:: 中文

    最简单的路由方式是启用 :setting:`task_create_missing_queues` 配置（默认已开启）。

    启用该设置后，在 :setting:`task_queues` 中未显式定义的命名队列会被自动创建。这使得执行简单的路由任务变得非常容易。

    假设你有两台处理常规任务的服务器 `x` 与 `y`，以及一台专门处理 feed 相关任务的服务器 `z`，你可以使用如下配置::

        task_routes = {'feed.tasks.import_feed': {'queue': 'feeds'}}

    启用上述路由后，feed 导入任务将会被路由到 `"feeds"` 队列，其它任务将会被路由到默认队列（历史原因下默认命名为 `"celery"`）。

    你也可以使用通配符或正则表达式来匹配 ``feed.tasks`` 命名空间中的所有任务：

    .. code-block:: python

        app.conf.task_routes = {'feed.tasks.*': {'queue': 'feeds'}}

    如果匹配顺序很重要，你应使用 *items* 格式来指定路由器：

    .. code-block:: python

        task_routes = ([
            ('feed.tasks.*', {'queue': 'feeds'}),
            ('web.tasks.*', {'queue': 'web'}),
            (re.compile(r'(video|image)\.tasks\..*'), {'queue': 'media'}),
        ],)

    .. note::

        配置项 :setting:`task_routes` 可以是一个字典，也可以是一个包含路由器对象的列表，
        所以在本例中我们使用元组包裹该列表以进行指定。

    在安装好路由器之后，你可以通过如下命令启动服务器 `z`，使其只处理 feeds 队列：

    .. code-block:: console

        user@z:/$ celery -A proj worker -Q feeds

    你可以指定任意数量的队列，因此你也可以让该服务器同时处理默认队列：

    .. code-block:: console

        user@z:/$ celery -A proj worker -Q feeds,celery

.. tab:: 英文

    The simplest way to do routing is to use the
    :setting:`task_create_missing_queues` setting (on by default).

    With this setting on, a named queue that's not already defined in
    :setting:`task_queues` will be created automatically. This makes it easy to
    perform simple routing tasks.

    Say you have two servers, `x`, and `y` that handle regular tasks,
    and one server `z`, that only handles feed related tasks. You can use this
    configuration::

        task_routes = {'feed.tasks.import_feed': {'queue': 'feeds'}}

    With this route enabled import feed tasks will be routed to the
    `"feeds"` queue, while all other tasks will be routed to the default queue
    (named `"celery"` for historical reasons).

    Alternatively, you can use glob pattern matching, or even regular expressions,
    to match all tasks in the ``feed.tasks`` name-space:

    .. code-block:: python

        app.conf.task_routes = {'feed.tasks.*': {'queue': 'feeds'}}

    If the order of matching patterns is important you should
    specify the router in *items* format instead:

    .. code-block:: python

        task_routes = ([
            ('feed.tasks.*', {'queue': 'feeds'}),
            ('web.tasks.*', {'queue': 'web'}),
            (re.compile(r'(video|image)\.tasks\..*'), {'queue': 'media'}),
        ],)

    .. note::

        The :setting:`task_routes` setting can either be a dictionary, or a
        list of router objects, so in this case we need to specify the setting
        as a tuple containing a list.

    After installing the router, you can start server `z` to only process the feeds
    queue like this:

    .. code-block:: console

        user@z:/$ celery -A proj worker -Q feeds

    You can specify as many queues as you want, so you can make this server
    process the default queue as well:

    .. code-block:: console

        user@z:/$ celery -A proj worker -Q feeds,celery

.. _routing-changing-default-queue:

更改默认队列的名称
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Changing the name of the default queue

.. tab:: 中文

    你可以通过以下配置修改默认队列的名称：

    .. code-block:: python

        app.conf.task_default_queue = 'default'

.. tab:: 英文

    You can change the name of the default queue by using the following
    configuration:

    .. code-block:: python

        app.conf.task_default_queue = 'default'

.. _routing-autoqueue-details:

队列的定义方式
~~~~~~~~~~~~~~~~~~~~~~~~~~

How the queues are defined

.. tab:: 中文

    该特性旨在为用户隐藏复杂的 AMQP 协议，实现基本需求即可使用。但你可能仍然对这些队列是如何声明的感兴趣。

    一个名为 `"video"` 的队列将会使用以下配置被创建：

    .. code-block:: javascript

        {'exchange': 'video',
        'exchange_type': 'direct',
        'routing_key': 'video'}

    对于非 AMQP 后端（如 `Redis` 或 `SQS`），它们不支持 exchange 的概念，因此要求 exchange 的名称与队列一致。该设计可确保其兼容。

.. tab:: 英文

    The point with this feature is to hide the complex AMQP protocol for users
    with only basic needs. However -- you may still be interested in how these queues
    are declared.

    A queue named `"video"` will be created with the following settings:

    .. code-block:: javascript

        {'exchange': 'video',
        'exchange_type': 'direct',
        'routing_key': 'video'}

    The non-AMQP backends like `Redis` or `SQS` don't support exchanges,
    so they require the exchange to have the same name as the queue. Using this
    design ensures it will work for them as well.

.. _routing-manual:

手动路由
--------------

Manual routing

.. tab:: 中文

    再次假设你有两台处理常规任务的服务器 `x` 与 `y`，以及一台专门处理 feed 任务的服务器 `z`，你可以使用如下配置：

    .. code-block:: python

        from kombu import Queue

        app.conf.task_default_queue = 'default'
        app.conf.task_queues = (
            Queue('default',    routing_key='task.#'),
            Queue('feed_tasks', routing_key='feed.#'),
        )
        app.conf.task_default_exchange = 'tasks'
        app.conf.task_default_exchange_type = 'topic'
        app.conf.task_default_routing_key = 'task.default'

    :setting:`task_queues` 是由 :class:`~kombu.entity.Queue` 实例组成的列表。
    如果你未为某项设置 exchange 或 exchange_type，这些值将从配置项
    :setting:`task_default_exchange` 与 :setting:`task_default_exchange_type` 中继承。

    要将任务路由至 `feed_tasks` 队列，可以在 :setting:`task_routes` 配置中添加如下条目：

    .. code-block:: python

        task_routes = {
                'feeds.tasks.import_feed': {
                    'queue': 'feed_tasks',
                    'routing_key': 'feed.import',
                },
        }

    你也可以通过 :meth:`Task.apply_async` 或 :func:`~celery.execute.send_task`
    的 `routing_key` 参数进行覆盖：

        >>> from feeds.tasks import import_feed
        >>> import_feed.apply_async(args=['http://cnn.com/rss'],
        ...                         queue='feed_tasks',
        ...                         routing_key='feed.import')

    要让服务器 `z` 专门消费 feed 队列，可以使用 :option:`celery worker -Q` 启动：

    .. code-block:: console

        user@z:/$ celery -A proj worker -Q feed_tasks --hostname=z@%h

    服务器 `x` 与 `y` 应配置为消费默认队列：

    .. code-block:: console

        user@x:/$ celery -A proj worker -Q default --hostname=x@%h
        user@y:/$ celery -A proj worker -Q default --hostname=y@%h

    如果你希望 feed 处理节点在高负载时也能处理常规任务，可以这样启动：

    .. code-block:: console

        user@z:/$ celery -A proj worker -Q feed_tasks,default --hostname=z@%h

    如果你想添加一个使用不同 exchange 的队列，只需显式指定 exchange 与类型：

    .. code-block:: python

        from kombu import Exchange, Queue

        app.conf.task_queues = (
            Queue('feed_tasks',    routing_key='feed.#'),
            Queue('regular_tasks', routing_key='task.#'),
            Queue('image_tasks',   exchange=Exchange('mediatasks', type='direct'),
                                routing_key='image.compress'),
        )

    如果你对上述术语感到困惑，建议你阅读 AMQP 相关文档。

    .. seealso::

        除了下面的 :ref:`amqp-primer` 外，还有一篇优秀的博文 `Rabbits and Warrens`_ 介绍了队列与交换机的概念；
        同时还有 `CloudAMQP 教程`，以及面向 RabbitMQ 用户的 `RabbitMQ FAQ`_，都可以作为信息来源。


.. tab:: 英文

    Say you have two servers, `x`, and `y` that handle regular tasks,
    and one server `z`, that only handles feed related tasks, you can use this
    configuration:

    .. code-block:: python

        from kombu import Queue

        app.conf.task_default_queue = 'default'
        app.conf.task_queues = (
            Queue('default',    routing_key='task.#'),
            Queue('feed_tasks', routing_key='feed.#'),
        )
        app.conf.task_default_exchange = 'tasks'
        app.conf.task_default_exchange_type = 'topic'
        app.conf.task_default_routing_key = 'task.default'

    :setting:`task_queues` is a list of :class:`~kombu.entity.Queue`
    instances.
    If you don't set the exchange or exchange type values for a key, these
    will be taken from the :setting:`task_default_exchange` and
    :setting:`task_default_exchange_type` settings.

    To route a task to the `feed_tasks` queue, you can add an entry in the
    :setting:`task_routes` setting:

    .. code-block:: python

        task_routes = {
                'feeds.tasks.import_feed': {
                    'queue': 'feed_tasks',
                    'routing_key': 'feed.import',
                },
        }


    You can also override this using the `routing_key` argument to
    :meth:`Task.apply_async`, or :func:`~celery.execute.send_task`:

        >>> from feeds.tasks import import_feed
        >>> import_feed.apply_async(args=['http://cnn.com/rss'],
        ...                         queue='feed_tasks',
        ...                         routing_key='feed.import')


    To make server `z` consume from the feed queue exclusively you can
    start it with the :option:`celery worker -Q` option:

    .. code-block:: console

        user@z:/$ celery -A proj worker -Q feed_tasks --hostname=z@%h

    Servers `x` and `y` must be configured to consume from the default queue:

    .. code-block:: console

        user@x:/$ celery -A proj worker -Q default --hostname=x@%h
        user@y:/$ celery -A proj worker -Q default --hostname=y@%h

    If you want, you can even have your feed processing worker handle regular
    tasks as well, maybe in times when there's a lot of work to do:

    .. code-block:: console

        user@z:/$ celery -A proj worker -Q feed_tasks,default --hostname=z@%h

    If you have another queue but on another exchange you want to add,
    just specify a custom exchange and exchange type:

    .. code-block:: python

        from kombu import Exchange, Queue

        app.conf.task_queues = (
            Queue('feed_tasks',    routing_key='feed.#'),
            Queue('regular_tasks', routing_key='task.#'),
            Queue('image_tasks',   exchange=Exchange('mediatasks', type='direct'),
                                routing_key='image.compress'),
        )

    If you're confused about these terms, you should read up on AMQP.

    .. seealso::

        In addition to the :ref:`amqp-primer` below, there's
        `Rabbits and Warrens`_, an excellent blog post describing queues and
        exchanges. There's also The `CloudAMQP tutorial`,
        For users of RabbitMQ the `RabbitMQ FAQ`_
        could be useful as a source of information.

.. _`Rabbits and Warrens`: http://web.archive.org/web/20160323134044/http://blogs.digitar.com/jjww/2009/01/rabbits-and-warrens/
.. _`CloudAMQP tutorial`: amqp in 10 minutes part 3
    https://www.cloudamqp.com/blog/2015-09-03-part4-rabbitmq-for-beginners-exchanges-routing-keys-bindings.html
.. _`RabbitMQ FAQ`: https://www.rabbitmq.com/faq.html

.. _routing-special_options:

特殊路由选项
=======================

Special Routing Options

.. _routing-options-rabbitmq-priorities:

RabbitMQ 消息优先级
---------------------------

RabbitMQ Message Priorities

.. tab:: 中文

    :supported transports: RabbitMQ

    .. versionadded:: 4.0

    可以通过设置 ``x-max-priority`` 参数来配置队列以支持优先级：

    .. code-block:: python

        from kombu import Exchange, Queue

        app.conf.task_queues = [
            Queue('tasks', Exchange('tasks'), routing_key='tasks',
                queue_arguments={'x-max-priority': 10}),
        ]

    可以使用 :setting:`task_queue_max_priority` 设置为所有队列配置一个默认优先级上限：

    .. code-block:: python

        app.conf.task_queue_max_priority = 10

    也可以使用 :setting:`task_default_priority` 为所有任务设置默认优先级：

    .. code-block:: python

        app.conf.task_default_priority = 5

.. tab:: 英文

    :supported transports: RabbitMQ

    .. versionadded:: 4.0

    Queues can be configured to support priorities by setting the
    ``x-max-priority`` argument:

    .. code-block:: python

        from kombu import Exchange, Queue

        app.conf.task_queues = [
            Queue('tasks', Exchange('tasks'), routing_key='tasks',
                queue_arguments={'x-max-priority': 10}),
        ]

    A default value for all queues can be set using the
    :setting:`task_queue_max_priority` setting:

    .. code-block:: python

        app.conf.task_queue_max_priority = 10

    A default priority for all tasks can also be specified using the
    :setting:`task_default_priority` setting:

    .. code-block:: python

        app.conf.task_default_priority = 5

.. _amqp-primer:


Redis 消息优先级
------------------------

Redis Message Priorities

.. tab:: 中文

    :supported transports: Redis

    虽然 Celery 的 Redis 传输支持读取任务的优先级字段，但 Redis 本身并不具备原生的优先级概念。在尝试使用 Redis 实现优先级功能前，请务必阅读以下说明，因为这可能会导致某些意料之外的行为。

    要启用基于优先级的任务调度，需配置传输选项中的 queue_order_strategy：

    .. code-block:: python

        app.conf.broker_transport_options = {
            'queue_order_strategy': 'priority',
        }

    该优先级支持机制是通过为每个队列创建多个列表（list）实现的。
    尽管理论上支持 10 个（0 到 9）优先级等级，但为了节省资源，默认会将其压缩为 4 个等级。
    也就是说，一个名为 celery 的队列实际上会被拆分为 4 个内部队列。

    优先级最高的队列仍然命名为 celery，其他的队列则会使用一个分隔符（默认是 `\x06\x16`）加上优先级数字附加在原始队列名后构成：

    .. code-block:: python

        ['celery', 'celery\x06\x163', 'celery\x06\x166', 'celery\x06\x169']

    如果你希望使用更多的优先级等级，或想更改默认分隔符，可以通过配置 priority_steps 与 sep 参数实现：

    .. code-block:: python

        app.conf.broker_transport_options = {
            'priority_steps': list(range(10)),
            'sep': ':',
            'queue_order_strategy': 'priority',
        }

    上述配置将生成如下的队列名称：

    .. code-block:: python

        ['celery', 'celery:1', 'celery:2', 'celery:3', 'celery:4', 'celery:5', 'celery:6', 'celery:7', 'celery:8', 'celery:9']

    需要注意的是，这种机制永远无法达到由消息代理服务器层实现的优先级那样的精确性，充其量是一种近似的实现。
    但对于大多数应用场景而言，这种机制可能已经足够用。


.. tab:: 英文

    :supported transports: Redis

    While the Celery Redis transport does honor the priority field, Redis itself has
    no notion of priorities. Please read this note before attempting to implement
    priorities with Redis as you may experience some unexpected behavior.

    To start scheduling tasks based on priorities you need to configure queue_order_strategy transport option.

    .. code-block:: python

        app.conf.broker_transport_options = {
            'queue_order_strategy': 'priority',
        }


    The priority support is implemented by creating n lists for each queue.
    This means that even though there are 10 (0-9) priority levels, these are
    consolidated into 4 levels by default to save resources. This means that a
    queue named celery will really be split into 4 queues.

    The highest priority queue will be named celery, and the the other queues will
    have a separator (by default `\x06\x16`) and their priority number appended to
    the queue name.

    .. code-block:: python

        ['celery', 'celery\x06\x163', 'celery\x06\x166', 'celery\x06\x169']


    If you want more priority levels or a different separator you can set the
    priority_steps and sep transport options:

    .. code-block:: python

        app.conf.broker_transport_options = {
            'priority_steps': list(range(10)),
            'sep': ':',
            'queue_order_strategy': 'priority',
        }

    The config above will give you these queue names:

    .. code-block:: python

        ['celery', 'celery:1', 'celery:2', 'celery:3', 'celery:4', 'celery:5', 'celery:6', 'celery:7', 'celery:8', 'celery:9']


    That said, note that this will never be as good as priorities implemented at the
    broker server level, and may be approximate at best. But it may still be good
    enough for your application.


AMQP 入门
===========

AMQP Primer

消息​​
--------

Messages

.. tab:: 中文

    一条消息由 *消息头* （headers）和 *消息体* （body）组成。Celery 使用消息头来存储消息的内容类型（content type）和内容编码（content encoding）。内容类型通常是用于序列化消息的格式。消息体包含要执行的任务名称、任务 ID（UUID）、调用时使用的参数，以及一些附加元数据 —— 比如重试次数或预计执行时间（ETA）等。

    以下是一个以 Python 字典形式表示的任务消息示例：

    .. code-block:: javascript

        {'task': 'myapp.tasks.add',
        'id': '54086c5e-6193-4575-8308-dbab76798756',
        'args': [4, 4],
        'kwargs': {}}

.. tab:: 英文

    A message consists of headers and a body. Celery uses headers to store
    the content type of the message and its content encoding. The
    content type is usually the serialization format used to serialize the
    message. The body contains the name of the task to execute, the
    task id (UUID), the arguments to apply it with and some additional
    meta-data -- like the number of retries or an ETA.

    This is an example task message represented as a Python dictionary:

    .. code-block:: javascript

        {'task': 'myapp.tasks.add',
        'id': '54086c5e-6193-4575-8308-dbab76798756',
        'args': [4, 4],
        'kwargs': {}}

.. _amqp-producers-consumers-brokers:

生产者、消费者和代理
---------------------------------

Producers, consumers, and brokers

.. tab:: 中文

    发送消息的一方通常称为 *发布者* （*publisher*）或 *生产者* （*producer*），而接收消息的一方称为 *消费者* （*consumer*）。

    *Broker* 是消息服务器，负责将消息从生产者路由给消费者。

    在 AMQP 相关的资料中，你很可能会频繁看到以下术语的使用：

.. tab:: 英文

    The client sending messages is typically called a *publisher*, or
    a *producer*, while the entity receiving messages is called
    a *consumer*.

    The *broker* is the message server, routing messages from producers
    to consumers.

    You're likely to see these terms used a lot in AMQP related material.

.. _amqp-exchanges-queues-keys:

交换器、队列和路由键
-----------------------------------

Exchanges, queues, and routing keys

.. tab:: 中文

    1. 消息被发送到交换器（exchange）。
    2. 交换器将消息路由到一个或多个队列。存在多种交换器类型，提供不同的路由机制或用于实现不同的消息模式。
    3. 消息在队列中等待，直到有消费者进行处理。
    4. 消息一旦被确认（acknowledge）处理后，就会从队列中删除。

    发送和接收消息的基本步骤如下：

    1. 创建一个交换器（exchange）
    2. 创建一个队列（queue）
    3. 将队列绑定到交换器

    Celery 会自动创建 :setting:`task_queues` 中定义的队列所需的实体（除非该队列的 `auto_declare` 设置为 :const:`False`）。

    下面是一个包含三个队列的配置示例；
    分别用于视频、图像，以及一个默认队列用于处理其他任务：

    .. code-block:: python

        from kombu import Exchange, Queue

        app.conf.task_queues = (
            Queue('default', Exchange('default'), routing_key='default'),
            Queue('videos',  Exchange('media'),   routing_key='media.video'),
            Queue('images',  Exchange('media'),   routing_key='media.image'),
        )
        app.conf.task_default_queue = 'default'
        app.conf.task_default_exchange_type = 'direct'
        app.conf.task_default_routing_key = 'default'

.. tab:: 英文

    1. Messages are sent to exchanges.
    2. An exchange routes messages to one or more queues. Several exchange types
       exists, providing different ways to do routing, or implementing
       different messaging scenarios.
    3. The message waits in the queue until someone consumes it.
    4. The message is deleted from the queue when it has been acknowledged.

    The steps required to send and receive messages are:

    1. Create an exchange
    2. Create a queue
    3. Bind the queue to the exchange.

    Celery automatically creates the entities necessary for the queues in
    :setting:`task_queues` to work (except if the queue's `auto_declare`
    setting is set to :const:`False`).

    Here's an example queue configuration with three queues;
    One for video, one for images, and one default queue for everything else:

    .. code-block:: python

        from kombu import Exchange, Queue

        app.conf.task_queues = (
            Queue('default', Exchange('default'), routing_key='default'),
            Queue('videos',  Exchange('media'),   routing_key='media.video'),
            Queue('images',  Exchange('media'),   routing_key='media.image'),
        )
        app.conf.task_default_queue = 'default'
        app.conf.task_default_exchange_type = 'direct'
        app.conf.task_default_routing_key = 'default'

.. _amqp-exchange-types:

交换器类型
--------------

Exchange types

.. tab:: 中文

    交换器类型（exchange type）定义了消息在交换器中是如何被路由的。
    AMQP 标准中定义的交换器类型有 `direct`、 `topic`、 `fanout` 和 `headers`。RabbitMQ 还支持一些非标准的交换器类型作为插件，比如 Michael Bridgen 提供的 `last-value-cache plug-in`_。

.. tab:: 英文

    The exchange type defines how the messages are routed through the exchange.
    The exchange types defined in the standard are `direct`, `topic`,
    `fanout` and `headers`. Also non-standard exchange types are available
    as plug-ins to RabbitMQ, like the `last-value-cache plug-in`_ by Michael
    Bridgen.

.. _`last-value-cache plug-in`:
    https://github.com/squaremo/rabbitmq-lvc-plugin

.. _amqp-exchange-type-direct:

直接交换器
~~~~~~~~~~~~~~~~

Direct exchanges

.. tab:: 中文

    Direct（直连）交换器按精确的路由键（routing key）进行匹配，因此一个绑定了路由键为 `video` 的队列只会接收到具有该路由键的消息。

.. tab:: 英文

    Direct exchanges match by exact routing keys, so a queue bound by
    the routing key `video` only receives messages with that routing key.

.. _amqp-exchange-type-topic:

主题交换器
~~~~~~~~~~~~~~~

Topic exchanges

.. tab:: 中文

    Topic（主题）交换器使用以点（ `.` ）分隔的单词作为路由键，并支持通配符： ``*`` （匹配一个单词）和 ``#`` （匹配零个或多个单词）。

    举例来说，若消息的路由键为 ``usa.news``、 ``usa.weather``、 ``norway.news`` 和 ``norway.weather``，则以下绑定方式均可使用：
    ``*.news`` （匹配所有新闻）、 ``usa.#`` （匹配所有美国相关消息）、 或 ``usa.weather`` （仅匹配美国天气类消息）。

.. tab:: 英文

    Topic exchanges matches routing keys using dot-separated words, and the
    wild-card characters: ``*`` (matches a single word), and ``#`` (matches
    zero or more words).

    With routing keys like ``usa.news``, ``usa.weather``, ``norway.news``, and
    ``norway.weather``, bindings could be ``*.news`` (all news), ``usa.#`` (all
    items in the USA), or ``usa.weather`` (all USA weather items).

.. _amqp-api:

相关 API 命令
--------------------

Related API commands

.. tab:: 中文

    .. method:: exchange.declare(exchange_name, type, passive,
                                durable, auto_delete, internal)

        按名称声明一个交换器（exchange）。

        参见 :meth:`amqp:Channel.exchange_declare <amqp.channel.Channel.exchange_declare>`。

        :keyword passive: 如果为 True，表示被动声明，即不会创建交换器，
            但可以用来检查该交换器是否已存在。

        :keyword durable: 持久化的交换器在 broker 重启后仍然存在。

        :keyword auto_delete: 表示当没有队列使用该交换器时，broker 会自动将其删除。


    .. method:: queue.declare(queue_name, passive, durable, exclusive, auto_delete)

        按名称声明一个队列。

        参见 :meth:`amqp:Channel.queue_declare <amqp.channel.Channel.queue_declare>`

        独占队列（exclusive）只能被当前连接消费。
        设为独占的队列也隐含了 `auto_delete` 属性。

    .. method:: queue.bind(queue_name, exchange_name, routing_key)

        使用路由键将一个队列绑定到一个交换器。

        未绑定的队列无法接收消息，因此绑定是必要的操作。

        参见 :meth:`amqp:Channel.queue_bind <amqp.channel.Channel.queue_bind>`

    .. method:: queue.delete(name, if_unused=False, if_empty=False)

        删除一个队列及其绑定关系。

        参见 :meth:`amqp:Channel.queue_delete <amqp.channel.Channel.queue_delete>`

    .. method:: exchange.delete(name, if_unused=False)

        删除一个交换器。

        参见 :meth:`amqp:Channel.exchange_delete <amqp.channel.exchange_delete>`

    .. note::

        声明（declare）并不一定意味着“创建”。声明的本质是 *断言* 该实体存在且可操作。
        并没有规定是消费者还是生产者负责最初创建交换器、队列或绑定。
        通常是首先需要它的一方负责创建。

.. tab:: 英文

    .. method:: exchange.declare(exchange_name, type, passive,
                                durable, auto_delete, internal)
        :no-index:

        Declares an exchange by name.

        See :meth:`amqp:Channel.exchange_declare <amqp.channel.Channel.exchange_declare>`.

        :keyword passive: Passive means the exchange won't be created, but you
            can use this to check if the exchange already exists.

        :keyword durable: Durable exchanges are persistent (i.e., they survive
            a broker restart).

        :keyword auto_delete: This means the exchange will be deleted by the broker
            when there are no more queues using it.


    .. method:: queue.declare(queue_name, passive, durable, exclusive, auto_delete)
        :no-index:

        Declares a queue by name.

        See :meth:`amqp:Channel.queue_declare <amqp.channel.Channel.queue_declare>`

        Exclusive queues can only be consumed from by the current connection.
        Exclusive also implies `auto_delete`.

    .. method:: queue.bind(queue_name, exchange_name, routing_key)
        :no-index:

        Binds a queue to an exchange with a routing key.

        Unbound queues won't receive messages, so this is necessary.

        See :meth:`amqp:Channel.queue_bind <amqp.channel.Channel.queue_bind>`

    .. method:: queue.delete(name, if_unused=False, if_empty=False)
        :no-index:

        Deletes a queue and its binding.

        See :meth:`amqp:Channel.queue_delete <amqp.channel.Channel.queue_delete>`

    .. method:: exchange.delete(name, if_unused=False)
        :no-index:

        Deletes an exchange.

        See :meth:`amqp:Channel.exchange_delete <amqp.channel.Channel.exchange_delete>`

    .. note::

        Declaring doesn't necessarily mean "create". When you declare you
        *assert* that the entity exists and that it's operable. There's no
        rule as to whom should initially create the exchange/queue/binding,
        whether consumer or producer. Usually the first one to need it will
        be the one to create it.

.. _amqp-api-hands-on:

API 实践
---------------------

Hands-on with the API

.. tab:: 中文

    Celery 提供了一个命令行工具 :program:`celery amqp`，
    可用于访问 AMQP API，执行管理任务，比如创建/删除队列和交换器、
    清空队列或发送消息。它也可以用于非 AMQP 的 broker，
    但不同实现可能不会支持所有命令。

    你可以将命令作为参数直接传给 :program:`celery amqp`，
    也可以不传参数启动交互式 shell 模式：

    .. code-block:: console

        $ celery -A proj amqp
        -> connecting to amqp://guest@localhost:5672/.
        -> connected.
        1>

    此处的 ``1>`` 是命令提示符。数字 1 表示你目前已执行的命令数。
    输入 ``help`` 可获取所有可用命令的列表。
    该工具还支持自动补全 —— 输入命令的前缀后按下 `tab` 键即可显示可能的匹配项。

    下面是创建一个可用于发送消息的队列的过程：

    .. code-block:: console

        $ celery -A proj amqp
        1> exchange.declare testexchange direct
        ok.
        2> queue.declare testqueue
        ok. queue:testqueue messages:0 consumers:0.
        3> queue.bind testqueue testexchange testkey
        ok.

    上述操作创建了一个 direct 类型的交换器 ``testexchange``，以及一个名为 ``testqueue`` 的队列。
    该队列使用路由键 ``testkey`` 与交换器绑定。

    从现在起，所有发送到交换器 ``testexchange`` 且路由键为 ``testkey`` 的消息都会被路由到该队列。
    你可以使用 ``basic.publish`` 命令发送一条消息：

    .. code-block:: console

        4> basic.publish 'This is a message!' testexchange testkey
        ok.

    消息发送后，你可以取回它。这里我们使用 ``basic.get`` 命令，它以同步方式轮询队列以获取新消息
    （该方式适合维护任务，对于服务则推荐使用 ``basic.consume``）。

    从队列中取出一条消息：

    .. code-block:: console

        5> basic.get testqueue
        {'body': 'This is a message!',
        'delivery_info': {'delivery_tag': 1,
                        'exchange': u'testexchange',
                        'message_count': 0,
                        'redelivered': False,
                        'routing_key': u'testkey'},
        'properties': {}}

    AMQP 使用确认（acknowledgment）机制来表明消息已成功接收并处理。
    如果消息未被确认且消费者通道被关闭，该消息将被重新投递给其他消费者。

    请注意上面结构中的 delivery tag；
    在一个连接通道中，每条接收到的消息都有一个唯一的 delivery tag，
    用于对该消息进行确认。
    需要注意的是 delivery tag 在不同连接之间并不唯一，因此另一个客户端中的 tag `1`
    可能对应不同的消息。

    你可以使用 ``basic.ack`` 命令确认接收到的消息：

    .. code-block:: console

        6> basic.ack 1
        ok.

    最后，为了清理测试过程中的资源，应删除创建的实体：

    .. code-block:: console

        7> queue.delete testqueue
        ok. 0 messages deleted.
        8> exchange.delete testexchange
        ok.


.. tab:: 英文

    Celery comes with a tool called :program:`celery amqp`
    that's used for command line access to the AMQP API, enabling access to
    administration tasks like creating/deleting queues and exchanges, purging
    queues or sending messages. It can also be used for non-AMQP brokers,
    but different implementation may not implement all commands.

    You can write commands directly in the arguments to :program:`celery amqp`,
    or just start with no arguments to start it in shell-mode:

    .. code-block:: console

        $ celery -A proj amqp
        -> connecting to amqp://guest@localhost:5672/.
        -> connected.
        1>

    Here ``1>`` is the prompt. The number 1, is the number of commands you
    have executed so far. Type ``help`` for a list of commands available.
    It also supports auto-completion, so you can start typing a command and then
    hit the `tab` key to show a list of possible matches.

    Let's create a queue you can send messages to:

    .. code-block:: console

        $ celery -A proj amqp
        1> exchange.declare testexchange direct
        ok.
        2> queue.declare testqueue
        ok. queue:testqueue messages:0 consumers:0.
        3> queue.bind testqueue testexchange testkey
        ok.

    This created the direct exchange ``testexchange``, and a queue
    named ``testqueue``. The queue is bound to the exchange using
    the routing key ``testkey``.

    From now on all messages sent to the exchange ``testexchange`` with routing
    key ``testkey`` will be moved to this queue. You can send a message by
    using the ``basic.publish`` command:

    .. code-block:: console

        4> basic.publish 'This is a message!' testexchange testkey
        ok.

    Now that the message is sent you can retrieve it again. You can use the
    ``basic.get`` command here, that polls for new messages on the queue
    in a synchronous manner
    (this is OK for maintenance tasks, but for services you want to use
    ``basic.consume`` instead)

    Pop a message off the queue:

    .. code-block:: console

        5> basic.get testqueue
        {'body': 'This is a message!',
        'delivery_info': {'delivery_tag': 1,
                        'exchange': u'testexchange',
                        'message_count': 0,
                        'redelivered': False,
                        'routing_key': u'testkey'},
        'properties': {}}


    AMQP uses acknowledgment to signify that a message has been received
    and processed successfully. If the message hasn't been acknowledged
    and consumer channel is closed, the message will be delivered to
    another consumer.

    Note the delivery tag listed in the structure above; Within a connection
    channel, every received message has a unique delivery tag,
    This tag is used to acknowledge the message. Also note that
    delivery tags aren't unique across connections, so in another client
    the delivery tag `1` might point to a different message than in this channel.

    You can acknowledge the message you received using ``basic.ack``:

    .. code-block:: console

        6> basic.ack 1
        ok.

    To clean up after our test session you should delete the entities you created:

    .. code-block:: console

        7> queue.delete testqueue
        ok. 0 messages deleted.
        8> exchange.delete testexchange
        ok.


.. _routing-tasks:

路由任务
=============

Routing Tasks

.. _routing-defining-queues:

定义队列
---------------

Defining queues

.. tab:: 中文

    在 Celery 中，可用的队列由 :setting:`task_queues` 设置定义。

    以下是一个包含三个队列的示例队列配置；
    一个用于视频，一个用于图像，还有一个默认队列，用于处理其他所有任务：

    .. code-block:: python

        default_exchange = Exchange('default', type='direct')
        media_exchange = Exchange('media', type='direct')

        app.conf.task_queues = (
            Queue('default', default_exchange, routing_key='default'),
            Queue('videos', media_exchange, routing_key='media.video'),
            Queue('images', media_exchange, routing_key='media.image')
        )
        app.conf.task_default_queue = 'default'
        app.conf.task_default_exchange = 'default'
        app.conf.task_default_routing_key = 'default'

    在上述配置中，:setting:`task_default_queue` 将用于路由那些未显式指定路由的任务。

    默认交换器、交换器类型和路由键将作为任务的默认路由参数，同时也作为
    :setting:`task_queues` 项中条目的默认值。

    还支持将多个绑定连接到同一个队列。以下是一个将两个路由键绑定到同一个队列的示例：

    .. code-block:: python

        from kombu import Exchange, Queue, binding

        media_exchange = Exchange('media', type='direct')

        CELERY_QUEUES = (
            Queue('media', [
                binding(media_exchange, routing_key='media.video'),
                binding(media_exchange, routing_key='media.image'),
            ]),
        )

.. tab:: 英文

    In Celery available queues are defined by the :setting:`task_queues` setting.

    Here's an example queue configuration with three queues;
    One for video, one for images, and one default queue for everything else:

    .. code-block:: python

        default_exchange = Exchange('default', type='direct')
        media_exchange = Exchange('media', type='direct')

        app.conf.task_queues = (
            Queue('default', default_exchange, routing_key='default'),
            Queue('videos', media_exchange, routing_key='media.video'),
            Queue('images', media_exchange, routing_key='media.image')
        )
        app.conf.task_default_queue = 'default'
        app.conf.task_default_exchange = 'default'
        app.conf.task_default_routing_key = 'default'

    Here, the :setting:`task_default_queue` will be used to route tasks that
    doesn't have an explicit route.

    The default exchange, exchange type, and routing key will be used as the
    default routing values for tasks, and as the default values for entries
    in :setting:`task_queues`.

    Multiple bindings to a single queue are also supported.  Here's an example
    of two routing keys that are both bound to the same queue:

    .. code-block:: python

        from kombu import Exchange, Queue, binding

        media_exchange = Exchange('media', type='direct')

        CELERY_QUEUES = (
            Queue('media', [
                binding(media_exchange, routing_key='media.video'),
                binding(media_exchange, routing_key='media.image'),
            ]),
        )


.. _routing-task-destination:

指定任务目标
---------------------------

Specifying task destination

.. tab:: 中文

    任务的投递目标由以下内容决定（按顺序）：

    1. 调用 :func:`Task.apply_async` 时传入的路由参数。
    2. 在 :class:`~celery.app.task.Task` 上定义的与路由相关的属性。
    3. 在 :setting:`task_routes` 中定义的 :ref:`routers`。

    最佳实践是不硬编码这些设置，而是通过使用 :ref:`routers` 留作配置选项；
    这是一种最灵活的方式，但仍可以通过任务属性设置合理的默认值。

.. tab:: 英文

    The destination for a task is decided by the following (in order):

    1. The routing arguments to :func:`Task.apply_async`.
    2. Routing related attributes defined on the :class:`~celery.app.task.Task`
       itself.
    3. The :ref:`routers` defined in :setting:`task_routes`.

    It's considered best practice to not hard-code these settings, but rather
    leave that as configuration options by using :ref:`routers`;
    This is the most flexible approach, but sensible defaults can still be set
    as task attributes.

.. _routers:

路由器
-------

Routers

.. tab:: 中文

    路由器是决定任务路由选项的函数。

    定义一个新的路由器函数，只需要定义一个具有如下签名的函数：
    ``(name, args, kwargs, options, task=None, **kw)``：

    .. code-block:: python

        def route_task(name, args, kwargs, options, task=None, **kw):
                if name == 'myapp.tasks.compress_video':
                    return {'exchange': 'video',
                            'exchange_type': 'topic',
                            'routing_key': 'video.compress'}

    如果你返回了 ``queue`` 键，它将会展开成该队列在 :setting:`task_queues` 中定义的设置：

    .. code-block:: javascript

        {'queue': 'video', 'routing_key': 'video.compress'}

    展开为 -->

    .. code-block:: javascript

            {'queue': 'video',
            'exchange': 'video',
            'exchange_type': 'topic',
            'routing_key': 'video.compress'}

    你可以通过将路由器类添加到 :setting:`task_routes` 设置中来安装它们：

    .. code-block:: python

        task_routes = (route_task,)

    路由器函数也可以通过名称添加：

    .. code-block:: python

        task_routes = ('myapp.routers.route_task',)

    对于简单的任务名 -> 路由映射，你可以直接将字典传递给 :setting:`task_routes`，
    以实现与上述示例相同的行为：

    .. code-block:: python

        task_routes = {
            'myapp.tasks.compress_video': {
                'queue': 'video',
                'routing_key': 'video.compress',
            },
        }

    之后路由器将按顺序遍历，只要遇到一个返回了真值的路由器，就会停止，并使用该路由作为任务的最终路由。

    你也可以将多个路由器按顺序定义在列表中：

    .. code-block:: python

        task_routes = [
            route_task,
            {
                'myapp.tasks.compress_video': {
                    'queue': 'video',
                    'routing_key': 'video.compress',
            },
        ]

    这些路由器将依次被调用，选择第一个返回值的路由器作为结果。

    如果你使用的是 Redis 或 RabbitMQ，也可以在路由中指定队列的默认优先级：

    .. code-block:: python

        task_routes = {
            'myapp.tasks.compress_video': {
                'queue': 'video',
                'routing_key': 'video.compress',
                'priority': 10,
            },
        }

    类似地，调用任务的 `apply_async` 方法也可以覆盖默认优先级：

    .. code-block:: python

        task.apply_async(priority=0)


    .. admonition:: 优先级顺序与集群响应性

        需要注意的是，由于 worker 预取（prefetching）机制的存在，
        如果一批任务在同一时间提交，可能最初不会按优先级顺序执行。
        禁用 worker 预取可以避免该问题，但对于短小快速的任务，这可能会导致性能下降。
        在大多数情况下，仅将 `worker_prefetch_multiplier` 降为 1 就是更简单且更优雅的方式，
        它能提高系统响应性而不需完全禁用预取。

        注意，在使用 Redis broker 时，优先级值是逆序排序的：0 表示最高优先级。


.. tab:: 英文

    A router is a function that decides the routing options for a task.

    All you need to define a new router is to define a function with
    the signature ``(name, args, kwargs, options, task=None, **kw)``:

    .. code-block:: python

        def route_task(name, args, kwargs, options, task=None, **kw):
                if name == 'myapp.tasks.compress_video':
                    return {'exchange': 'video',
                            'exchange_type': 'topic',
                            'routing_key': 'video.compress'}

    If you return the ``queue`` key, it'll expand with the defined settings of
    that queue in :setting:`task_queues`:

    .. code-block:: javascript

        {'queue': 'video', 'routing_key': 'video.compress'}

    becomes -->

    .. code-block:: javascript

            {'queue': 'video',
            'exchange': 'video',
            'exchange_type': 'topic',
            'routing_key': 'video.compress'}


    You install router classes by adding them to the :setting:`task_routes`
    setting:

    .. code-block:: python

        task_routes = (route_task,)

    Router functions can also be added by name:

    .. code-block:: python

        task_routes = ('myapp.routers.route_task',)


    For simple task name -> route mappings like the router example above,
    you can simply drop a dict into :setting:`task_routes` to get the
    same behavior:

    .. code-block:: python

        task_routes = {
            'myapp.tasks.compress_video': {
                'queue': 'video',
                'routing_key': 'video.compress',
            },
        }

    The routers will then be traversed in order, it will stop at the first router
    returning a true value, and use that as the final route for the task.

    You can also have multiple routers defined in a sequence:

    .. code-block:: python

        task_routes = [
            route_task,
            {
                'myapp.tasks.compress_video': {
                    'queue': 'video',
                    'routing_key': 'video.compress',
            },
        ]

    The routers will then be visited in turn, and the first to return
    a value will be chosen.

    If you\'re using Redis or RabbitMQ you can also specify the queue\'s default priority
    in the route.

    .. code-block:: python

        task_routes = {
            'myapp.tasks.compress_video': {
                'queue': 'video',
                'routing_key': 'video.compress',
                'priority': 10,
            },
        }


    Similarly, calling `apply_async` on a task will override that
    default priority.

    .. code-block:: python

        task.apply_async(priority=0)


    .. admonition:: Priority Order and Cluster Responsiveness

        It is important to note that, due to worker prefetching, if a bunch of tasks
        submitted at the same time they may be out of priority order at first.
        Disabling worker prefetching will prevent this issue, but may cause less than
        ideal performance for small, fast tasks. In most cases, simply reducing
        `worker_prefetch_multiplier` to 1 is an easier and cleaner way to increase the
        responsiveness of your system without the costs of disabling prefetching
        entirely.

        Note that priorities values are sorted in reverse when
        using the redis broker: 0 being highest priority.


广播
---------

Broadcast

.. tab:: 中文

    Celery 也支持广播路由（broadcast routing）。
    下面是一个名为 ``broadcast_tasks`` 的交换器示例，它会将任务的副本
    发送给所有连接到它的 worker：

    .. code-block:: python

        from kombu.common import Broadcast

        app.conf.task_queues = (Broadcast('broadcast_tasks'),)
        app.conf.task_routes = {
            'tasks.reload_cache': {
                'queue': 'broadcast_tasks',
                'exchange': 'broadcast_tasks'
            }
        }

    现在， ``tasks.reload_cache`` 任务将会被发送给所有从该队列消费的 worker。

    以下是另一个使用广播路由的示例，这次是结合 :program:`celery beat` 调度器：

    .. code-block:: python

        from kombu.common import Broadcast
        from celery.schedules import crontab

        app.conf.task_queues = (Broadcast('broadcast_tasks'),)

        app.conf.beat_schedule = {
            'test-task': {
                'task': 'tasks.reload_cache',
                'schedule': crontab(minute=0, hour='*/3'),
                'options': {'exchange': 'broadcast_tasks'}
            },
        }


    .. admonition:: 广播与结果存储

        请注意，Celery 的任务结果机制并未定义当两个任务具有相同 task_id 时会发生什么。
        如果同一个任务被分发给多个 worker，那么任务状态的历史记录可能无法被保留。

        在这种情况下，建议设置 ``task.ignore_result`` 属性以避免不一致。


.. tab:: 英文

    Celery can also support broadcast routing.
    Here is an example exchange ``broadcast_tasks`` that delivers
    copies of tasks to all workers connected to it:

    .. code-block:: python

        from kombu.common import Broadcast

        app.conf.task_queues = (Broadcast('broadcast_tasks'),)
        app.conf.task_routes = {
            'tasks.reload_cache': {
                'queue': 'broadcast_tasks',
                'exchange': 'broadcast_tasks'
            }
        }

    Now the ``tasks.reload_cache`` task will be sent to every
    worker consuming from this queue.

    Here is another example of broadcast routing, this time with
    a :program:`celery beat` schedule:

    .. code-block:: python

        from kombu.common import Broadcast
        from celery.schedules import crontab

        app.conf.task_queues = (Broadcast('broadcast_tasks'),)

        app.conf.beat_schedule = {
            'test-task': {
                'task': 'tasks.reload_cache',
                'schedule': crontab(minute=0, hour='*/3'),
                'options': {'exchange': 'broadcast_tasks'}
            },
        }


    .. admonition:: Broadcast & Results

        Note that Celery result doesn't define what happens if two
        tasks have the same task_id. If the same task is distributed to more
        than one worker, then the state history may not be preserved.

        It's a good idea to set the ``task.ignore_result`` attribute in
        this case.
