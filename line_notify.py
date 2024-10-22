import requests

def send_line_notify(notification_message):
      line_notify_token = 'kiBU9eCYMY0GYY7h2MkcGSK8mp2JnwTyd5zGrPUQTCY'  # アクセストークンをここに入力
      line_notify_api = 'https://notify-api.line.me/api/notify'
      headers = {'Authorization': f'Bearer {line_notify_token}'}
      data = {'message': notification_message}
      response = requests.post(line_notify_api, headers=headers, data=data)
      return response.status_code, response.text