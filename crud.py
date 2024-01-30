import asyncio
from core.models import db_helper, User, Profile, Post, Order, Product
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import joinedload, selectinload


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print(f"user {user}")
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    result: Result = await session.execute(stmt)
    user: User | None = result.scalar_one_or_none()
    print(f"found user {username}, {user}")
    return user


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
) -> Profile:
    profile = Profile(user_id=user_id, first_name=first_name, last_name=last_name)

    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profile(session: AsyncSession) -> list[User]:
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    # result: Result = await session.execute(stmt)
    users = await session.scalars(stmt)
    for user in users:
        print(user)
        print(user.profile.first_name)


async def create_posts(
    session: AsyncSession, user_id: int, *posts_titles: str
) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in posts_titles]

    session.add_all(posts)
    await session.commit()
    print(posts)
    return posts
    


async def get_users_with_posts(
    session: AsyncSession
):
    stmt = select(User).options(joinedload(User.posts)).order_by(User.id)
    users = await session.scalars(stmt)
    
    for user in users.unique():
        print('**')
        print(user)
        for post in user.posts:
            print(post)
    ...
    
    
async def get_posts_with_authors(session:AsyncSession):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)
    
    for post in posts:
        print('-',post)
        print('+',post.user.username)
        
        
        
async def get_users_with_posts_and_profiles(
    session: AsyncSession
):
    stmt = select(User).options(joinedload(User.profile),selectinload(User.posts)).order_by(User.id)
    users = await session.scalars(stmt)
    
    for user in users.unique():
        print('**')
        print(user)
        print(user.profile.first_name)
        
        for post in user.posts:
            print(post)
    ...
        
        
async def get_profiles_with_users_and_users_with_posts(session:AsyncSession):
    stmt = (
        select(Profile)
        .join(Profile.user)
        .options(
            joinedload(Profile.user).selectinload(User.posts)
        )
        .where(User.username == 'john')
        .order_by(Profile.id)   
    )
    
    
    profiles = await session.scalars(stmt)
    
    
    for profile in profiles:
        print(profile.first_name , profile.user)
        print( profile.user.posts)
        
    ...
    
    
    
async def main_relations(session:AsyncSession):
    # await create_user(session=session,username='john')
    # await create_user(session=session,username='sam')

    # user_sam = await get_user_by_username(session=session, username="sam")
    # user_john = await get_user_by_username(session=session, username="john")
    # await create_user_profile(
    #     session=session, user_id=user_john.id, first_name="John"
    # )

    # await create_user_profile(
    #     session=session, user_id=user_sam.id, first_name="Sam",last_name='White'
    # )
    # await show_users_with_profile(session=session)
    
    # await create_posts(
    #     session,
    #     user_john.id,
    #     'SQLa 2.0','SQLa join'
    # )
    
    # await create_posts(
    #     session,
    #     user_sam.id,
    #     'FastAPI intro','FastAPI advanced','FastApi more'
    # )
    
    
    # await get_users_with_posts(session=session)
    
    # await get_posts_with_authors(session=session)
    
    await get_profiles_with_users_and_users_with_posts(session=session)
    ...
    
    
    
    
   
async def create_order(session:AsyncSession, promocode:str |None = None) -> Order:
    order  = Order(promocode=promocode)
    
    session.add(order)
    await session.commit()
    return order
    
    
async def create_product(session:AsyncSession, name:str ,description:str,price:int) -> Product:
    product = Product(name=name,description=description,price=price)   
    session.add(product)
    await session.commit()
    return product
    
    
    
async def  demo_m2m(session:AsyncSession):
    order_one = await create_order(session)
    order_promo = await create_order(session, promocode='promo')
    
    mouse = await create_product(session,'mouse','greate gaming mouse',123)
    keyboard = await create_product(session,'keyboard','awesome keyboard',222)
    display = await create_product(session,'display','office display',300)
    
    
    
    order_one =await session.get(
        Order,order_one.id,
        options=(selectinload(Order.products))
    )
    
     
    order_promo =await session.get(
        Order,order_one.id,
        options=(selectinload(Order.products))
    )
    
    
    order_one.products.append(mouse)
    order_one.products.append(keyboard)
    
    
    order_promo.products.append(keyboard)
    order_one.products.append(display)
    
    
    
    pass
    
    

async def main():
    async with db_helper.session_factory() as session:
        await demo_m2m(session)
        
        ...
       


if __name__ == "__main__":
    asyncio.run(main())
