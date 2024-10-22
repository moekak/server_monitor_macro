import requests, datetime
from line_notify import send_line_notify

def parse_txt_file(file_path):
      urls = {}
      with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                  # line.strip()は行の先頭と末尾の空白文字（スペース、タブ、改行など）を削除
                  # .split(None, 1)は行を最大2つの部分に分割
                  # Noneは、任意の空白文字で分割
                  # 1は、分割を1回だけ行うことを指定
                  parts = line.strip().split(None, 1)
                  if len(parts) == 2:
                        key, value = parts
                        urls[key] = value
      return urls

def check_api_health(url, name):
      print(url)
      retry_count = 3
      timeouts = [10, 10, 10]  # 各試行のタイムアウト秒数

      for i in range(retry_count):
            try:
                  response = requests.get(url, timeout=timeouts[i])
                  print(response)
            
            except requests.exceptions.HTTPError as errh:
                  send_line_notify(f"\nHTTPエラーが起こりました。 \n\n【エラー内容】{errh} \n\n【時刻】: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n【サーバー名】: {name} \n【URL】: {url}")
                  return
            except requests.exceptions.ConnectionError as errc:
                  send_line_notify(f"\n\nネットワーク接続エラーが起こりました。 \n\n【エラー内容】{errc} \n\n【時刻】: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n【サーバー名】: {name} \n【URL】: {url}")
                  return
            except requests.exceptions.Timeout as errt:
                  if i == 1:  # 2回目の接続失敗時
                        send_line_notify(f"\n\n警告: サイトへのアクセス試行から10秒経過しましたが、ページが完全にロードされていません。サーバーの応答が遅れている可能性があります。\n\n【時刻】: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n【サーバー名】: {name} \n【URL】: {url} ")
                  if i == 2:  # 3回目の接続失敗時
                        send_line_notify(f"\n\n異常: サーバー障害が発生してます。サイトにアクセスできません。\n\n【時刻】: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n【サーバー名】: {name} \n【URL】: {url} ")
                  continue
            except requests.exceptions.RequestException as err:
                  send_line_notify(f"\n\n予期しないエラーが起こりました。 \n\n【時刻】: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n【エラー内容】: {err} \n\n【サーバー名】: {name} \n【URL】: {url}")
                  return


# ヘルスチェックの実行
urls = parse_txt_file("./site_url.txt")
for key, value in urls.items():
      check_api_health(value, key)
