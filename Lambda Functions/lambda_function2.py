import json
import csv
import boto3
def lambda_handler(event, context):
	region = 'us-east-1'
	records = []
	try:
		s3 = boto3.client('s3')
		dynamodb = boto3.client('dynamodb', region_name = region)
		bucket = event['Records'][0]['s3']['bucket']['name']
		file = event['Records'][0]['s3']['object']['key']
		print('Bucket: ', bucket, 'key: ', file)

		csv_file = s3.get_object(Bucket= bucket, Key=file)
		records = csv_file['Body'].read().decode('utf-8').split('\n')
		csv_reader = csv.reader(records, delimiter= ',', quotechar='"')

		for row in csv_reader:
			Experiment = row[0]
			Material = row[1]
			Feedrate = row[2]
			ClampPressure =row[3]
			Tool_Condition=row[4]
			Machining_Finalized=row[5]
			Passed_Visual_inspection = row[6]
			
			
			add_to_db = dynamodb.put_item(
				TableName = 'cnc_machine_outcome',
				Item = {
				'Experiment' : {'N': str(Experiment)},
				'Material' : {'S': str(Material)},
				'Feedrate' : {'N': str(Feedrate)},
				'ClampPressure' : {'N': str(ClampPressure)},
				'Tool_Condition' : {'S': str(Tool_Condition)},
				'Machining_Finalized' : {'S': str(Machining_Finalized)},
				'Passed_Visual_inspection' : {'S': str(Passed_Visual_inspection)},
				})
		print('Records were added')

	except Exception as e:
		print(str(e))
	return {
			'statusCode': 200,
			'body': json.dumps('Data Successfully Loaded into DynamoDB')
	}

