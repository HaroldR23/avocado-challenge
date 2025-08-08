import React, { useState } from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemButton,
  Divider,
  Box,
  Typography,
  Collapse,
} from '@mui/material';
import {
  Dashboard,
  Assignment,
  BarChart,
  AdminPanelSettings,
  ExpandLess,
  ExpandMore,
  CheckCircle,
  PendingActions,
  Schedule,
} from '@mui/icons-material';

const drawerWidth = 280;

interface SidebarProps {
  activeView?: string;
  onViewChange?: (view: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ activeView = 'dashboard', onViewChange }) => {
  const [taskMenuOpen, setTaskMenuOpen] = useState(true);

  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Dashboard },
    { id: 'all-tasks', label: 'All Tasks', icon: Assignment, parent: 'tasks' },
    { id: 'completed', label: 'Completed', icon: CheckCircle, parent: 'tasks' },
    { id: 'pending', label: 'Pending', icon: PendingActions, parent: 'tasks' },
    { id: 'in-progress', label: 'In Progress', icon: Schedule, parent: 'tasks' },
    { id: 'analytics', label: 'Analytics', icon: BarChart },
  ];
  const currentUser = { role: 'admin' }; 
  if (currentUser?.role === 'admin') {
    menuItems.push({ id: 'admin', label: 'Admin Panel', icon: AdminPanelSettings });
  }

  const handleItemClick = (itemId: string) => {
    onViewChange?.(itemId);
  };

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
          borderRight: '1px solid',
          borderColor: 'divider',
        },
      }}
    >
      <Box sx={{ p: 2 }}>
        <Typography variant="h6" fontWeight={600}>
          TaskFlow Pro
        </Typography>
      </Box>
      
      <Divider />
      
      <List sx={{ flexGrow: 1, pt: 2 }}>
        <ListItem disablePadding>
          <ListItemButton 
            selected={activeView === 'dashboard'}
            onClick={() => handleItemClick('dashboard')}
          >
            <ListItemIcon>
              <Dashboard />
            </ListItemIcon>
            <ListItemText primary="Dashboard" />
          </ListItemButton>
        </ListItem>

        <ListItem disablePadding>
          <ListItemButton onClick={() => setTaskMenuOpen(!taskMenuOpen)}>
            <ListItemIcon>
              <Assignment />
            </ListItemIcon>
            <ListItemText primary="Tasks" />
            {taskMenuOpen ? <ExpandLess /> : <ExpandMore />}
          </ListItemButton>
        </ListItem>

        <Collapse in={taskMenuOpen} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            {menuItems.filter(item => item.parent === 'tasks').map((item) => (
              <ListItem key={item.id} disablePadding sx={{ pl: 2 }}>
                <ListItemButton 
                  selected={activeView === item.id}
                  onClick={() => handleItemClick(item.id)}
                >
                  <ListItemIcon>
                    <item.icon />
                  </ListItemIcon>
                  <ListItemText primary={item.label} />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        </Collapse>

        <ListItem disablePadding>
          <ListItemButton 
            selected={activeView === 'analytics'}
            onClick={() => handleItemClick('analytics')}
          >
            <ListItemIcon>
              <BarChart />
            </ListItemIcon>
            <ListItemText primary="Analytics" />
          </ListItemButton>
        </ListItem>

        {currentUser?.role === 'admin' && (
          <ListItem disablePadding>
            <ListItemButton 
              selected={activeView === 'admin'}
              onClick={() => handleItemClick('admin')}
            >
              <ListItemIcon>
                <AdminPanelSettings />
              </ListItemIcon>
              <ListItemText primary="Admin Panel" />
            </ListItemButton>
          </ListItem>
        )}
      </List>
    </Drawer>
  );
};

export default Sidebar;