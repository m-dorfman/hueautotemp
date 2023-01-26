import { aws_lambda as lambda } from "aws-cdk-lib";
import { aws_iam as iam } from "aws-cdk-lib";
import { aws_sns as sns } from "aws-cdk-lib";
import { aws_sqs as sqs } from "aws-cdk-lib";
import { aws_s3 as s3} from "aws-cdk-lib";
import { aws_ssm as ssm } from "aws-cdk-lib";
import { aws_events_targets as targets } from "aws-cdk-lib";
import { aws_events as events } from "aws-cdk-lib";
import {Construct} from "constructs";
import {getLambdaCodePath} from './utils'

export interface WebParams {
  address: string,
  hueApiKey: ssm.StringParameter,
}

export function createModelGeneratorFn(
    scope: Construct, temperatureCycleFn: lambda.Function,
    modelGeneratorFnModuleName: string, modelBucket: s3.Bucket,
) {
  const modelGeneratorFn = new lambda.Function(scope, 'ModelGeneratorFn', {
    description: 'Generates a model and serializes it for the temperature cycle funct',
    runtime: lambda.Runtime.PYTHON_3_8,
    handler: `${modelGeneratorFnModuleName}.lambda_handler`,
    code: lambda.Code.fromAsset(getLambdaCodePath(modelGeneratorFnModuleName)),
    environment: {
      "CALLER_FUNCTION_NAME": temperatureCycleFn.functionName,
      "MODEL_BUCKET_NAME": modelBucket.bucketName,
      "MODEL_OBJECT_KEY_ENV_VAR": "MODEL_OBJECT_KEY", // this is the env var key from the temperature fn
    },
  });

 modelGeneratorFn.addToRolePolicy(new iam.PolicyStatement({
   actions: ['s3:PutObject',],
   resources:[modelBucket.bucketArn,]
 }));
 modelGeneratorFn.addToRolePolicy(new iam.PolicyStatement({
   actions: ['lambda:UpdateFunctionConfiguration',],
   resources: [temperatureCycleFn.functionArn,]
 }));

 return modelGeneratorFn
}

export function createTemperatureCycleFn(
    scope:Construct, webParams: WebParams,
    modelBucket: s3.Bucket, temperatureFnModuleName: string,
    lightGroup: string, cronTriggerEvent: events.Rule,
) {
  const temperatureCycleFn = new lambda.Function(scope, 'TemperatureCycleFn', {
    description: 'Sends request to Hue device(s) to set light temperature',
    runtime: lambda.Runtime.PYTHON_3_8,
    handler: `${temperatureFnModuleName}.lambda_handler`,
    code: lambda.Code.fromAsset(getLambdaCodePath(temperatureFnModuleName)),
    environment: {
      "API_KEY_SSM_PARAM": webParams.hueApiKey.parameterName,
      "ADDRESS": webParams.address,
      "MODEL_BUCKET_NAME": modelBucket.bucketName,
      "MODEL_OBJECT_KEY": '',
      "LIGHT_GROUP": lightGroup,
    },
  });

  cronTriggerEvent.addTarget(new targets.LambdaFunction(temperatureCycleFn));
  targets.addLambdaPermission(cronTriggerEvent, temperatureCycleFn);

  temperatureCycleFn.addToRolePolicy(new iam.PolicyStatement({
    actions: ['s3:GetObject',],
    resources: [modelBucket.bucketArn,]
  }));
  temperatureCycleFn.addToRolePolicy(new iam.PolicyStatement({
    actions: ['ssm:GetParameter',],
    resources: [webParams.hueApiKey.parameterArn,]
  }));

  return temperatureCycleFn;
}

export function createUpdaterFn(
    scope: Construct, webParams: WebParams,
    cronTriggerEvent: events.Rule,  updaterFnModuleName: string,
    writeQueue?: sqs.Queue,
) {
  const updaterFn = new lambda.Function(scope, 'UpdaterFn', {
    description: 'Performs updating functions upon light actions',
    runtime: lambda.Runtime.PYTHON_3_8,
    handler: `${updaterFnModuleName}.lambda_handler`,
    code: lambda.Code.fromAsset(getLambdaCodePath(updaterFnModuleName)),
    environment: {
      "API_KEY_SSM_PARAM": webParams.hueApiKey.parameterName,
      "ADDRESS": webParams.address,
      "CRON_EVENT_NAME": cronTriggerEvent.ruleName,
    },
  });
  if (typeof writeQueue !== 'undefined') {
    updaterFn.addEnvironment("WRITE_QUEUE_NAME", writeQueue.queueName);
    updaterFn.addToRolePolicy(new iam.PolicyStatement({
      actions: ['sqs:SendMessage', 'sqs:GetQueueAttributes', 'sqs:GetQueueUrl',],
      resources: [writeQueue.queueArn,]
    }));
  } else {
    updaterFn.addEnvironment("WRITE_QUEUE_NAME", '')
  }
  updaterFn.addToRolePolicy(new iam.PolicyStatement({
    actions: ['ssm:GetParameter',],
    resources: [webParams.hueApiKey.parameterArn,]
  }));
  updaterFn.addToRolePolicy(new iam.PolicyStatement({
    actions: ['events:DisableRule', 'events:EnableRule',],
    resources: [cronTriggerEvent.ruleArn,]
  }));

  return updaterFn;
}