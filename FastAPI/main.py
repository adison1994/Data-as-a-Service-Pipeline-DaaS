from fastapi import FastAPI
from typing import Optional
import boto3
from boto3.dynamodb.conditions import Key, Attr
from pydantic import BaseModel

from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from fastapi import Security, Depends, FastAPI, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse
API_KEY = "1234567asdfgh"
Input="Enter Api Access Key"

api_key_query = APIKeyQuery(name=Input,auto_error=False)


app = FastAPI()

async def get_api_key(
    api_key_query: str = Security(api_key_query)):
    if api_key_query == API_KEY:
        return api_key_query
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

auto_error=False

class Item(BaseModel):
   Experiment_Owner: str
   M1_CURRENT_FEEDRATE: str
   S1_ActualAcceleration: str

class Outc(BaseModel):
   Material: str
   Tool_Condition: str
   Passed_Visual_inspection: str



region = 'us-east-1'
dynamodb_client = boto3.client('dynamodb', region_name = region)

TableName = "cnc_machine_experiments"
TableName_ = "cnc_machine_outcome"
dynamodb = boto3.resource('dynamodb', region_name=region)
table = dynamodb.Table(TableName)
table_ = dynamodb.Table(TableName_)


@app.get("/",tags=["Welcome to CNC Mill"])
async def read_root():
	return {"Hello": "World"}

@app.get("/all_exp/",tags=["CNC Mill Experiments Data"])
async def get_all_experiments(api_key: APIKey = Depends(get_api_key)):
    if APIKey:
        response = table.scan()
    else:
        response = JSONResponse(
        get_openapi(title="FastAPI security test", version=1, routes=app.routes)
        )
    return response


@app.get("/experiment/{experiment_id}",tags=["CNC Mill Experiments Data"])
async def get_items_by_experiment(experiment_id: str, api_key: APIKey = Depends(get_api_key)):
    if APIKey:
        response = table.scan(
            FilterExpression=Attr('Experiment').eq(experiment_id)
            )
    else:
        response = JSONResponse(
        get_openapi(title="FastAPI security test", version=1, routes=app.routes)
        )

    return response


@app.get("/owner/{experiment_owner}",tags=["CNC Mill Experiments Data"])
async def get_items_by_owner(experiment_owner: str, api_key: APIKey = Depends(get_api_key)):
    if APIKey:
        response = table.scan(
            FilterExpression=Attr('Experiment_owner').eq(experiment_owner))
    else:
        response = JSONResponse(
        get_openapi(title="FastAPI security test", version=1, routes=app.routes)
        )
    return response

#multiple path parameters
@app.get("/owner/{experiment_owner}/event/{event_id}",tags=["CNC Mill Experiments Data"])
async def get_items_by_event(experiment_owner: str, event_id: int, api_key: APIKey = Depends(get_api_key)):
    if APIKey:
        response = table.get_item(
                Key={
                    'Event_Id': event_id,
                    'Experiment_owner': experiment_owner
                })
    else:
        response = JSONResponse(
        get_openapi(title="FastAPI security test", version=1, routes=app.routes)
        )
    return response

### Get data for an Specific columns based on range conditions
@app.get("/eventRange/",tags=["CNC Mill Experiments Data"])
async def get_items_by_event_range(min_event_id: int, max_event_id: int, api_key: APIKey = Depends(get_api_key)):
    if APIKey:
        response = table.scan(
            FilterExpression=Key('Event_Id').between(min_event_id,max_event_id), 
            ProjectionExpression= "Event_Id, Experiment, Experiment_owner, Machining_Process, S1_ActualAcceleration")
    else:
        response = JSONResponse(
        get_openapi(title="FastAPI security test", version=1, routes=app.routes)
        )
    return response


@app.get("/Acceleration/{min_acceleration}",tags=["CNC Mill Experiments Data"])
async def get_items_by_acceleration(min_acceleration: str, api_key: APIKey = Depends(get_api_key)):
    if APIKey:
        response = table.scan(
            FilterExpression=Attr('X1_ActualAcceleration').gte(min_acceleration))
    else:
        response = JSONResponse(
        get_openapi(title="FastAPI security test", version=1, routes=app.routes)
        )
    return response 

@app.get("/OutputVoltage/",tags=["CNC Mill Experiments Data"])
async def get_items_by_Outputvoltage(min_voltage: int, max_voltage: int, api_key: APIKey = Depends(get_api_key)):
    if APIKey:
        response = table.scan(
            FilterExpression=Attr('X1_OutputVoltage').between(min_voltage,max_voltage))
    else:
        response = JSONResponse(
        get_openapi(title="FastAPI security test", version=1, routes=app.routes)
        )
    return response 

@app.get("/OutputCurrent/{min_current}",tags=["CNC Mill Experiments Data"])
async def get_items_by_Outputcurrent(min_current: int, api_key: APIKey = Depends(get_api_key)):
    if APIKey:
        response = table.scan(
            FilterExpression=Attr('X1_OutputCurrent').gte(min_current))
    else:
        response = JSONResponse(
        get_openapi(title="FastAPI security test", version=1, routes=app.routes)
        )
    return response 


@app.put("/delete_item/",tags=["CNC Mill Update Experiments"])
async def delete_items_by_event(event_id: int, owner: str, api_key: APIKey = Depends(get_api_key)):
    if APIKey:
        response = table.delete_item(Key={
                    'Event_Id': event_id,
                    'Experiment_owner': owner
                })
    else:
        response = JSONResponse(
        get_openapi(title="FastAPI security test", version=1, routes=app.routes)
        )
    return response


@app.put("/update_item/",tags=["CNC Mill Update Experiments"])
async def update_items_by_event(event_id: int, item:Item, api_key: APIKey = Depends(get_api_key)):
    if APIKey:
        response = table.update_item(
        Key={
            'Event_Id': event_id,
            'Experiment_owner': item.Experiment_Owner
        },
        UpdateExpression="set M1_CURRENT_FEEDRATE=:r, S1_ActualAcceleration=:p",
        ExpressionAttributeValues={
            ':r': item.M1_CURRENT_FEEDRATE,
            ':p': item.S1_ActualAcceleration
        },
        ReturnValues="UPDATED_NEW"
    )
    else:
        response = JSONResponse(
        get_openapi(title="FastAPI security test", version=1, routes=app.routes)
        )
    return response


### Get data for Outcomes files 
@app.get("/outcomes/",tags=["CNC Mill Outcomes Data"])
async def get_all_experiment_outcomes(api_key: APIKey = Depends(get_api_key)):
    if APIKey:
        response = table_.scan()
    else:
        response = JSONResponse(
        get_openapi(title="FastAPI security test", version=1, routes=app.routes)
        )
    return response

@app.get("/outcomes/{tool_condition}",tags=["CNC Mill Outcomes Data"])
async def get_outcome_by_toolcondition(tool_condition: str, api_key: APIKey = Depends(get_api_key)):
    if APIKey:
        response = table_.scan(
            FilterExpression=Attr('Tool_Condition').eq(tool_condition))
    else:
        response = JSONResponse(
        get_openapi(title="FastAPI security test", version=1, routes=app.routes)
        )
    return response

@app.get("/inspection/{Passed_Visual_inspection}",tags=["CNC Mill Outcomes Data"])
async def get_outcome_by_visual(Passed_Visual_inspection: str, api_key: APIKey = Depends(get_api_key)):
    if APIKey:
        response = table_.scan(
            FilterExpression=Attr('Passed_Visual_inspection').eq(Passed_Visual_inspection))

    else:
        response = JSONResponse(
        get_openapi(title="FastAPI security test", version=1, routes=app.routes)
        )
    return response


@app.get("/Feedrate/",tags=["CNC Mill Outcomes Data"])
async def get_outcomes_by_Feedrate(min_feedrate: int, max_feedrate: int, api_key: APIKey = Depends(get_api_key)):
    if APIKey:
        response = table_.scan(
            FilterExpression=Attr('Feedrate').between(min_feedrate,max_feedrate))
    else:
        response = JSONResponse(
        get_openapi(title="FastAPI security test", version=1, routes=app.routes)
        )
    return response 


@app.put("/update_outcomes/",tags=["CNC Mill Update Outcomes Data"])
async def update_outcomes(experiment: int, item:Outc, api_key: APIKey = Depends(get_api_key)):
    if APIKey:
        response = table_.update_item(
        Key={
            'Experiment': experiment
        },
        UpdateExpression="set Material=:r, Tool_Condition=:p, Passed_Visual_inspection=:q",
        ExpressionAttributeValues={
            ':r': item.Material,
            ':p': item.Tool_Condition,
            ':q': item.Passed_Visual_inspection
        },
        ReturnValues="UPDATED_NEW"
    )
    else:
        response = JSONResponse(
        get_openapi(title="FastAPI security test", version=1, routes=app.routes)
        )
    return response

