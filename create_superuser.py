import asyncio
import sys
import getpass
from sqlmodel import select
from lazy_crawler.api.database.db import engine, get_session
from lazy_crawler.api.database.models import User
from lazy_crawler.api.auth import get_password_hash

async def create_superuser(email: str, full_name: str, password: str):
    async_session_gen = get_session()
    session = await anext(async_session_gen)
    
    try:
        # Check if user already exists
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        existing_user = result.first()
        
        if existing_user:
            print(f"User with email {email} already exists. Updating to superuser...")
            existing_user.is_superuser = True
            existing_user.is_active = True
            if password:
                existing_user.hashed_password = get_password_hash(password)
            session.add(existing_user)
        else:
            print(f"Creating new superuser {email}...")
            new_user = User(
                email=email,
                full_name=full_name,
                hashed_password=get_password_hash(password),
                is_superuser=True,
                is_active=True,
                provider="email"
            )
            session.add(new_user)
            
        await session.commit()
        print(f"Successfully created/updated superuser: {email}")
        
    except Exception as e:
        await session.rollback()
        print(f"Error creating superuser: {e}")
    finally:
        await session.close()

if __name__ == "__main__":
    email = input("Enter email: ")
    full_name = input("Enter full name: ")
    password = getpass.getpass("Enter password: ")
    confirm_password = getpass.getpass("Confirm password: ")
    
    if password != confirm_password:
        print("Passwords do not match!")
        sys.exit(1)
        
    asyncio.run(create_superuser(email, full_name, password))
