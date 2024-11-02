from fastapi import HTTPException, status


class NewsException(HTTPException):
    def __init__(self, code: int, message: str):
        super().__init__(status_code=code, detail={"code": code, "message": message})

    def __str__(self) -> str:
        return f"{self.status_code}--{self.detail}"


class InvalidCredentialsException(NewsException):
    def __init__(self):
        super().__init__(code=40001, message="令牌认证出错")


class EmailAlreadyExistsException(NewsException):
    def __init__(self):
        super().__init__(code=40002, message="邮箱已经存在")


class UserAlreadyExistsException(NewsException):
    def __init__(self):
        super().__init__(code=40009, message="用户已存在")


class NewsNotFoundException(NewsException):
    def __init__(self):
        super().__init__(code=40004, message="新闻没找到")


class CategoryNotFoundException(NewsException):
    def __init__(self):
        super().__init__(code=40005, message="分类没找到")


class TagNotFoundException(NewsException):
    def __init__(self):
        super().__init__(code=40006, message="标签没找到")


class CommentNotFoundException(NewsException):
    def __init__(self):
        super().__init__(code=40007, message="评论没找到")


class InactiveUserException(NewsException):
    def __init__(self):
        super().__init__(code=40003, message="不活跃用户")


class UnauthorizedException(NewsException):
    def __init__(self):
        super().__init__(code=40101, message="无法验证凭证或凭证已过期")


class ForbiddenException(NewsException):
    def __init__(self):
        super().__init__(code=40301, message="没有足够权限")


class InvalidStatusTransitionException(NewsException):
    def __init__(self):
        super().__init__(code=40008, message="无效状态转换")


class UserNotFoundException(NewsException):
    def __init__(self):
        super().__init__(code=40009, message="用户没找到")


class DuplicateUsernameException(NewsException):
    def __init__(self):
        super().__init__(code=40011, message="用户名已存在")


class TokenExpiredException(NewsException):
    def __init__(self):
        super().__init__(code=40012, message="令牌过期")


class InvalidTokenException(NewsException):
    def __init__(self):
        super().__init__(code=40013, message="令牌验证异常")
