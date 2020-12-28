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
			ind = row[0]
			X1_ActualPosition = row[1]
			X1_ActualVelocity = row[2]
			X1_ActualAcceleration=row[3]
			X1_CommandPosition=row[4]
			X1_CommandVelocity=row[5]
			X1_CommandAcceleration = row[6]
			X1_CurrentFeedback=row[7]
			X1_DCBusVoltage=row[8]
			X1_OutputCurrent=row[9]
			X1_OutputVoltage=row[10]
			X1_OutputPower=row[11]
			Y1_ActualPosition=row[12]
			Y1_ActualVelocity=row[13]
			Y1_ActualAcceleration=row[14]
			Y1_CommandPosition=row[15]
			Y1_CommandVelocity=row[16]
			Y1_CommandAcceleration=row[17]
			Y1_CurrentFeedback=row[18]
			Y1_DCBusVoltage=row[19]
			Y1_OutputCurrent=row[20]
			Y1_OutputVoltage=row[21]
			Y1_OutputPower=row[22]
			Z1_ActualPosition=row[23]
			Z1_ActualVelocity=row[24]
			Z1_ActualAcceleration=row[25]
			Z1_CommandPosition=row[26]
			Z1_CommandVelocity=row[27]
			Z1_CommandAcceleration=row[28]
			Z1_CurrentFeedback=row[29]
			Z1_DCBusVoltage=row[30]
			Z1_OutputCurrent=row[31]
			Z1_OutputVoltage=row[32]
			S1_ActualPosition=row[33]
			S1_ActualVelocity=row[34]
			S1_ActualAcceleration=row[35]
			S1_CommandPosition=row[36]
			S1_CommandVelocity=row[37]
			S1_CommandAcceleration=row[38]
			S1_CurrentFeedback=row[39]
			S1_DCBusVoltage=row[40]
			S1_OutputCurrent=row[41]
			S1_OutputVoltage=row[42]
			S1_OutputPower=row[43]
			S1_SystemInertia=row[44]
			M1_CURRENT_PROGRAM_NUMBER=row[45]
			M1_sequence_number=row[46]
			M1_CURRENT_FEEDRATE=row[47]
			Machining_Process=row[48]
			Experiment = row[49]
			Experiment_owner = row[50]
			
			
			add_to_db = dynamodb.put_item(
				TableName = 'cnc_machine_experiments',
				Item = {
				'Event_Id' : {'N': str(ind)},
				'X1_ActualPosition' : {'S': str(X1_ActualPosition)},
				'X1_ActualVelocity' : {'S': str(X1_ActualVelocity)},
			'X1_ActualAcceleration' : {'S': str(X1_ActualAcceleration)},
				'X1_CommandPosition' : {'S': str(X1_CommandPosition)},
				'X1_CommandVelocity' : {'S': str(X1_CommandVelocity)},
				'X1_CommandAcceleration' : {'S': str(X1_CommandAcceleration)},
				'X1_CurrentFeedback' : {'S': str(X1_CurrentFeedback)},
				'X1_DCBusVoltage' : {'S': str(X1_DCBusVoltage)},
				'X1_OutputCurrent' : {'N': str(X1_OutputCurrent)},
				'X1_OutputVoltage' : {'N': str(X1_OutputVoltage)},
				'X1_OutputPower' : {'S': str(X1_OutputPower)},
				'Y1_ActualPosition' : {'S': str(Y1_ActualPosition)},
				'Y1_ActualVelocity' : {'S': str(Y1_ActualVelocity)},
			'Y1_ActualAcceleration' : {'S': str(Y1_ActualAcceleration)},
				'Y1_CommandPosition' : {'S': str(Y1_CommandPosition)},
				'Y1_CommandVelocity' : {'S': str(Y1_CommandVelocity)},
			'Y1_CommandAcceleration' : {'S': str(Y1_CommandAcceleration)},
				'Y1_CurrentFeedback' : {'S': str(Y1_CurrentFeedback)},
				'Y1_DCBusVoltage' : {'S': str(Y1_DCBusVoltage)},
				'Y1_OutputCurrent' : {'S': str(Y1_OutputCurrent)},
				'Y1_OutputVoltage' : {'S': str(Y1_OutputVoltage)},
				'Y1_OutputPower' : {'S': str(Y1_OutputPower)},
				'Z1_ActualPosition' : {'S': str(Z1_ActualPosition)},
				'Z1_ActualVelocity' : {'S': str(Z1_ActualVelocity)},
			'Z1_ActualAcceleration' : {'S': str(Z1_ActualAcceleration)},
				'Z1_CommandPosition' : {'S': str(Z1_CommandPosition)},
				'Z1_CommandVelocity' : {'S': str(Z1_CommandVelocity)},
				'Z1_CommandAcceleration' : {'S': str(Z1_CommandAcceleration)},
				'Z1_CurrentFeedback' : {'S': str(Z1_CurrentFeedback)},
				'Z1_DCBusVoltage' : {'S': str(Z1_DCBusVoltage)},
				'Z1_OutputCurrent' : {'N': str(Z1_OutputCurrent)},
				'Z1_OutputVoltage' : {'N': str(Z1_OutputVoltage)},
				'S1_ActualPosition' : {'S': str(S1_ActualPosition)},
				'S1_ActualVelocity' : {'S': str(S1_ActualVelocity)},
				'S1_ActualAcceleration' : {'S': str(S1_ActualAcceleration)},
				'S1_CommandPosition' : {'S': str(S1_CommandPosition)},
				'S1_CommandVelocity' : {'S': str(S1_CommandVelocity)},
				'S1_CommandAcceleration' : {'S': str(S1_CommandAcceleration)},
				'S1_CurrentFeedback' : {'S': str(S1_CurrentFeedback)},
				'S1_DCBusVoltage' : {'S': str(S1_DCBusVoltage)},
				'S1_OutputCurrent' : {'N': str(S1_OutputCurrent)},
				'S1_OutputVoltage' : {'N': str(S1_OutputVoltage)},
				'S1_OutputPower' : {'S': str(S1_OutputPower)},
				'S1_SystemInertia' : {'S': str(S1_SystemInertia)},
			'M1_CURRENT_PROGRAM_NUMBER' : {'S': str(M1_CURRENT_PROGRAM_NUMBER)},
				'M1_sequence_number' : {'S': str(M1_sequence_number)},
				'M1_CURRENT_FEEDRATE' : {'S': str(M1_CURRENT_FEEDRATE)},
				'Machining_Process' : {'S': str(Machining_Process)},
				'Experiment' : {'S': str(Experiment)},
				'Experiment_owner' : {'S': str(Experiment_owner)}
				})
		print('Records were added')

	except Exception as e:
		print(str(e))
	return {
			'statusCode': 200,
			'body': json.dumps('Data Successfully Loaded into DynamoDB')
	}

