# Workspace & Layout System

## Architecture Overview

The Workspace System leverages `react-grid-layout` to provide a fully customizable, draggable, and resizable layout engine. It builds upon the Panel Framework (Phase 9) by allowing dynamic instantiation of panels into user-defined workspaces.

### Core Components
1. **GridLayout (`src/components/workspace/GridLayout.tsx`)**: Wraps the `react-grid-layout` ResponsiveGrid, rendering dynamically instantiated `PanelContainer` components based on the active workspace layout configuration.
2. **WorkspaceStore (`src/store/useWorkspaceStore.ts`)**: A Zustand store that manages all workspace state, handles optimistic UI updates, and synchronizes layouts with the backend via debounced API calls.
3. **PanelPicker (`src/components/workspace/PanelPicker.tsx`)**: A modal that reads from the `panelRegistry` and allows users to instantiate new panels onto their grid.
4. **LayoutValidator (`src/utils/layoutValidator.ts`)**: Ensures that loaded layouts are structurally sound, fixing missing coordinates or stripping dead panel references.

## Layout Persistence Strategy
When a user drags, resizes, or configures a panel, the `useWorkspaceStore` immediately applies the change to the local Zustand state for instantaneous UI response (Optimistic Updates).

Simultaneously, a debounced API call (500ms) is triggered to sync the entire serialized `WorkspaceLayout` JSON blob to the backend (`PATCH /api/v1/workspaces/{id}`). This prevents flooding the API with intermediate coordinates during drag operations.

## Backend Integration
The layout system requires the backend workspaces API (implemented as a Phase 10 prerequisite since it was omitted in Phase 7). The API stores the `layout` as a Postgres JSON column, giving the frontend total control over panel structures without needing strict relational models for every panel setting.

## Responsive Design
The system uses the `WidthProvider` and `Responsive` extensions of `react-grid-layout`. Breakpoints are defined for Large (1200px/12 cols) down to Extra Small (480px/4 cols). Currently, we primarily drive layout off the `lg` breakpoint, allowing the grid engine to natively auto-collapse panels on smaller screens.

## Keyboard Shortcuts
*(Future Implementation)*
- Add support for saving/new workspace via keyboard listeners.
