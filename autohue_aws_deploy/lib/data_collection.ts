import {aws_ec2 as ec2, Duration} from 'aws-cdk-lib';
import {Construct} from "constructs";
import { aws_rds as rds } from "aws-cdk-lib";

export function createVPC(scope: Construct) {
   const vpc = new ec2.Vpc(scope, 'AuxiliaryComponentsVPC',{
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
           {
               cidrMask: 24,
               name: 'Public',
               subnetType: ec2.SubnetType.PUBLIC,
           },
       ],
   });
}
export function createDB(scope:Construct, vpc:ec2.Vpc) {
    const secGroup = new ec2.SecurityGroup(scope, 'UsageDBSecGroup', {
        vpc: vpc,
        description: 'Security group for light usage db',
        allowAllOutbound: true,
    });
    secGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(54600))

    const usageDB = new rds.DatabaseInstance(scope, 'lightUsageDB', {
        engine: rds.DatabaseInstanceEngine.POSTGRES,
        vpc: vpc,
        vpcSubnets: { subnetType: ec2.SubnetType.PRIVATE_ISOLATED},
        instanceType: ec2.InstanceType.of(
            ec2.InstanceClass.T4G,
            ec2.InstanceSize.MICRO,
        ),
        multiAz: false,
        allowMajorVersionUpgrade: true,
        backupRetention: Duration.days(2),
        securityGroups: secGroup,
    });
}