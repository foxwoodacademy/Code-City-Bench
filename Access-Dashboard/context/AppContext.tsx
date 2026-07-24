import React, { createContext, useContext } from 'react';

// This context can be expanded to hold application-wide state.
// For now, it's a placeholder.
interface AppContextType {
    // Example state
    theme: 'dark' | 'light';
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const value = {
        theme: 'dark' as const, // Default theme
    };

    return (
        <AppContext.Provider value={value}>
            {children}
        </AppContext.Provider>
    );
};

export const useAppContext = () => {
    const context = useContext(AppContext);
    if (context === undefined) {
        throw new Error('useAppContext must be used within an AppProvider');
    }
    return context;
};
