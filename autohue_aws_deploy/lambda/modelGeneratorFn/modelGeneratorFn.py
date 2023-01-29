import os
import boto3
from numpy import polynomial
import pickle

CALLER_FUNCTION_NAME = os.environ.get('CALLER_FUCTION_NAME')
MODEL_BUCKET_NAME = os.environ.get('MODEL_BUCKET_NAME')
MODEL_OBJECT_KEY_ENV_VAR = os.environ.get('MODEL_OBJECT_KEY_ENV_VAR')
s3 = boto3.resource('s3')
lmda = boto3.resource('lambda')

def model_generator(minutes_x: list[int], temperature_k_y: list[int]):
    # Generates our model based on kelvin light temperature
    model_k = polynomial.Polynomial.fit(minutes_x, temperature_k_y, deg=6)
    minutes_x_final = minutes_x[len(minutes_x) - 1]
    temperature_k_y_final = temperature_k_y[len(temperature_k_y) - 1]
    model_name = f"{minutes_x[0]}-{temperature_k_y[0]}--{minutes_x_final}-{temperature_k_y_final}"
    return model_k, model_name

def model_serializer(model, model_name):
    model_byte_obj = pickle.dump(model)
    s3.Object(MODEL_BUCKET_NAME, model_name).put(model_byte_obj)


def lambda_handler(event, context):
    operation = event['operation']
    minutes_x = event['payload']['minutes_x']
    temperature_k_y = event['payload']['temperature_k_y']

    if operation is 'model-update':
        model, model_name = model_generator(minutes_x, temperature_k_y)
        model_serializer(model, model_name)
        lmda.update_function_configuration(
            FunctionName=CALLER_FUNCTION_NAME,
            Environment={
                'Variables':{
                    MODEL_OBJECT_KEY_ENV_VAR:model_name
                }
            }
        )
        # TODO add the return
    else:
        raise ValueError(f'Unrecognized operation "{operation}"')


if __name__ == "__main__":
    os.environ['CALLER_FUCTION_NAME'] = 'caller_function'
    os.environ['MODEL_BUCKET_NAME'] = 'model_bucket'
    os.environ['MODEL_OBJECT_KEY_ENV_VAR'] = 'object_key'
