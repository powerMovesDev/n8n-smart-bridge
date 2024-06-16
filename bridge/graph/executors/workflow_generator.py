import functools

from colorama import Fore, Style
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.prompt_values import PromptValue
from langchain_core.runnables import RunnableLambda

from bridge.graph.models.evaluation_models import CorrectionsEval
from bridge.graph.models.output_models import JsonOutput
from bridge.graph.prompts.workflow_generation_agent_prompts import WORKFLOW_GENERATION_AGENT_PROMPTS
from bridge.util.GptModels import GptModels


def run_with_errors(prompt_input: list | PromptValue, agent):
    messages = (
        prompt_input if isinstance(prompt_input, list) else prompt_input.as_messages()
    )
    for _ in range(3):
        res = agent.invoke(messages)
        if res["parsed"]:
            return res["parsed"]
        messages.extend(
            [
                res["raw"],
                ToolMessage(
                    content=f'Respond by calling the function correctly. Exceptions found:\n\n{res["parsing_error"]}',
                    tool_call_id=res["raw"].tool_calls[0]["id"],
                ),
            ]
        )
    raise ValueError("Failed to extract")


def generate_n8n_workflow(state, agent, eval_msg=None, attempts=0):
    workflow_requirements = state['requirements']
    print(
        f"{Fore.CYAN}Generating n8n workflow based on the following requirements - Attempt #{attempts}:\n"
        f"{workflow_requirements}{Style.RESET_ALL}")
    system_msg = SystemMessage(WORKFLOW_GENERATION_AGENT_PROMPTS)
    messages = [system_msg,
                HumanMessage(f"""
                Use the following workflow requirements and information to generate the n8n workflow json payload:
                
                Requirements & Workflow Information:
                {workflow_requirements}
                """)]
    if eval_msg:
        messages = eval_msg
    print(f"{Fore.GREEN}Messages:\n{messages}{Style.RESET_ALL}")
    if state['publish_result']:
        messages = state['messages']
        print(f"{Fore.RED}N8N Workflow Gen Agent - Correcting ERROR: {state['publish_result']}{Style.RESET_ALL}")
        messages += [HumanMessage(f"Correct the workflow to fix the following error:\n{state['publish_result']}")]

    resilient_agent = RunnableLambda(
        functools.partial(run_with_errors, agent=agent.with_structured_output(JsonOutput, include_raw=True)))
    workflow_generation = resilient_agent.invoke(messages)
    messages += [AIMessage(f"{workflow_generation.json_output}")]
    print(f"{Fore.GREEN}==== Generated Workflow ====:\n{workflow_generation.json_output}{Style.RESET_ALL}")
    if attempts <= 3 and state['publish_result'] is None:
        resilient_evaluator = RunnableLambda(functools.partial(run_with_errors,
                                                               agent=GptModels().claude_3.with_structured_output(CorrectionsEval, include_raw=True)))
        requirements_eval = (resilient_evaluator.invoke([
            SystemMessage(f"""
            Evaluate the generated n8n workflow json payload for correctness and report any issues that need to be
            corrected in order for the workflow to be functional. Also ensure that the requirements for the workflow
            have been met. 
            If corrections are needed provide a clear and concise explanation of the corrections needed and what to
            do specifically to correct them.
            """),
            HumanMessage(f"""
            The generated n8n workflow json payload:\n{workflow_generation.json_output}
            
            Requirements & Workflow Information:\n
            {workflow_requirements}""")]))
        print(f"{Fore.RED}Evaluation Results:\n{requirements_eval}{Style.RESET_ALL}")
        if requirements_eval.has_corrections:
            eval_msgs = messages + [HumanMessage(f"{',\n'.join(requirements_eval.corrections)}")]
            return generate_n8n_workflow(state, agent, eval_msgs, attempts + 1)

    return {"generated_workflow": workflow_generation.json_output, "messages": messages, "publish_result": None,
            "is_successfulLy_published": False}


if __name__ == "__main__":
    state = {
        "requirements": ['Webflow API Key: AIzaSyDhM-2XN4R4vRv5aJvX-3mU7MbHJZ5Jvhk',
                         'Webflow Site ID: 1a2b3c4d5e6f7g8h9i0j',
                         'Webflow Collection ID: 0j9i8h7g6f5e4d3c2b1a',
                         'Blog Post Fields: Title, Content, Author, and Publication Date',
                         'Blog Content Source: Provided via a text file',
                         'Trigger: On-demand',
                         'Error Handling and Notifications: Required for both success and failure of the blog post']
    }
    agent = GptModels().gpt_4_omni
    workflow = generate_n8n_workflow(state, agent)
    print(f"Generated n8n Workflow:\n{workflow}")
