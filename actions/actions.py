# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from collections import Counter

class ActionGetTopLabels(Action):
    def name(self) -> Text:
        return "action_get_top_labels"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Fazer uma solicitação HTTP à API do GitHub para obter as issues do projeto "JabRef"
        github_api_url = "https://api.github.com/repos/JabRef/jabref/issues?per_page=100&state=open"
        response = requests.get(github_api_url)

        if response.status_code == 200:
            issues = response.json()
            labels_counter = Counter()

            # Contar as atividades associadas a cada label
            for issue in issues:
                for label in issue["labels"]:
                    labels_counter[label["name"]] += 1

            # Obter as 5 labels com mais atividades
            top_labels = labels_counter.most_common(5)

            # Montar a mensagem de resposta
            if top_labels:
                message = "As 5 labels com mais atividades associadas são:\n"
                for label, count in top_labels:
                    message += f"- {label}: {count} atividades\n"
            else:
                message = "Nenhuma atividade encontrada para as labels no projeto JabRef."

            dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(text="Desculpe, ocorreu um erro ao obter as informações do GitHub.")

        return []
    
class ActionGetGoodFirstIssues(Action):
    def name(self) -> Text:
        return "action_get_good_first_issues"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Fazer uma solicitação HTTP à API do GitHub para obter as issues do projeto "JabRef"
        github_api_url = "https://api.github.com/repos/JabRef/jabref/issues?per_page=100&state=open"
        response = requests.get(github_api_url)

        if response.status_code == 200:
            issues = response.json()

            # Filtrar as issues com a label "Good First Issue"
            good_first_issues = [issue for issue in issues if any(label["name"] == "good first issue" for label in issue["labels"])]

            # Montar a mensagem de resposta
            if good_first_issues:
                message = "Aqui estão as atividades vinculadas à label 'Good First Issue':\n"
                for issue in good_first_issues:
                    title = issue["title"]
                    url = issue["html_url"]
                    message += f"- {title}: {url}\n"
            else:
                message = "Nenhuma atividade encontrada vinculada à label 'Good First Issue' no projeto JabRef."

            dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(text="Desculpe, ocorreu um erro ao obter as informações do GitHub.")

        return []

class ActionGetIssuesByLabel(Action):
    def name(self) -> Text:
        return "action_get_issues_by_label"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Obter a escolha da label feita pelo usuário na ação anterior
        label_choice = next(tracker.get_latest_entity_values("label"), None)

        if not label_choice:
            dispatcher.utter_message(text="Desculpe, não foi possível identificar a label escolhida.")
            return []

        # Fazer uma solicitação HTTP à API do GitHub para obter as issues do projeto "JabRef"
        github_api_url = "https://api.github.com/repos/JabRef/jabref/issues?per_page=100&state=open"
        response = requests.get(github_api_url)

        if response.status_code == 200:
            issues = response.json()

            # Filtrar as issues com a label escolhida pelo usuário
            selected_label_issues = [issue for issue in issues if any(label["name"] == label_choice for label in issue["labels"])]

            # Montar a mensagem de resposta
            if selected_label_issues:
                message = f"Aqui estão as atividades vinculadas à label '{label_choice}':\n"
                for issue in selected_label_issues:
                    title = issue["title"]
                    url = issue["html_url"]
                    message += f"- {title}: {url}\n"
            else:
                message = f"Nenhuma atividade encontrada vinculada à label '{label_choice}' no projeto JabRef."

            dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(text="Desculpe, ocorreu um erro ao obter as informações do GitHub.")

        return []
    
class ActionWelcomeUser(Action):
    def name(self) -> Text:
        return "action_welcome_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(response="utter_greet")   
        return []
    
class ActionGoodbyeUser(Action):
    def name(self) -> Text:
        return "action_goodbye_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(response="utter_goodbye_user")
        return []