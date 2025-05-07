.. _cookbook-tasks:

================
Task Cookbook
================



.. _cookbook-task-serial:

确保每次只执行一个任务
==============================================

Ensuring a task is only executed one at a time

.. tab:: 中文

    您可以通过使用锁来实现这一点。

    在这个例子中，我们将使用缓存框架来设置一个对所有工作者可访问的锁。

    它是一个虚构的 RSS 源导入器的一部分，名为 `djangofeeds`。
    该任务将一个源 URL 作为唯一参数，并将该源导入到
    一个名为 `Feed` 的 Django 模型中。我们通过设置一个缓存键
    （由源 URL 的 MD5 校验和组成）来确保不可能有两个或更多的工作者
    同时导入相同的源。

    缓存键会在一定时间后过期，以防发生意外情况，
    而意外总是会发生……

    因此，您的任务运行时间不应超过超时。

    .. note::

        为了使其正确工作，您需要使用一个缓存
        后端，其中 ``.add`` 操作是原子的。已知 ``memcached`` 在此目的下
        能很好地工作。

    .. code-block:: python

        import time
        from celery import task
        from celery.utils.log import get_task_logger
        from contextlib import contextmanager
        from django.core.cache import cache
        from hashlib import md5
        from djangofeeds.models import Feed

        logger = get_task_logger(__name__)

        LOCK_EXPIRE = 60 * 10  # 锁定在10分钟后过期

        @contextmanager
        def memcache_lock(lock_id, oid):
            timeout_at = time.monotonic() + LOCK_EXPIRE - 3
            # cache.add 如果键已存在则失败
            status = cache.add(lock_id, oid, LOCK_EXPIRE)
            try:
                yield status
            finally:
                # memcache 删除操作非常慢，但我们必须使用它以利用
                # 使用 add() 实现原子锁定
                if time.monotonic() < timeout_at and status:
                    # 如果超过超时则不释放锁
                    # 以减少释放已过期锁的机会
                    # 该锁可能已被其他人拥有
                    # 如果我们没有成功获取锁，也不释放锁
                    cache.delete(lock_id)

        @task(bind=True)
        def import_feed(self, feed_url):
            # 缓存键由任务名称和源 URL 的 MD5 摘要组成。
            feed_url_hexdigest = md5(feed_url).hexdigest()
            lock_id = '{0}-lock-{1}'.format(self.name, feed_url_hexdigest)
            logger.debug('正在导入源: %s', feed_url)
            with memcache_lock(lock_id, self.app.oid) as acquired:
                if acquired:
                    return Feed.objects.import_feed(feed_url).url
            logger.debug(
                '源 %s 正在被另一个工作者导入', feed_url)


.. tab:: 英文

    You can accomplish this by using a lock.

    In this example we'll be using the cache framework to set a lock that's
    accessible for all workers.

    It's part of an imaginary RSS feed importer called `djangofeeds`.
    The task takes a feed URL as a single argument, and imports that feed into
    a Django model called `Feed`. We ensure that it's not possible for two or
    more workers to import the same feed at the same time by setting a cache key
    consisting of the MD5 check-sum of the feed URL.

    The cache key expires after some time in case something unexpected happens,
    and something always will...

    For this reason your tasks run-time shouldn't exceed the timeout.


    .. note::

        In order for this to work correctly you need to be using a cache
        backend where the ``.add`` operation is atomic.  ``memcached`` is known
        to work well for this purpose.

    .. code-block:: python

        import time
        from celery import task
        from celery.utils.log import get_task_logger
        from contextlib import contextmanager
        from django.core.cache import cache
        from hashlib import md5
        from djangofeeds.models import Feed

        logger = get_task_logger(__name__)

        LOCK_EXPIRE = 60 * 10  # Lock expires in 10 minutes

        @contextmanager
        def memcache_lock(lock_id, oid):
            timeout_at = time.monotonic() + LOCK_EXPIRE - 3
            # cache.add fails if the key already exists
            status = cache.add(lock_id, oid, LOCK_EXPIRE)
            try:
                yield status
            finally:
                # memcache delete is very slow, but we have to use it to take
                # advantage of using add() for atomic locking
                if time.monotonic() < timeout_at and status:
                    # don't release the lock if we exceeded the timeout
                    # to lessen the chance of releasing an expired lock
                    # owned by someone else
                    # also don't release the lock if we didn't acquire it
                    cache.delete(lock_id)

        @task(bind=True)
        def import_feed(self, feed_url):
            # The cache key consists of the task name and the MD5 digest
            # of the feed URL.
            feed_url_hexdigest = md5(feed_url).hexdigest()
            lock_id = '{0}-lock-{1}'.format(self.name, feed_url_hexdigest)
            logger.debug('Importing feed: %s', feed_url)
            with memcache_lock(lock_id, self.app.oid) as acquired:
                if acquired:
                    return Feed.objects.import_feed(feed_url).url
            logger.debug(
                'Feed %s is already being imported by another worker', feed_url)
