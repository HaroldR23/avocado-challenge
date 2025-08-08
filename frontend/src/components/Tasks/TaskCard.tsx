import { useState } from "react";
import { Card, CardContent, Chip, Divider, Grid, Typography, IconButton, Tooltip, Box } from "@mui/material";
import { Edit as EditIcon } from "@mui/icons-material";
import { format } from "date-fns";
import { Task } from "../../types";
import TaskForm from "./TaskForm";

const TaskCard: React.FC<{ task: Task }> = ({ task }) => {
  const [openEdit, setOpenEdit] = useState(false);

  return (
    <>
      <Grid item xs={12} sm={6} md={4} key={task.id}>
        <Card variant="outlined" sx={{ borderRadius: 3, position: "relative" }}>
          <Box sx={{ position: "absolute", top: 8, right: 8 }}>
            <Tooltip title="Editar tarea">
              <IconButton
                size="small"
                color="primary"
                onClick={() => setOpenEdit(true)}
              >
                <EditIcon fontSize="small" />
              </IconButton>
            </Tooltip>
          </Box>

          <CardContent>
            <Typography variant="h6" fontWeight="bold" gutterBottom>
              {task.title}
            </Typography>

            <Typography
              variant="body2"
              color="text.secondary"
              gutterBottom
              sx={{ minHeight: 48 }}
            >
              {task.description}
            </Typography>

            <Divider sx={{ my: 1 }} />

            <Typography variant="body2" sx={{ mb: 1 }}>
              💬 {task.comments?.length || 0} comentarios
            </Typography>

            {task.dueDate && (
              <Chip
                label={`Vence: ${format(new Date(task.dueDate), "dd/MM/yyyy")}`}
                color="warning"
                size="small"
                sx={{ mb: 1 }}
              />
            )}

            <Typography variant="caption" color="text.secondary">
              Creado:{" "}
              {format(
                new Date(task?.createdAt ? task.createdAt : 0),
                "dd/MM/yyyy HH:mm"
              )}
            </Typography>
          </CardContent>
        </Card>
      </Grid>

      <TaskForm
        open={openEdit}
        onClose={() => setOpenEdit(false)}
        task={task}
      />
    </>
  );
};

export default TaskCard;
