class Session:
    precommit_hooks: dict = {}
    isolation_level: str = None
    conn = None

    def __init__(self, engine, isolation_level=None, **kwargs):
        if not engine:
            raise Exception('Engine is required to create a session')

        self._engine = engine
        self.isolation_level = isolation_level

    def __enter__(self):
        if self.isolation_level:
            self.conn = self._engine.connect().execution_options(isolation_level=self.isolation_level)
        else:
            self.conn = self._engine.connect()

        self._transaction = self.conn.begin()
        self._transaction.__enter__()

        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_value is None:
            for fn in self.precommit_hooks.values():
                fn()

        self._transaction.__exit__(exc_type, exc_value, tb)
        self.conn.close()

    def register_precommit(self, key, fn):
        self.precommit_hooks[key] = fn
