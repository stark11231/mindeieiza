import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
from keyauth import api
from myserver import server_on
# ตั้งค่าบอท
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# การตั้งค่า KeyAuth
keyauthapp = api(
    name="x48",  # Application Name
    ownerid="lbncSD9Lex",  # Owner ID
    secret="87858cc70128b2c9fd0ab40cd6b94aa56a3439d27cda5de2fecda14b68cc2a86",  # Application Secret
    version="1.0",
    hash_to_check=None  # ลองส่ง None แทน
)


ROLE_ID = 1310275659213443092  # ใส่ Role ID ที่ต้องการ

@bot.event
async def on_ready():
    print(f'ล็อกอินในชื่อ {bot.user} เรียบร้อยแล้ว')

# สร้าง Modal เพื่อให้กรอก License Key
class RedeemLicenseModal(Modal):
    def __init__(self):
        super().__init__(title="กรอก License Key ของคุณ")
        self.license_key = TextInput(
            label="License Key", 
            placeholder="กรอกคีย์ของคุณที่นี่",
            required=True
        )
        self.add_item(self.license_key)

    async def on_submit(self, interaction: discord.Interaction):
        key = self.license_key.value
        
        # ตรวจสอบคีย์กับ KeyAuth API
        result = keyauthapp.license(key)
        
        # อัปเดตการจัดการเมื่อคีย์ถูกต้อง
        role = interaction.guild.get_role(ROLE_ID)
        if role is not None:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"คีย์ได้รับการยอมรับ! คุณได้รับยศ '{role.name}' แล้ว.", ephemeral=True)
        else:
            await interaction.response.send_message(f"ไม่พบยศที่มี ID '{ROLE_ID}'", ephemeral=True)

# สร้างปุ่มและ embed เพื่อแสดง Modal
@bot.command()
async def redeem(ctx, image_url=None):
    # ตรวจสอบว่าผู้ใช้ส่งลิงก์รูปภาพมาหรือไม่
    if image_url is None:
        image_url = "https://img2.pic.in.th/pic/FREE_TP01_BY-FUNNY679fc58758bf38a7.png"  # ลิงก์รูปภาพเริ่มต้น

    embed = discord.Embed(
        title="Redeem Key เพื่อรับยศ และ ดาวน์โหลด",
        description="โปรดคลิกปุ่มด้านล่างเพื่อกรอกคีย์และรับยศในเซิร์ฟเวอร์",
        color=discord.Color.from_rgb(255, 165, 0)  # สีม่วง
    )

    # ใส่รูปภาพใน embed
    embed.set_image(url=image_url)

    # สร้างปุ่ม Redeem License
    button = Button(label="Redeem License", style=discord.ButtonStyle.green)

    # เมื่อคลิกปุ่ม Redeem License จะเปิด Modal
    async def button_callback(interaction):
        modal = RedeemLicenseModal()
        await interaction.response.send_modal(modal)

    # ผูก callback กับปุ่ม
    button.callback = button_callback

    # สร้าง View เพื่อใช้กับปุ่ม
    view = View()
    view.add_item(button)

    # ส่ง embed และปุ่มไปที่ช่อง
    await ctx.send(embed=embed, view=view)

server_on()

bot.run(os.getenv('TOKEN'))
