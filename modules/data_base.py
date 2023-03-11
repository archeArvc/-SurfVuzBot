import aiosqlite

# проверка на существование в БД
async def check_data(user_id):
    async with aiosqlite.connect("main.db") as db:
        cursor = await db.execute(f"SELECT user_id FROM users")
        users_ids = await cursor.fetchall()
        print(users_ids)
        for user in users_ids:
            if user[0] == user_id:
                return "also_have"
            

#
async def upload_subject(user_id, subject):
    async with aiosqlite.connect("main.db") as db:
        cursor = await db.execute(f"SELECT subjects FROM users WHERE user_id = {user_id}")
        users_subject = await cursor.fetchone()
        return users_subject
        


async def insert_data(user_id, city, subjects):
    async with aiosqlite.connect("main.db") as db:
        await db.execute(f"DELETE FROM users WHERE user_id = {user_id}")
        await db.commit()
        datas = (user_id, city, subjects, 1, 1)
        print(datas)
        await db.execute(f"INSERT INTO users VALUES(?, ?, ?, ?, ?)", datas)
        await db.commit()
        return "ok"
        

async def get_data(user_id):
    async with aiosqlite.connect("main.db") as db:
        cursor = await db.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
        user_cursor = await cursor.fetchall()
        return(user_cursor[0])

async def edit_dops(user_id, dop):
    async with aiosqlite.connect("main.db") as db:
        try:
            await db.execute(f"UPDATE users SET dop = {dop} WHERE user_id = {user_id}")
            await db.commit()
            return "succes"
        except:
            return "not_exist"


async def update(user_id, city):
    async with aiosqlite.connect("main.db") as db:
        try:
            await db.execute(f"UPDATE users SET city = '{city}' WHERE user_id = {user_id}")
            await db.commit()
            return "succes"
        except:
            return "not_exist"
        
async def updata_math_profile(user_id, prf):
    async with aiosqlite.connect("main.db") as db:
        await db.execute(f"UPDATE users SET math_profile = {prf} WHERE user_id = {user_id}")
        await db.commit()
        print(prf)
        return "succes"


async def update_subjects():
    pass