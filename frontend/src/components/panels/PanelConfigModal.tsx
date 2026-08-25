import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '../ui/dialog';
import { Button } from '../ui/button';
import { Label } from '../ui/label';
import { Input } from '../ui/input';
import { PanelConfiguration } from '../../types/panel';
import { validateConfiguration } from '../../utils/panelUtils';

interface PanelConfigModalProps {
  isOpen: boolean;
  onClose: () => void;
  configuration: PanelConfiguration;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  schema?: any;
  onSave: (newConfig: PanelConfiguration) => void;
}

export const PanelConfigModal: React.FC<PanelConfigModalProps> = ({
  isOpen,
  onClose,
  configuration,
  schema,
  onSave
}) => {
  const [localConfig, setLocalConfig] = useState<PanelConfiguration>(configuration);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen) {
      setLocalConfig(configuration);
      setError(null);
    }
  }, [isOpen, configuration]);

  const handleSave = () => {
    try {
      if (schema) {
        validateConfiguration(localConfig, schema);
      }
      onSave(localConfig);
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Invalid configuration');
    }
  };

  const handleChange = (key: string, value: string | boolean | number) => {
    setLocalConfig(prev => ({ ...prev, [key]: value }));
    setError(null); // clear error on change
  };

  // Very basic dynamic form generation based on schema
  const renderFormFields = () => {
    if (!schema || !schema.properties) {
      return <p className="text-sm text-muted-foreground">No configuration options available.</p>;
    }

    return Object.entries(schema.properties).map(([key, prop]: [string, any]) => {
      const type = prop.type;
      const title = prop.title || key;
      const description = prop.description;

      return (
        <div key={key} className="grid gap-2">
          <Label htmlFor={key}>{title}</Label>
          {type === 'boolean' ? (
            <input
              type="checkbox"
              id={key}
              checked={!!localConfig[key]}
              onChange={(e) => handleChange(key, e.target.checked)}
              className="mt-1"
            />
          ) : (
            <Input
              id={key}
              type={type === 'number' || type === 'integer' ? 'number' : 'text'}
              value={localConfig[key] !== undefined ? String(localConfig[key]) : ''}
              onChange={(e) => {
                const val = type === 'number' || type === 'integer' ? Number(e.target.value) : e.target.value;
                handleChange(key, val);
              }}
            />
          )}
          {description && <p className="text-xs text-muted-foreground">{description}</p>}
        </div>
      );
    });
  };

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Panel Configuration</DialogTitle>
        </DialogHeader>

        <div className="grid gap-4 py-4">
          {renderFormFields()}

          {error && (
            <div className="text-sm font-medium text-destructive mt-2 p-2 bg-destructive/10 rounded-md">
              {error}
            </div>
          )}
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button onClick={handleSave}>Save changes</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};
