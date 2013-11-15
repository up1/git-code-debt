
import collections
import flask


from git_code_debt.discovery import get_metric_parsers

Metric = collections.namedtuple('Metric', ['name', 'value', 'sha', 'date'])

def get_metric_ids():
    metric_ids = []
    metric_parsers = get_metric_parsers()
    for metric_parser_cls in metric_parsers:
        for metric_id in metric_parser_cls().get_possible_metric_ids():
            metric_ids.append(metric_id)
    return metric_ids

def most_recent_metric(metric_name):
    result = flask.g.db.execute(
        '''
        SELECT
            running_value,
            sha,
            timestamp
        FROM metric_data
        INNER JOIN metric_names ON
            metric_names.id == metric_data.metric_id
        WHERE
            metric_names.name == ?
        ORDER BY timestamp DESC
        LIMIT 1
        ''',
        [metric_name]
    ).fetchone()

    if result:
        return Metric(metric_name, *result)
    else:
        return Metric(metric_name, 0, 'No Data', 0)

def metrics_for_dates(repo, sha, metric_name, dates):

    def get_metric_for_timestamp(timestamp):
        result = flask.g.db.execute(
            '''
            SELECT
                running_value,
                sha,
                timestamp
            FROM metric_data
            INNER JOIN metric_names ON
                metric_names.id == metric_data.metric_id
            WHERE
                metric_names.name == ? AND
                timestamp < ?
            ORDER BY timestamp DESC
            LIMIT 1
            ''',
            [metric_name, timestamp],
        ).fetchone()
        if result:
            return Metric(metric_name, *result)
        else:
            return Metric(metric_name, 0, 'No Data', date)

    return [get_metric_for_timestamp(date) for date in dates]
