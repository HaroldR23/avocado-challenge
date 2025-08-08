import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { Provider } from 'react-redux';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import TaskForm from '../components/Tasks/TaskForm';
import { createMockStore } from './TaskList.test';

const theme = createTheme();

const renderWithProviders = (component: React.ReactElement, store = createMockStore()) => {
  return render(
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        {component}
      </ThemeProvider>
    </Provider>
  );
};

describe('TaskForm', () => {
  const mockOnClose = jest.fn();

  beforeEach(() => {
    mockOnClose.mockClear();
  });

  test('renders create task form when no task provided', () => {
    renderWithProviders(<TaskForm open={true} onClose={mockOnClose} />);
    
    expect(screen.getByText('Create New Task')).toBeInTheDocument();
    expect(screen.getByLabelText('Task Title')).toBeInTheDocument();
    expect(screen.getByLabelText('Description')).toBeInTheDocument();
  });

  test('renders edit task form when task provided', () => {
    const task = {
      id: '1',
      title: 'Existing Task',
      description: 'Existing Description',
      priority: 'high' as const,
      status: 'pending' as const,
      dueDate: new Date('2024-12-31'),
      createdAt: new Date(),
      updatedAt: new Date(),
      assignedTo: '1',
      tags: [],
    };

    renderWithProviders(<TaskForm open={true} onClose={mockOnClose} task={task} />);
    
    expect(screen.getByText('Edit Task')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Existing Task')).toBeInTheDocument();
  });

  test('validates required fields', async () => {
    renderWithProviders(<TaskForm open={true} onClose={mockOnClose} />);
    
    const createButton = screen.getByText('Create Task');
    fireEvent.click(createButton);
    
    await waitFor(() => {
      expect(screen.getByText('Title is required')).toBeInTheDocument();
    });
  });

  test('calls onClose when cancel button clicked', () => {
    renderWithProviders(<TaskForm open={true} onClose={mockOnClose} />);
    
    const cancelButton = screen.getByText('Cancel');
    fireEvent.click(cancelButton);
    
    expect(mockOnClose).toHaveBeenCalled();
  });
});