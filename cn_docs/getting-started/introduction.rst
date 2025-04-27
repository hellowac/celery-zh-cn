.. _intro:

========================
Celery 简介
========================

Introduction to Celery


什么是任务队列？
====================

What's a Task Queue?

.. tab:: 中文

    任务队列用于在不同的线程或机器之间分发工作负载。

    任务队列的输入是一种称为任务（task）的工作单元。专门的 worker 进程会持续监控任务队列，以获取新的工作任务来执行。

    Celery 通过消息进行通信，通常使用一个消息代理（broker）在客户端与 worker 之间进行协调。要启动一个任务，客户端会向队列中添加一条消息，然后 broker 会将该消息传递给某个 worker。

    一个 Celery 系统可以由多个 worker 和 broker 组成，从而实现高可用性（HA）和水平扩展（horizontal scaling）。

    Celery 使用 Python 编写，但其协议可以由任何语言实现。除了 Python，还有适用于 Node.js 的 node-celery_ 和 node-celery-ts_，以及一个 `PHP 客户端`_。

    也可以通过暴露 HTTP 接口，并让任务发起请求（即 webhook）来实现不同语言之间的互操作。

.. tab:: 英文

    Task queues are used as a mechanism to distribute work across threads or
    machines.

    A task queue's input is a unit of work called a task. Dedicated worker
    processes constantly monitor task queues for new work to perform.

    Celery communicates via messages, usually using a broker
    to mediate between clients and workers. To initiate a task the client adds a
    message to the queue, the broker then delivers that message to a worker.

    A Celery system can consist of multiple workers and brokers, giving way
    to high availability and horizontal scaling.

    Celery is written in Python, but the protocol can be implemented in any
    language. In addition to Python there's node-celery_ and node-celery-ts_ for Node.js,
    and a `PHP client`_.

    Language interoperability can also be achieved
    exposing an HTTP endpoint and having a task that requests it (webhooks).

.. _`PHP client`: https://github.com/gjedeer/celery-php
.. _`PHP 客户端`: https://github.com/gjedeer/celery-php
.. _node-celery: https://github.com/mher/node-celery
.. _node-celery-ts: https://github.com/IBM/node-celery-ts

我需要什么？
===============

What do I need?

.. tab:: 中文

    .. sidebar:: 版本要求
        :subtitle: Celery 5.3 支持的环境

        - Python ❨3.8, 3.9, 3.10, 3.11❩
        - PyPy3.8+ ❨v7.3.11+❩

        Celery 4.x 是最后一个支持 Python 2.7 的版本，
        从 Celery 5.x 开始，需要 Python 3.6 或更新的版本。
        Celery 5.1.x 也要求 Python 3.6 或更新，
        Celery 5.2.x 则需要 Python 3.7 或更新。

        如果你正在使用较旧版本的 Python，则需要使用对应的较旧版本的 Celery：

        - Python 2.7 或 Python 3.5：Celery 4.4 系列或更早版本。
        - Python 2.6：Celery 3.1 系列或更早版本。
        - Python 2.5：Celery 3.0 系列或更早版本。
        - Python 2.4：Celery 2.2 系列或更早版本。

        Celery 是一个资金非常有限的项目，
        因此我们**不支持 Microsoft Windows 平台**。
        请不要针对该平台提交任何问题。

    *Celery* 需要一个消息传输机制来发送和接收消息。
    RabbitMQ 和 Redis 的 broker 传输实现是功能完整的，
    此外还有许多其他实验性解决方案可用，包括使用 SQLite 进行本地开发。

    *Celery* 可以运行在单台机器上、多台机器上，甚至可以跨数据中心运行。

.. tab:: 英文

    .. sidebar:: Version Requirements
        :subtitle: Celery version 5.3 runs on

        - Python ❨3.8, 3.9, 3.10, 3.11❩
        - PyPy3.8+ ❨v7.3.11+❩

        Celery 4.x was the last version to support Python 2.7,
        Celery 5.x requires Python 3.6 or newer.
        Celery 5.1.x also requires Python 3.6 or newer.
        Celery 5.2.x requires Python 3.7 or newer.


        If you're running an older version of Python, you need to be running
        an older version of Celery:

        - Python 2.7 or Python 3.5: Celery series 4.4 or earlier.
        - Python 2.6: Celery series 3.1 or earlier.
        - Python 2.5: Celery series 3.0 or earlier.
        - Python 2.4 was Celery series 2.2 or earlier.

        Celery is a project with minimal funding,
        so we don't support Microsoft Windows.
        Please don't open any issues related to that platform.

    *Celery* requires a message transport to send and receive messages.
    The RabbitMQ and Redis broker transports are feature complete,
    but there's also support for a myriad of other experimental solutions, including
    using SQLite for local development.

    *Celery* can run on a single machine, on multiple machines, or even
    across data centers.

开始使用
===========

Get Started

.. tab:: 中文

    如果这是你第一次使用 Celery，或者你在 3.1 版本之后没有持续关注其发展（即从更早版本迁移过来），
    那么你应该首先阅读我们的入门教程：

    - :ref:`first-steps`
    - :ref:`next-steps`

.. tab:: 英文

    If this is the first time you're trying to use Celery, or if you haven't
    kept up with development in the 3.1 version and are coming from previous versions,
    then you should read our getting started tutorials:

    - :ref:`first-steps`
    - :ref:`next-steps`

Celery 是……
==============

Celery is…

.. _`mailing-list`: https://groups.google.com/group/celery-users

.. topic:: \

    .. tab:: 中文

        - **简单易用**

          Celery 易于使用和维护，且 *无需配置文件*。

          Celery 拥有一个活跃而友好的社区，
          你可以通过 `邮件列表`_ 和 :ref:`IRC 频道 <irc-channel>` 寻求支持。

          下面是一个最简单的应用示例：

          .. code-block:: python

                from celery import Celery

                app = Celery('hello', broker='amqp://guest@localhost//')

                @app.task
                def hello():
                    return 'hello world'

        - **高可用性**

          在连接丢失或失败时，worker 和客户端会自动重试连接，
          而且某些 broker 支持 *主主（Primary/Primary）* 或 *主备（Primary/Replica）* 复制机制。

        - **高性能**

          单个 Celery 进程可以每分钟处理数百万个任务，
          往返延迟（round-trip latency）可低于毫秒级（使用 RabbitMQ、librabbitmq 以及经过优化的配置）。

        - **高度灵活**

          *Celery* 几乎所有部分都可以被扩展或单独使用，
          包括自定义的进程池实现、序列化器、压缩方案、日志记录器、
          调度器（schedulers）、消费者（consumers）、生产者（producers）、broker 传输机制等等。

    .. tab:: 英文

        - **Simple**

            Celery is easy to use and maintain, and it *doesn't need configuration files*.

            It has an active, friendly community you can talk to for support,
            including a `mailing-list`_ and an :ref:`IRC channel <irc-channel>`.

            Here's one of the simplest applications you can make:

            .. code-block:: python

                from celery import Celery

                app = Celery('hello', broker='amqp://guest@localhost//')

                @app.task
                def hello():
                    return 'hello world'

        - **Highly Available**

            Workers and clients will automatically retry in the event
            of connection loss or failure, and some brokers support
            HA in way of *Primary/Primary* or *Primary/Replica* replication.

        - **Fast**

            A single Celery process can process millions of tasks a minute,
            with sub-millisecond round-trip latency (using RabbitMQ,
            librabbitmq, and optimized settings).

        - **Flexible**

            Almost every part of *Celery* can be extended or used on its own,
            Custom pool implementations, serializers, compression schemes, logging,
            schedulers, consumers, producers, broker transports, and much more.


.. topic:: 支持以下功能 / It supports

    .. tab:: 中文

        .. hlist::
            :columns: 2

            - **消息代理（Brokers）**

              - :ref:`RabbitMQ <broker-rabbitmq>`、:ref:`Redis <broker-redis>`，
              - :ref:`Amazon SQS <broker-sqs>`，以及更多……

            - **并发模式（Concurrency）**

              - prefork（多进程）
              - Eventlet_、gevent_
              - thread（多线程）
              - `solo`（单线程）

            - **结果存储（Result Stores）**

              - AMQP、Redis
              - Memcached
              - SQLAlchemy、Django ORM
              - Apache Cassandra、Elasticsearch、Riak
              - MongoDB、CouchDB、Couchbase、ArangoDB
              - Amazon DynamoDB、Amazon S3
              - Microsoft Azure Block Blob、Microsoft Azure Cosmos DB
              - Google Cloud Storage
              - 文件系统（File system）

            - **序列化（Serialization）**

              - *pickle*、*json*、*yaml*、*msgpack*
              - *zlib*、*bzip2* 压缩
              - 消息加密签名（Cryptographic message signing）

    .. tab:: 英文

        .. hlist::
            :columns: 2

            - **Brokers**

                - :ref:`RabbitMQ <broker-rabbitmq>`, :ref:`Redis <broker-redis>`,
                - :ref:`Amazon SQS <broker-sqs>`, and more…

            - **Concurrency**

                - prefork (multiprocessing),
                - Eventlet_, gevent_
                - thread (multithreaded)
                - `solo` (single threaded)

            - **Result Stores**

                - AMQP, Redis
                - Memcached,
                - SQLAlchemy, Django ORM
                - Apache Cassandra, Elasticsearch, Riak
                - MongoDB, CouchDB, Couchbase, ArangoDB
                - Amazon DynamoDB, Amazon S3
                - Microsoft Azure Block Blob, Microsoft Azure Cosmos DB
                - Google Cloud Storage
                - File system

            - **Serialization**

                - *pickle*, *json*, *yaml*, *msgpack*.
                - *zlib*, *bzip2* compression.
                - Cryptographic message signing.

功能
========

Features

.. topic:: \

    .. tab:: 中文
    
       .. hlist::
          :columns: 2
    
          - **监控（Monitoring）**
    
            worker 会发出一系列监控事件，
            内置工具和外部工具可以利用这些事件实时了解集群的运行状况。
    
            :ref:`阅读更多… <guide-monitoring>`。
    
          - **工作流（Work-flows）**
    
            可以使用一套我们称之为 "canvas" 的强大原语（primitives），
            来组合简单或复杂的工作流，
            包括分组（grouping）、链式调用（chaining）、分块处理（chunking）等。
    
            :ref:`阅读更多… <guide-canvas>`。
    
          - **时间与速率限制（Time & Rate Limits）**
    
            你可以控制每秒/每分钟/每小时执行的任务数量，
            也可以限制单个任务的最长运行时间，
            这些限制可以设置为默认值、应用于特定 worker，
            或单独应用于每种任务类型。
    
            :ref:`阅读更多… <worker-time-limits>`。
    
          - **调度（Scheduling）**
    
            你可以通过秒数或 :class:`~datetime.datetime` 指定任务的运行时间，
            也可以使用周期性任务（periodic tasks），
            基于简单的时间间隔或 Crontab 表达式进行重复调度，
            支持按分钟、小时、星期几、每月几号和每年几月进行设置。
    
            :ref:`阅读更多… <guide-beat>`。
    
          - **资源泄漏保护（Resource Leak Protection）**
    
            当用户任务发生资源泄漏（如内存或文件描述符泄漏）且无法控制时，
            可以使用 :option:`--max-tasks-per-child <celery worker --max-tasks-per-child>` 选项来进行保护。
    
            :ref:`阅读更多… <worker-max-tasks-per-child>`。
    
          - **用户自定义组件（User Components）**
    
            每个 worker 组件都可以自定义，
            用户还可以定义额外的组件。
            worker 是通过一组称为 "bootsteps" 的依赖关系图构建起来的，
            允许对 worker 内部行为进行细粒度控制。

    .. tab:: 英文
    
        .. hlist::
            :columns: 2
    
            - **Monitoring**
    
                A stream of monitoring events is emitted by workers and
                is used by built-in and external tools to tell you what
                your cluster is doing -- in real-time.
    
                :ref:`Read more… <guide-monitoring>`.
    
            - **Work-flows**
    
                Simple and complex work-flows can be composed using
                a set of powerful primitives we call the "canvas",
                including grouping, chaining, chunking, and more.
    
                :ref:`Read more… <guide-canvas>`.
    
            - **Time & Rate Limits**
    
                You can control how many tasks can be executed per second/minute/hour,
                or how long a task can be allowed to run, and this can be set as
                a default, for a specific worker or individually for each task type.
    
                :ref:`Read more… <worker-time-limits>`.
    
            - **Scheduling**
    
                You can specify the time to run a task in seconds or a
                :class:`~datetime.datetime`, or you can use
                periodic tasks for recurring events based on a
                simple interval, or Crontab expressions
                supporting minute, hour, day of week, day of month, and
                month of year.
    
                :ref:`Read more… <guide-beat>`.
    
            - **Resource Leak Protection**
    
                The :option:`--max-tasks-per-child <celery worker --max-tasks-per-child>`
                option is used for user tasks leaking resources, like memory or
                file descriptors, that are simply out of your control.
    
                :ref:`Read more… <worker-max-tasks-per-child>`.
    
            - **User Components**
    
                Each worker component can be customized, and additional components
                can be defined by the user. The worker is built up using "bootsteps" — a
                dependency graph enabling fine grained control of the worker's
                internals.

.. _`Eventlet`: http://eventlet.net/
.. _`gevent`: http://gevent.org/

框架集成
=====================

Framework Integration

.. tab:: 中文

    Celery 易于与各类 Web 框架集成，其中一些框架甚至提供了专门的集成包：

    +--------------------+------------------------+
    | `Pyramid`_         | :pypi:`pyramid_celery` |
    +--------------------+------------------------+
    | `Pylons`_          | :pypi:`celery-pylons`  |
    +--------------------+------------------------+
    | `Flask`_           | 不需要                 |
    +--------------------+------------------------+
    | `web2py`_          | :pypi:`web2py-celery`  |
    +--------------------+------------------------+
    | `Tornado`_         | :pypi:`tornado-celery` |
    +--------------------+------------------------+
    | `Tryton`_          | :pypi:`celery_tryton`  |
    +--------------------+------------------------+

    关于 `Django`_ ，请参考 :ref:`django-first-steps`。

    这些集成包并不是必需的，
    但它们可以使开发过程更简单，
    有时还提供了重要的扩展钩子，
    例如在 :manpage:`fork(2)` 时正确关闭数据库连接。

.. tab:: 英文

    Celery is easy to integrate with web frameworks, some of them even have
    integration packages:

    +--------------------+------------------------+
    | `Pyramid`_         | :pypi:`pyramid_celery` |
    +--------------------+------------------------+
    | `Pylons`_          | :pypi:`celery-pylons`  |
    +--------------------+------------------------+
    | `Flask`_           | not needed             |
    +--------------------+------------------------+
    | `web2py`_          | :pypi:`web2py-celery`  |
    +--------------------+------------------------+
    | `Tornado`_         | :pypi:`tornado-celery` |
    +--------------------+------------------------+
    | `Tryton`_          | :pypi:`celery_tryton`  |
    +--------------------+------------------------+

    For `Django`_ see :ref:`django-first-steps`.

    The integration packages aren't strictly necessary, but they can make
    development easier, and sometimes they add important hooks like closing
    database connections at :manpage:`fork(2)`.

.. _`Django`: https://djangoproject.com/
.. _`Pylons`: http://pylonshq.com/
.. _`Flask`: http://flask.pocoo.org/
.. _`web2py`: http://web2py.com/
.. _`Bottle`: https://bottlepy.org/
.. _`Pyramid`: http://docs.pylonsproject.org/en/latest/docs/pyramid.html
.. _`Tornado`: http://www.tornadoweb.org/
.. _`Tryton`: http://www.tryton.org/
.. _`tornado-celery`: https://github.com/mher/tornado-celery/

快速跳转
==========

Quick Jump

.. tab:: 中文

    .. topic:: 我想要 ⟶

        .. hlist::
            :columns: 2

            - :ref:`获取任务的返回值 <task-states>`
            - :ref:`在任务中使用日志记录 <task-logging>`
            - :ref:`了解最佳实践 <task-best-practices>`
            - :ref:`创建自定义的任务基类 <task-custom-classes>`
            - :ref:`为一组任务添加回调函数 <canvas-chord>`
            - :ref:`将一个任务拆分成多个小块 <canvas-chunks>`
            - :ref:`优化 worker 性能 <guide-optimizing>`
            - :ref:`查看内置任务状态列表 <task-builtin-states>`
            - :ref:`创建自定义任务状态 <custom-states>`
            - :ref:`设置自定义任务名称 <task-names>`
            - :ref:`跟踪任务何时开始执行 <task-track-started>`
            - :ref:`在任务失败时进行重试 <task-retry>`
            - :ref:`获取当前任务的 ID <task-request-info>`
            - :ref:`了解任务被发送到的队列 <task-request-info>`
            - :ref:`查看正在运行的 worker 列表 <monitoring-control>`
            - :ref:`清除所有消息 <monitoring-control>`
            - :ref:`查看 worker 正在执行的操作 <monitoring-control>`
            - :ref:`查看 worker 已注册的任务 <monitoring-control>`
            - :ref:`将任务迁移到新的消息代理 <monitoring-control>`
            - :ref:`查看事件消息类型列表 <event-reference>`
            - :ref:`参与 Celery 开发贡献 <contributing>`
            - :ref:`了解可用的配置项 <configuration>`
            - :ref:`查看使用 Celery 的公司和组织 <res-using-celery>`
            - :ref:`编写自定义远程控制命令 <worker-custom-control-commands>`
            - :ref:`在运行时修改 worker 的队列 <worker-queues>`

    .. topic:: 快速跳转 ⟶

        .. hlist::
            :columns: 4

            - :ref:`消息代理（Brokers） <brokers>`
            - :ref:`应用程序（Applications） <guide-app>`
            - :ref:`任务（Tasks） <guide-tasks>`
            - :ref:`调用（Calling） <guide-calling>`
            - :ref:`Worker（Workers） <guide-workers>`
            - :ref:`后台运行（Daemonizing） <daemonizing>`
            - :ref:`监控（Monitoring） <guide-monitoring>`
            - :ref:`优化（Optimizing） <guide-optimizing>`
            - :ref:`安全（Security） <guide-security>`
            - :ref:`路由（Routing） <guide-routing>`
            - :ref:`配置（Configuration） <configuration>`
            - :ref:`Django 集成（Django） <django>`
            - :ref:`贡献指南（Contributing） <contributing>`
            - :ref:`信号机制（Signals） <signals>`
            - :ref:`常见问题（FAQ） <faq>`
            - :ref:`API 参考（API Reference） <apiref>`


.. tab:: 英文

    .. topic:: I want to ⟶

        .. hlist::
            :columns: 2

            - :ref:`get the return value of a task <task-states>`
            - :ref:`use logging from my task <task-logging>`
            - :ref:`learn about best practices <task-best-practices>`
            - :ref:`create a custom task base class <task-custom-classes>`
            - :ref:`add a callback to a group of tasks <canvas-chord>`
            - :ref:`split a task into several chunks <canvas-chunks>`
            - :ref:`optimize the worker <guide-optimizing>`
            - :ref:`see a list of built-in task states <task-builtin-states>`
            - :ref:`create custom task states <custom-states>`
            - :ref:`set a custom task name <task-names>`
            - :ref:`track when a task starts <task-track-started>`
            - :ref:`retry a task when it fails <task-retry>`
            - :ref:`get the id of the current task <task-request-info>`
            - :ref:`know what queue a task was delivered to <task-request-info>`
            - :ref:`see a list of running workers <monitoring-control>`
            - :ref:`purge all messages <monitoring-control>`
            - :ref:`inspect what the workers are doing <monitoring-control>`
            - :ref:`see what tasks a worker has registered <monitoring-control>`
            - :ref:`migrate tasks to a new broker <monitoring-control>`
            - :ref:`see a list of event message types <event-reference>`
            - :ref:`contribute to Celery <contributing>`
            - :ref:`learn about available configuration settings <configuration>`
            - :ref:`get a list of people and companies using Celery <res-using-celery>`
            - :ref:`write my own remote control command <worker-custom-control-commands>`
            - :ref:`change worker queues at runtime <worker-queues>`

    .. topic:: Jump to ⟶

        .. hlist::
            :columns: 4

            - :ref:`Brokers <brokers>`
            - :ref:`Applications <guide-app>`
            - :ref:`Tasks <guide-tasks>`
            - :ref:`Calling <guide-calling>`
            - :ref:`Workers <guide-workers>`
            - :ref:`Daemonizing <daemonizing>`
            - :ref:`Monitoring <guide-monitoring>`
            - :ref:`Optimizing <guide-optimizing>`
            - :ref:`Security <guide-security>`
            - :ref:`Routing <guide-routing>`
            - :ref:`Configuration <configuration>`
            - :ref:`Django <django>`
            - :ref:`Contributing <contributing>`
            - :ref:`Signals <signals>`
            - :ref:`FAQ <faq>`
            - :ref:`API Reference <apiref>`

.. include:: ../includes/installation.txt
