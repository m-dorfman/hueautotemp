import path = require('path');
import { Construct } from "constructs";

export function getLambdaCodePath(moduleName: string) {
    return path.join('lambda', moduleName);
}

export function getRequiredContext(scope: Construct, key: string) {
    const value = scope.node.tryGetContext(key)
    if (value === undefined) {
        throw new Error(`Could not resolve required key ${key}. Check cdk.json or command line.`)
    }
    return value;
}