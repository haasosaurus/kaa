# coding=utf-8


import os

# import discord
from discord.ext import commands
from googleapiclient import discovery


class ResourceCog(commands.Cog, name='Resource Commands'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='save_resource', help='!save_resource CATEGORY URL')
    async def save_resource(self, ctx, category: str = None, link: str = None):
        """save link to resources"""

        if not link:
            await ctx.send(
                'Link and/or Category Missing - Link not saved' +
                '`' * 3 + 'Usage: !save_resource CATEGORY URL' + '`' * 3
                )
        else:
            # need to check that the resource isn't already there?
            category = category.lower()
            service = discovery.build(
                'sheets',
                'v4',
                credentials=None
            )
            spreadsheet_id = os.getenv('SPREADSHEET_ID')
            request = service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range='A2:C',
                majorDimension='ROWS'
            )
            response = request.execute()

            # get last row of google sheet to prevent overwriting
            lastrow = len(response['values'])
            new_values = [[link, category, str(ctx.author)]]
            new_body = {'values' : new_values}
            new_range = 'A' + str(lastrow + 2) + ':C'
            update_request = service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=new_range,
                valueInputOption='RAW',
                body=new_body
            )

            # new_response = update_request.execute()
            update_request.execute()
            await ctx.send('Link successfully saved to ' + category + '!')


def setup(bot):
    bot.add_cog(ResourceCog(bot))
