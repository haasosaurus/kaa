import discord
from discord.ext import commands
from googleapiclient import discovery
import os


class UtilitiesCog(commands.Cog, name="Utilities Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='save', aliases=['PythonBot'])
    async def save_link(self, ctx, category: str, link: str):
        """save link"""
        if not category:
            await ctx.send('Category Missing - Link not saved')
        elif not link: 
            await ctx.send('Link Missing - Link not saved')
        credentials = None
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/path/to/file.json"
        service = discovery.build('sheets', 'v4', credentials=credentials)
        # ID of spreadsheet
        spreadsheet_id = '1uX64HjNS9QTvyfgOmz7rJ26azw4wVcaQ_a6ZBUQmZ_c'
        range_ = 'A2:C'
        # get last row of google sheet to prevent overwriting
        request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_, majorDimension='ROWS')
        response = request.execute()
        
        value_input_option = 'RAW'
        lastrow = len(response['values'])
        new_values = [[link, category, str(ctx.author)]]
        new_body = {'values' : new_values}
        new_range = 'A' + str(lastrow + 2) + ':C'
        update_request = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=new_range, valueInputOption=value_input_option, body=new_body)
        new_response = update_request.execute()
        
        await ctx.send('Link successfully saved!')


def setup(bot):
    bot.add_cog(UtilitiesCog(bot))
