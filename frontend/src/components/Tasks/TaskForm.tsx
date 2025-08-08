import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Box,
  Grid,
} from '@mui/material';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Task } from '../../types';
import { useAppDispatch } from '../../store';
import { addTask, updateTask } from '../../store/slices/tasksSlice';

const taskSchema = z.object({
  title: z.string().min(1, 'El título es requerido').max(100, 'Título muy largo'),
  description: z.string().max(500, 'Descripción muy larga'),
  priority: z.enum(['baja', 'media', 'alta']),
  dueDate: z.string().optional(),
  assignedTo: z.string().optional(),
});

type TaskFormData = z.infer<typeof taskSchema>;

interface TaskFormProps {
  open: boolean;
  onClose: () => void;
  task?: Task | null;
}

const TaskForm: React.FC<TaskFormProps> = ({ open, onClose, task }) => {
  const dispatch = useAppDispatch();
  const users = {
    items: [
      { id: 256, name: 'Admin user' },
    ]
  }

  const {
    control,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<TaskFormData>({
    resolver: zodResolver(taskSchema),
    defaultValues: {
      title: task?.title || '',
      description: task?.description || '',
      priority: task?.priority || 'baja',
      dueDate: task?.dueDate ? task.dueDate.toISOString().split('T')[0] : '',
      assignedTo: task?.assignedTo || '',
    },
  });

  const onSubmit = (data: TaskFormData) => {
    const taskData = {
      ...data,
      dueDate: data.dueDate ? new Date(data.dueDate) : new Date(),
      status: 'pending' as const,
      tags: [] as string[],
    };

    if (task) {
      dispatch(updateTask({ id: task.id ? task.id : '', ...taskData }));
    } else {
      dispatch(addTask(taskData));
    }
    
    handleClose();
  };

  const handleClose = () => {
    reset();
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <DialogTitle>
        {task ? 'Editar Tarea' : 'Crear Nueva Tarea'}
      </DialogTitle>
      
      <form onSubmit={handleSubmit(onSubmit)}>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3, pt: 2 }}>
            <Controller
              name="title"
              control={control}
              render={({ field }) => (
                <TextField
                  {...field}
                  label="Título de la tarea"
                  error={!!errors.title}
                  helperText={errors.title?.message}
                  fullWidth
                  required
                />
              )}
            />

            <Controller
              name="description"
              control={control}
              render={({ field }) => (
                <TextField
                  {...field}
                  label="Descripción"
                  multiline
                  rows={3}
                  error={!!errors.description}
                  helperText={errors.description?.message}
                  fullWidth
                />
              )}
            />

            <Controller
              name="priority"
              control={control}
              render={({ field }) => (
                <FormControl fullWidth>
                  <InputLabel>Prioridad</InputLabel>
                  <Select {...field} label="Prioridad">
                    <MenuItem value="baja">Baja</MenuItem>
                    <MenuItem value="media">Media</MenuItem>
                    <MenuItem value="alta">Alta</MenuItem>
                  </Select>
                </FormControl>
              )}
            />

            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Controller
                  name="dueDate"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Fecha de vencimiento"
                      type="date"
                      fullWidth
                      helperText="Opcional"
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <Controller
                  name="assignedTo"
                  control={control}
                  render={({ field }) => (
                    <FormControl fullWidth>
                      <InputLabel>Asignado a</InputLabel>
                      <Select {...field} label="Asignado a">
                        <MenuItem value="">Sin asignar</MenuItem>
                        {users.items.map((user) => (
                          <MenuItem key={user.id} value={user.id}>
                            {user.name}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                  )}
                />
              </Grid>
            </Grid>
          </Box>
        </DialogContent>

        <DialogActions sx={{ p: 3 }}>
          <Button onClick={handleClose} color="inherit">
            Cancelar
          </Button>
          <Button type="submit" variant="contained">
            {task ? 'Actualizar Tarea' : 'Crear Tarea'}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
};

export default TaskForm;