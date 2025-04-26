.. _brokers:

======================
Backends 和 Brokers
======================

Backends and Brokers

.. tab:: 中文

.. tab:: 英文

:Release: |version|
:Date: |today|

Celery supports several message transport alternatives.

.. _broker_toc:

Broker Instructions
===================

Broker Instructions

.. tab:: 中文

.. tab:: 英文

.. toctree::
    :maxdepth: 1

    rabbitmq
    redis
    sqs
    kafka
    gcpubsub

.. _broker-overview:

Broker Overview
===============

Broker Overview

.. tab:: 中文

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

Summaries
=========

Summaries

.. tab:: 中文

.. tab:: 英文

*Note: This section is not comprehensive of backends and brokers.*

Celery has the ability to communicate and store with many different backends (Result Stores) and brokers (Message Transports).

Redis
-----

Redis

.. tab:: 中文

.. tab:: 英文

Redis can be both a backend and a broker.

**As a Broker:** Redis works well for rapid transport of small messages. Large messages can congest the system.

:ref:`See documentation for details <broker-redis>`

**As a Backend:** Redis is a super fast K/V store, making it very efficient for fetching the results of a task call. As with the design of Redis, you do have to consider the limit memory available to store your data, and how you handle data persistence. If result persistence is important, consider using another DB for your backend.

RabbitMQ
--------

RabbitMQ

.. tab:: 中文

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

.. tab:: 英文

SQS is a broker.

If you already integrate tightly with AWS, and are familiar with SQS, it presents a great option as a broker. It is extremely scalable and completely managed, and manages task delegation similarly to RabbitMQ. It does lack some of the features of the RabbitMQ broker such as ``worker remote control commands``.

:ref:`See documentation for details <broker-sqs>`

SQLAlchemy
----------

SQLAlchemy

.. tab:: 中文

.. tab:: 英文

SQLAlchemy is a backend.

It allows Celery to interface with MySQL, PostgreSQL, SQlite, and more. It is an ORM, and is the way Celery can use a SQL DB as a result backend.

:ref:`See documentation for details <conf-database-result-backend>`

GCPubSub
--------

GCPubSub

.. tab:: 中文

.. tab:: 英文

Google Cloud Pub/Sub is a broker.

If you already integrate tightly with Google Cloud, and are familiar with Pub/Sub, it presents a great option as a broker. It is extremely scalable and completely managed, and manages task delegation similarly to RabbitMQ.

:ref:`See documentation for details <broker-gcpubsub>`
