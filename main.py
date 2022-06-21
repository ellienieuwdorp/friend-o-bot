import json
import os
import re

import_data_folder = "discord_data"
output_data_folder = "finetune_data"

id_dojobear = "547606513041145858"
id_nihil = "478517190945931275"

output_file = open(output_data_folder + "\\" + id_dojobear + ".json", "x", encoding='utf-8')


def parse_discord_folder():
    for filename in os.listdir(import_data_folder):
        file = os.path.join(import_data_folder, filename)
        if os.path.isfile(file):
            print(file)
            data = open(file, encoding='utf-8')

            json_file = json.load(data)
            parse_discord_file(json_file)

            data.close()
    output_file.close()


def get_referenced_message(message_id, json_data):
    for message in json_data["messages"]:
        if message["id"] == message_id:
            return message["content"]

    return ""


def parse_discord_file(json_data):
    for message in json_data["messages"]:
        if message["author"]["id"] == id_dojobear:
            output = ""
            if "reference" in message:
                referenced_message = get_referenced_message(message["reference"]["messageId"], json_data)
                output = parse_message_with_reference(message, referenced_message)
            elif len(message["content"]) > 1:
                if message["content"][0] == ">" and message["content"][1] == " ":
                    output = parse_quote_message(message)
            else:
                output = parse_message(message)

            output_file.write(output)


def parse_message(message):
    prompt = ""
    content = message["content"]

    return create_record(prompt, content)


def parse_quote_message(message):
    # print("quote message parsed")
    # print(message)
    prompt = get_quote_prompt(message["content"])
    content = get_quote_message(message["content"])

    return create_record(prompt, content)


def parse_message_with_reference(message, referenced_message):
    # print("parsed reference message")

    # prompt = referenced_message["content"]
    content = message["content"]
    return create_record(referenced_message, content)


def create_record(prompt, content):
    pattern_new_line = re.compile(r"\n", re.IGNORECASE)
    pattern_quote = re.compile(r"\"", re.IGNORECASE)

    prompt = pattern_new_line.sub(" ", prompt)
    content = pattern_new_line.sub(" ", content)

    prompt = pattern_quote.sub("\\\"", prompt)
    content = pattern_quote.sub("\\\"", content)
    return "{\"prompt\": \"" + prompt + "\", \"completion\": \"" + content + "\"}\n"


def get_quote_prompt(content):
    pattern = re.compile(r"(?<=> ).*(?=\n)", re.IGNORECASE)
    text = pattern.findall(content)
    # print("prompt")
    # print(text)
    # print(content)
    if len(text) == 0:
        return ""
    else:
        return text[0]


def get_quote_message(content):
    pattern = re.compile(r"(?=> ).*(?=\n)", re.IGNORECASE)
    text = pattern.sub("", content)
    return text


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parse_discord_folder()

    # prompt = get_quote_prompt("> And yeah ra4ndoms are frustrating hence i think everyone should find a group of people to play with\\n\\n\\uD83D\\uDCAF  I find I play _a lot_ better even with only one coordinated teammate - and empirically speaking, there's definitely a noticeable improvement in my damage / kills when coordinating with someone or adapting to random players.")
    # message = get_quote_message("> And yeah ra4ndoms are frustrating hence i think everyone should find a group of people to play with\\n\\n\\uD83D\\uDCAF  I find I play _a lot_ better even with only one coordinated teammate - and empirically speaking, there's definitely a noticeable improvement in my damage / kills when coordinating with someone or adapting to random players.")
    #
    # print(prompt)
    # print(message)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
