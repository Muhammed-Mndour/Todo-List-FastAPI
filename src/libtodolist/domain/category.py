from datetime import datetime

from pydantic import field_validator

from libtodolist.data import entities
from libtodolist.exceptions import CategoryValidationException, ForbiddenActionException
from libutil.util import BaseModel


class GetCategories(BaseModel):

    def execute(self, ctx, session):
        categories = entities.category.get_categories(session.conn, ctx.id_user)

        return categories


class AddCategory(BaseModel):
    label: str

    @field_validator('label')
    @classmethod
    def validate_label(cls, value: str) -> str:
        if not value.isalnum():
            raise ValueError('label must be alphanumeric')
        return value

    def execute(self, ctx, session):
        code = self._generate_category_code()
        entities.category.insert_category(session.conn, ctx.id_user, code, self.label)

    def _generate_category_code(self):
        return f"C{int(datetime.now().timestamp() * 1000)}"


class UpdateCategory(BaseModel):
    class Category(BaseModel):
        label: str

    code: str
    category: Category

    def execute(self, ctx, session):
        self._validate(session.conn, ctx.id_user)

        entities.category.update_category(session.conn, self.code, self.category.label)

    def _validate(self, conn, id_user):
        category = entities.category.get_by_code(conn, self.code, is_active=True)

        if not category:
            raise CategoryValidationException(f"Category {self.code} does not exist!")

        if category['id_user'] != id_user:
            raise ForbiddenActionException()


class DeleteCategory(BaseModel):
    code: str

    def execute(self, ctx, session):
        self._validate(session.conn, ctx.id_user)

        entities.category.delete_category(session.conn, self.code)

    def _validate(self, conn, id_user):
        category = entities.category.get_by_code(conn, self.code, is_active=True)

        if not category:
            raise CategoryValidationException(f"Category {self.code} does not exist!")

        if category['id_user'] != id_user:
            raise ForbiddenActionException()
