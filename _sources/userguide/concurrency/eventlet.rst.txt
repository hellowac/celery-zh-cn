.. _concurrency-eventlet:

===========================
Eventlet 并发
===========================

Concurrency with Eventlet

.. _eventlet-introduction:

简介
============

Introduction

.. tab:: 中文

    `Eventlet`_ 的主页将其描述为一个 Python 的并发网络库，它允许你“改变代码的运行方式，而非编写方式”。
    
    * 它使用 `epoll(4)`_ 或 `libevent`_ 实现
      `高度可扩展的非阻塞 I/O <highly scalable non-blocking I/O>`_ 。
    * `协程（Coroutines） <Coroutines>`_ amqp-exchanges-queues-keys 确保开发者可以使用类似线程的阻塞式编程风格，
      同时享有非阻塞 I/O 的性能优势。
    * 事件分发是隐式进行的：这意味着你可以轻松地在 Python 解释器中使用 Eventlet，
      或将其作为大型应用程序中的一小部分使用。
    
    Celery 支持将 Eventlet 作为替代的执行池实现，并且在某些场景下其表现优于 prefork。
    不过，需要确保单个任务不会长时间阻塞事件循环。
    一般来说，CPU 密集型操作不适合使用 Eventlet。
    另外需要注意，有些库（尤其是包含 C 扩展的库）无法被 monkey patch，因此无法在 Eventlet 下正常协作。
    如果不确定，请查阅相应库的文档。例如，`pylibmc` 无法与 Eventlet 协作，
    而 `psycopg2`（尽管也是 C 扩展库）在某些条件下则可以协作。
    
    `prefork` 池使用多个进程，但其数量通常受到每个 CPU 可用进程数的限制。
    而使用 Eventlet 时，你可以高效地生成数百甚至上千个 green thread。
    在一个非正式的 feed hub 系统测试中，Eventlet 池每秒可以抓取和处理数百个 feed，
    而 prefork 池则需要 14 秒来处理 100 个 feed。
    需要注意的是，这正是异步 I/O 尤其擅长的应用场景（如异步 HTTP 请求）。
    你可以混合使用 Eventlet 和 prefork worker，并根据兼容性或实际效果对任务进行路由分配。

.. tab:: 英文

    The `Eventlet`_ homepage describes it as
    a concurrent networking library for Python that allows you to
    change how you run your code, not how you write it.
    
    * It uses `epoll(4)`_ or `libevent`_ for
      `highly scalable non-blocking I/O`_.
    * `Coroutines`_ ensure that the developer uses a blocking style of
      programming that's similar to threading, but provide the benefits of
      non-blocking I/O.
    * The event dispatch is implicit: meaning you can easily use Eventlet
      from the Python interpreter, or as a small part of a larger application.
    
    
    Celery supports Eventlet as an alternative execution pool implementation and
    in some cases superior to prefork. However, you need to ensure one task doesn't
    block the event loop too long. Generally, CPU-bound operations don't go well
    with Eventlet. Also note that some libraries, usually with C extensions,
    cannot be monkeypatched and therefore cannot benefit from using Eventlet.
    Please refer to their documentation if you are not sure. For example, pylibmc
    does not allow cooperation with Eventlet but psycopg2 does when both of them
    are libraries with C extensions.
    
    
    The prefork pool can take use of multiple processes, but how many is
    often limited to a few processes per CPU. With Eventlet you can efficiently
    spawn hundreds, or thousands of green threads. In an informal test with a
    feed hub system the Eventlet pool could fetch and process hundreds of feeds
    every second, while the prefork pool spent 14 seconds processing 100
    feeds. Note that this is one of the applications async I/O is especially good
    at (asynchronous HTTP requests). You may want a mix of both Eventlet and
    prefork workers, and route tasks according to compatibility or
    what works best.

启用 Eventlet
=================

Enabling Eventlet

.. tab:: 中文

    你可以使用 :option:`celery worker -P` 选项启用 Eventlet worker 池：

    .. code-block:: console

        $ celery -A proj worker -P eventlet -c 1000

.. tab:: 英文

  You can enable the Eventlet pool by using the :option:`celery worker -P`
  worker option.

  .. code-block:: console

      $ celery -A proj worker -P eventlet -c 1000

.. _eventlet-examples:

示例
========

Examples

.. tab:: 中文

    有关使用 Eventlet 的示例，请参阅 Celery 发布包中的 `Eventlet examples`_ 目录。

.. tab:: 英文

    See the `Eventlet examples`_ directory in the Celery distribution for
    some examples taking use of Eventlet support.

.. _`Eventlet`: http://eventlet.net
.. _`epoll(4)`: http://linux.die.net/man/4/epoll
.. _`libevent`: http://monkey.org/~provos/libevent/
.. _`highly scalable non-blocking I/O`:
    https://en.wikipedia.org/wiki/Asynchronous_I/O#Select.28.2Fpoll.29_loops
.. _`Coroutines`: https://en.wikipedia.org/wiki/Coroutine
.. _`Eventlet examples`:
    https://github.com/celery/celery/tree/main/examples/eventlet

