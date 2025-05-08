.. _internals-worker:

=======================
内部的 worker
=======================

Internals: The worker


简介
============

Introduction

.. tab:: 中文

    Worker 包含四个主要组件：consumer（消费者）、scheduler（调度器）、mediator（协调器）和 task pool（任务池）。  
    这些组件并行运行，并使用两种数据结构：就绪队列（ready queue）和 ETA 调度表（ETA schedule）。

.. tab:: 英文

    The worker consists of 4 main components: the consumer, the scheduler,
    the mediator and the task pool. All these components runs in parallel working
    with two data structures: the ready queue and the ETA schedule.

数据结构
===============

Data structures

计时器
-----

timer

.. tab:: 中文

    定时器使用 :mod:`heapq` 来调度内部函数。  
    它非常高效，能够处理数十万个调度项。

.. tab:: 英文


    The timer uses :mod:`heapq` to schedule internal functions.
    It's very efficient and can handle hundred of thousands of entries.


组件
==========

Components


消费者
--------

Consumer

.. tab:: 中文

    通过 :pypi:`Kombu` 从 broker 接收消息。

    当接收到一条消息时，它会被转换为一个  
    :class:`celery.worker.request.Request` 对象。

    带有 ETA（最早可执行时间）或速率限制（rate-limit）的任务会被送入 `timer`，  
    可以立即执行的消息则被送入执行池（execution pool）。

    ETA 与速率限制同时使用时，任务会在 ETA 到达后执行，并遵循速率限制要求。

.. tab:: 英文


    Receives messages from the broker using :pypi:`Kombu`.

    When a message is received it's converted into a
    :class:`celery.worker.request.Request` object.

    Tasks with an ETA, or rate-limit are entered into the `timer`,
    messages that can be immediately processed are sent to the execution pool.

    ETA and rate-limit when used together will result in the rate limit being
    observed with the task being scheduled after the ETA.

计时器
-----

Timer

.. tab:: 中文

    定时器不仅调度内部函数（如清理操作与内部监控），  
    还调度 ETA 任务与速率受限任务。  
    如果调度任务的 ETA 已过，则该任务将被移动到执行池中。

.. tab:: 英文


    The timer schedules internal functions, like cleanup and internal monitoring,
    but also it schedules ETA tasks and rate limited tasks.
    If the scheduled tasks ETA has passed it is moved to the execution pool.

任务池
--------

TaskPool

.. tab:: 中文

    任务池是对 :class:`multiprocessing.Pool` 的轻微修改版本。  
    其行为基本一致，不同之处在于它确保所有 worker 始终在运行。  
    如果某个 worker 缺失，它将自动创建一个新的替代。

.. tab:: 英文


    This is a slightly modified :class:`multiprocessing.Pool`.
    It mostly works the same way, except it makes sure all of the workers
    are running at all times. If a worker is missing, it replaces
    it with a new one.
