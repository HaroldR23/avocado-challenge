import React, { ReactNode } from 'react';
import { Box, CssBaseline, ThemeProvider, createTheme } from '@mui/material';
import Header from './Header';
import Sidebar from './Sidebar';

interface LayoutProps {
  children: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const themeMode = "light";
  const theme = createTheme({
    palette: {
      mode: themeMode,
      primary: {
        main: themeMode === 'light' ? '#2563eb' : '#3b82f6',
      },
      secondary: {
        main: themeMode === 'light' ? '#059669' : '#10b981',
      },
    },
    typography: {
      fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    },
  });

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', minHeight: '100vh' }}>
        <Sidebar />
        <Box 
          component="main" 
          sx={{ 
            flexGrow: 1, 
            display: 'flex', 
            flexDirection: 'column',
            backgroundColor: themeMode === 'light' ? 'grey.50' : 'grey.900',
          }}
        >
          <Header />
          <Box sx={{ flex: 1, p: 3 }}>
            {children}
          </Box>
        </Box>
      </Box>
    </ThemeProvider>
  );
};

export default Layout;