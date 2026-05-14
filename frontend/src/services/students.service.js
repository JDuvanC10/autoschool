import { api } from '@/lib/api';

export const studentsService = {
  getStudents: async () => {
    const response = await api.get('/students/');
    return response.data.results || response.data;
  },

  createStudent: async (data) => {
    const response = await api.post('/students/', data);
    return response.data;
  },

  uploadPicture: async (studentId, file) => {
    if (!studentId || !file) {
      throw new Error('Faltan datos para subir la imagen.');
    }

    const formData = new FormData();

    // TODO(actividad): Agregar el archivo en FormData con la clave correcta
    formData.append('profile_picture', file);

        // Consumir endpoint del backend
    const response = await api.post(
      `/students/${studentId}/upload-picture/`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    return response.data;
  },
};

