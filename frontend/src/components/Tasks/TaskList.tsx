import React, { useState } from "react";
import { useAppSelector } from "../../store";
import {
  Card,
  CardContent,
  Typography,
  Grid,
  Skeleton,
  Box,
  Button,
} from "@mui/material";
import { Task } from "../../types";
import TaskCard from "./TaskCard";
import TaskForm from "./TaskForm";

const TaskList: React.FC = () => {
  const { items: tasks, loading } = useAppSelector((state) => state.tasks);
  const [openForm, setOpenForm] = useState(false);

  return (
    <>
      <Box sx={{ display: "flex", justifyContent: "flex-end", mb: 2 }}>
        <Button variant="contained" onClick={() => setOpenForm(true)}>
          Nueva tarea
        </Button>
      </Box>
      <Grid container spacing={2}>
        {loading
          ?
            Array.from({ length: 6 }).map((_, index) => (
              <Grid item xs={12} sm={6} md={4} key={index}>
                <Card variant="outlined" sx={{ borderRadius: 3 }}>
                  <CardContent>
                    <Skeleton variant="text" height={28} width="70%" />
                    <Skeleton variant="text" height={20} width="100%" />
                    <Skeleton variant="rectangular" height={80} sx={{ mt: 1, borderRadius: 1 }} />
                  </CardContent>
                </Card>
              </Grid>
            ))
          : tasks.length > 0
          ? 
            tasks.map((task: Task) => (
              <TaskCard key={task.id} task={task} />
            ))
          :
            !loading && (
              <Box sx={{ width: "100%", textAlign: "center", mt: 4 }}>
                <Typography variant="body1" color="text.secondary">
                  No hay tareas disponibles.
                </Typography>
              </Box>
            )}
      </Grid>
      <TaskForm open={openForm} onClose={() => setOpenForm(false)} />
    </>
  );
};

export default TaskList;
