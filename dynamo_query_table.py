import decimal
import json

from boto3 import resource
from boto3.dynamodb.conditions import Key


class DecimalEncoder(json.JSONEncoder):
    '''
    Helper class to conver a DynamoDB item to JSON
    '''

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


class DynamoRepository:
    def __init__(self, target_dynamo_table, region='us-east-2'):
        self.dynamodb = resource(service_name='dynamodb', region_name=region)
        self.dynamo_table = target_dynamo_table
        self.table = self.dynamodb.Table(self.dynamo_table)

    def query_dynamo_record_by_partition(self, partition_key, partition_value):
        try:
            response = self.table.query(
                KeyConditionExpression=Key(partition_key).eq(partition_value)
            )
            for record in response.get('Items'):
                print(json.dumps(record, cls=DecimalEncoder))
            return
        except Exception as e:
            print(f'Exception {str(type(e))} type')
            print(f'Exception message: {str(e)}')

    def query_dynamo_record_by_partition_sort_key(
        self, partition_key, partition_value, sort_key, sort_value
    ):
        try:
            response = self.table.query(
                KeyConditionExpression=Key(partition_key).eq(partition_value)
                & Key(sort_key).gte(sort_value)
            )
            for record in response.get('Items'):
                print(json.dumps(record, cls=DecimalEncoder))
        except Exception as e:
            print(f'Exception type {str(type(e))}')
            print(f'Exception message: {str(e)}')


def main():
    table_name = 'user-visits'
    partition_key = 'EventId'
    partition_value = '324'
    sort_key = 'EventDay'
    sort_value = 20171001

    dynamo_repo = DynamoRepository(table_name)

    print(f'Reading all data for partition_key: {partition_value}')
    dynamo_repo.query_dynamo_record_by_partition(partition_key, partition_value)

    print(f'Reading data for partition_key: {partition_value} with data > {sort_value}')
    dynamo_repo.query_dynamo_record_by_partition_sort_key(
        partition_key, partition_value, sort_key, sort_value
    )


if __name__ == '__main__':
    main()
