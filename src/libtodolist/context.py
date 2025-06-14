from typing import Optional

from libutil.util import BaseModel


class RequestContext(BaseModel):
    # todolist service context attributes
    id_user: Optional[int] = None
    user_code: str = None

    @staticmethod
    def from_todolist_service(user_code, **kwargs):
        """
        Creates a RequestContext for requests coming from the todolist service.
        Add more service-specific factory methods as needed:
        - from_auth_service()
        - from_payment_service()
        - from_notification_service()
        etc.
        """

        from libtodolist.data import engine_todolist, entities

        id_user = entities.user.get_id_by_code(engine_todolist, user_code)
        if not id_user:
            id_user = entities.user.insert_user(engine_todolist, user_code)

        kwargs.update(
            {
                'id_user': id_user,
                'user_code': user_code,
            }
        )

        return RequestContext(**kwargs)

    @staticmethod
    def mock(**kwargs):
        """
        Creates a mock RequestContext for testing, background jobs, or cron tasks.
        Useful for:
        - Unit tests
        - Background workers
        - Cron jobs
        - Development environments
        """
        return RequestContext(**kwargs)
