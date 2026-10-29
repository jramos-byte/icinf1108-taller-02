import copy
from typing import Dict, Any

class InMemoryStore:
    def __init__(self):
        self._data: Dict[str, Any] = {
            "students": {},
            "pets": {}
        }
        self._backup: Dict[str, Any] = None

    def begin_transaction(self):
        """Inicia una transacción guardando el estado actual."""
        if self._backup is not None:
            raise Exception("Ya hay una transaccion activa en este hilo.")
        self._backup = copy.deepcopy(self._data)

    def commit(self):
        """Confirma los cambios eliminando el respaldo."""
        if self._backup is None:
            raise Exception("No hay ninguna transaccion activa para confirmar.")
        self._backup = None

    def rollback(self):
        """Revierte el estado al momento exacto de begin_transaction."""
        if self._backup is None:
            raise Exception("No hay ninguna transaccion activa para revertir.")
        self._data = copy.deepcopy(self._backup)
        self._backup = None

    def transaction(self):
        class TransactionContext:
            def __init__(self, store):
                self.store = store
            def __enter__(self):
                self.store.begin_transaction()
                return self.store
            def __exit__(self, exc_type, exc_val, exc_tb):
                if exc_type is not None:
                    self.store.rollback()
                else:
                    self.store.commit()
                return False 
        return TransactionContext(self)

store_instance = InMemoryStore()
