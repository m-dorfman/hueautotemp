import { aws_lambda as lambda } from "aws-cdk-lib";
import { aws_sqs as sqs } from "aws-cdk-lib";
import { aws_s3 as s3 } from "aws-cdk-lib";
import { aws_ssm as ssm } from "aws-cdk-lib";
import { aws_events as events } from "aws-cdk-lib";
import { Construct } from "constructs";
export interface WebParams {
    address: string;
    hueApiKey: ssm.StringParameter;
}
export declare function createModelGeneratorFn(scope: Construct, temperatureCycleFn: lambda.Function, modelGeneratorFnModuleName: string, modelBucket: s3.Bucket): lambda.Function;
export declare function createTemperatureCycleFn(scope: Construct, webParams: WebParams, modelBucket: s3.Bucket, temperatureFnModuleName: string, lightGroup: string, cronTriggerEvent: events.Rule): lambda.Function;
export declare function createUpdaterFn(scope: Construct, webParams: WebParams, cronTriggerEvent: events.Rule, updaterFnModuleName: string, writeQueue?: sqs.Queue): lambda.Function;
