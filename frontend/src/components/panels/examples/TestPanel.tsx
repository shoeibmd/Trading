import React from 'react';
import { PanelDefinition, PanelProps } from '../../../types/panel';
import { usePanelContext } from '../../../contexts/PanelContext';

export const TestPanel: React.FC<PanelProps> = () => {
  // Use context to get data and configuration
  const { state, configuration } = usePanelContext();

  // Safe extraction of data and textColor from config
  const data = state.data;
  const textColor = configuration.textColor || '#000000';
  const customMessage = configuration.message || 'Default Hello World';
  const showBorder = configuration.showBorder || false;

  return (
    <div
      className={`w-full h-full p-6 flex flex-col items-center justify-center ${showBorder ? 'border-4 border-dashed border-primary/50' : ''}`}
      style={{ color: textColor }}
    >
      <h2 className="text-2xl font-bold mb-4">{customMessage}</h2>

      <div className="bg-muted p-4 rounded-md w-full max-w-sm overflow-hidden text-sm">
        <p className="font-semibold mb-2 text-foreground">Data Received:</p>
        <pre className="text-xs text-muted-foreground overflow-auto">
          {JSON.stringify(data, null, 2)}
        </pre>
      </div>

      <p className="mt-4 text-xs opacity-70">
        This is a test panel demonstrating the framework capabilities.
        Try changing settings to see empty/error states or change text color.
      </p>
    </div>
  );
};

export const testPanelDefinition: PanelDefinition = {
  id: 'test-panel',
  type: 'Test',
  title: 'Test Panel',
  category: 'utility',
  description: 'A simple panel to test the panel framework functionality.',
  defaultSize: 'medium',
  icon: 'Activity',
  configurationSchema: {
    type: 'object',
    properties: {
      title: {
        type: 'string',
        title: 'Panel Title',
        description: 'Override the default panel title',
        default: 'Test Panel'
      },
      message: {
        type: 'string',
        title: 'Custom Message',
        description: 'Message to display in the panel',
        default: 'Hello World'
      },
      textColor: {
        type: 'string',
        title: 'Text Color',
        description: 'Hex color code for the text',
        default: 'currentColor'
      },
      showBorder: {
        type: 'boolean',
        title: 'Show Border',
        description: 'Draw a dashed border around the content',
        default: false
      },
      simulateError: {
        type: 'boolean',
        title: 'Simulate Error State',
        description: 'Force the panel into an error state',
        default: false
      },
      simulateEmpty: {
        type: 'boolean',
        title: 'Simulate Empty State',
        description: 'Force the panel into an empty state',
        default: false
      }
    }
  },
  dataRequirements: [
    { type: 'instrument', limit: 10 }
  ],
  component: TestPanel
};
