import Ajv from 'ajv';
import addFormats from 'ajv-formats';
import { PanelConfiguration } from '../types/panel';

const ajv = new Ajv({ allErrors: true });
addFormats(ajv);

/**
 * Generates a unique ID for a panel instance.
 */
export function generatePanelId(): string {
  return `panel-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
}

/**
 * Validates a configuration object against a JSON schema.
 * @param config The configuration to validate
 * @param schema The JSON schema
 * @returns boolean true if valid, throws error if invalid
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function validateConfiguration(config: PanelConfiguration, schema: any): boolean {
  if (!schema) return true; // No schema means any config is valid

  const validate = ajv.compile(schema);
  const isValid = validate(config);

  if (!isValid) {
    const errors = validate.errors?.map(err => `${err.instancePath} ${err.message}`).join(', ');
    throw new Error(`Configuration validation failed: ${errors}`);
  }

  return true;
}

/**
 * Extracts default configuration from a JSON schema.
 * (Simple implementation handling properties with 'default' keys)
 * @param schema The JSON schema
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function getDefaultConfiguration(schema?: any): PanelConfiguration {
  const defaultConfig: PanelConfiguration = {};

  if (!schema || !schema.properties) {
    return defaultConfig;
  }

  Object.keys(schema.properties).forEach(key => {
    const prop = schema.properties[key];
    if (prop.default !== undefined) {
      defaultConfig[key] = prop.default;
    }
  });

  return defaultConfig;
}
