import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { TemplateConfig } from "./template-configs";
export declare class AutohueAwsDeployStack extends cdk.Stack {
    constructor(scope: Construct, id: string, templateConfig: TemplateConfig, props?: cdk.StackProps);
    private createFunctions;
}
