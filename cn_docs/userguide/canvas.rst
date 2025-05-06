.. _guide-canvas:

==============================
Canvas：设计工作流
==============================

Canvas: Designing Work-flows

.. _canvas-subtasks:

.. _canvas-signatures:

签名
==========

Signatures

.. tab:: 中文

    .. versionadded:: 2.0
    
    你已经在 :ref:`calling <guide-calling>` 指南中学习了如何使用任务的 ``delay`` 方法来调用任务，这通常已足够，但有时你可能希望将任务调用的签名传递给另一个进程，或者作为参数传递给另一个函数。
    
    :func:`~celery.signature` 会将一次任务调用的参数、关键字参数及执行选项封装起来，以便它可以被传递给其他函数，甚至被序列化并通过网络发送。
    
    - 你可以使用任务名称为 ``add`` 任务创建一个签名，如下所示：
    
      .. code-block:: pycon
    
          >>> from celery import signature
          >>> signature('tasks.add', args=(2, 2), countdown=10)
          tasks.add(2, 2)
    
      此任务的签名为 arity 为 2（两个参数）：``(2, 2)``，
      并设置执行选项 `countdown` 为 10。
    
    - 或者你可以使用任务的 ``signature`` 方法来创建签名：
    
      .. code-block:: pycon
    
          >>> add.signature((2, 2), countdown=10)
          tasks.add(2, 2)
    
    - 也可以使用星号参数的快捷方式：
    
      .. code-block:: pycon
    
          >>> add.s(2, 2)
          tasks.add(2, 2)
    
    - 同样也支持关键字参数：
    
      .. code-block:: pycon
    
          >>> add.s(2, 2, debug=True)
          tasks.add(2, 2, debug=True)
    
    - 你可以从任意签名实例中检查不同的字段：
    
      .. code-block:: pycon
    
          >>> s = add.signature((2, 2), {'debug': True}, countdown=10)
          >>> s.args
          (2, 2)
          >>> s.kwargs
          {'debug': True}
          >>> s.options
          {'countdown': 10}
    
    - 它支持 ``delay``、``apply_async`` 等“调用 API”，包括可直接调用（即 ``__call__``）。
    
      调用该签名将在当前进程中直接执行任务：
    
      .. code-block:: pycon
    
          >>> add(2, 2)
          4
          >>> add.s(2, 2)()
          4
    
      ``delay`` 是我们喜爱的快捷方式，相当于使用星号参数调用 ``apply_async``：
    
      .. code-block:: pycon
    
          >>> result = add.delay(2, 2)
          >>> result.get()
          4
    
      ``apply_async`` 接受的参数与 :meth:`Task.apply_async <@Task.apply_async>` 方法相同：
    
      .. code-block:: pycon
    
          >>> add.apply_async(args, kwargs, **options)
          >>> add.signature(args, kwargs, **options).apply_async()
    
          >>> add.apply_async((2, 2), countdown=1)
          >>> add.signature((2, 2), countdown=1).apply_async()
    
    - 你不能通过 :meth:`~@Task.s` 方法定义选项，但可以通过链式调用 ``set`` 方法来设置：
    
      .. code-block:: pycon
    
          >>> add.s(2, 2).set(countdown=1)
          proj.tasks.add(2, 2)

.. tab:: 英文
    
    .. versionadded:: 2.0
    
    You just learned how to call a task using the tasks ``delay`` method
    in the :ref:`calling <guide-calling>` guide, and this is often all you need,
    but sometimes you may want to pass the signature of a task invocation to
    another process or as an argument to another function.
    
    A :func:`~celery.signature` wraps the arguments, keyword arguments, and execution options
    of a single task invocation in a way such that it can be passed to functions
    or even serialized and sent across the wire.
    
    - You can create a signature for the ``add`` task using its name like this:
    
      .. code-block:: pycon
    
          >>> from celery import signature
          >>> signature('tasks.add', args=(2, 2), countdown=10)
          tasks.add(2, 2)
    
      This task has a signature of arity 2 (two arguments): ``(2, 2)``,
      and sets the countdown execution option to 10.
    
    - or you can create one using the task's ``signature`` method:
    
      .. code-block:: pycon
      
          >>> add.signature((2, 2), countdown=10)
          tasks.add(2, 2)
    
    - There's also a shortcut using star arguments:
    
      .. code-block:: pycon
      
          >>> add.s(2, 2)
          tasks.add(2, 2)
    
    - Keyword arguments are also supported:
    
      .. code-block:: pycon
      
          >>> add.s(2, 2, debug=True)
          tasks.add(2, 2, debug=True)
    
    - From any signature instance you can inspect the different fields:
    
      .. code-block:: pycon
      
          >>> s = add.signature((2, 2), {'debug': True}, countdown=10)
          >>> s.args
          (2, 2)
          >>> s.kwargs
          {'debug': True}
          >>> s.options
          {'countdown': 10}
    
    - It supports the "Calling API" of ``delay``,
      ``apply_async``, etc., including being called directly (``__call__``).
    
      Calling the signature will execute the task inline in the current process:
      
      .. code-block:: pycon
      
          >>> add(2, 2)
          4
          >>> add.s(2, 2)()
          4
      
      ``delay`` is our beloved shortcut to ``apply_async`` taking star-arguments:
      
      .. code-block:: pycon
      
          >>> result = add.delay(2, 2)
          >>> result.get()
          4
      
      ``apply_async`` takes the same arguments as the
      :meth:`Task.apply_async <@Task.apply_async>` method:
      
      .. code-block:: pycon
      
          >>> add.apply_async(args, kwargs, **options)
          >>> add.signature(args, kwargs, **options).apply_async()
      
          >>> add.apply_async((2, 2), countdown=1)
          >>> add.signature((2, 2), countdown=1).apply_async()
    
    - You can't define options with :meth:`~@Task.s`, but a chaining
      ``set`` call takes care of that:
    
      .. code-block:: pycon
    
          >>> add.s(2, 2).set(countdown=1)
          proj.tasks.add(2, 2)

部分代码
--------

Partials

.. tab:: 中文

    使用签名，你可以在 worker 中执行任务：
    
    .. code-block:: pycon
    
        >>> add.s(2, 2).delay()
        >>> add.s(2, 2).apply_async(countdown=1)
    
    或者也可以在当前进程中直接调用：
    
    .. code-block:: pycon
    
        >>> add.s(2, 2)()
        4
    
    向 ``apply_async``/``delay`` 提供额外的 args、kwargs 或 options，会创建部分签名（partial）：
    
    - 所添加的位置参数会被追加到签名中的已有参数前面：
    
      .. code-block:: pycon
    
          >>> partial = add.s(2)          # 不完整的签名
          >>> partial.delay(4)            # 4 + 2
          >>> partial.apply_async((4,))  # 同上
    
    - 所添加的关键字参数会与签名中的关键字参数合并，
      新添加的关键字参数将覆盖已有参数：
    
      .. code-block:: pycon
    
          >>> s = add.s(2, 2)
          >>> s.delay(debug=True)                    # -> add(2, 2, debug=True)
          >>> s.apply_async(kwargs={'debug': True})  # 同上
    
    - 所添加的选项会与签名中的选项合并，
      新添加的选项将覆盖已有选项：
    
      .. code-block:: pycon
    
          >>> s = add.signature((2, 2), countdown=10)
          >>> s.apply_async(countdown=1)  # countdown 现在为 1
    
    你还可以克隆签名以创建派生签名：
    
    .. code-block:: pycon
    
        >>> s = add.s(2)
        proj.tasks.add(2)
    
        >>> s.clone(args=(4,), kwargs={'debug': True})
        proj.tasks.add(4, 2, debug=True)


.. tab:: 英文

    With a signature, you can execute the task in a worker:
    
    .. code-block:: pycon
    
        >>> add.s(2, 2).delay()
        >>> add.s(2, 2).apply_async(countdown=1)
    
    Or you can call it directly in the current process:
    
    .. code-block:: pycon
    
        >>> add.s(2, 2)()
        4
    
    Specifying additional args, kwargs, or options to ``apply_async``/``delay``
    creates partials:
    
    - Any arguments added will be prepended to the args in the signature:
    
      .. code-block:: pycon
      
          >>> partial = add.s(2)          # incomplete signature
          >>> partial.delay(4)            # 4 + 2
          >>> partial.apply_async((4,))  # same
    
    - Any keyword arguments added will be merged with the kwargs in the signature,
      with the new keyword arguments taking precedence:
    
      .. code-block:: pycon
      
          >>> s = add.s(2, 2)
          >>> s.delay(debug=True)                    # -> add(2, 2, debug=True)
          >>> s.apply_async(kwargs={'debug': True})  # same
    
    - Any options added will be merged with the options in the signature,
      with the new options taking precedence:
    
      .. code-block:: pycon
      
          >>> s = add.signature((2, 2), countdown=10)
          >>> s.apply_async(countdown=1)  # countdown is now 1
    
    You can also clone signatures to create derivatives:
    
    .. code-block:: pycon
    
        >>> s = add.s(2)
        proj.tasks.add(2)
    
        >>> s.clone(args=(4,), kwargs={'debug': True})
        proj.tasks.add(4, 2, debug=True)
    
不变性
------------

Immutability

.. tab:: 中文

    .. versionadded:: 3.0

    部分签名（Partials）主要用于回调函数。任何通过 ``link`` 关联的任务或 chord 的回调函数，都会接收到父任务的返回结果。
    但有时你可能希望指定一个**不接受附加参数**的回调函数，此时可以将签名设置为不可变（immutable）：

    .. code-block:: pycon

        >>> add.apply_async((2, 2), link=reset_buffers.signature(immutable=True))

    你也可以使用 ``.si()`` 这个快捷方式来创建不可变签名：

    .. code-block:: pycon

        >>> add.apply_async((2, 2), link=reset_buffers.si())

    当一个签名是不可变的时，只能设置其执行选项，
    因此无法通过传递额外的参数或关键字参数来调用该签名。

    .. note::

        在本教程中，我有时会对签名使用前缀操作符 `~`。
        在生产环境中你可能不应使用这个操作符，但在 Python 交互式 shell 中做实验时它非常方便：

        .. code-block:: pycon

            >>> ~sig

            >>> # 等价于
            >>> sig.delay().get()

.. tab:: 英文

    .. versionadded:: 3.0

    Partials are meant to be used with callbacks, any tasks linked, or chord
    callbacks will be applied with the result of the parent task.
    Sometimes you want to specify a callback that doesn't take
    additional arguments, and in that case you can set the signature
    to be immutable:

    .. code-block:: pycon

        >>> add.apply_async((2, 2), link=reset_buffers.signature(immutable=True))

    The ``.si()`` shortcut can also be used to create immutable signatures:

    .. code-block:: pycon

        >>> add.apply_async((2, 2), link=reset_buffers.si())

    Only the execution options can be set when a signature is immutable,
    so it's not possible to call the signature with partial args/kwargs.

    .. note::

        In this tutorial I sometimes use the prefix operator `~` to signatures.
        You probably shouldn't use it in your production code, but it's a handy shortcut
        when experimenting in the Python shell:

        .. code-block:: pycon

            >>> ~sig

            >>> # is the same as
            >>> sig.delay().get()


.. _canvas-callbacks:

回调函数
---------

Callbacks

.. tab:: 中文

    .. versionadded:: 3.0

    你可以使用 ``apply_async`` 的 ``link`` 参数，为任何任务添加回调函数：

    .. code-block:: pycon

        add.apply_async((2, 2), link=other_task.s())

    该回调任务仅在前一个任务成功完成时才会被执行，
    且其参数将是前一个任务的返回值。

    如前所述，**任何添加到签名上的参数都会被追加在签名原本定义的参数之前！**

    如果你有以下签名：

    .. code-block:: pycon

        >>> sig = add.s(10)

    那么 `sig.delay(result)` 实际相当于：

    .. code-block:: pycon

        >>> add.apply_async(args=(result, 10))

    ...

    现在让我们通过部分参数，给 ``add`` 任务设置一个回调函数：

    .. code-block:: pycon

        >>> add.apply_async((2, 2), link=add.s(8))

    如预期，这首先会启动一个任务来计算 :math:`2 + 2`，然后启动另一个任务来计算 :math:`8 + 4`。


.. tab:: 英文

    .. versionadded:: 3.0

    Callbacks can be added to any task using the ``link`` argument
    to ``apply_async``:

    .. code-block:: pycon

        add.apply_async((2, 2), link=other_task.s())

    The callback will only be applied if the task exited successfully,
    and it will be applied with the return value of the parent task as argument.

    As I mentioned earlier, any arguments you add to a signature,
    will be prepended to the arguments specified by the signature itself!

    If you have the signature:

    .. code-block:: pycon

        >>> sig = add.s(10)

    then `sig.delay(result)` becomes:

    .. code-block:: pycon

        >>> add.apply_async(args=(result, 10))

    ...

    Now let's call our ``add`` task with a callback using partial
    arguments:

    .. code-block:: pycon

        >>> add.apply_async((2, 2), link=add.s(8))

    As expected this will first launch one task calculating :math:`2 + 2`, then
    another task calculating :math:`8 + 4`.

原语
==============

The Primitives

.. tab:: 中文

    .. versionadded:: 3.0
    
    .. topic:: 概览
    
        - ``group``
    
          group 原语是一个签名，接收一个任务列表，并并行执行这些任务。
    
        - ``chain``
    
          chain 原语可以将多个签名连接在一起，按顺序依次执行，
          本质上形成一个回调链（*chain*）。
    
        - ``chord``
    
          chord 就像是带有回调的 group。chord 包含一个 header 组和一个 body，
          当 header 中的所有任务都完成后，body 中的任务将被执行。
    
        - ``map``
    
          map 原语的行为类似内置的 ``map`` 函数，但会创建一个临时任务，
          将参数列表逐个应用于任务中。
          例如 ``task.map([1, 2])`` 实际相当于执行：
    
          .. code-block:: python
    
              res = [task(1), task(2)]
    
        - ``starmap``
    
          starmap 的行为与 map 类似，但参数会以 ``*args`` 的形式展开。
          例如 ``add.starmap([(2, 2), (4, 4)])`` 实际会执行：
    
          .. code-block:: python
    
              res = [add(2, 2), add(4, 4)]
    
        - ``chunks``
    
          chunking（分块）会将一个长参数列表拆分成多个部分，例如：
    
          .. code-block:: pycon
    
              >>> items = zip(range(1000), range(1000))  # 共有 1000 个条目
              >>> add.chunks(items, 10)
    
          会将参数列表按 10 个为一组进行拆分，最终生成 100 个任务（每个任务依次处理 10 个条目）。
    
    这些原语本身也是签名对象，因此可以通过任意方式组合使用，来构建复杂的工作流。
    
    以下是一些示例：
    
    - 简单的 chain
    
      这是一个简单的 chain，第一个任务执行后会将其返回值作为参数传递给下一个任务，以此类推。
    
      .. code-block:: pycon
    
          >>> from celery import chain
    
          >>> # 2 + 2 + 4 + 8
          >>> res = chain(add.s(2, 2), add.s(4), add.s(8))()
          >>> res.get()
          16
    
      也可以使用管道语法来写：
    
      .. code-block:: pycon
    
          >>> (add.s(2, 2) | add.s(4) | add.s(8))().get()
          16
    
    - 不可变签名（Immutable signatures）
    
      签名可以是部分签名，因此可以向其中添加额外参数，但有时你可能并不希望这样，
      比如你不希望链中前一个任务的结果作为下一个任务的参数。
    
      此时可以将签名标记为不可变（immutable），使其参数不可更改：
    
      .. code-block:: pycon
    
          >>> add.signature((2, 2), immutable=True)
    
      你也可以使用 ``.si()`` 快捷方式，这是推荐的创建不可变签名的方式：
    
      .. code-block:: pycon
    
          >>> add.si(2, 2)
    
      现在你可以创建一个互不依赖的任务链：
    
      .. code-block:: pycon
    
          >>> res = (add.si(2, 2) | add.si(4, 4) | add.si(8, 8))()
          >>> res.get()
          16
    
          >>> res.parent.get()
          8
    
          >>> res.parent.parent.get()
          4
    
    - 简单的 group
    
      你可以很容易地创建一个任务组以并行执行：
    
      .. code-block:: pycon
    
          >>> from celery import group
          >>> res = group(add.s(i, i) for i in range(10))()
          >>> res.get(timeout=1)
          [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
    
    - 简单的 chord
    
      chord 原语允许我们在 group 的所有任务完成后执行一个回调函数。
      对于一些无法完全并行化的算法，这种机制非常有用：
    
      .. code-block:: pycon
    
          >>> from celery import chord
          >>> res = chord((add.s(i, i) for i in range(10)), tsum.s())()
          >>> res.get()
          90
    
      上面的示例会启动 10 个并行任务，当所有任务完成后，
      它们的返回值会被组合成一个列表传递给 ``tsum`` 任务。
    
      chord 的 body 也可以设置为不可变，这样 group 的返回值就不会传递给回调函数：
    
      .. code-block:: pycon
    
          >>> chord((import_contact.s(c) for c in contacts),
          ...       notify_complete.si(import_id)).apply_async()
    
      注意上面使用了 ``.si``，这会创建一个不可变签名，意味着无论是新的参数还是前一个任务的返回值都会被忽略。
    
    - 混合组合，解锁脑洞
    
      chain 本身也可以是部分签名：
    
      .. code-block:: pycon
    
          >>> c1 = (add.s(4) | mul.s(8))
    
          # (16 + 4) * 8
          >>> res = c1(16)
          >>> res.get()
          160
    
      这意味着 chain 也可以组合在一起：
    
      .. code-block:: pycon
    
          # ((4 + 16) * 2 + 4) * 8
          >>> c2 = (add.s(4, 16) | mul.s(2) | (add.s(4) | mul.s(8)))
    
          >>> res = c2()
          >>> res.get()
          352
    
      将 group 与另一个任务组合时，会自动转换为 chord：
    
      .. code-block:: pycon
    
          >>> c3 = (group(add.s(i, i) for i in range(10)) | tsum.s())
          >>> res = c3()
          >>> res.get()
          90
    
      group 和 chord 也支持部分参数，在链中，前一个任务的返回值会被转发给 group 中的所有任务：
    
      .. code-block:: pycon
    
          >>> new_user_workflow = (create_user.s() | group(
          ...                      import_contacts.s(),
          ...                      send_welcome_email.s()))
          ... new_user_workflow.delay(username='artv',
          ...                         first='Art',
          ...                         last='Vandelay',
          ...                         email='art@vandelay.com')
    
      如果你不希望将参数转发到 group 中的任务，可以将 group 中的签名设为不可变：
    
      .. code-block:: pycon
    
          >>> res = (add.s(4, 4) | group(add.si(i, i) for i in range(10)))()
          >>> res.get()
          [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
    
          >>> res.parent.get()
          8


.. tab:: 英文

    .. versionadded:: 3.0
    
    .. topic:: Overview
    
        - ``group``
    
          The group primitive is a signature that takes a list of tasks that should
          be applied in parallel.
    
        - ``chain``
    
          The chain primitive lets us link together signatures so that one is called
          after the other, essentially forming a *chain* of callbacks.
    
        - ``chord``
    
          A chord is just like a group but with a callback. A chord consists
          of a header group and a body,  where the body is a task that should execute
          after all of the tasks in the header are complete.
    
        - ``map``
    
          The map primitive works like the built-in ``map`` function, but creates
          a temporary task where a list of arguments is applied to the task.
          For example, ``task.map([1, 2])`` -- results in a single task
          being called, applying the arguments in order to the task function so
          that the result is:
    
          .. code-block:: python
    
              res = [task(1), task(2)]
    
        - ``starmap``
    
          Works exactly like map except the arguments are applied as ``*args``.
          For example ``add.starmap([(2, 2), (4, 4)])`` results in a single
          task calling:
    
          .. code-block:: python
    
              res = [add(2, 2), add(4, 4)]
    
        - ``chunks``
    
          Chunking splits a long list of arguments into parts, for example
          the operation:
    
          .. code-block:: pycon
    
              >>> items = zip(range(1000), range(1000))  # 1000 items
              >>> add.chunks(items, 10)
    
          will split the list of items into chunks of 10, resulting in 100
          tasks (each processing 10 items in sequence).
    
    
    The primitives are also signature objects themselves, so that they can be combined
    in any number of ways to compose complex work-flows.
    
    Here're some examples:
    
    - Simple chain
    
      Here's a simple chain, the first task executes passing its return value
      to the next task in the chain, and so on.
      
      .. code-block:: pycon
      
          >>> from celery import chain
      
          >>> # 2 + 2 + 4 + 8
          >>> res = chain(add.s(2, 2), add.s(4), add.s(8))()
          >>> res.get()
          16
      
      This can also be written using pipes:
      
      .. code-block:: pycon
      
          >>> (add.s(2, 2) | add.s(4) | add.s(8))().get()
          16
    
    - Immutable signatures
    
      Signatures can be partial so arguments can be
      added to the existing arguments, but you may not always want that,
      for example if you don't want the result of the previous task in a chain.
      
      In that case you can mark the signature as immutable, so that the arguments
      cannot be changed:
      
      .. code-block:: pycon
      
          >>> add.signature((2, 2), immutable=True)
      
      There's also a ``.si()`` shortcut for this, and this is the preferred way of
      creating signatures:
      
      .. code-block:: pycon
      
          >>> add.si(2, 2)
      
      Now you can create a chain of independent tasks instead:
      
      .. code-block:: pycon
      
          >>> res = (add.si(2, 2) | add.si(4, 4) | add.si(8, 8))()
          >>> res.get()
          16
      
          >>> res.parent.get()
          8
      
          >>> res.parent.parent.get()
          4
    
    - Simple group
    
      You can easily create a group of tasks to execute in parallel:
      
      .. code-block:: pycon
      
          >>> from celery import group
          >>> res = group(add.s(i, i) for i in range(10))()
          >>> res.get(timeout=1)
          [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
    
    - Simple chord
    
      The chord primitive enables us to add a callback to be called when
      all of the tasks in a group have finished executing.  This is often
      required for algorithms that aren't *embarrassingly parallel*:
      
      .. code-block:: pycon
      
          >>> from celery import chord
          >>> res = chord((add.s(i, i) for i in range(10)), tsum.s())()
          >>> res.get()
          90
      
      The above example creates 10 tasks that all start in parallel,
      and when all of them are complete the return values are combined
      into a list and sent to the ``tsum`` task.
      
      The body of a chord can also be immutable, so that the return value
      of the group isn't passed on to the callback:
      
      .. code-block:: pycon
      
          >>> chord((import_contact.s(c) for c in contacts),
          ...       notify_complete.si(import_id)).apply_async()
      
      Note the use of ``.si`` above; this creates an immutable signature,
      meaning any new arguments passed (including to return value of the
      previous task) will be ignored.
    
    - Blow your mind by combining
    
      Chains can be partial too:
      
      .. code-block:: pycon
      
          >>> c1 = (add.s(4) | mul.s(8))
      
          # (16 + 4) * 8
          >>> res = c1(16)
          >>> res.get()
          160
      
      this means that you can combine chains:
      
      .. code-block:: pycon
      
          # ((4 + 16) * 2 + 4) * 8
          >>> c2 = (add.s(4, 16) | mul.s(2) | (add.s(4) | mul.s(8)))
      
          >>> res = c2()
          >>> res.get()
          352
      
      Chaining a group together with another task will automatically
      upgrade it to be a chord:
      
      .. code-block:: pycon
      
          >>> c3 = (group(add.s(i, i) for i in range(10)) | tsum.s())
          >>> res = c3()
          >>> res.get()
          90
      
      Groups and chords accepts partial arguments too, so in a chain
      the return value of the previous task is forwarded to all tasks in the group:
      
      .. code-block:: pycon
      
      
          >>> new_user_workflow = (create_user.s() | group(
          ...                      import_contacts.s(),
          ...                      send_welcome_email.s()))
          ... new_user_workflow.delay(username='artv',
          ...                         first='Art',
          ...                         last='Vandelay',
          ...                         email='art@vandelay.com')
      
      
      If you don't want to forward arguments to the group then
      you can make the signatures in the group immutable:
      
      .. code-block:: pycon
      
          >>> res = (add.s(4, 4) | group(add.si(i, i) for i in range(10)))()
          >>> res.get()
          [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
      
          >>> res.parent.get()
          8
    

.. _canvas-chain:

链
------

Chains

.. tab:: 中文

    .. versionadded:: 3.0
    
    任务可以彼此链接：当一个任务成功返回时，会调用所链接的任务：
    
    .. code-block:: pycon
    
        >>> res = add.apply_async((2, 2), link=mul.s(16))
        >>> res.get()
        4
    
    所链接的任务将以其父任务的结果作为第一个参数来调用。在上述示例中，结果为 4，因此会执行 ``mul(4, 16)``。
    
    结果对象会追踪原始任务所调用的所有子任务，可以通过结果实例访问这些子任务：
    
    .. code-block:: pycon
    
        >>> res.children
        [<AsyncResult: 8c350acf-519d-4553-8a53-4ad3a5c5aeb4>]
    
        >>> res.children[0].get()
        64
    
    结果实例还提供了 :meth:`~@AsyncResult.collect` 方法，它会将结果视为一张图，使你可以迭代地访问所有结果：
    
    .. code-block:: pycon
    
        >>> list(res.collect())
        [(<AsyncResult: 7b720856-dc5f-4415-9134-5c89def5664e>, 4),
         (<AsyncResult: 8c350acf-519d-4553-8a53-4ad3a5c5aeb4>, 64)]
    
    默认情况下，如果图未完全构建（即有任务尚未完成），:meth:`~@AsyncResult.collect` 会抛出 :exc:`~@IncompleteStream` 异常，
    但你也可以选择获取图的中间状态：
    
    .. code-block:: pycon
    
        >>> for result, value in res.collect(intermediate=True):
        ....
    
    你可以将任意数量的任务链接起来，签名（signature）也同样支持链接：
    
    .. code-block:: pycon
    
        >>> s = add.s(2, 2)
        >>> s.link(mul.s(4))
        >>> s.link(log_result.s())
    
    你也可以通过 `on_error` 方法添加 *错误回调*：
    
    .. code-block:: pycon
    
        >>> add.s(2, 2).on_error(log_error.s()).delay()
    
    当应用该签名时，实际执行的 ``.apply_async`` 调用如下所示：
    
    .. code-block:: pycon
    
        >>> add.apply_async((2, 2), link_error=log_error.s())
    
    Worker 并不会以任务形式调用 errback，而是直接调用 errback 函数，
    这样可以将原始请求对象、异常对象和 traceback 对象传递给它。
    
    以下是一个 errback 的示例：
    
    .. code-block:: python
    
        import os
    
        from proj.celery import app
    
        @app.task
        def log_error(request, exc, traceback):
            with open(os.path.join('/var/errors', request.id), 'a') as fh:
                print('--\n\n{0} {1} {2}'.format(
                    request.id, exc, traceback), file=fh)
    
    为了简化任务的链接操作，Celery 提供了一个特殊的签名类 :class:`~celery.chain`，可以用来将多个任务链式连接：
    
    .. code-block:: pycon
    
        >>> from celery import chain
        >>> from proj.tasks import add, mul
    
        >>> # (4 + 4) * 8 * 10
        >>> res = chain(add.s(4, 4), mul.s(8), mul.s(10))
        proj.tasks.add(4, 4) | proj.tasks.mul(8) | proj.tasks.mul(10)
    
    调用该 chain 会在当前进程中依次调用每个任务，并返回链中最后一个任务的结果：
    
    .. code-block:: pycon
    
        >>> res = chain(add.s(4, 4), mul.s(8), mul.s(10))()
        >>> res.get()
        640
    
    它还会设置 ``parent`` 属性，这样你就可以向上遍历任务链以获取中间结果：
    
    .. code-block:: pycon
    
        >>> res.parent.get()
        64
    
        >>> res.parent.parent.get()
        8
    
        >>> res.parent.parent
        <AsyncResult: eeaad925-6778-4ad1-88c8-b2a63d017933>
    
    你也可以使用 ``|`` （管道）操作符来创建任务链：
    
    .. code-block:: pycon
    
        >>> (add.s(2, 2) | mul.s(8) | mul.s(10)).apply_async()


.. tab:: 英文
    
    .. versionadded:: 3.0
    
    Tasks can be linked together: the linked task is called when the task
    returns successfully:
    
    .. code-block:: pycon
    
        >>> res = add.apply_async((2, 2), link=mul.s(16))
        >>> res.get()
        4
    
    The linked task will be applied with the result of its parent
    task as the first argument. In the above case where the result was 4,
    this will result in ``mul(4, 16)``.
    
    The results will keep track of any subtasks called by the original task,
    and this can be accessed from the result instance:
    
    .. code-block:: pycon
    
        >>> res.children
        [<AsyncResult: 8c350acf-519d-4553-8a53-4ad3a5c5aeb4>]
    
        >>> res.children[0].get()
        64
    
    The result instance also has a :meth:`~@AsyncResult.collect` method
    that treats the result as a graph, enabling you to iterate over
    the results:
    
    .. code-block:: pycon
    
        >>> list(res.collect())
        [(<AsyncResult: 7b720856-dc5f-4415-9134-5c89def5664e>, 4),
         (<AsyncResult: 8c350acf-519d-4553-8a53-4ad3a5c5aeb4>, 64)]
    
    By default :meth:`~@AsyncResult.collect` will raise an
    :exc:`~@IncompleteStream` exception if the graph isn't fully
    formed (one of the tasks hasn't completed yet),
    but you can get an intermediate representation of the graph
    too:
    
    .. code-block:: pycon
    
        >>> for result, value in res.collect(intermediate=True):
        ....
    
    You can link together as many tasks as you like,
    and signatures can be linked too:
    
    .. code-block:: pycon
    
        >>> s = add.s(2, 2)
        >>> s.link(mul.s(4))
        >>> s.link(log_result.s())
    
    You can also add *error callbacks* using the `on_error` method:
    
    .. code-block:: pycon
    
        >>> add.s(2, 2).on_error(log_error.s()).delay()
    
    This will result in the following ``.apply_async`` call when the signature
    is applied:
    
    .. code-block:: pycon
    
        >>> add.apply_async((2, 2), link_error=log_error.s())
    
    The worker won't actually call the errback as a task, but will
    instead call the errback function directly so that the raw request, exception
    and traceback objects can be passed to it.
    
    Here's an example errback:
    
    .. code-block:: python
    
    
        import os
    
        from proj.celery import app
    
        @app.task
        def log_error(request, exc, traceback):
            with open(os.path.join('/var/errors', request.id), 'a') as fh:
                print('--\n\n{0} {1} {2}'.format(
                    request.id, exc, traceback), file=fh)
    
    To make it even easier to link tasks together there's
    a special signature called :class:`~celery.chain` that lets
    you chain tasks together:
    
    .. code-block:: pycon
    
        >>> from celery import chain
        >>> from proj.tasks import add, mul
    
        >>> # (4 + 4) * 8 * 10
        >>> res = chain(add.s(4, 4), mul.s(8), mul.s(10))
        proj.tasks.add(4, 4) | proj.tasks.mul(8) | proj.tasks.mul(10)
    
    
    Calling the chain will call the tasks in the current process
    and return the result of the last task in the chain:
    
    .. code-block:: pycon
    
        >>> res = chain(add.s(4, 4), mul.s(8), mul.s(10))()
        >>> res.get()
        640
    
    It also sets ``parent`` attributes so that you can
    work your way up the chain to get intermediate results:
    
    .. code-block:: pycon
    
        >>> res.parent.get()
        64
    
        >>> res.parent.parent.get()
        8
    
        >>> res.parent.parent
        <AsyncResult: eeaad925-6778-4ad1-88c8-b2a63d017933>
    
    
    Chains can also be made using the ``|`` (pipe) operator:
    
    .. code-block:: pycon
    
        >>> (add.s(2, 2) | mul.s(8) | mul.s(10)).apply_async()

任务 ID
~~~~~~~

Task ID

.. tab:: 中文

    .. versionadded:: 5.4

    链将继承链中最后一个任务的任务 ID。

.. tab:: 英文

    .. versionadded:: 5.4

    A chain will inherit the task id of the last task in the chain.

图表
~~~~~~

Graphs

.. tab:: 中文

    此外，你还可以将结果图作为 :class:`~celery.utils.graph.DependencyGraph` 来操作：

    .. code-block:: pycon

        >>> res = chain(add.s(4, 4), mul.s(8), mul.s(10))()

        >>> res.parent.parent.graph
        285fa253-fcf8-42ef-8b95-0078897e83e6(1)
            463afec2-5ed4-4036-b22d-ba067ec64f52(0)
        872c3995-6fa0-46ca-98c2-5a19155afcf0(2)
            285fa253-fcf8-42ef-8b95-0078897e83e6(1)
                463afec2-5ed4-4036-b22d-ba067ec64f52(0)

    你甚至可以将这些图转换为 *dot* 格式：

    .. code-block:: pycon

        >>> with open('graph.dot', 'w') as fh:
        ...     res.parent.parent.graph.to_dot(fh)

    并生成图像：

    .. code-block:: console

        $ dot -Tpng graph.dot -o graph.png

    .. image:: ../images/result_graph.png

.. tab:: 英文

    In addition you can work with the result graph as a
    :class:`~celery.utils.graph.DependencyGraph`:

    .. code-block:: pycon

        >>> res = chain(add.s(4, 4), mul.s(8), mul.s(10))()

        >>> res.parent.parent.graph
        285fa253-fcf8-42ef-8b95-0078897e83e6(1)
            463afec2-5ed4-4036-b22d-ba067ec64f52(0)
        872c3995-6fa0-46ca-98c2-5a19155afcf0(2)
            285fa253-fcf8-42ef-8b95-0078897e83e6(1)
                463afec2-5ed4-4036-b22d-ba067ec64f52(0)

    You can even convert these graphs to *dot* format:

    .. code-block:: pycon

        >>> with open('graph.dot', 'w') as fh:
        ...     res.parent.parent.graph.to_dot(fh)


    and create images:

    .. code-block:: console

        $ dot -Tpng graph.dot -o graph.png

    .. image:: ../images/result_graph.png

.. _canvas-group:

组
------

Groups

.. tab:: 中文

    .. versionadded:: 3.0

    .. note::

        与 chords 类似，group 中使用的任务也 *不能* 忽略它们的结果。
        参阅 ":ref:`chord-important-notes`" 以获取更多信息。

    Group 可用于并行执行多个任务。

    :class:`~celery.group` 函数接收一个签名列表作为参数：

    .. code-block:: pycon

        >>> from celery import group
        >>> from proj.tasks import add

        >>> group(add.s(2, 2), add.s(4, 4))
        (proj.tasks.add(2, 2), proj.tasks.add(4, 4))

    如果你 **调用** 该 group，任务将会在当前进程中一个接一个地执行，并返回一个 :class:`~celery.result.GroupResult`
    实例，用于跟踪结果状态，或查看有多少任务已经完成等等：

    .. code-block:: pycon

        >>> g = group(add.s(2, 2), add.s(4, 4))
        >>> res = g()
        >>> res.get()
        [4, 8]

    Group 也支持迭代器作为输入：

    .. code-block:: pycon

        >>> group(add.s(i, i) for i in range(100))()

    Group 是一个签名对象，因此可以与其他签名组合使用。

.. tab:: 英文

    .. versionadded:: 3.0

    .. note::

        Similarly to chords, tasks used in a group must *not* ignore their results.
        See ":ref:`chord-important-notes`" for more information.


    A group can be used to execute several tasks in parallel.

    The :class:`~celery.group` function takes a list of signatures:

    .. code-block:: pycon

        >>> from celery import group
        >>> from proj.tasks import add

        >>> group(add.s(2, 2), add.s(4, 4))
        (proj.tasks.add(2, 2), proj.tasks.add(4, 4))

    If you **call** the group, the tasks will be applied
    one after another in the current process, and a :class:`~celery.result.GroupResult`
    instance is returned that can be used to keep track of the results,
    or tell how many tasks are ready and so on:

    .. code-block:: pycon

        >>> g = group(add.s(2, 2), add.s(4, 4))
        >>> res = g()
        >>> res.get()
        [4, 8]

    Group also supports iterators:

    .. code-block:: pycon

        >>> group(add.s(i, i) for i in range(100))()

    A group is a signature object, so it can be used in combination
    with other signatures.

.. _group-callbacks:

组回调函数和错误处理
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Group Callbacks and Error Handling

.. tab:: 中文

    Group 也可以绑定回调（callback）和错误回调（errback）签名，但其行为可能略显意外，
    因为 group 并不是真正的任务对象，而只是将链接的任务传递给其封装的各个签名。
    这意味着 group 的返回值不会被收集起来传递给链接的回调签名。
    此外，链接的任务也 *不保证* 只有在所有 group 任务都完成后才会被激活。

    例如，以下使用简单 `add(a, b)` 任务的片段是错误的，因为所链接的 `add.s()` 签名并不会收到最终的 group 结果作为参数：

    .. code-block:: pycon

        >>> g = group(add.s(2, 2), add.s(4, 4))
        >>> g.link(add.s())
        >>> res = g()
        [4, 8]

    注意，前两个任务的最终结果被返回了，但回调签名在后台运行时会抛出异常，
    因为它没有收到预期的两个参数。

    Group 的 errback 也会被传递给封装的各个签名，
    这意味着如果 group 中有多个任务失败，那么仅链接一次的 errback 可能会被调用多次。
    例如，以下片段中使用了一个会抛出异常的 `fail()` 任务，可以预期 `log_error()` 签名会针对 group 中每一个失败的任务被调用一次：

    .. code-block:: pycon

        >>> g = group(fail.s(), fail.s())
        >>> g.link_error(log_error.s())
        >>> res = g()

    因此，通常建议将 errback 设计为幂等或可计数的任务，能容忍被多次调用。

    对于这类使用场景，更推荐使用 :class:`~celery.chord` 类，
    该类在某些后端实现中提供了更合适的支持。

.. tab:: 英文

    Groups can have callback and errback signatures linked to them as well, however
    the behaviour can be somewhat surprising due to the fact that groups are not
    real tasks and simply pass linked tasks down to their encapsulated signatures.
    This means that the return values of a group are not collected to be passed to
    a linked callback signature.
    Additionally, linking the task will *not* guarantee that it will activate only
    when all group tasks have finished.
    As an example, the following snippet using a simple `add(a, b)` task is faulty
    since the linked `add.s()` signature will not receive the finalised group
    result as one might expect.

    .. code-block:: pycon

        >>> g = group(add.s(2, 2), add.s(4, 4))
        >>> g.link(add.s())
        >>> res = g()
        [4, 8]

    Note that the finalised results of the first two tasks are returned, but the
    callback signature will have run in the background and raised an exception
    since it did not receive the two arguments it expects.

    Group errbacks are passed down to encapsulated signatures as well which opens
    the possibility for an errback linked only once to be called more than once if
    multiple tasks in a group were to fail.
    As an example, the following snippet using a `fail()` task which raises an
    exception can be expected to invoke the `log_error()` signature once for each
    failing task which gets run in the group.

    .. code-block:: pycon

        >>> g = group(fail.s(), fail.s())
        >>> g.link_error(log_error.s())
        >>> res = g()

    With this in mind, it's generally advisable to create idempotent or counting
    tasks which are tolerant to being called repeatedly for use as errbacks.

    These use cases are better addressed by the :class:`~celery.chord` class which
    is supported on certain backend implementations.

.. _group-results:

组结果
~~~~~~~~~~~~~

Group Results

.. tab:: 中文

    group 任务也会返回一个特殊的结果对象，
    这个结果对象的行为与普通的任务结果相似，
    只是它作用于整个 group：
    
    .. code-block:: pycon
    
        >>> from celery import group
        >>> from tasks import add
    
        >>> job = group([
        ...             add.s(2, 2),
        ...             add.s(4, 4),
        ...             add.s(8, 8),
        ...             add.s(16, 16),
        ...             add.s(32, 32),
        ... ])
    
        >>> result = job.apply_async()
    
        >>> result.ready()  # 所有子任务都完成了吗？
        True
        >>> result.successful() # 所有子任务都成功了吗？
        True
        >>> result.get()
        [4, 8, 16, 32, 64]
    
    :class:`~celery.result.GroupResult` 接收一个由 :class:`~celery.result.AsyncResult` 实例组成的列表，并将它们作为一个整体任务进行操作。
    
    它支持以下操作：
    
    * :meth:`~celery.result.GroupResult.successful`
    
      如果所有子任务都成功完成（例如没有抛出异常），返回 :const:`True`。
    
    * :meth:`~celery.result.GroupResult.failed`
    
      如果有任意一个子任务失败，返回 :const:`True`。
    
    * :meth:`~celery.result.GroupResult.waiting`
    
      如果仍有任意子任务尚未就绪，返回 :const:`True`。
    
    * :meth:`~celery.result.GroupResult.ready`
    
      如果所有子任务都已就绪，返回 :const:`True`。
    
    * :meth:`~celery.result.GroupResult.completed_count`
    
      返回已完成的子任务数量。注意，在此上下文中“完成”是指“成功”。换句话说，该方法的返回值是 `successful` 任务的数量。
    
    * :meth:`~celery.result.GroupResult.revoke`
    
      撤销所有子任务。
    
    * :meth:`~celery.result.GroupResult.join`
    
      收集所有子任务的结果，并按调用顺序返回（作为列表）。


.. tab:: 英文

    The group task returns a special result too,
    this result works just like normal task results, except
    that it works on the group as a whole:
    
    .. code-block:: pycon
    
        >>> from celery import group
        >>> from tasks import add
    
        >>> job = group([
        ...             add.s(2, 2),
        ...             add.s(4, 4),
        ...             add.s(8, 8),
        ...             add.s(16, 16),
        ...             add.s(32, 32),
        ... ])
    
        >>> result = job.apply_async()
    
        >>> result.ready()  # have all subtasks completed?
        True
        >>> result.successful() # were all subtasks successful?
        True
        >>> result.get()
        [4, 8, 16, 32, 64]
    
    The :class:`~celery.result.GroupResult` takes a list of
    :class:`~celery.result.AsyncResult` instances and operates on them as
    if it was a single task.
    
    It supports the following operations:
    
    * :meth:`~celery.result.GroupResult.successful`
    
      Return :const:`True` if all of the subtasks finished
      successfully (e.g., didn't raise an exception).
    
    * :meth:`~celery.result.GroupResult.failed`
    
      Return :const:`True` if any of the subtasks failed.
    
    * :meth:`~celery.result.GroupResult.waiting`
    
      Return :const:`True` if any of the subtasks
      isn't ready yet.
    
    * :meth:`~celery.result.GroupResult.ready`
    
      Return :const:`True` if all of the subtasks
      are ready.
    
    * :meth:`~celery.result.GroupResult.completed_count`
    
      Return the number of completed subtasks. Note that `complete` means `successful` in
      this context. In other words, the return value of this method is the number of
      ``successful`` tasks.
    
    * :meth:`~celery.result.GroupResult.revoke`
    
      Revoke all of the subtasks.
    
    * :meth:`~celery.result.GroupResult.join`
    
      Gather the results of all subtasks
      and return them in the same order as they were called (as a list).

.. _group-unrolling:

组展开
~~~~~~~~~~~~~~~

Group Unrolling

.. tab:: 中文

    当 group 中仅包含一个签名时，在链式调用中它将会被“展开”为单个签名。
    这意味着如下 group 会根据其中元素的数量，
    向后续 chain 传递一个结果或结果列表：

    .. code-block:: pycon

        >>> from celery import chain, group
        >>> from tasks import add
        >>> chain(add.s(2, 2), group(add.s(1)), add.s(1))
        add(2, 2) | add(1) | add(1)
        >>> chain(add.s(2, 2), group(add.s(1), add.s(2)), add.s(1))
        add(2, 2) | %add((add(1), add(2)), 1)

    这意味着，如果你打算在大型 canvas 中使用该任务，
    应确保 `add` 任务能够同时接受列表或单个元素作为输入。

    .. warning::

        在 Celery 4.x 中，以下 group 不会在链中被“展开”，而是由于 bug 的原因，canvas 会被升级为 chord：

        .. code-block:: pycon

            >>> from celery import chain, group
            >>> from tasks import add
            >>> chain(group(add.s(1, 1)), add.s(2))
            %add([add(1, 1)], 2)

        而在 Celery 5.x 中此 bug 已被修复，group 会被正确地展开为单个签名：

        .. code-block:: pycon

            >>> from celery import chain, group
            >>> from tasks import add
            >>> chain(group(add.s(1, 1)), add.s(2))
            add(1, 1) | add(2)

.. tab:: 英文

    A group with a single signature will be unrolled to a single signature when chained.
    This means that the following group may pass either a list of results or a single result to the chain
    depending on the number of items in the group.

    .. code-block:: pycon

        >>> from celery import chain, group
        >>> from tasks import add
        >>> chain(add.s(2, 2), group(add.s(1)), add.s(1))
        add(2, 2) | add(1) | add(1)
        >>> chain(add.s(2, 2), group(add.s(1), add.s(2)), add.s(1))
        add(2, 2) | %add((add(1), add(2)), 1)

    This means that you should be careful and make sure the ``add`` task can accept either a list or a single item as input
    if you plan to use it as part of a larger canvas.

    .. warning::

        In Celery 4.x the following group below would not unroll into a chain due to a bug but instead the canvas would be
        upgraded into a chord.

        .. code-block:: pycon

            >>> from celery import chain, group
            >>> from tasks import add
            >>> chain(group(add.s(1, 1)), add.s(2))
            %add([add(1, 1)], 2)

        In Celery 5.x this bug was fixed and the group is correctly unrolled into a single signature.

        .. code-block:: pycon

            >>> from celery import chain, group
            >>> from tasks import add
            >>> chain(group(add.s(1, 1)), add.s(2))
            add(1, 1) | add(2)

.. _canvas-chord:

合集
------

Chords

.. tab:: 中文

    .. versionadded:: 2.3

    .. note::

        chord 中的任务 *不得* 忽略其结果。  
        如果 chord 中的任意任务（无论是 header 还是 body）禁用了结果后端，  
        请阅读 ":ref:`chord-important-notes`"。  
        当前 chord 不支持 RPC 结果后端。

    chord 是一种特殊的任务，仅当 group 中的所有任务都执行完毕后才会执行。

    我们来计算如下表达式的和：
    :math:`1 + 1 + 2 + 2 + 3 + 3 ... n + n`，直到 100：

    首先你需要两个任务，:func:`add` 和 :func:`tsum`（:func:`sum` 是内建函数）：

    .. code-block:: python

        @app.task
        def add(x, y):
            return x + y

        @app.task
        def tsum(numbers):
            return sum(numbers)

    接下来你可以使用 chord 来并行计算每一对相加操作，
    然后对它们的结果求和：

    .. code-block:: pycon

        >>> from celery import chord
        >>> from tasks import add, tsum

        >>> chord(add.s(i, i)
        ...       for i in range(100))(tsum.s()).get()
        9900

    当然这只是一个人为构造的示例，
    消息传递和同步的开销使得它远比原生 Python 实现要慢：

    .. code-block:: pycon

        >>> sum(i + i for i in range(100))

    同步步骤代价较高，因此应尽可能避免使用 chord。
    尽管如此，chord 依然是一个强大的原语，
    在许多并行算法中， *同步* 是不可避免的。

    我们将 chord 表达式分解如下：

    .. code-block:: pycon

        >>> callback = tsum.s()
        >>> header = [add.s(i, i) for i in range(100)]
        >>> result = chord(header)(callback)
        >>> result.get()
        9900

    请记住，callback 只会在 header 中所有任务都返回后才会执行。
    header 中的每一步都是一个任务，可能会并行执行在不同节点上。
    然后 callback 会以这些任务的返回值为输入被调用。
    :meth:`chord` 返回的任务 ID 实际上是 callback 的 ID，
    因此你可以等待其完成并获取最终结果（但请牢记要 :ref:`避免任务之间同步等待 <task-synchronous-subtasks>`）。

.. tab:: 英文

    .. versionadded:: 2.3
    
    .. note::
    
        Tasks used within a chord must *not* ignore their results. If the result
        backend is disabled for *any* task (header or body) in your chord you
        should read ":ref:`chord-important-notes`". Chords are not currently
        supported with the RPC result backend.
    
    
    A chord is a task that only executes after all of the tasks in a group have
    finished executing.
    
    
    Let's calculate the sum of the expression
    :math:`1 + 1 + 2 + 2 + 3 + 3 ... n + n` up to a hundred digits.
    
    First you need two tasks, :func:`add` and :func:`tsum` (:func:`sum` is
    already a standard function):
    
    .. code-block:: python
    
        @app.task
        def add(x, y):
            return x + y
    
        @app.task
        def tsum(numbers):
            return sum(numbers)
    
    
    Now you can use a chord to calculate each addition step in parallel, and then
    get the sum of the resulting numbers:
    
    .. code-block:: pycon
    
        >>> from celery import chord
        >>> from tasks import add, tsum
    
        >>> chord(add.s(i, i)
        ...       for i in range(100))(tsum.s()).get()
        9900
    
    
    This is obviously a very contrived example, the overhead of messaging and
    synchronization makes this a lot slower than its Python counterpart:
    
    .. code-block:: pycon
    
        >>> sum(i + i for i in range(100))
    
    The synchronization step is costly, so you should avoid using chords as much
    as possible. Still, the chord is a powerful primitive to have in your toolbox
    as synchronization is a required step for many parallel algorithms.
    
    Let's break the chord expression down:
    
    .. code-block:: pycon
    
        >>> callback = tsum.s()
        >>> header = [add.s(i, i) for i in range(100)]
        >>> result = chord(header)(callback)
        >>> result.get()
        9900
    
    Remember, the callback can only be executed after all of the tasks in the
    header have returned. Each step in the header is executed as a task, in
    parallel, possibly on different nodes. The callback is then applied with
    the return value of each task in the header. The task id returned by
    :meth:`chord` is the id of the callback, so you can wait for it to complete
    and get the final return value (but remember to :ref:`never have a task wait
    for other tasks <task-synchronous-subtasks>`)

.. _chord-errors:

错误处理
~~~~~~~~~~~~~~

Error handling

.. tab:: 中文

    那么如果其中一个任务抛出异常会发生什么？
    
    chord 的回调结果将会进入失败状态，并且错误会被设置为
    :exc:`~@ChordError` 异常：
    
    .. code-block:: pycon
    
        >>> c = chord([add.s(4, 4), raising_task.s(), add.s(8, 8)])
        >>> result = c()
        >>> result.get()
    
    .. code-block:: pytb
    
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "*/celery/result.py", line 120, in get
            interval=interval)
          File "*/celery/backends/amqp.py", line 150, in wait_for
            raise meta['result']
        celery.exceptions.ChordError: Dependency 97de6f3f-ea67-4517-a21c-d867c61fcb47
            raised ValueError('something something',)
    
    虽然回溯信息可能会因所使用的结果后端不同而有所不同，
    但你可以看到错误描述中包含了失败任务的 ID，以及原始异常的字符串表示。
    你还可以在 ``result.traceback`` 中找到原始的回溯信息。
    
    注意，其他任务仍然会继续执行，所以即使中间的任务失败了，
    第三个任务（ ``add.s(8, 8)`` ）依然会被执行。
    同时，:exc:`~@ChordError` 只会显示第一个（按时间先后）失败的任务：
    它不会遵循 header 分组中的顺序。
    
    为了在 chord 失败时执行某些操作，你可以为 chord 回调附加一个 errback：
    
    .. code-block:: python
    
        @app.task
        def on_chord_error(request, exc, traceback):
            print('Task {0!r} raised error: {1!r}'.format(request.id, exc))
    
    .. code-block:: pycon
    
        >>> c = (group(add.s(i, i) for i in range(10)) |
        ...      tsum.s().on_error(on_chord_error.s())).delay()
    
    chord 允许将回调和错误回调（errback）签名关联起来，这解决了将签名链接到 group 的一些问题。
    这样可以将提供的签名连接到 chord 的 body 上，确保 body 完成时仅调用一次回调，
    或者当 header 或 body 中的任何任务失败时，仅调用一次 errback。
    
    你可以通过设置 :ref:`task_allow_error_cb_on_chord_header <task_allow_error_cb_on_chord_header>` 标志，
    来控制是否允许对 chord header 的错误进行处理。
    启用此标志后，chord header 中失败的任务将触发对 body 的 errback（默认行为），
    *并且* header 中失败的任务也会触发 errback。

.. tab:: 英文

    So what happens if one of the tasks raises an exception?
    
    The chord callback result will transition to the failure state, and the error is set
    to the :exc:`~@ChordError` exception:
    
    .. code-block:: pycon
    
        >>> c = chord([add.s(4, 4), raising_task.s(), add.s(8, 8)])
        >>> result = c()
        >>> result.get()
    
    .. code-block:: pytb
    
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "*/celery/result.py", line 120, in get
            interval=interval)
          File "*/celery/backends/amqp.py", line 150, in wait_for
            raise meta['result']
        celery.exceptions.ChordError: Dependency 97de6f3f-ea67-4517-a21c-d867c61fcb47
            raised ValueError('something something',)
    
    While the traceback may be different depending on the result backend used,
    you can see that the error description includes the id of the task that failed
    and a string representation of the original exception. You can also
    find the original traceback in ``result.traceback``.
    
    Note that the rest of the tasks will still execute, so the third task
    (``add.s(8, 8)``) is still executed even though the middle task failed.
    Also the :exc:`~@ChordError` only shows the task that failed
    first (in time): it doesn't respect the ordering of the header group.
    
    To perform an action when a chord fails you can therefore attach
    an errback to the chord callback:
    
    .. code-block:: python
    
        @app.task
        def on_chord_error(request, exc, traceback):
            print('Task {0!r} raised error: {1!r}'.format(request.id, exc))
    
    .. code-block:: pycon
    
        >>> c = (group(add.s(i, i) for i in range(10)) |
        ...      tsum.s().on_error(on_chord_error.s())).delay()
    
    Chords may have callback and errback signatures linked to them, which addresses
    some of the issues with linking signatures to groups.
    Doing so will link the provided signature to the chord's body which can be
    expected to gracefully invoke callbacks just once upon completion of the body,
    or errbacks just once if any task in the chord header or body fails.
    
    This behavior can be manipulated to allow error handling of the chord header using the :ref:`task_allow_error_cb_on_chord_header <task_allow_error_cb_on_chord_header>` flag.
    Enabling this flag will cause the chord header to invoke the errback for the body (default behavior) *and* any task in the chord's header that fails.

.. _chord-important-notes:

重要说明
~~~~~~~~~~~~~~~

Important Notes

.. tab:: 中文

    在 chord 中使用的任务 *不能* 忽略其结果。实际使用中，
    你必须启用 :const:`result_backend` 才能使用 chord。
    此外，如果你的配置中设置了 :const:`task_ignore_result` 为 :const:`True`，
    请确保参与 chord 的每个任务都设置了 :const:`ignore_result=False`。
    这对于任务子类和装饰器任务都适用。

    任务子类示例：

    .. code-block:: python

        class MyTask(Task):
            ignore_result = False

    装饰器任务示例：

    .. code-block:: python

        @app.task(ignore_result=False)
        def another_task(project):
            do_something()

    默认情况下，同步步骤的实现方式是启动一个周期性任务，
    每秒轮询一次 group 是否完成，并在准备就绪时调用签名。

    示例实现：

    .. code-block:: python

        from celery import maybe_signature

        @app.task(bind=True)
        def unlock_chord(self, group, callback, interval=1, max_retries=None):
            if group.ready():
                return maybe_signature(callback).delay(group.join())
            raise self.retry(countdown=interval, max_retries=max_retries)

    除了 Redis、Memcached 和 DynamoDB 以外的所有结果后端都使用该方式：
    它们在 header 中每个任务完成后递增计数器，并在计数器超过任务总数时应用回调。

    Redis、Memcached 和 DynamoDB 的方式则更加高效，但在其他后端中不易实现
    （欢迎提出建议！）。

    .. note::

        在 Redis 2.2 之前的版本中，chord 无法正常工作；
        你需要至少升级到 redis-server 2.2 才能使用它们。

    .. note::

        如果你在使用 Redis 结果后端时还重写了
        :meth:`Task.after_return` 方法，请确保调用了父类的实现，
        否则 chord 回调将不会被触发。

        .. code-block:: python

            def after_return(self, *args, **kwargs):
                do_something()
                super().after_return(*args, **kwargs)


.. tab:: 英文

    Tasks used within a chord must *not* ignore their results. In practice this
    means that you must enable a :const:`result_backend` in order to use
    chords. Additionally, if :const:`task_ignore_result` is set to :const:`True`
    in your configuration, be sure that the individual tasks to be used within
    the chord are defined with :const:`ignore_result=False`. This applies to both
    Task subclasses and decorated tasks.

    Example Task subclass:

    .. code-block:: python

        class MyTask(Task):
            ignore_result = False


    Example decorated task:

    .. code-block:: python

        @app.task(ignore_result=False)
        def another_task(project):
            do_something()

    By default the synchronization step is implemented by having a recurring task
    poll the completion of the group every second, calling the signature when
    ready.

    Example implementation:

    .. code-block:: python

        from celery import maybe_signature

        @app.task(bind=True)
        def unlock_chord(self, group, callback, interval=1, max_retries=None):
            if group.ready():
                return maybe_signature(callback).delay(group.join())
            raise self.retry(countdown=interval, max_retries=max_retries)


    This is used by all result backends except Redis, Memcached and DynamoDB: they
    increment a counter after each task in the header, then applies the callback
    when the counter exceeds the number of tasks in the set.

    The Redis, Memcached and DynamoDB approach is a much better solution, but not easily
    implemented in other backends (suggestions welcome!).

    .. note::

        Chords don't properly work with Redis before version 2.2; you'll need to
        upgrade to at least redis-server 2.2 to use them.

    .. note::

        If you're using chords with the Redis result backend and also overriding
        the :meth:`Task.after_return` method, you need to make sure to call the
        super method or else the chord callback won't be applied.

        .. code-block:: python

            def after_return(self, *args, **kwargs):
                do_something()
                super().after_return(*args, **kwargs)

.. _canvas-map:

map 和 starmap
-------------

Map & Starmap

.. tab:: 中文

    :class:`~celery.map` 和 :class:`~celery.starmap` 是内置任务，
    它们会对序列中的每个元素调用指定的调用任务。
    
    它们与 :class:`~celery.group` 不同之处在于：
    
    - 只发送一条任务消息。
    
    - 操作是顺序执行的。
    
    例如使用 ``map``：
    
    .. code-block:: pycon
    
        >>> from proj.tasks import add
    
        >>> ~tsum.map([list(range(10)), list(range(100))])
        [45, 4950]
    
    这等价于一个任务这样做：
    
    .. code-block:: python
    
        @app.task
        def temp():
            return [tsum(range(10)), tsum(range(100))]
    
    使用 ``starmap``：
    
    .. code-block:: pycon
    
        >>> ~add.starmap(zip(range(10), range(10)))
        [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
    
    这等价于一个任务这样写：
    
    .. code-block:: python
    
        @app.task
        def temp():
            return [add(i, i) for i in range(10)]
    
    ``map`` 和 ``starmap`` 都是签名对象，因此它们可以像其他签名一样使用，
    并与 group 等组合使用，例如可以在 10 秒后调用 starmap：
    
    .. code-block:: pycon
    
        >>> add.starmap(zip(range(10), range(10))).apply_async(countdown=10)

.. tab:: 英文

    :class:`~celery.map` and :class:`~celery.starmap` are built-in tasks
    that call the provided calling task for every element in a sequence.

    They differ from :class:`~celery.group` in that:

    - only one task message is sent.

    - the operation is sequential.

    For example using ``map``:

    .. code-block:: pycon

        >>> from proj.tasks import add

        >>> ~tsum.map([list(range(10)), list(range(100))])
        [45, 4950]

    is the same as having a task doing:

    .. code-block:: python

        @app.task
        def temp():
            return [tsum(range(10)), tsum(range(100))]

    and using ``starmap``:

    .. code-block:: pycon

        >>> ~add.starmap(zip(range(10), range(10)))
        [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

    is the same as having a task doing:

    .. code-block:: python

        @app.task
        def temp():
            return [add(i, i) for i in range(10)]

    Both ``map`` and ``starmap`` are signature objects, so they can be used as
    other signatures and combined in groups etc., for example
    to call the starmap after 10 seconds:

    .. code-block:: pycon

        >>> add.starmap(zip(range(10), range(10))).apply_async(countdown=10)

.. _canvas-chunks:

数据块
------

Chunks

.. tab:: 中文

    chunking 允许你将一个可迭代的工作集分割成多块，因此如果你有一百万个对象，
    可以将它们分成 10 个任务，每个任务处理十万个对象。
    
    有些人可能担心将任务切块会降低并行度，但这在实际中很少发生，
    尤其是在繁忙的集群中，因为它减少了消息传递的开销，
    所以通常可以显著提升性能。
    
    要创建 chunk 签名，可以使用 :meth:`@Task.chunks` 方法：
    
    .. code-block:: pycon
    
        >>> add.chunks(zip(range(100), range(100)), 10)
    
    与 :class:`~celery.group` 一样，chunk 的消息发送操作是在当前进程中完成的：
    
    .. code-block:: pycon
    
        >>> from proj.tasks import add
    
        >>> res = add.chunks(zip(range(100), range(100)), 10)()
        >>> res.get()
        [[0, 2, 4, 6, 8, 10, 12, 14, 16, 18],
         [20, 22, 24, 26, 28, 30, 32, 34, 36, 38],
         [40, 42, 44, 46, 48, 50, 52, 54, 56, 58],
         [60, 62, 64, 66, 68, 70, 72, 74, 76, 78],
         [80, 82, 84, 86, 88, 90, 92, 94, 96, 98],
         [100, 102, 104, 106, 108, 110, 112, 114, 116, 118],
         [120, 122, 124, 126, 128, 130, 132, 134, 136, 138],
         [140, 142, 144, 146, 148, 150, 152, 154, 156, 158],
         [160, 162, 164, 166, 168, 170, 172, 174, 176, 178],
         [180, 182, 184, 186, 188, 190, 192, 194, 196, 198]]
    
    而调用 ``.apply_async`` 则会创建一个独立任务，
    从而在 worker 中应用这些单独的任务：
    
    .. code-block:: pycon
    
        >>> add.chunks(zip(range(100), range(100)), 10).apply_async()
    
    你也可以将 chunks 转换为一个 group：
    
    .. code-block:: pycon
    
        >>> group = add.chunks(zip(range(100), range(100)), 10).group()
    
    然后使用 group 的 skew 方法为每个任务设置递增的 countdown：
    
    .. code-block:: pycon
    
        >>> group.skew(start=1, stop=10)()
    
    这意味着第一个任务将在 1 秒后执行，第二个任务在 2 秒后，依此类推。

.. tab:: 英文

    Chunking lets you divide an iterable of work into pieces, so that if
    you have one million objects, you can create 10 tasks with a hundred
    thousand objects each.
    
    Some may worry that chunking your tasks results in a degradation
    of parallelism, but this is rarely true for a busy cluster
    and in practice since you're avoiding the overhead  of messaging
    it may considerably increase performance.
    
    To create a chunks' signature you can use :meth:`@Task.chunks`:
    
    .. code-block:: pycon
    
        >>> add.chunks(zip(range(100), range(100)), 10)
    
    As with :class:`~celery.group` the act of sending the messages for
    the chunks will happen in the current process when called:
    
    .. code-block:: pycon
    
        >>> from proj.tasks import add
    
        >>> res = add.chunks(zip(range(100), range(100)), 10)()
        >>> res.get()
        [[0, 2, 4, 6, 8, 10, 12, 14, 16, 18],
         [20, 22, 24, 26, 28, 30, 32, 34, 36, 38],
         [40, 42, 44, 46, 48, 50, 52, 54, 56, 58],
         [60, 62, 64, 66, 68, 70, 72, 74, 76, 78],
         [80, 82, 84, 86, 88, 90, 92, 94, 96, 98],
         [100, 102, 104, 106, 108, 110, 112, 114, 116, 118],
         [120, 122, 124, 126, 128, 130, 132, 134, 136, 138],
         [140, 142, 144, 146, 148, 150, 152, 154, 156, 158],
         [160, 162, 164, 166, 168, 170, 172, 174, 176, 178],
         [180, 182, 184, 186, 188, 190, 192, 194, 196, 198]]
    
    while calling ``.apply_async`` will create a dedicated
    task so that the individual tasks are applied in a worker
    instead:
    
    .. code-block:: pycon
    
        >>> add.chunks(zip(range(100), range(100)), 10).apply_async()
    
    You can also convert chunks to a group:
    
    .. code-block:: pycon
    
        >>> group = add.chunks(zip(range(100), range(100)), 10).group()
    
    and with the group skew the countdown of each task by increments
    of one:
    
    .. code-block:: pycon
    
        >>> group.skew(start=1, stop=10)()
    
    This means that the first task will have a countdown of one second, the second
    task a countdown of two seconds, and so on.

.. _canvas-stamping:

标记
========

Stamping

.. tab:: 中文

    .. versionadded:: 5.3

    Stamping API 的目标是提供为签名及其组成部分打标签的能力，
    以便于调试信息的标注。
    例如，在 canvas 是一个复杂结构时，可能需要为结构中的部分或全部元素打标签。
    复杂性在展开嵌套 group 或替换 chain 元素时进一步增加。
    在此类情况下，可能需要知道某个元素属于哪个 group 或它处于哪个嵌套层级。
    这就需要一个遍历 canvas 元素并以特定元数据标注它们的机制。
    Stamping API 允许基于 Visitor 模式实现这一功能。

    例如：

    .. code-block:: pycon

        >>> sig1 = add.si(2, 2)
        >>> sig1_res = sig1.freeze()
        >>> g = group(sig1, add.si(3, 3))
        >>> g.stamp(stamp='your_custom_stamp')
        >>> res = g.apply_async()
        >>> res.get(timeout=TIMEOUT)
        [4, 6]
        >>> sig1_res._get_task_meta()['stamp']
        ['your_custom_stamp']

    这将初始化一个 group ``g``，并为其组件打上 ``your_custom_stamp`` 标签。

    要使该功能生效，你需要将配置项 :setting:`result_extended` 设置为 ``True``，
    或使用配置指令 ``result_extended = True``。

.. tab:: 英文

    .. versionadded:: 5.3

    The goal of the Stamping API is to give an ability to label
    the signature and its components for debugging information purposes.
    For example, when the canvas is a complex structure, it may be necessary to
    label some or all elements of the formed structure. The complexity
    increases even more when nested groups are rolled-out or chain
    elements are replaced. In such cases, it may be necessary to
    understand which group an element is a part of or on what nested
    level it is. This requires a mechanism that traverses the canvas
    elements and marks them with specific metadata. The stamping API
    allows doing that based on the Visitor pattern.

    For example,

    .. code-block:: pycon

        >>> sig1 = add.si(2, 2)
        >>> sig1_res = sig1.freeze()
        >>> g = group(sig1, add.si(3, 3))
        >>> g.stamp(stamp='your_custom_stamp')
        >>> res = g.apply_async()
        >>> res.get(timeout=TIMEOUT)
        [4, 6]
        >>> sig1_res._get_task_meta()['stamp']
        ['your_custom_stamp']

    will initialize a group ``g`` and mark its components with stamp ``your_custom_stamp``.

    For this feature to be useful, you need to set the :setting:`result_extended`
    configuration option to ``True`` or directive ``result_extended = True``.

Canvas 标记
----------------

Canvas stamping

.. tab:: 中文

    你还可以通过自定义 stamping 逻辑来标记 canvas，
    方法是继承 visitor 类 ``StampingVisitor`` 以实现自定义 stamping visitor。

.. tab:: 英文

    We can also stamp the canvas with custom stamping logic, using the visitor class ``StampingVisitor``
    as the base class for the custom stamping visitor.

自定义标记
----------------

Custom stamping

.. tab:: 中文

    如果需要更复杂的标记（stamping）逻辑，可以基于访问者模式（Visitor pattern）实现自定义标记行为。
    实现此类自定义逻辑的类必须继承自 ``StampingVisitor`` 并实现相应的方法。

    例如，下面这个名为 ``InGroupVisitor`` 的示例将会给某个 group 中的任务打上 ``in_group`` 的标签：

    .. code-block:: python

        class InGroupVisitor(StampingVisitor):
            def __init__(self):
                self.in_group = False

            def on_group_start(self, group, **headers) -> dict:
                self.in_group = True
                return {"in_group": [self.in_group], "stamped_headers": ["in_group"]}

            def on_group_end(self, group, **headers) -> None:
                self.in_group = False

            def on_chain_start(self, chain, **headers) -> dict:
                return {"in_group": [self.in_group], "stamped_headers": ["in_group"]}

            def on_signature(self, sig, **headers) -> dict:
                return {"in_group": [self.in_group], "stamped_headers": ["in_group"]}

    下面是另一个自定义的标记访问器示例，它会给所有任务加上一个自定义的 ``monitoring_id``。
    这个 ``monitoring_id`` 可以代表外部监控系统中的 UUID 值，可用于通过包含此 ID 来追踪任务执行情况。
    该 ID 可以是随机生成的 UUID，或是监控系统中的唯一 span ID 等标识符。

    .. code-block:: python

        class MonitoringIdStampingVisitor(StampingVisitor):
            def on_signature(self, sig, **headers) -> dict:
                return {'monitoring_id': uuid4().hex}

    .. note::

        在 ``on_signature`` （或任何其他访问器方法）中返回的 ``stamped_headers`` 键用于指定
        应该打到任务上的 header。如果未指定此键，访问器会假设返回的字典中的所有键都是要标记的 header。

        这意味着，下面的代码块行为等同于前面的示例。

    .. code-block:: python

        class MonitoringIdStampingVisitor(StampingVisitor):
            def on_signature(self, sig, **headers) -> dict:
                return {'monitoring_id': uuid4().hex, 'stamped_headers': ['monitoring_id']}

    接下来，我们看看如何使用 ``MonitoringIdStampingVisitor`` 示例访问器对不同的画布结构（canvas）进行打标：

    .. code-block:: python

        sig_example = signature('t1')
        sig_example.stamp(visitor=MonitoringIdStampingVisitor())

        group_example = group([signature('t1'), signature('t2')])
        group_example.stamp(visitor=MonitoringIdStampingVisitor())

        chord_example = chord([signature('t1'), signature('t2')], signature('t3'))
        chord_example.stamp(visitor=MonitoringIdStampingVisitor())

        chain_example = chain(signature('t1'), group(signature('t2'), signature('t3')), signature('t4'))
        chain_example.stamp(visitor=MonitoringIdStampingVisitor())

    最后需要说明的是，上述示例中的每个任务会获得不同的 monitoring id。

.. tab:: 英文

    If more complex stamping logic is required, it is possible
    to implement custom stamping behavior based on the Visitor
    pattern. The class that implements this custom logic must
    inherit ``StampingVisitor`` and implement appropriate methods.

    For example, the following example ``InGroupVisitor`` will label
    tasks that are in side of some group by label ``in_group``.

    .. code-block:: python

        class InGroupVisitor(StampingVisitor):
            def __init__(self):
                self.in_group = False

            def on_group_start(self, group, **headers) -> dict:
                self.in_group = True
                return {"in_group": [self.in_group], "stamped_headers": ["in_group"]}

            def on_group_end(self, group, **headers) -> None:
                self.in_group = False

            def on_chain_start(self, chain, **headers) -> dict:
                return {"in_group": [self.in_group], "stamped_headers": ["in_group"]}

            def on_signature(self, sig, **headers) -> dict:
                return {"in_group": [self.in_group], "stamped_headers": ["in_group"]}

    The following example shows another custom stamping visitor, which labels all
    tasks with a custom ``monitoring_id`` which can represent a UUID value of an external monitoring system,
    that can be used to track the task execution by including the id with such a visitor implementation.
    This ``monitoring_id`` can be a randomly generated UUID, or a unique identifier of the span id used by
    the external monitoring system, etc.

    .. code-block:: python

        class MonitoringIdStampingVisitor(StampingVisitor):
            def on_signature(self, sig, **headers) -> dict:
                return {'monitoring_id': uuid4().hex}

    .. note::

        The ``stamped_headers`` key returned in ``on_signature`` (or any other visitor method) is used to
        specify the headers that will be stamped on the task. If this key is not specified, the stamping
        visitor will assume all keys in the returned dictionary are the stamped headers from the visitor.

        This means the following code block will result in the same behavior as the previous example.

    .. code-block:: python

        class MonitoringIdStampingVisitor(StampingVisitor):
            def on_signature(self, sig, **headers) -> dict:
                return {'monitoring_id': uuid4().hex, 'stamped_headers': ['monitoring_id']}

    Next, let's see how to use the ``MonitoringIdStampingVisitor`` example stamping visitor.

    .. code-block:: python

        sig_example = signature('t1')
        sig_example.stamp(visitor=MonitoringIdStampingVisitor())

        group_example = group([signature('t1'), signature('t2')])
        group_example.stamp(visitor=MonitoringIdStampingVisitor())

        chord_example = chord([signature('t1'), signature('t2')], signature('t3'))
        chord_example.stamp(visitor=MonitoringIdStampingVisitor())

        chain_example = chain(signature('t1'), group(signature('t2'), signature('t3')), signature('t4'))
        chain_example.stamp(visitor=MonitoringIdStampingVisitor())

    Lastly, it's important to mention that each monitoring id stamp in the example above would be different from each other between tasks.

回调函数标记
------------------

Callbacks stamping

.. tab:: 中文

    标记 API 也支持对回调（callback）进行隐式标记。
    这意味着当某个回调添加到任务上时，访问器也会应用到该回调上。

    .. warning::

        回调必须在标记之前链接到签名（signature）上。

    例如，下面是一个自定义标记访问器的定义：

    .. code-block:: python

        class CustomStampingVisitor(StampingVisitor):
            def on_signature(self, sig, **headers) -> dict:
                return {'header': 'value'}

            def on_callback(self, callback, **header) -> dict:
                return {'on_callback': True}

            def on_errback(self, errback, **header) -> dict:
                return {'on_errback': True}

    这个自定义访问器将会对签名、回调和错误回调打上 ``{'header': 'value'}``，
    并分别为回调和错误回调添加 ``{'on_callback': True}`` 与 ``{'on_errback': True}``：

    .. code-block:: python

            c = chord([add.s(1, 1), add.s(2, 2)], xsum.s())
            callback = signature('sig_link')
            errback = signature('sig_link_error')
            c.link(callback)
            c.link_error(errback)
            c.stamp(visitor=CustomStampingVisitor())

    该示例的最终结果为：

    .. code-block:: python

        >>> c.options
        {'header': 'value', 'stamped_headers': ['header']}
        >>> c.tasks.tasks[0].options
        {'header': 'value', 'stamped_headers': ['header']}
        >>> c.tasks.tasks[1].options
        {'header': 'value', 'stamped_headers': ['header']}
        >>> c.body.options
        {'header': 'value', 'stamped_headers': ['header']}
        >>> c.body.options['link'][0].options
        {'header': 'value', 'on_callback': True, 'stamped_headers': ['header', 'on_callback']}
        >>> c.body.options['link_error'][0].options
        {'header': 'value', 'on_errback': True, 'stamped_headers': ['header', 'on_errback']}


.. tab:: 英文

    The stamping API also supports stamping callbacks implicitly.
    This means that when a callback is added to a task, the stamping
    visitor will be applied to the callback as well.

    .. warning::

        The callback must be linked to the signature before stamping.

    For example, let's examine the following custom stamping visitor.

    .. code-block:: python

        class CustomStampingVisitor(StampingVisitor):
            def on_signature(self, sig, **headers) -> dict:
                return {'header': 'value'}

            def on_callback(self, callback, **header) -> dict:
                return {'on_callback': True}

            def on_errback(self, errback, **header) -> dict:
                return {'on_errback': True}

    This custom stamping visitor will stamp the signature, callbacks, and errbacks with ``{'header': 'value'}``
    and stamp the callbacks and errbacks with ``{'on_callback': True}`` and ``{'on_errback': True}`` respectively as shown below.

    .. code-block:: python

        c = chord([add.s(1, 1), add.s(2, 2)], xsum.s())
        callback = signature('sig_link')
        errback = signature('sig_link_error')
        c.link(callback)
        c.link_error(errback)
        c.stamp(visitor=CustomStampingVisitor())

    This example will result in the following stamps:

    .. code-block:: python

        >>> c.options
        {'header': 'value', 'stamped_headers': ['header']}
        >>> c.tasks.tasks[0].options
        {'header': 'value', 'stamped_headers': ['header']}
        >>> c.tasks.tasks[1].options
        {'header': 'value', 'stamped_headers': ['header']}
        >>> c.body.options
        {'header': 'value', 'stamped_headers': ['header']}
        >>> c.body.options['link'][0].options
        {'header': 'value', 'on_callback': True, 'stamped_headers': ['header', 'on_callback']}
        >>> c.body.options['link_error'][0].options
        {'header': 'value', 'on_errback': True, 'stamped_headers': ['header', 'on_errback']}
