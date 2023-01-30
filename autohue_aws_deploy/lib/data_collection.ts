import {aws_ec2 as ec2, aws_iam, aws_secretsmanager, aws_sns, Duration} from 'aws-cdk-lib';
import {Construct} from "constructs";
import { aws_rds as rds } from "aws-cdk-lib";
import { aws_sqs as sqs} from "aws-cdk-lib";
import { aws_lambda as lambda } from "aws-cdk-lib";
import { aws_iam as iam } from "aws-cdk-lib";
import { aws_sns as sns } from "aws-cdk-lib";
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import { aws_ssm as ssm } from "aws-cdk-lib";
import { getLambdaCodePath } from './utils'

export class DataCollectionBuild extends Construct {
    dbWriterFnModuleName: string;
    public readonly databaseCredentialsSecret: secretsmanager.Secret;
    public readonly vpc:ec2.Vpc;
    public readonly usageDB: rds.DatabaseInstance;
    public readonly queue: sqs.Queue;

    constructor(scope: Construct, id: string, dbWriterFnModuleName: string) {
        super(scope, id);
        this.dbWriterFnModuleName = dbWriterFnModuleName;
        this.vpc = new ec2.Vpc(this, 'AuxiliaryComponentsVPC', {
            natGateways: 1,
            subnetConfiguration: [
                {
                    cidrMask: 24,
                    name: 'Private',
                    subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
                },
                {
                    cidrMask: 24,
                    name: 'PrivateWithEgress',
                    subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
                },
            ],
        });

        this.databaseCredentialsSecret = new secretsmanager.Secret(this, 'UsageDBCredentialsSecret', {
            secretName: 'ussage-db-credentials',
            generateSecretString: {
                secretStringTemplate: JSON.stringify({
                    username: 'postgres',
                }),
                excludePunctuation: true,
                includeSpace: false,
                generateStringKey: 'password'
            }
        });

        const ssm_key = new ssm.StringParameter(this, 'UsageDBCredentialsArn', {
            parameterName: 'usage-credentials-arn',
            stringValue: this.databaseCredentialsSecret.secretArn,
        });

        const dbSecGroup = new ec2.SecurityGroup(this, 'UsageDBSecGroup', {
            vpc: this.vpc,
            description: 'Security group for light usage db',
            allowAllOutbound: true,
        });
        dbSecGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(54600))

        this.usageDB = new rds.DatabaseInstance(scope, 'lightUsageDB', {
            engine: rds.DatabaseInstanceEngine.POSTGRES,
            vpc: this.vpc,
            vpcSubnets: {subnetType: ec2.SubnetType.PRIVATE_ISOLATED},
            instanceType: ec2.InstanceType.of(
                ec2.InstanceClass.T4G,
                ec2.InstanceSize.MICRO,
            ),
            multiAz: false,
            allowMajorVersionUpgrade: true,
            backupRetention: Duration.days(2),
            securityGroups: [dbSecGroup],
            maxAllocatedStorage: 1,
            credentials: rds.Credentials.fromSecret(this.databaseCredentialsSecret)
        });

        this.queue = new sqs.Queue(this, 'LightBehaviorQueue')
        const notifies = new sns.Topic(this, 'dbFailNotifier')

        const dbWriterSecGrp = new ec2.SecurityGroup(this, 'DBWriterSecurityGroup', {
            vpc: this.vpc,
            allowAllOutbound: false,
        });
        const dbWriterFn = new lambda.DockerImageFunction(this, 'DBWriterFn', {
            description: 'Writes light trigger action and time to Postgres db',
            code: lambda.DockerImageCode.fromImageAsset(
                getLambdaCodePath(this.dbWriterFnModuleName)
            ),
            environment: {'DB_CREDENTIALS': ssm_key.parameterName},
            architecture: lambda.Architecture.ARM_64,
            vpc: this.vpc,
            vpcSubnets: this.vpc.selectSubnets({
                subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
            }),
            securityGroups: [dbWriterSecGrp]
            },
        );

        dbWriterFn.addToRolePolicy(new iam.PolicyStatement({
            actions: ['ssm:GetParameter',],
            resources: [ssm_key.parameterArn]
        }));
    }
}