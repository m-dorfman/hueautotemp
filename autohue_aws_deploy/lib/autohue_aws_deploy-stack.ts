import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { aws_ssm as ssm} from "aws-cdk-lib";
import { aws_s3 as s3 } from "aws-cdk-lib";
import { aws_events as events } from "aws-cdk-lib";
import { TemplateConfig } from "./template-configs";
import { aws_sqs as sqs } from "aws-cdk-lib";
import { aws_apigateway as api} from "aws-cdk-lib";
import * as functions from "./functions";
import {ServicePrincipal} from "aws-cdk-lib/aws-iam";

export class AutohueAwsDeployStack extends cdk.Stack {
  constructor(scope: Construct, id: string, templateConfig: TemplateConfig, props?: cdk.StackProps) {
    super(scope, id, props);

    const hueApiKeyParam = new ssm.StringParameter(this, 'HueApiKeyParameter', {
      description: 'Parameter for the Philips Hue API',
      parameterName: 'hue-api-key',
      stringValue: templateConfig.hueApiKey,
    });

    const modelBucket = new s3.Bucket(this, 'ModelBucket');

    const cronRule = new events.Rule(this, 'TemperatureCronRule', {
      schedule: events.Schedule.expression('cron(* 6-23 * * *)')
    });

    const [updaterFn, modelGeneratorFn] = this.createFunctions(
        templateConfig.lambdaFunctions.modelGeneratorFnModuleName,
        templateConfig.lambdaFunctions.temperatureCycleFnModuleName,
        templateConfig.lambdaFunctions.updaterFnModuleName,
        modelBucket, templateConfig.hueAddress, hueApiKeyParam,
        templateConfig.lightGroup, cronRule);

    // create the api
    const lightsApi = new api.RestApi(this, 'ServerlessLightsApi', {
      restApiName: `lightsApi`
    });
    // separate resources and methods for each function that needs the api
    const updaterApiResource = lightsApi.root.addResource('updater');
    updaterApiResource.addMethod('PUT',
        new api.LambdaIntegration(updaterFn), {
          //apiKeyRequired: true,
        });
    const modelGeneratorApiResource = lightsApi.root.addResource('modelGenerator');
    modelGeneratorApiResource.addMethod('PUT',
        new api.LambdaIntegration(modelGeneratorFn), {
          //apiKeyRequired: true
        });
    // permissions for the api to invoke functions
    updaterFn.addPermission('PermitUpdaterFnInvocation', {
      principal: new ServicePrincipal('apigateway.amazonaws.com'),
      sourceArn: lightsApi.arnForExecuteApi('*'),
    });
    modelGeneratorFn.addPermission('PermitModelGeneratorFnInvocation', {
      principal: new ServicePrincipal('apigateway.amazonaws.com'),
      sourceArn: lightsApi.arnForExecuteApi('*'),
    });
  }

  private createFunctions(
      modelGeneratorFnModuleName: string, temperatureCycleFnModuleName: string,
      updaterFnModuleName: string, modelBucket: s3.Bucket,
      address: string, hueApiKey: ssm.StringParameter,
      lightGroup: string, cronTriggerEvent: events.Rule,
      dbWriterFnModuleName?: string, writeQueue?: sqs.Queue,
  ){
    const webParams: functions.WebParams = {
      address: address,
      hueApiKey: hueApiKey
    }
    const updateFn = functions.createUpdaterFn(
        this, webParams, cronTriggerEvent, updaterFnModuleName,
        );
    const temperatureCycleFn = functions.createTemperatureCycleFn(
        this, webParams, modelBucket, temperatureCycleFnModuleName, lightGroup, cronTriggerEvent
    );
    const modelGeneratorFn = functions.createModelGeneratorFn(
        this, temperatureCycleFn, modelGeneratorFnModuleName, modelBucket
    )

    return [updateFn, modelGeneratorFn] as const;

  }
}

