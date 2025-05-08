.. _brokers:

======================
Backends 和 Brokers
======================

Backends and Brokers

:Release: |version|
:Date: |today|

Celery 支持多种消息传输替代方案。

Celery supports several message transport alternatives.

.. _broker_toc:

Broker 指南
===================

Broker Instructions

.. toctree::
    :maxdepth: 1

    rabbitmq
    redis
    sqs
    kafka
    gcpubsub

.. _broker-overview:

Broker 概览
===============

Broker Overview

.. tab:: 中文

    这是各类传输方式的比较表，更多信息可参见每个传输方式的文档（见 :ref:`broker_toc`）。
    
    +---------------+--------------+----------------+--------------------+
    | **名称**      | **状态**     | **监控**       | **远程控制**       |
    +---------------+--------------+----------------+--------------------+
    | *RabbitMQ*    | Stable       | Yes            | Yes                |
    +---------------+--------------+----------------+--------------------+
    | *Redis*       | Stable       | Yes            | Yes                |
    +---------------+--------------+----------------+--------------------+
    | *Amazon SQS*  | Stable       | No             | No                 |
    +---------------+--------------+----------------+--------------------+
    | *Zookeeper*   | 实验性       | No             | No                 |
    +---------------+--------------+----------------+--------------------+
    | *Kafka*       | 实验性       | No             | No                 |
    +---------------+--------------+----------------+--------------------+
    | *GC PubSub*   | 实验性       | Yes            | Yes                |
    +---------------+--------------+----------------+--------------------+

    实验性代理可能可以正常工作，但没有专门的维护者。

    缺乏监控支持意味着该传输方式不实现事件功能，因此 Flower、 `celery events`、 `celerymon` 以及其他基于事件的监控工具将无法使用。

    远程控制支持表示可通过 `celery inspect` 和 `celery control` 命令（以及其他使用远程控制 API 的工具）在运行时检查和管理 worker。


.. tab:: 英文

    This is comparison table of the different transports supports,
    more information can be found in the documentation for each
    individual transport (see :ref:`broker_toc`).
    
    +---------------+--------------+----------------+--------------------+
    | **Name**      | **Status**   | **Monitoring** | **Remote Control** |
    +---------------+--------------+----------------+--------------------+
    | *RabbitMQ*    | Stable       | Yes            | Yes                |
    +---------------+--------------+----------------+--------------------+
    | *Redis*       | Stable       | Yes            | Yes                |
    +---------------+--------------+----------------+--------------------+
    | *Amazon SQS*  | Stable       | No             | No                 |
    +---------------+--------------+----------------+--------------------+
    | *Zookeeper*   | Experimental | No             | No                 |
    +---------------+--------------+----------------+--------------------+
    | *Kafka*       | Experimental | No             | No                 |
    +---------------+--------------+----------------+--------------------+
    | *GC PubSub*   | Experimental | Yes            | Yes                |
    +---------------+--------------+----------------+--------------------+
    
    Experimental brokers may be functional but they don't have
    dedicated maintainers.
    
    Missing monitor support means that the transport doesn't
    implement events, and as such Flower, `celery events`, `celerymon`
    and other event-based monitoring tools won't work.
    
    Remote control means the ability to inspect and manage workers
    at runtime using the `celery inspect` and `celery control` commands
    (and other tools using the remote control API).

摘要
=========

Summaries

.. tab:: 中文

    *注意：本节并不全面覆盖所有后端与消息代理。*

    Celery 能够使用多种后端（结果存储）与消息代理（消息传输）进行通信和数据存储。

.. tab:: 英文

    *Note: This section is not comprehensive of backends and brokers.*

    Celery has the ability to communicate and store with many different backends (Result Stores) and brokers (Message Transports).

Redis
-----

Redis

.. tab:: 中文

    Redis 可同时作为后端和消息代理使用。

    **作为 Broker：** Redis 适用于小消息的快速传输。大消息可能会导致系统拥堵。

    :ref:`详见文档 <broker-redis>`

    **作为 Backend：** Redis 是一个超快速的键值存储系统，使得任务结果的获取非常高效。需要考虑的是 Redis 的内存限制和持久化策略。如果结果持久化很重要，建议考虑其他数据库作为后端。


.. tab:: 英文

    Redis can be both a backend and a broker.

    **As a Broker:** Redis works well for rapid transport of small messages. Large messages can congest the system.

    :ref:`See documentation for details <broker-redis>`

    **As a Backend:** Redis is a super fast K/V store, making it very efficient for fetching the results of a task call. As with the design of Redis, you do have to consider the limit memory available to store your data, and how you handle data persistence. If result persistence is important, consider using another DB for your backend.

RabbitMQ
--------

RabbitMQ

.. tab:: 中文

    RabbitMQ 是一个消息代理。

    **作为 Broker：** RabbitMQ 对大消息的处理能力优于 Redis，但如果短时间内涌入大量消息，扩展能力可能成为问题。除非 RabbitMQ 运行在大规模部署环境下，否则可以考虑 Redis 或 SQS。

    :ref:`详见文档 <broker-rabbitmq>`

    **作为 Backend：** RabbitMQ 可通过 ``rpc://`` 后端存储结果，该后端会为每个客户端创建独立的临时队列。

    *注：RabbitMQ（作为 broker）与 Redis（作为 backend）是非常常见的组合。如果需要更可靠的结果持久化存储，可考虑使用 PostgreSQL、MySQL（通过 SQLAlchemy）、Cassandra 或自定义后端。*


.. tab:: 英文

    RabbitMQ is a broker.

    **As a Broker:** RabbitMQ handles larger messages better than Redis, however if many messages are coming in very quickly, scaling can become a concern and Redis or SQS should be considered unless RabbitMQ is running at very large scale.

    :ref:`See documentation for details <broker-rabbitmq>`

    **As a Backend:** RabbitMQ can store results via ``rpc://`` backend. This backend creates separate temporary queue for each client.

    *Note: RabbitMQ (as the broker) and Redis (as the backend) are very commonly used together. If more guaranteed long-term persistence is needed from the result store, consider using PostgreSQL or MySQL (through SQLAlchemy), Cassandra, or a custom defined backend.*

SQS
---

SQS

.. tab:: 中文

    SQS 是一个消息代理。

    如果你已经深度集成 AWS 并熟悉 SQS，它是一个很好的 broker 选择。它具备极强的可扩展性并由 AWS 完全托管，任务调度机制类似于 RabbitMQ。但它缺乏某些功能，例如 ``worker 远程控制命令``。

    :ref:`详见文档 <broker-sqs>`

.. tab:: 英文

    SQS is a broker.

    If you already integrate tightly with AWS, and are familiar with SQS, it presents a great option as a broker. It is extremely scalable and completely managed, and manages task delegation similarly to RabbitMQ. It does lack some of the features of the RabbitMQ broker such as ``worker remote control commands``.

    :ref:`See documentation for details <broker-sqs>`

SQLAlchemy
----------

SQLAlchemy

.. tab:: 中文

    SQLAlchemy 是一个后端。

    它使 Celery 能够与 MySQL、PostgreSQL、SQLite 等数据库进行接口交互。作为 ORM，它是 Celery 使用 SQL 数据库存储结果的方式。

    :ref:`详见文档 <conf-database-result-backend>`

.. tab:: 英文

    SQLAlchemy is a backend.

    It allows Celery to interface with MySQL, PostgreSQL, SQlite, and more. It is an ORM, and is the way Celery can use a SQL DB as a result backend.

    :ref:`See documentation for details <conf-database-result-backend>`

GCPubSub
--------

GCPubSub

.. tab:: 中文

    Google Cloud Pub/Sub 是一个消息代理。

    如果你已经深度集成 Google Cloud 并熟悉 Pub/Sub，它是一个很好的 broker 选择。它具备极强的可扩展性并由 Google 完全托管，任务调度机制类似于 RabbitMQ。

    :ref:`详见文档 <broker-gcpubsub>`

.. tab:: 英文

    Google Cloud Pub/Sub is a broker.

    If you already integrate tightly with Google Cloud, and are familiar with Pub/Sub, it presents a great option as a broker. It is extremely scalable and completely managed, and manages task delegation similarly to RabbitMQ.

    :ref:`See documentation for details <broker-gcpubsub>`
