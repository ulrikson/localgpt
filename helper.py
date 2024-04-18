import json


class PromptHelper:
    @staticmethod
    def get_prompt(task, language):
        with open("/Users/eriklp/code/localgpt/prompts.json") as file:
            prompt = json.load(file)

        return prompt[language][task]
