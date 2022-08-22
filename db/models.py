from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    posts = relationship('Post', back_populates='user')
    comments = relationship('Comment', back_populates='user')

    def __str__(self):
        return f'<User: username={self.username}>'


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')

    def __str__(self):
        return f'<Post: title={self.title}>'


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    post_id = Column(ForeignKey('posts.id', ondelete='CASCADE'))
    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'))
    post = relationship('Post', back_populates='comments')
    user = relationship('User', back_populates='comments')

    def __str__(self):
        return f'<Comment: post={self.post.title} user={self.user.username}>'
