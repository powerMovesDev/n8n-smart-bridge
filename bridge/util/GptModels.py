import os
from enum import Enum

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI


class Model(Enum):
    GPT4 = 'gpt-4'
    GPT4_TURBO = 'gpt-4-1106-preview'
    GPT4_TURBO_2024 = 'gpt-4-turbo-2024-04-09'
    GPT4_32K = 'gpt-4-32k'
    GPT4_VISION = 'gpt-4-vision-preview'
    GPT4_OMNI = 'gpt-4o-2024-05-13'


class GptModels:

    def __init__(self):
        load_dotenv()
        self.langsmith_project = os.getenv("LANGCHAIN_PROJECT")
        self._gpt_4_vision = None
        self._gpt_4_turbo = None
        self._gpt_4 = None
        self._gpt_4_omni = None
        self._azure_llm = None
        self._claude_3 = None
        self._gemini_pro = None

    @property
    def gpt_4_vision(self):
        if self._gpt_4_vision is None:
            self._gpt_4_vision = ChatOpenAI(model=Model.GPT4_VISION.value, temperature=0)
        return self._gpt_4_vision

    @property
    def gpt_4_turbo(self):
        if self._gpt_4_turbo is None:
            self._gpt_4_turbo = ChatOpenAI(model=Model.GPT4_TURBO.value, max_tokens=4096, temperature=0)
        return self._gpt_4_turbo

    @property
    def gpt_4_turbo_2024(self):
        if self._gpt_4_turbo is None:
            self._gpt_4_turbo = ChatOpenAI(model=Model.GPT4_TURBO_2024.value, max_tokens=4096, temperature=0)
        return self._gpt_4_turbo

    @property
    def gpt_4(self):
        if self._gpt_4 is None:
            self._gpt_4 = ChatOpenAI(model=Model.GPT4.value, max_tokens=4096, temperature=0)
        return self._gpt_4

    @property
    def gpt_4_omni(self):
        if self._gpt_4_omni is None:
            self._gpt_4_omni = ChatOpenAI(model=Model.GPT4_OMNI.value, temperature=0)
        return self._gpt_4_omni

    @property
    def claude_3(self) -> BaseChatModel:
        if self._claude_3 is None:
            self._claude_3 = ChatAnthropic(model='claude-3-opus-20240229', max_tokens=4096, temperature=0)
        return self._claude_3
