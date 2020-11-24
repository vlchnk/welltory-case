import json
from jsonschema import Draft7Validator
import sys

from os import walk

old_stdout = sys.stdout

log_file = open("README.MD","w")

sys.stdout = log_file

print('**Log file**')

events = []
for (dirpath, dirnames, filenames) in walk('./event'):
    events.extend(filenames)
    break


for el in events:
    path = f'./event/{str(el)}'
    with open(path) as json_file:
        event = json.load(json_file)

    try:
        event_name = event['event'].replace(" ", "")
    except:
        if type(event) == dict:
            err = '---\n'
            err += f'File: **{el}**\n\n'
            print(err + f'**Error**: empty dict\n')
        else:
            err = '---\n'
            err += f'File: **{el}**\n\n'
            print(err + f'**Error**: different file type\n\n')
        continue

    if event_name == 'cmarker_created':
        with open('./schema/cmarker_created.schema') as json_file:
            schema = json.load(json_file)
    elif event_name == 'label_selected':
        with open('./schema/label_selected.schema') as json_file:
            schema = json.load(json_file)
    elif event_name == 'sleep_created':
        with open('./schema/sleep_created.schema') as json_file:
            schema = json.load(json_file)
    elif event_name == 'workout_created':
        with open('./schema/workout_created.schema') as json_file:
            schema = json.load(json_file)
    else:
        err = '---\n'
        err += f'File: **{el}**, schema: **{event["event"]}**\n\n'
        print(err + f'**Error**: "{event["event"]}" don\'t find schema in folder "schema"\n\n')
        schema = False

    if schema:
        v = Draft7Validator(schema)
        errors = sorted(v.iter_errors(event['data']), key=lambda e: e.path)
        err = '---\n'
        err += f'File: **{el}**, schema: **{event_name}**\n\n'
        for error in errors:
            err += f'**Type**: {list(error.relative_schema_path)},**Path**: {list(error.path)}, **Error**: {error.message}\n\n'
            print(err)

sys.stdout = old_stdout

log_file.close()

