"""Error types for the Neon Ronin first persistence proof."""

from __future__ import annotations

class PersistenceProofError(Exception):
    """Base error for the persistence proof."""


class ValidationError(PersistenceProofError):
    """Raised when caller input violates the proof contract."""


class AuditWriteError(PersistenceProofError):
    """Raised when audit writing fails inside the transaction."""


class NotFoundError(PersistenceProofError):
    """Raised when an expected record does not exist."""
