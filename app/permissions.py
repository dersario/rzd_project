from abc import ABC, abstractmethod

from app.models.user import User


class BasePermission(ABC):
    @abstractmethod
    def check_permission(self, account: User | None):
        pass


class Authenticated(BasePermission):
    def check_permission(self, account):
        return account is not None


class Anonymous(BasePermission):
    def check_permission(self, account):
        return account is None
