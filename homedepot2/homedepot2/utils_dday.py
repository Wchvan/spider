from config import service_url, config
import json
import requests

from note import Note


def get_note_by_id(id):
    url = service_url.NOTE_URL + str(id) + '/'
    res = requests.get(url, headers=config.HEADERS)
    res_text = res.text
    data = json.loads(res_text)
    note = Note()
    note.new(**data)
    return note


def get_notes_by_group_id_and_page(group_id,page):
    url = service_url.NOTE_URL
    res = requests.get(url, params={'groupIdSearch': group_id,'page':page}, headers=config.HEADERS)
    res_text = res.text
    data = json.loads(res_text)
    # print(data)
    next_url = data['next']
    note_data_list = data['results']
    note_list = []
    for note_data in note_data_list:
        tmp_note = Note()
        tmp_note.new(**note_data)
        note_list.append(tmp_note)

    return note_list, next_url


def get_notes_by_group_id_and_page_and_gpt_problem(group_id, page, gpt_problem):
    url = service_url.NOTE_URL
    page_size = 150
    res = requests.get(url, params={'groupIdSearch': group_id, 'page': page, 'gptProblemSearch': gpt_problem,'page_size':page_size},
                       headers=config.HEADERS)
    res_text = res.text
    data = json.loads(res_text)
    # print(data)
    next_url = data['next']
    note_data_list = data['results']
    note_list = []
    for note_data in note_data_list:
        tmp_note = Note()
        tmp_note.new(**note_data)
        note_list.append(tmp_note)
    # print(note_list)

    return note_list, next_url