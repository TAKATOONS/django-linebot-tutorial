from django.shortcuts import render
from django.views.generic.base import View
from django.http.response import HttpResponse,HttpResponseBadRequest,HttpResponseServerError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import pya3rt

line_bot_api = LineBotApi(settings.CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.CHANNEL_SECRET)
talk_api = settings.TALK_API

class CallbackView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('OK')

    def post(self, request, *args, **kwargs):
        #リクエストヘッダから署名検証のための値を取得
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        #リクエストボディを取得
        body = request.body.decode('utf-8')
        
        try:
            handler.handle(body,signature)
        except InvalidSignatureError:   #署名検証失敗
            return HttpResponseBadRequest()
        except LineBotApiError:     #APIエラー
            return HttpResponseServerError()
        
        return HttpResponse('OK')
    
    #外部からのアクセスを可能にする
    #(csrf_tokenを渡していないpostメソッドは403エラーになるため)
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CallbackView, self).dispatch(*args, **kwargs)
    
    #staticmethodはインスタンス化せずに呼び出せる関数のこと
    #handlerのaddメソッドで、リクエストのイベント毎に実行する関数を記述
    @staticmethod
    @handler.add(MessageEvent, message=TextMessage)
    def message_event(event):

        reply = event.message.text
        
        #AI
        #client = pya3rt.TalkClient(talk_api)
        #response = client.talk(event.message.text)
        #reply = response['results'][0]['reply']
        
        if reply=='ただいま':
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="おかえりなさい！今日もお疲れ様です！")
            )

        elif reply=='おかえり':
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="おかえりなさい！今日もお疲れ様です！")
            )

        #メッセージ送信部分
        #line_bot_api.reply_message(
        #    event.reply_token,
        #    TextSendMessage(text=reply)
        #)