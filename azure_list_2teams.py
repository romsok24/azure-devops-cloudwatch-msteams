import os, argparse
from azure.cli.core import get_default_cli
import pymsteams, string
from datetime import datetime

app_ver = '21.0915'

def az_cli (args_str):
    args = args_str.split()
    cli = get_default_cli()
    cli.invoke(args)
    if cli.result.result:
        return cli.result.result
    elif cli.result.error:
        raise cli.result.error
    return True

def dbg_HTMLdump(txt_towrite):

    f=open("dbg.html","w")
    f.write(txt_towrite.replace("<table>","<table border=1>"))
    f.close()
    print(f'\n [ DEBUG MODE ] html file prepared\n')

ap = argparse.ArgumentParser()
ap.add_argument("--azure_subs", nargs='+', required=True)
ap.add_argument("--teams_webhook", required=True)
arg = ap.parse_args()

for azure_sub in arg.azure_subs:
    teamstxt="<table>"
    myTeamsMessage = pymsteams.connectorcard(arg.teams_webhook)
    myTeamsMessage.title("This is automatic "+datetime.today().strftime('%A')+"'s Azure tags report")
    teamstxt=teamstxt+"<tr><td colspan=2><h2>"+azure_sub+" subscription</h2></td></tr><tr><td>"
    response = az_cli("group list --subscription "+azure_sub+" --query [].[name,tags] --output table")

    for responseln in response:
        teamstxt=teamstxt+'</td><td>'.join(str(e) for e in responseln)+"</tr><tr><td>"

    teamstxt=' '.join(teamstxt.rsplit('<tr><td>', 1))
    chars_2remove = "{'}"
    for char_2remove in chars_2remove:
        teamstxt=teamstxt.replace(char_2remove,"")

    teamstxt=teamstxt+"<tr><td colspan=2 style=\"text-align:right\"><font size=1>App ver: "+app_ver +"</font></td></tr>"

    myTeamsMessage.text(teamstxt)
    myTeamsMessage.send()
    # myTeamsMessage.printme()
    # dbg_HTMLdump(teamstxt)
    teamstxt=""
