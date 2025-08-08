import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { Task, TaskFilters, TaskSort } from '../../types';

interface TasksState {
  items: Task[];
  filters: TaskFilters;
  sort: TaskSort;
  loading: boolean;
}

const initialState: TasksState = {
  items: [],
  filters: {},
  sort: { direction: 'desc' },
  loading: false,
};

const tasksSlice = createSlice({
  name: 'tasks',
  initialState,
  reducers: {
    addTask: (state, action: PayloadAction<Task>) => {
      const task: Task = {
        ...action.payload,
        id: crypto.randomUUID(),
        createdAt: new Date(),
        updatedAt: new Date(),
      };
      state.items.push(task);
    },
    updateTask: (state, action: PayloadAction<Partial<Task> & { id: string }>) => {
      const index = state.items.findIndex(task => task.id === action.payload.id);
      if (index !== -1) {
        state.items[index] = {
          ...state.items[index],
          ...action.payload,
          updatedAt: new Date(),
        };
      }
    },
    deleteTask: (state, action: PayloadAction<string>) => {
      state.items = state.items.filter(task => task.id !== action.payload);
    },
    setFilters: (state, action: PayloadAction<TaskFilters>) => {
      state.filters = action.payload;
    },
    setSort: (state, action: PayloadAction<TaskSort>) => {
      state.sort = action.payload;
    },
    clearFilters: (state) => {
      state.filters = {};
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
  },
});

export const {
  addTask,
  updateTask,
  deleteTask,
  setFilters,
  setSort,
  clearFilters,
  setLoading,
} = tasksSlice.actions;

export default tasksSlice.reducer;