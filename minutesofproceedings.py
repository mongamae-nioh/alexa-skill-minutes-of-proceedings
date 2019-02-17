# coding: UTF-8
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk.standard import StandardSkillBuilder

sb = StandardSkillBuilder(table_name="TakingTheMinutes", auto_create_table=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 担当者タプル（担当者全員を記載）
pictaple = ('担当者1',
            '担当者2',
            '担当者3'
            )

# タプル要素数
lengthoftaple = len(pictaple)

class LaunchRequestHandler(AbstractRequestHandler):
     def can_handle(self, handler_input):
         return is_request_type("LaunchRequest")(handler_input)

     def handle(self, handler_input):
         speech_text = "前回、議事録を書いたかたのお名前を教えてください"

         handler_input.response_builder.speak(speech_text).ask(speech_text).set_should_end_session(False)
         return handler_input.response_builder.response

class DecidePICIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("DecidePICIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        lasttime_is = str(slots["name"].value)
        session_attr = handler_input.attributes_manager.session_attributes
        
        # 名前ゆれ吸収
        # 苗字あるいは下の名前でも呼ばれる人はどちらかへ統一する
        if lasttime_is == 'すずき' or lasttime_is == 'いちろう':
            lasttime_is = 'すずき'
        
        thistime_pic_number = int(pictaple.index(lasttime_is)) + 1

        # タプルの最後は最初へ戻る
        if thistime_pic_number == int(lengthoftaple):
            thistime_pic_number = 0
            
        thistime_is = pictaple[thistime_pic_number]

        session_attr['pic'] = thistime_is
        session_attr['pic_number'] = pictaple.index(thistime_is)

        speech_text = "今回は{}さんです。いらっしゃいますか？".format(thistime_is)

        handler_input.response_builder.speak(speech_text).ask(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response

class YesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes

        if session_attr['pic'] is None:
            speech_text = "前回、議事録を書いたかたのお名前を教えてください"

        speech_text = "{}さん、よろしくお願いします".format(session_attr['pic'])

        handler_input.response_builder.speak(speech_text).ask(speech_text).set_should_end_session(True)
        return handler_input.response_builder.response

class NoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.NoIntent")(handler_input)

    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes

        # 次の当番
        next_pic_number = int(session_attr['pic_number']) + 1

        # タプルの最後は最初へ戻る
        if next_pic_number == int(lengthoftaple):
            next_pic_number = 0
            session_attr['pic_number'] = 0
        else:
            session_attr['pic_number'] = next_pic_number
            
        thistime_is = pictaple[next_pic_number]
        session_attr['pic'] = thistime_is

        if session_attr['pic'] is None:
            speech_text = "前回、議事録を書いたかたのお名前を教えてください"

        speech_text = "次は{}さんです。いらっしゃいますか？".format(thistime_is)

        handler_input.response_builder.speak(speech_text).ask(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "議事録の当番をお知らせします。だれだれさんの次はだれ？というふうに聞いてみてください"

        handler_input.response_builder.speak(speech_text).ask(speech_text)
        return handler_input.response_builder.response

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "いつでも呼んでください"

        handler_input.response_builder.speak(speech_text).ask(speech_text)
        return handler_input.response_builder.response
        
class AllExceptionHandler(AbstractExceptionHandler):

    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):

        # Log the exception in CloudWatch Logs
        print(exception)

        speech = "すみません、わかりませんでした。もう一度言ってください。"
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(DecidePICIntentHandler())
sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(NoIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())

sb.add_exception_handler(AllExceptionHandler())

handler = sb.lambda_handler()
