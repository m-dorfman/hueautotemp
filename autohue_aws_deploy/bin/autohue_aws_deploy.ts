#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { AutoHueAwsDeployStack } from '../lib/autohue_aws_deploy-stack';
import { TemplateConfig } from "../lib/template-configs";
import { getRequiredContext } from "../lib/utils";
import {Construct} from "constructs";


const app = new cdk.App();

const templateConfig : TemplateConfig ={
    hueAddress: getRequiredContext(app, 'hueAddress'),
    hueApiKey: getRequiredContext(app, 'hueApiKey'),
    lightGroup: getRequiredContext(app, 'lightGroup'),
    lambdaFunctions: getRequiredContext(app, 'lambdaFunctions')
}

console.log(templateConfig)

new AutoHueAwsDeployStack(app, 'AutohueAwsDeployStack', templateConfig);