export type TaskPriority = 'baja' | 'media' | 'alta';
export type UserRole = 'admin' | 'usuario';
export type ThemeMode = 'light' | 'dark';

export interface Task {
  id?: string;
  title: string;
  description: string;
  priority?: TaskPriority;
  completed?: boolean;
  dueDate?: Date;
  createdAt?: Date;
  updatedAt?: Date;
  assignedTo?: string;
}

export interface User {
  id: string;
  name: string;
  email: string;
  role: UserRole;
}

export interface TaskFilters {
  completed?: boolean;
  priority?: TaskPriority;
  assignedTo?: string;
  beforeDueDate?: Date;
  afterDueDate?: Date;
  orderBy?: TaskSort;
}

export interface TaskSort {
  direction: 'asc' | 'desc';
}
