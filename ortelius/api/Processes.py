import hug
import datetime

from ortelius.types.errors import NotFound, BadRequest
from ortelius.types.historical_date import HistoricalDate as hd
from ortelius.types.historical_date import DateError
from ortelius.database import db
from ortelius.models.Date import Date
from ortelius.models.Process import Process
from ortelius.middleware import serialize, make_api_response


def filter_by_time(query, start_date, end_date):
    '''Filter processes by date'''
    if start_date:
        start = hd(start_date)
    else:
        start = hd(-50000101)
    if end_date:
        end = hd(end_date)
    else:
        end = hd(datetime.datetime.now())
    query = query.filter(Process.start_date.has(Date.date >= start.to_int()),
                         Process.end_date.has(Date.date <= end.to_int())
                        )
    return query


def filter_by_ids(query, ids):
    pass


def filter_by_weight(query, weight):
    '''Filter processes by weight'''
    if weight:
        query = query.filter(Process.weight <= weight)
    else:
        return query


@hug.get('/processes',
         examples=['start_date=12-22-1560&end_date=03-30-1570&weight=1',
                   'ids=[1,2,3,4]']
        )
def get_processes(start_date: hug.types.text=None,
                  end_date: hug.types.text=None,
                  weight: int=None,
                  ids: list=None):
    '''API function for getting list of processes'''
    query = db.query(Process)
    try:
        query = filter_by_time(query, start_date, end_date)
    except DateError:
        # response = make_api_response(e.api_error(400))
        # response.status_code = 400
        # return response
        raise BadRequest()
    query = filter_by_weight(query, weight)
    result = query.all()
    serialized_result = []

    for process in result:
        serialized = serialize(process)
        serialized['start_date'] = process.start_date.date.to_string()
        serialized['end_date'] = process.end_date.date.to_string()
        serialized['type'] = {'name': process.type.name, 'label': process.type.label}
        # serialized['shape'] = serialized['shape_id']
        # serialized['description'] = serialized['description']
        serialized.pop('start_date_id')
        serialized.pop('end_date_id')
        # serialized.pop('shape_id')
        serialized.pop('type_name')
        serialized.pop('text')
        serialized_result.append(serialized)

    return make_api_response(serialized_result)


@hug.get('/processes/{process_id}')
def get_process(process_id):
    '''API function for getting single process by id'''
    process = db.query(Process).get(process_id)
    if process:
        result = serialize(process)

        result['start_date'] = process.start_date.date.to_string()
        result['end_date'] = process.end_date.date.to_string()
        result['type'] = {'name': process.type.name, 'label': process.type.label}
        # result['description'] = convert_wikitext(result['description'])
        # result['text'] = convert_wikitext(result['text'])
        # result.pop('text')
        result.pop('start_date_id')
        result.pop('end_date_id')
        result.pop('type_name')
        return make_api_response(result)
    else:
        raise NotFound(resource_type='Process', identifiers={'id': process_id})
