=======================
命令行接口
=======================

Command Line Interface

.. tab:: 中文

   .. NOTE:: 
      
      下述环境变量的名称必须添加前缀 `CELERY_` 。例如， `APP` 应改为 `CELERY_APP`。

.. tab:: 英文

   .. NOTE:: 
      
      The prefix `CELERY_` must be added to the names of the environment variables described below. E.g., `APP` becomes `CELERY_APP`.

.. click:: celery.bin.celery:celery
   :prog: celery
   :nested: full
