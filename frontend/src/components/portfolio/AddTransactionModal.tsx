import React, { useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '../ui/dialog';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { useWorkspaceStore } from '../../store/useWorkspaceStore';

interface AddTransactionModalProps {
  isOpen: boolean;
  onClose: () => void;
  portfolioId: string;
}

export const AddTransactionModal: React.FC<AddTransactionModalProps> = ({ isOpen, onClose, portfolioId }) => {
  const [instrumentId, setInstrumentId] = useState('');
  const [type, setType] = useState('BUY');
  const [quantity, setQuantity] = useState('');
  const [price, setPrice] = useState('');
  const [fees, setFees] = useState('0');
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const [notes, setNotes] = useState('');

  // NOTE: Assuming there's a portfolio method in the API directly to add tx,
  // we would dispatch this to the workspaceStore or a custom usePortfolioStore.
  // For the skeleton, we just mock the payload building.

  const handleSubmit = async () => {
     try {
        // Validation handled implicitly via number casting in the store logic
        const tx = {
           instrument_id: instrumentId,
           transaction_type: type,
           quantity: parseFloat(quantity),
           price: parseFloat(price),
           fees: parseFloat(fees),
           transaction_date: date + 'T00:00:00Z',
           notes
        };
        // await portfolioApi.addTransaction(portfolioId, tx);
        console.log("Submitting transaction:", tx);
        onClose();
     } catch (e) {
        console.error(e);
     }
  };

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Add Transaction</DialogTitle>
        </DialogHeader>

        <div className="grid gap-4 py-4">
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="instrument" className="text-right">Instrument ID</Label>
            <Input id="instrument" value={instrumentId} onChange={e => setInstrumentId(e.target.value)} className="col-span-3" placeholder="UUID" />
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label className="text-right">Type</Label>
            <select className="col-span-3 h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm" value={type} onChange={e => setType(e.target.value)}>
               <option value="BUY">BUY</option>
               <option value="SELL">SELL</option>
               <option value="DIVIDEND">DIVIDEND</option>
            </select>
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="qty" className="text-right">Quantity</Label>
            <Input id="qty" type="number" value={quantity} onChange={e => setQuantity(e.target.value)} className="col-span-3" />
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="price" className="text-right">Price</Label>
            <Input id="price" type="number" value={price} onChange={e => setPrice(e.target.value)} className="col-span-3" />
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="fees" className="text-right">Fees</Label>
            <Input id="fees" type="number" value={fees} onChange={e => setFees(e.target.value)} className="col-span-3" />
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="date" className="text-right">Date</Label>
            <Input id="date" type="date" value={date} onChange={e => setDate(e.target.value)} className="col-span-3" />
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="notes" className="text-right">Notes</Label>
            <Input id="notes" value={notes} onChange={e => setNotes(e.target.value)} className="col-span-3" />
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button onClick={handleSubmit}>Save Transaction</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};
