import json




def publish_new_workflow(state):
    workflow = state['generated_workflow']
    publish_result, status_code = post_workflow_request(json.loads(workflow))
    is_successful = True if status_code == 200 or status_code == 201 else False
    return {"publish_result": publish_result, "is_successfulLy_published": is_successful}
