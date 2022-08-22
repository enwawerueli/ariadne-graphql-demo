from ariadne import (
    QueryType,
    MutationType,
    ObjectType,
    load_schema_from_path,
    make_executable_schema
)
from ariadne.asgi import GraphQL
from ariadne.types import Extension, ContextValue
from sqlalchemy import select

from db import Session
from db.models import User, Post, Comment

# Load shema file
type_defs = load_schema_from_path('./schema.graphql')

types = (
    # Root query
    query_type := QueryType(),
    # Root mutation
    mutation_type := MutationType(),
    # User type
    user_type := ObjectType('User'),
    # Post type
    post_type := ObjectType('Post'),
    # Comment type
    comment_type := ObjectType('Comment')
)

post_type.set_alias('author', 'user')
comment_type.set_alias('author', 'user')


class DBSession(Extension):
    """Database session manager"""

    def request_started(self, context: ContextValue):
        context['session'] = Session()

    def request_finished(self, context: ContextValue):
        if (session := context.get('session')) is not None:
            session.close()


def assert_session(f):
    def _f(parent, info, **kwargs):
        assert info.context.get(
            'session') is not None, 'A database session is not available'
        return f(parent, info, **kwargs)
    return _f


@mutation_type.field('createUser')
@assert_session
def resolve_create_user(parent, info, **kwargs):
    session = info.context['session']
    user = User(**kwargs)
    session.add(user)
    session.commit()
    return user


@query_type.field('users')
@assert_session
def resolve_users(parent, info, **kwargs):
    session = info.context['session']
    return session.execute(select(User)).scalars().all()


@query_type.field('user')
@assert_session
def resolve_user(parent, info, id, **kwargs):
    session = info.context['session']
    return session.execute(select(User).where(User.id == id)).scalar_one()


@mutation_type.field('createPost')
@assert_session
def resolve_create_post(parent, info, **kwargs):
    session = info.context['session']
    user = Post(**kwargs)
    session.add(user)
    session.commit()
    return user


@query_type.field('posts')
@assert_session
def resolve_posts(parent, info, **kwargs):
    session = info.context['session']
    return session.execute(select(Post)).scalars().all()


@query_type.field('post')
@assert_session
def resolve_post(parent, info, id, **kwargs):
    session = info.context['session']
    return session.execute(select(Post).where(Post.id == id)).scalar_one()


@mutation_type.field('createComment')
@assert_session
def resolve_create_comment(parent, info, **kwargs):
    session = info.context['session']
    user = Comment(**kwargs)
    session.add(user)
    session.commit()
    return user


@query_type.field('comments')
@assert_session
def resolve_comments(parent, info, **kwargs):
    session = info.context['session']
    return session.execute(select(Comment)).scalars().all()


@query_type.field('comment')
@assert_session
def resolve_comment(parent, info, id, **kwargs):
    session = info.context['session']
    return session.execute(select(Comment).where(Comment.id == id)).scalar_one()


schema = make_executable_schema(
    type_defs, *types, convert_kwargs_to_snake_case=True)
app = GraphQL(schema, extensions=(DBSession,))
