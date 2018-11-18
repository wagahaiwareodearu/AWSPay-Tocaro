import subprocess
import requests
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

# 日付取得
today = datetime.today()
srt = today.replace(day=1)
end = (today + relativedelta(months=1)).replace(day=1) - timedelta(days=1)

# AWSコマンド設定
def price(start, end):
    aws_main = "/usr/local/bin/aws "
    aws_opt = "ce get-cost-and-usage "
    aws_period = "--time-period "
    aws_srt = ("Start=" + datetime.strftime(start, '%Y-%m-%d') + ",")
    aws_end = ("End=" + datetime.strftime(end, '%Y-%m-%d') + " ")
    aws_granularity = "--granularity MONTHLY "
    aws_metrics = "--metrics BlendedCost "
    aws_group = "--group-by Type=DIMENSION,Key=SERVICE "
    aws_pipe = "| "
    aws_jq = "jq -c '.ResultsByTime[].Groups[] | {(.Keys[]): .Metrics.BlendedCost.Amount}'"
    aws_cli = (aws_main + aws_opt + aws_period + aws_srt + aws_end + aws_granularity + aws_metrics + aws_group + aws_pipe + aws_jq)
    print (aws_cli)
    return aws_cli

# AWSコマンド発行
proc = subprocess.run(price(srt, end),stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell =True)

# Line通知
line_notify_token = ''
line_notify_api = 'https://notify-api.line.me/api/notify'
body = (proc.stdout.decode("utf8"))
payload = {'message': body}
headers = {'Authorization': 'Bearer ' + line_notify_token}
line_notify = requests.post(line_notify_api, data=payload, headers=headers)