from typing import Callable

from colorama import Fore, Style
from langchain_core.messages import SystemMessage, HumanMessage

from bridge.graph.models.evaluation_models import RequirementsEval
from bridge.graph.models.output_models import Requirements
from bridge.graph.prompts.requirements_agent_prompts import REQ_AGENT_SYSTEM_PROMPT
from bridge.util.GptModels import GptModels


def collect_requirements_from_user(state, agent, user_callback: Callable, conversation_history=None):
    system_msg = SystemMessage(REQ_AGENT_SYSTEM_PROMPT)
    messages = [system_msg,
                HumanMessage(f"""
                Ask the user about what kind of workflow they want to create with the n8n workflow. Start with a single 
                simple question focused on the task the user wants to automate with n8n. It should be a single sentence.
                """)]
    if conversation_history:
        messages = conversation_history

    question = agent.invoke(messages)
    user_response = user_callback(question.content)

    requirements_eval = (GptModels().
                         gpt_4_omni.
                         with_structured_output(RequirementsEval).
                         invoke([SystemMessage(f"""Evaluate the provided conversation to determine if the user
                         has indicated that they are finished providing requirements for the n8n workflow.
                         
                         Important: The user is only complete once they explicitly indicate that they are finished
                         providing requirements. 
                         
                         
                            AI:
                            {question.content}
                            
                            User:
                            {user_response}
                         """)]))
    if not requirements_eval.is_complete:
        print(f"{Fore.RED} User has not completed providing requirements. {Style.RESET_ALL}")
        messages.append(HumanMessage(f"""
        The following is the user response: {user_response}
                                     
         Evaluate the response and ask any clarifying questions if needed. If there is 
         additional information that the user will need to provide to achieve what they 
         described include requests for the needed information such as API authentication 
         tokens, emails, etc.
                                     
        If you have no further questions, ask the user if they have any additional requirements or if they are finished.
                                     
                                     """))
        return collect_requirements_from_user(state, agent, user_callback, messages)

    else:
        print(f"{Fore.GREEN} User has completed providing requirements. {Style.RESET_ALL}")
        final_requirements = HumanMessage(f"""
            The following was provided by the user: {user_response}
        """)

    messages += [question,
                 final_requirements,
                 HumanMessage(f""" The user has completed providing the requirements for the n8n workflow. Based on 
                 this conversation create a list of requirements that the developer will need to create the n8n 
                 workflow. The requirements should be paraphrased an easy to understand format of instructions for 
                 the developer to create the workflow """)
                 ]

    workflow_requirements = agent.with_structured_output(Requirements).invoke(messages)

    return {"requirements": workflow_requirements.requirements}


if __name__ == "__main__":
    def user_callback(question):
        print(question)
        return input("")


    state = {}
    agent = GptModels().gpt_4_omni

    workflow_requirements = collect_requirements_from_user(state, agent, user_callback)
    print(workflow_requirements)
