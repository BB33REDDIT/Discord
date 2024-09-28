import discord
from discord.ext import commands
import requests

class CatGifCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cat(self, ctx):
        api_key = 'AIzaSyB4gNHq8OR1TFKcUxzo0Qg1GHmSw8zt94s'
        url = f"https://api.tenor.com/v1/random?key={api_key}&tag=cat&limit=1"

        try:
            response = requests.get(url)
            print(f"Response Status Code: {response.status_code}")  # Debug print
            print(f"Response Text: {response.text}")  # Debug print
            
            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()
                if data['results']:
                    gif_url = data['results'][0]['media'][0]['gif']['url']
                    await ctx.send(gif_url)
                else:
                    await ctx.send("No cat GIFs found!")
            else:
                await ctx.send("Error fetching GIFs. Please try again later.")
        except Exception as e:
            await ctx.send("An error occurred while fetching the cat GIF.")
            print(f"Error: {e}")  # Debug print for the error

def setup(bot):
    bot.add_cog(CatGifCommand(bot))
