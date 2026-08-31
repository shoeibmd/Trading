import React from 'react';
import { PanelDefinition, PanelProps } from '../../../types/panel';
import { usePanelContext } from '../../../contexts/PanelContext';
import { formatCurrency, formatNumber } from '../../../utils/fundamentalsUtils';
import { Building2, Globe, MapPin, Users } from 'lucide-react';

export const CompanyProfilePanel: React.FC<PanelProps> = () => {
  const { state } = usePanelContext();

  const profile = state.data;

  if (!profile) return null;

  return (
    <div className="w-full h-full p-4 overflow-y-auto bg-background flex flex-col gap-4">
      <div className="flex items-start gap-4 pb-4 border-b">
        <div className="h-12 w-12 bg-primary/10 rounded-lg flex items-center justify-center text-primary font-bold text-xl shrink-0">
          {profile.company_name?.substring(0, 1) || 'C'}
        </div>
        <div>
          <h2 className="text-xl font-bold">{profile.company_name}</h2>
          <div className="flex items-center gap-2 text-sm text-muted-foreground mt-1">
            <span className="bg-muted px-2 py-0.5 rounded-sm">{profile.sector}</span>
            <span>•</span>
            <span>{profile.industry}</span>
          </div>
        </div>
      </div>

      <div className="text-sm leading-relaxed opacity-90">
        {profile.description}
      </div>

      <div className="grid grid-cols-2 gap-4 mt-2">
        <div className="flex items-center gap-2 text-sm">
          <Building2 className="h-4 w-4 text-muted-foreground" />
          <span>Founded: <span className="font-semibold">{profile.founded_year || 'N/A'}</span></span>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <Users className="h-4 w-4 text-muted-foreground" />
          <span>Employees: <span className="font-semibold">{profile.employees ? formatNumber(profile.employees) : 'N/A'}</span></span>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <Globe className="h-4 w-4 text-muted-foreground" />
          <a href={profile.website} target="_blank" rel="noreferrer" className="text-primary hover:underline truncate">
            {profile.website ? profile.website.replace(/^https?:\/\//, '') : 'N/A'}
          </a>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <MapPin className="h-4 w-4 text-muted-foreground" />
          <span className="truncate">{profile.headquarters || 'N/A'}</span>
        </div>
      </div>

      <div className="mt-4 pt-4 border-t grid grid-cols-2 gap-4">
        <div>
          <p className="text-xs text-muted-foreground uppercase tracking-wider font-semibold">Market Cap</p>
          <p className="text-lg font-bold">{profile.market_cap ? formatCurrency(profile.market_cap) : 'N/A'}</p>
        </div>
        <div>
          <p className="text-xs text-muted-foreground uppercase tracking-wider font-semibold">CEO</p>
          <p className="text-lg font-bold">{profile.ceo || 'N/A'}</p>
        </div>
      </div>
    </div>
  );
};

export const companyProfilePanelDefinition: PanelDefinition = {
  id: 'company-profile',
  type: 'CompanyProfile',
  title: 'Company Profile',
  category: 'fundamentals',
  description: 'Displays comprehensive business information.',
  defaultSize: 'medium',
  icon: 'Building2',
  configurationSchema: {
    type: 'object',
    properties: {
      symbol: { type: 'string', default: 'RELIANCE', title: 'Instrument ID/Symbol' },
      endpoint: { type: 'string', default: 'fundamentals-profile', title: 'Endpoint' }
    },
    required: ['symbol']
  },
  dataRequirements: [{ type: 'fundamentals' } as any],
  component: CompanyProfilePanel
};
