.. _concurrency:

=============
并发
=============

Concurrency

:Release: |version|
:Date: |today|

.. tab:: 中文

    Celery 中的并发机制支持任务的并行执行。默认使用的 `prefork` 模式适用于多种场景，通常推荐大多数用户采用。
    实际上，切换到其他模式时，某些功能（如 `soft_timeout` 和 `max_tasks_per_child`）会被悄然禁用。

    本页面简要介绍了可用的并发选项。你可以在启动 worker 时使用 `--pool` 选项进行选择。

.. tab:: 英文

    Concurrency in Celery enables the parallel execution of tasks. The default
    model, `prefork`, is well-suited for many scenarios and generally recommended
    for most users.  In fact, switching to another mode will silently disable
    certain features like `soft_timeout` and `max_tasks_per_child`.

    This page gives a quick overview of the available options which you can pick
    between using the `--pool` option when starting the worker.

并发选项概述
-------------------------------

Overview of Concurrency Options

.. tab:: 中文

    - `prefork`：默认选项，适用于 CPU 密集型任务和大多数使用场景。
      它稳健可靠，除非有特殊需求，推荐使用该模式。
    - `eventlet` 和 `gevent`：适用于 IO 密集型任务，这些模式使用 greenlet 提供高并发能力。
      注意，某些特性如 `soft_timeout` 在这些模式下不可用。相关文档详见下方链接。
    - `solo`：在主线程中顺序执行任务。
    - `threads`：通过线程实现并发，需要系统支持 `concurrent.futures` 模块。
    - `custom`：可通过环境变量指定自定义的 worker 池实现。

    .. note::
        虽然 `eventlet` 和 `gevent` 等替代模式可用，但它们可能缺少相较于 `prefork` 的某些功能。
        除非有明确的需求，否则建议默认从 `prefork` 模式开始使用。

.. tab:: 英文

    - `prefork`: The default option, ideal for CPU-bound tasks and most use cases.
      It is robust and recommended unless there's a specific need for another model.
    - `eventlet` and `gevent`: Designed for IO-bound tasks, these models use
      greenlets for high concurrency. Note that certain features, like `soft_timeout`,
      are not available in these modes.  These have detailed documentation pages
      linked below.
    - `solo`: Executes tasks sequentially in the main thread.
    - `threads`: Utilizes threading for concurrency, available if the
      `concurrent.futures` module is present.
    - `custom`: Enables specifying a custom worker pool implementation through
      environment variables.

    .. note::
        While alternative models like `eventlet` and `gevent` are available, they
        may lack certain features compared to `prefork`. We recommend `prefork` as
        the starting point unless specific requirements dictate otherwise.

.. toctree::
    :maxdepth: 2

    eventlet
    gevent
