import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Box,
  Tooltip,
} from '@mui/material';
import {
  LightMode,
  DarkMode,
} from '@mui/icons-material';
import { useAppSelector, useAppDispatch } from '../../store';
import { toggleTheme } from '../../store/slices/themeSlice';

const Header: React.FC = () => {
  const dispatch = useAppDispatch();
  const themeMode = useAppSelector(state => state.theme.mode);

  const handleThemeToggle = () => {
    dispatch(toggleTheme());
  };

  return (
    <AppBar position="static" color="default" elevation={1}>
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Task Management Dashboard
        </Typography>
        
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Tooltip title="Toggle theme">
            <IconButton onClick={handleThemeToggle}>
              {themeMode === 'light' ? <DarkMode /> : <LightMode />}
            </IconButton>
          </Tooltip>     
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;