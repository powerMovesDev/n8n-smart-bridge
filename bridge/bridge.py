class N8NBridge:
    def __init__(self, **kwargs):
        self.tokens = kwargs

    def post_content(self, platform, content):
        # switch between platforms execute a different function
        if platform == 'discord':
            self._discord_post(content)
        elif platform == 'slack':
            self._slack_post(content)
        else:
            raise ValueError('Unsupported platform')

    def generate_workflow(self, prompt):
        pass

    def _discord_post(self, content):
        # post content to discord
        print(f'Posting to Discord: {content}')

    def _slack_post(self, content):
        # post content to slack
        print(f'Posting to Slack: {content}')
