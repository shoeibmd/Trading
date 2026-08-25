# Panel Framework Documentation

## Architecture Overview

The Panel Framework provides a robust, reusable architecture for building and rendering dynamic modules ("panels") within the financial terminal workspace. It handles state management, configurations, data fetching abstraction, and layout integration entirely independent of specific panel implementations.

### Core Components
1. **PanelRegistry (`src/services/panelRegistry.ts`)**: A singleton used to register and retrieve available panel definitions.
2. **PanelContext (`src/contexts/PanelContext.tsx`)**: Provides configuration, state, and utility functions to child components of a panel.
3. **usePanelData (`src/hooks/usePanelData.ts`)**: Abstract data hook handling data requirements, fetching, WebSocket subscriptions, and state transitions (loading, error, empty, success).
4. **PanelContainer (`src/components/panels/PanelContainer.tsx`)**: The visual shell for a panel. It wraps the panel component, handles errors and loading states, renders the `PanelHeader`, and manages the `PanelConfigModal`.

## How to Add a New Panel

1. **Create the Component**: Create a functional component that accepts `PanelProps` (or uses `usePanelContext`).
2. **Define the Panel**: Create a `PanelDefinition` object specifying the ID, category, data requirements, and configuration schema (using JSON Schema).
3. **Register the Panel**: Import the definition and register it in `src/panels/index.ts`.

### Example
```tsx
import { PanelDefinition, PanelProps } from '../../../types/panel';
import { usePanelContext } from '../../../contexts/PanelContext';

const MyPanel: React.FC<PanelProps> = () => {
  const { state, configuration } = usePanelContext();

  if (!state.data) return null;

  return <div>{state.data.message} - {configuration.customText}</div>;
};

export const myPanelDefinition: PanelDefinition = {
  id: 'my-unique-panel',
  type: 'My Panel',
  title: 'My Custom Panel',
  category: 'market',
  description: 'Displays custom data',
  defaultSize: 'medium',
  configurationSchema: {
    type: 'object',
    properties: {
      customText: { type: 'string', default: 'Hello' }
    }
  },
  dataRequirements: [{ type: 'quote', limit: 1 }],
  component: MyPanel
};
```

## Panel Lifecycle & States
All panels seamlessly transition between standard states controlled by the `usePanelData` hook:
- `loading`: Rendered via `PanelLoading` skeleton.
- `error`: Rendered via `PanelError` with an optional retry action.
- `empty`: Rendered via `PanelEmpty` when no data matches requirements.
- `success`: The core component is rendered with data.

## Configuration Schema
We use `ajv` to strictly validate panel configuration against JSON Schemas defined in `PanelDefinition`. The `PanelConfigModal` reads this schema to automatically generate a rudimentary configuration form for users.
