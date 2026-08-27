import React, { useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '../ui/dialog';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { Button } from '../ui/button';
import { useWorkspaceStore } from '../../store/useWorkspaceStore';
import { Trash2, Star, Edit2 } from 'lucide-react';

interface WorkspaceManagerProps {
  isOpen: boolean;
  onClose: () => void;
}

export const WorkspaceManager: React.FC<WorkspaceManagerProps> = ({ isOpen, onClose }) => {
  const { workspaces, activeWorkspaceId, setActiveWorkspace, addWorkspace, updateWorkspace, deleteWorkspace } = useWorkspaceStore();
  const [isCreating, setIsCreating] = useState(false);
  const [newName, setNewName] = useState('');
  const [newDesc, setNewDesc] = useState('');

  const handleCreate = async () => {
    if (!newName.trim()) return;
    await addWorkspace(newName, newDesc);
    setIsCreating(false);
    setNewName('');
    setNewDesc('');
  };

  const handleSetDefault = async (id: string) => {
    await updateWorkspace(id, { isDefault: true });
  };

  const handleDelete = async (id: string, isDefault: boolean) => {
    if (isDefault) {
      alert('Cannot delete the default workspace.');
      return;
    }
    if (confirm('Are you sure you want to delete this workspace?')) {
      await deleteWorkspace(id);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Manage Workspaces</DialogTitle>
        </DialogHeader>

        <div className="py-4 space-y-4 max-h-[60vh] overflow-y-auto">
          {workspaces.map(w => (
            <div key={w.id} className={`flex items-center justify-between p-3 border rounded-md ${activeWorkspaceId === w.id ? 'border-primary bg-primary/5' : ''}`}>
              <div className="flex-1 cursor-pointer" onClick={() => { setActiveWorkspace(w.id); onClose(); }}>
                <div className="flex items-center gap-2">
                  <h4 className="font-medium text-sm">{w.name}</h4>
                  {w.isDefault && <Star className="h-3 w-3 text-yellow-500 fill-yellow-500" />}
                  {activeWorkspaceId === w.id && <span className="text-[10px] bg-primary text-primary-foreground px-1.5 py-0.5 rounded-full">Active</span>}
                </div>
                {w.description && <p className="text-xs text-muted-foreground mt-0.5">{w.description}</p>}
              </div>

              <div className="flex items-center gap-1 ml-4">
                {!w.isDefault && (
                  <Button variant="ghost" size="icon" className="h-7 w-7" onClick={() => handleSetDefault(w.id)} title="Set as Default">
                    <Star className="h-3.5 w-3.5 text-muted-foreground" />
                  </Button>
                )}
                {!w.isDefault && (
                  <Button variant="ghost" size="icon" className="h-7 w-7 text-destructive hover:bg-destructive/10" onClick={() => handleDelete(w.id, w.isDefault)} title="Delete">
                    <Trash2 className="h-3.5 w-3.5" />
                  </Button>
                )}
              </div>
            </div>
          ))}

          {isCreating ? (
            <div className="border rounded-md p-3 space-y-3 bg-muted/30">
              <div>
                <Label htmlFor="ws-name">Name</Label>
                <Input id="ws-name" value={newName} onChange={e => setNewName(e.target.value)} placeholder="Workspace Name" className="h-8 mt-1" />
              </div>
              <div>
                <Label htmlFor="ws-desc">Description (Optional)</Label>
                <Input id="ws-desc" value={newDesc} onChange={e => setNewDesc(e.target.value)} placeholder="Brief description" className="h-8 mt-1" />
              </div>
              <div className="flex justify-end gap-2 pt-2">
                <Button variant="outline" size="sm" onClick={() => setIsCreating(false)}>Cancel</Button>
                <Button size="sm" onClick={handleCreate} disabled={!newName.trim()}>Create</Button>
              </div>
            </div>
          ) : (
            <Button variant="outline" className="w-full border-dashed" onClick={() => setIsCreating(true)}>
              + Create New Workspace
            </Button>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
};
