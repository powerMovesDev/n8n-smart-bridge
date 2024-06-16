from colorama import Fore, Style

from bridge.graph.state.graph_state import N8State


def publish_router(state: N8State):
    print(f"{Fore.CYAN}Routing Publish Result\n{state['is_successfulLy_published']}{Style.RESET_ALL}")
    is_success = state['is_successfulLy_published']
    if is_success:
        return "SUCCESS"
    else:
        return "NEED_REVISION"
