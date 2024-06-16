from typing import List

from pydantic.v1 import BaseModel, Field


class Requirements(BaseModel):
    requirements: List[str] = Field("List of requirements")


class JsonOutput(BaseModel):
    json_output: str = Field("The json output of the workflow")


class N8TunnelOutput(BaseModel):
    tunnel_url: str = Field("The tunnel url of the n8n instance")
