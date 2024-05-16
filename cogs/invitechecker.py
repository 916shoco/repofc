import os
import aiosqlite
from discord.ext import commands, tasks
from discord import Status, Activity, ActivityType

invite_codes = ["discord.gg/rtmFSVNU9z", "gg/shadowsrealm"]
role_id = 1198347965828444257

DATABASE_PATH = f"{os.path.realpath(os.path.dirname(__file__))}/../database/members.db"

async def has_role(member, role_id):
    role = member.guild.get_role(role_id)
    return role in member.roles

class StatusChecker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        if self.bot.guilds:
            self.check_status.start()

    @tasks.loop(minutes=2)
    async def check_status(self):
        await self.bot.wait_until_ready()
        online_statuses = [Status.online, Status.idle, Status.do_not_disturb]
        try:
            db_path = DATABASE_PATH
            if not os.path.exists(DATABASE_PATH):
                return
            async with aiosqlite.connect(db_path) as conn:
                cursor = await conn.cursor()
                await cursor.execute('CREATE TABLE IF NOT EXISTS members (member_id INTEGER PRIMARY KEY)')
                await conn.commit()
                await cursor.execute('SELECT member_id FROM members')
                member_ids = [row[0] for row in await cursor.fetchall()]
                for guild in self.bot.guilds:  
                    for member in guild.members:
                        if member.status == Status.offline:
                            continue  # Skip this member if they are offline
                        if member.id in member_ids:
                            if not member.activity or member.activity.type != ActivityType.custom or not any(invite_code in member.activity.name.lower().split() for invite_code in invite_codes):
                                await cursor.execute('DELETE FROM members WHERE member_id = ?', (member.id,))
                                if await has_role(member, role_id):
                                    await member.remove_roles(member.guild.get_role(role_id))
                        elif member.activity and member.activity.type == ActivityType.custom and any(invite_code in member.activity.name.lower().split() for invite_code in invite_codes):
                            await cursor.execute('INSERT INTO members (member_id) VALUES (?)', (member.id,))
                            if not await has_role(member, role_id):
                                await member.add_roles(member.guild.get_role(role_id))
                await conn.commit()
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    @check_status.before_loop
    async def before_printer(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(StatusChecker(bot))
