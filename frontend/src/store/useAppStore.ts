import { create } from 'zustand';

interface AppState {
  activeWorkspaceId: string | null;
  theme: 'light' | 'dark';
  isLoading: boolean;
  globalError: string | null;

  setActiveWorkspaceId: (id: string | null) => void;
  toggleTheme: () => void;
  setLoading: (status: boolean) => void;
  setError: (error: string | null) => void;
}

export const useAppStore = create<AppState>((set) => ({
  activeWorkspaceId: null,
  theme: 'dark',
  isLoading: false,
  globalError: null,

  setActiveWorkspaceId: (id) => set({ activeWorkspaceId: id }),
  toggleTheme: () => set((state) => ({ theme: state.theme === 'light' ? 'dark' : 'light' })),
  setLoading: (status) => set({ isLoading: status }),
  setError: (error) => set({ globalError: error }),
}));
