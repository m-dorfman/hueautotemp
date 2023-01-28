export interface TemplateConfig {
    hueAddress: string,
    hueApiKey: string,
    lightGroup: string,
    lambdaFunctions: {
        modelGeneratorFnModuleName: string,
        temperatureCycleFnModuleName: string,
        updaterFnModuleName: string,
        dbWriteFnModuleName?: string,
    }
}