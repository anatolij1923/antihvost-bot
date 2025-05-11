async def get_user_rating(self, user_id: int) -> int:
    """Получить рейтинг пользователя"""
    query = """
    SELECT COUNT(*) 
    FROM tasks 
    WHERE user_id = $1 
    AND status = 'Сдано' 
    AND subject IN ('Информатика', 'Программирование', 'Дискретная математика')
    """
    result = await self.pool.fetchval(query, user_id)
    return result or 0

async def get_user_rank(self, user_id: int) -> int:
    """Получить место пользователя в рейтинге"""
    query = """
    WITH user_ratings AS (
        SELECT 
            user_id,
            COUNT(*) as rating
        FROM tasks 
        WHERE status = 'Сдано' 
        AND subject IN ('Информатика', 'Программирование', 'Дискретная математика')
        GROUP BY user_id
    )
    SELECT COUNT(*) + 1
    FROM user_ratings
    WHERE rating > (
        SELECT rating 
        FROM user_ratings 
        WHERE user_id = $1
    )
    """
    result = await self.pool.fetchval(query, user_id)
    return result or 1

async def get_total_users(self) -> int:
    """Получить общее количество пользователей"""
    query = "SELECT COUNT(DISTINCT user_id) FROM tasks"
    return await self.pool.fetchval(query) or 0

async def get_top_students(self, limit: int = 5):
    """Получить топ студентов"""
    query = """
    WITH user_ratings AS (
        SELECT 
            t.user_id,
            u.name,
            COUNT(*) as rating
        FROM tasks t
        JOIN users u ON t.user_id = u.user_id
        WHERE t.status = 'Сдано' 
        AND t.subject IN ('Информатика', 'Программирование', 'Дискретная математика')
        GROUP BY t.user_id, u.name
    )
    SELECT name, rating
    FROM user_ratings
    ORDER BY rating DESC
    LIMIT $1
    """
    return await self.pool.fetch(query, limit) 