
import discord
from discord.ext import commands
from discord import app_commands
import os

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
CARGO_ID = int(os.getenv("CARGO_ID"))

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Sócrates está online como {{bot.user}}")
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"🌐 Comandos sincronizados: {{len(synced)}}")
    except Exception as e:
        print(f"❌ Erro ao sincronizar comandos: {{e}}")

@bot.tree.command(name="verifique", description="Envia o botão de verificação", guild=discord.Object(id=GUILD_ID))
async def verifique(interaction: discord.Interaction):
    view = Verificacao()
    embed = discord.Embed(
        title="📥 Iniciação Filosófica",
        description=f"Antes de adentrar o Tribunal, leia o [📜 código-da-razão](https://discord.com/channels/{{GUILD_ID}}/1129812519461081188).\n\nApós ler, clique no botão abaixo para se tornar <@&{{CARGO_ID}}>.",
        color=0x6A5ACD
    )
    await interaction.response.send_message(embed=embed, view=view)

class Verificacao(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="✅ Li e aceito o Código da Razão", style=discord.ButtonStyle.success)
    async def aceitar(self, interaction: discord.Interaction, button: discord.ui.Button):
        cargo = interaction.guild.get_role(CARGO_ID)
        if cargo in interaction.user.roles:
            await interaction.response.send_message("Você já é um Discípulo da Razão.", ephemeral=True)
        else:
            await interaction.user.add_roles(cargo)
            await interaction.response.send_message("Bem-vindo ao Tribunal. Que a razão te acompanhe.", ephemeral=True)

bot.run(TOKEN)
