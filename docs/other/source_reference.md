# Source reference

Copied from the existing working MVP. The original checkout was left unchanged.
This project starts a separate Git history with no inherited remote.

Original remote (reference only; never a push destination):
`https://github.com/boris2289/uldar.net.git`

Original directories: `uldar.net/uldar_net/settings/` and
`uldar.net/UldarFront/UldarFront/`.

They are now `stack-underflow/backend/stack_underflow/` and
`stack-underflow/frontend/`. The settings package became `stack_underflow`;
its base.py, conf.py, env/, urls.py, asgi.py, wsgi.py and celery.py keep their filenames.
Django app labels, table names and migration contents are unchanged.

The old names in this file are intentionally kept as historical reference.

The optional existing seed command now reads `STACK_UNDERFLOW_SEED_PASSWORD`
from the environment instead of using a shared password in source code.
