"""
.. tab:: 中文

    Sphinx 文档插件用于为任务生成文档。

.. tab:: 英文

    Sphinx documentation plugin used to document tasks.

简介
============

Introduction

用法
-----

Usage

.. tab:: 中文

    Celery 的 Sphinx 扩展要求 Sphinx 版本为 2.0 或更高。

    在你的 :file:`docs/conf.py` 配置模块中添加该扩展：

    .. code-block:: python

        extensions = (...,
                    'celery.contrib.sphinx')

    如果你希望在参考文档中更改任务的前缀，可以设置 ``celery_task_prefix`` 配置项：

    .. code-block:: python

        celery_task_prefix = '(task)'  # < 默认值

    安装该扩展后，`autodoc` 会自动识别使用装饰器标记的任务对象（例如在使用 automodule 指令时），
    并正确生成文档（同时添加 ``(task)`` 前缀）。你也可以使用 `:task:proj.tasks.add` 语法引用任务。

    你也可以使用 ``.. autotask::`` 来手动为某个任务编写文档。


.. tab:: 英文

    The Celery extension for Sphinx requires Sphinx 2.0 or later.

    Add the extension to your :file:`docs/conf.py` configuration module:

    .. code-block:: python

        extensions = (...,
                    'celery.contrib.sphinx')

    If you'd like to change the prefix for tasks in reference documentation
    then you can change the ``celery_task_prefix`` configuration value:

    .. code-block:: python

        celery_task_prefix = '(task)'  # < default

    With the extension installed `autodoc` will automatically find
    task decorated objects (e.g. when using the automodule directive)
    and generate the correct (as well as add a ``(task)`` prefix),
    and you can also refer to the tasks using `:task:proj.tasks.add`
    syntax.

    Use ``.. autotask::`` to alternatively manually document a task.
"""

from inspect import signature

from docutils import nodes
from sphinx.domains.python import PyFunction
from sphinx.ext.autodoc import FunctionDocumenter

from celery.app.task import BaseTask


class TaskDocumenter(FunctionDocumenter):
    """Document task definitions."""

    objtype = "task"
    member_order = 11

    @classmethod
    def can_document_member(cls, member, membername, isattr, parent):
        return isinstance(member, BaseTask) and getattr(member, "__wrapped__")

    def format_args(self):
        wrapped = getattr(self.object, "__wrapped__", None)
        if wrapped is not None:
            sig = signature(wrapped)
            if "self" in sig.parameters or "cls" in sig.parameters:
                sig = sig.replace(parameters=list(sig.parameters.values())[1:])
            return str(sig)
        return ""

    def document_members(self, all_members=False):
        pass

    def check_module(self):
        # Normally checks if *self.object* is really defined in the module
        # given by *self.modname*. But since functions decorated with the @task
        # decorator are instances living in the celery.local, we have to check
        # the wrapped function instead.
        wrapped = getattr(self.object, "__wrapped__", None)
        if wrapped and getattr(wrapped, "__module__") == self.modname:
            return True
        return super().check_module()


class TaskDirective(PyFunction):
    """Sphinx task directive."""

    def get_signature_prefix(self, sig):
        return [nodes.Text(self.env.config.celery_task_prefix)]


def autodoc_skip_member_handler(app, what, name, obj, skip, options):
    """Handler for autodoc-skip-member event."""
    # Celery tasks created with the @task decorator have the property
    # that *obj.__doc__* and *obj.__class__.__doc__* are equal, which
    # trips up the logic in sphinx.ext.autodoc that is supposed to
    # suppress repetition of class documentation in an instance of the
    # class. This overrides that behavior.
    if isinstance(obj, BaseTask) and getattr(obj, "__wrapped__"):
        if skip:
            return False
    return None


def setup(app):
    """Setup Sphinx extension."""
    app.setup_extension("sphinx.ext.autodoc")
    app.add_autodocumenter(TaskDocumenter)
    app.add_directive_to_domain("py", "task", TaskDirective)
    app.add_config_value("celery_task_prefix", "(task)", True)
    app.connect("autodoc-skip-member", autodoc_skip_member_handler)

    return {"parallel_read_safe": True}
