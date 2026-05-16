from sqlalchemy.ext.asyncio import AsyncSession

class AsyncUnitOfWork:
    """
    Implements the Unit of Work pattern to manage atomic database transactions (NFR-R1).
    """
    def __init__(self, session: AsyncSession):
        self.session = session
        self._committed = False

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.session.rollback()
        elif not self._committed:
            await self.session.commit()
            
    async def commit(self):
        await self.session.commit()
        self._committed = True
        
    async def rollback(self):
        await self.session.rollback()
