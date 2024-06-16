import functools
from typing import Callable

from langgraph.constants import END
from langgraph.graph import StateGraph

from bridge.graph.executors.requirements_manager import collect_requirements_from_user
from bridge.graph.executors.workflow_generator import generate_n8n_workflow
from bridge.graph.executors.workflow_publisher import publish_new_workflow
from bridge.graph.router.router import publish_router
from bridge.graph.state.graph_state import N8State
from bridge.util.GptModels import GptModels


def start_workflow(user_callback: Callable):
    agent = GptModels().gpt_4_omni

    workflow = StateGraph(N8State)

    requirements_collection_node = functools.partial(collect_requirements_from_user, agent=agent,
                                                     user_callback=user_callback)
    workflow_generation_node = functools.partial(generate_n8n_workflow, agent=agent)

    workflow.add_node("Collect Requirements", requirements_collection_node)
    workflow.add_node("Generate n8n Workflow", workflow_generation_node)
    workflow.add_node("Publish n8n Workflow", publish_new_workflow)

    workflow.add_edge("Collect Requirements", "Generate n8n Workflow")
    workflow.add_edge("Generate n8n Workflow", "Publish n8n Workflow")
    workflow.add_conditional_edges("Publish n8n Workflow", publish_router, {
        "NEED_REVISION": "Generate n8n Workflow",
        "SUCCESS": END
    })

    workflow.set_entry_point("Collect Requirements")

    graph = workflow.compile()
    output = graph.invoke({"messages": []})
    return output


if __name__ == "__main__":
    def user_callback(question):
        print(question)
        return input("")


    result = start_workflow(user_callback)
    print(result)
