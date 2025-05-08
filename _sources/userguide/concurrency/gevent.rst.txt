.. _concurrency-eventlet:

===========================
gevent 并发
===========================

Concurrency with gevent

.. _gevent-introduction:

简介
============

Introduction

.. tab:: 中文

    `gevent`_ 的主页将其描述为一个基于协程（coroutine）_ 的 Python_ 网络库，使用
    `greenlet <https://greenlet.readthedocs.io>`_ 提供基于 `libev`_ 或 `libuv`_ 事件循环的高层同步 API。
    
    其特性包括：
    
    * 基于 `libev`_ 或 `libuv`_ 的高速事件循环；
    * 基于 greenlet 的轻量级执行单元；
    * 重用 Python 标准库中的概念设计的 API（例如 `events`_ 和 `queues`_）；
    * 支持 SSL 的协作式 socket：
      `协作式 socket，含 SSL 支持 <http://www.gevent.org/api/index.html#networking>`_
    * 通过线程池、dnspython 或 c-ares 实现的
      `协作式 DNS 查询 <http://www.gevent.org/dns.html>`_；
    * 通过 monkey patching 让第三方模块支持协作式 I/O 的工具：
      `monkey patch 工具 <http://www.gevent.org/intro.html#monkey-patching>`_；
    * 支持 TCP/UDP/HTTP 服务；
    * 子进程支持（通过 `gevent.subprocess`_）；
    * 线程池支持。
    
    `gevent` 受 `eventlet <https://eventlet.readthedocs.io/en/latest/>`_ 启发而来，但提供更一致的 API、更简洁的实现以及更好的性能。
    你可以了解其他人 `为何 <http://blog.gevent.org/2010/02/27/why-gevent/>`_ `使用 gevent <http://groups.google.com/group/gevent/browse_thread/thread/4de9703e5dca8271>`_，并查看 `基于 gevent 的开源项目列表 <https://github.com/gevent/gevent/wiki/Projects>`_。

.. tab:: 英文

    The `gevent`_ homepage describes it a coroutine_ -based Python_ networking library that uses
    `greenlet <https://greenlet.readthedocs.io>`_ to provide a high-level synchronous API on top of the `libev`_
    or `libuv`_ event loop.
    
    Features include:
    
    * Fast event loop based on `libev`_ or `libuv`_.
    * Lightweight execution units based on greenlets.
    * API that reuses concepts from the Python standard library (for
      examples there are `events`_ and
      `queues`_).
    * `Cooperative sockets with SSL support <http://www.gevent.org/api/index.html#networking>`_
    * `Cooperative DNS queries <http://www.gevent.org/dns.html>`_ performed through a threadpool,
      dnspython, or c-ares.
    * `Monkey patching utility <http://www.gevent.org/intro.html#monkey-patching>`_ to get 3rd party modules to become cooperative
    * TCP/UDP/HTTP servers
    * Subprocess support (through `gevent.subprocess`_)
    * Thread pools
    
    gevent is `inspired by eventlet`_ but features a more consistent API,
    simpler implementation and better performance. Read why others `use
    gevent`_ and check out the list of the `open source projects based on
    gevent`_.


启用 gevent
=================

Enabling gevent

.. tab:: 中文

    你可以使用 :option:`celery worker -P gevent` 或
    :option:`celery worker --pool=gevent` 选项启用 gevent worker 池：

    .. code-block:: console

        $ celery -A proj worker -P gevent -c 1000

.. tab:: 英文

    You can enable the gevent pool by using the
    :option:`celery worker -P gevent` or  :option:`celery worker --pool=gevent`
    worker option.

    .. code-block:: console

        $ celery -A proj worker -P gevent -c 1000

.. _eventlet-examples:

示例
========

Examples

.. tab:: 中文

    Celery 发布包中提供了使用 gevent 的示例，请参阅 `gevent examples`_ 目录。

.. tab:: 英文

    See the `gevent examples`_ directory in the Celery distribution for
    some examples taking use of Eventlet support.

已知问题
============

Known issues

.. tab:: 中文

    在 Python 3.11 与 gevent 一起使用时存在已知问题。
    该问题已被记录在 `此处 <https://github.com/gevent/gevent/issues/1959>`_ 并在
    `gevent issue`_ 中处理。升级到 greenlet 3.0 即可解决该问题。

.. tab:: 英文

    There is a known issue using python 3.11 and gevent.
    The issue is documented `here`_ and addressed in a `gevent issue`_.
    Upgrading to greenlet 3.0 solves it.

.. _events: http://www.gevent.org/api/gevent.event.html#gevent.event.Event
.. _queues: http://www.gevent.org/api/gevent.queue.html#gevent.queue.Queue
.. _`gevent`: http://www.gevent.org/
.. _`gevent examples`:
    https://github.com/celery/celery/tree/main/examples/gevent
.. _gevent.subprocess: http://www.gevent.org/api/gevent.subprocess.html#module-gevent.subprocess

.. _coroutine: https://en.wikipedia.org/wiki/Coroutine
.. _Python: http://python.org
.. _libev: http://software.schmorp.de/pkg/libev.html
.. _libuv: http://libuv.org
.. _inspired by eventlet: http://blog.gevent.org/2010/02/27/why-gevent/
.. _use gevent: http://groups.google.com/group/gevent/browse_thread/thread/4de9703e5dca8271
.. _open source projects based on gevent: https://github.com/gevent/gevent/wiki/Projects
.. _what's new: http://www.gevent.org/whatsnew_1_5.html
.. _changelog: http://www.gevent.org/changelog.html
.. _here: https://github.com/celery/celery/issues/8425
.. _gevent issue: https://github.com/gevent/gevent/issues/1985
