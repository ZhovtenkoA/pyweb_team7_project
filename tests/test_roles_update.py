import unittest
from unittest.mock import AsyncMock
from fastapi import HTTPException, status
from fastapi.requests import Request
from pyweb_team7_project.database.models import Role, User

from pyweb_team7_project.services.roles import RoleAccess


class TestRoleAccess(unittest.TestCase):
    async def test_allowed_role(self):
        request = Request()
        user = User(role=Role.admin)
        allowed_roles = [Role.admin, Role.moderator, Role.user]
        role_access = RoleAccess(allowed_roles)

        try:
            await role_access(request=request, user=user)
        except HTTPException as e:
            self.fail(f"Unexpected HTTPException: {e}")

    async def test_forbidden_role(self):
        request = Request()
        user = User(role=Role.guest)
        allowed_roles = [Role.admin, Role.moderator, Role.user]
        role_access = RoleAccess(allowed_roles)

        with self.assertRaises(HTTPException) as context:
            await role_access(request=request, user=user)

        self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(context.exception.detail, "Forbidden operation")

    async def test_default_user(self):
        request = Request()
        user = User(role=Role.user)
        allowed_roles = [Role.admin, Role.moderator]
        role_access = RoleAccess(allowed_roles)

        with self.assertRaises(HTTPException) as context:
            await role_access(request=request, user=user)

        self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(context.exception.detail, "Forbidden operation")

    async def test_allowed_role_with_default_user(self):
        request = Request()
        user = User(role=Role.user)
        allowed_roles = [Role.admin, Role.moderator, Role.user]
        role_access = RoleAccess(allowed_roles)

        try:
            await role_access(request=request)
        except HTTPException as e:
            self.fail(f"Unexpected HTTPException: {e}")

    async def test_no_current_user(self):
        request = Request()
        user = None
        allowed_roles = [Role.admin, Role.moderator]
        role_access = RoleAccess(allowed_roles)

        with self.assertRaises(HTTPException) as context:
            await role_access(request=request, user=user)

        self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(context.exception.detail, "Forbidden operation")

    async def test_empty_allowed_roles(self):
        request = Request()
        user = User(role=Role.admin)
        allowed_roles = []
        role_access = RoleAccess(allowed_roles)

        with self.assertRaises(HTTPException) as context:
            await role_access(request=request, user=user)

        self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(context.exception.detail, "Forbidden operation")

    async def test_allowed_role_with_mocked_dependency(self):
        request = Request()
        user = User(role=Role.admin)
        allowed_roles = [Role.admin, Role.moderator]
        role_access = RoleAccess(allowed_roles)

        mocked_dependency = AsyncMock(return_value=user)
        try:
            await role_access(request=request, user=await mocked_dependency())
        except HTTPException as e:
            self.fail(f"Unexpected HTTPException: {e}")

    async def test_forbidden_role_with_mocked_dependency(self):
        request = Request()
        user = User(role=Role.guest)
        allowed_roles = [Role.admin, Role.moderator]
        role_access = RoleAccess(allowed_roles)

        mocked_dependency = AsyncMock(return_value=user)
        with self.assertRaises(HTTPException) as context:
            await role_access(request=request, user=await mocked_dependency())

        self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(context.exception.detail, "Forbidden operation")

    async def test_no_current_user_with_mocked_dependency(self):
        request = Request()
        user = None
        allowed_roles = [Role.admin, Role.moderator]
        role_access = RoleAccess(allowed_roles)

        mocked_dependency = AsyncMock(return_value=user)
        with self.assertRaises(HTTPException) as context:
            await role_access(request=request, user=await mocked_dependency())

        self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(context.exception.detail, "Forbidden operation")

    async def test_allowed_role_with_empty_allowed_roles(self):
        request = Request()
        user = User(role=Role.admin)
        allowed_roles = []
        role_access = RoleAccess(allowed_roles)

        try:
            await role_access(request=request, user=user)
        except HTTPException as e:
            self.fail(f"Unexpected HTTPException: {e}")

    async def test_forbidden_role_with_empty_allowed_roles(self):
        request = Request()
        user = User(role=Role.guest)
        allowed_roles = []
        role_access = RoleAccess(allowed_roles)

        with self.assertRaises(HTTPException) as context:
            await role_access(request=request, user=user)

        self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(context.exception.detail, "Forbidden operation")

    async def test_no_current_user_with_empty_allowed_roles(self):
        request = Request()
        user = None
        allowed_roles = []
        role_access = RoleAccess(allowed_roles)

        with self.assertRaises(HTTPException) as context:
            await role_access(request=request, user=user)

        self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(context.exception.detail, "Forbidden operation")


if __name__ == '__main__':
    unittest.main()
