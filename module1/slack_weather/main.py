from slack_sdk.rtm_v2 import RTMClient
from slack_sdk import WebClient
from weather_info_parser import WeatherInfoParser
import os

rtm = RTMClient(token='xoxb-6555023466485-6557214157829-hqk9aapBWIdm61E3IpM58ybg')
web_client = WebClient(token='xoxb-6555023466485-6557214157829-hqk9aapBWIdm61E3IpM58ybg')
weather_info_parser = WeatherInfoParser()

def send_weather_info():
    weather_info = weather_info_parser.getWeatherInfo(keyword='창동 날씨')

    # slack 채널 ID 를 설정해주세요.
    channel_id = 'C06GG5PCT6W'

    rtm.web_client.chat_postMessage(
        channel=channel_id,
        blocks=[
            {'type':'divider'},
            {
                'type':'section',
                'text': {
                    'type':'plain_text',
                    'text':f'{weather_info.area}'
                }
            },
            {'type':'divider'},
            {
                'type':'section',
                'text': {
                    'type':'plain_text',
                    'text':f"""{weather_info.weather_today}
현재기온:{weather_info.temperature_now}
최고기온:{weather_info.temperature_high}
최저기온:{weather_info.temperature_low}
"""
                }
            },
        ],
    )

    weather_info_parser.getScreenshot(keyword='창동 날씨')

    web_client.files_upload_v2(
        channel=channel_id,
        file='info.png',
        title='날씨 정보',
    )

def main():
    send_weather_info()

if __name__ == '__main__':
    main()

# import requests
 
# def post_message(token, channel, text):
#     response = requests.post("https://slack.com/api/chat.postMessage",
#         headers={"Authorization": "Bearer "+token},
#         data={"channel": channel,"text": text}
#     )
#     print(response)