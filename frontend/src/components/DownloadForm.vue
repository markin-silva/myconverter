<template>
  <div class="container">
    <h1>🎬 YouTube Downloader</h1>
    <form @submit.prevent="download">
      <input
        v-model="url"
        type="text"
        placeholder="URL do vídeo"
        required
      />
      <select v-model="format" required>
        <option value="mp3">MP3 (Áudio)</option>
        <option value="mp4">MP4 (Vídeo)</option>
      </select>
      <button type="submit" :disabled="loading">
        {{ loading ? "Processando..." : "Baixar" }}
      </button>
    </form>

    <div v-if="successMessage" class="download-section">
      <h2>{{ successMessage }}</h2>
    </div>

    <div v-if="error" class="error">
      ❌ {{ error }}
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DownloadForm',
  data() {
    return {
      url: '',
      format: 'mp3',
      successMessage: '',
      error: '',
      loading: false,
    };
  },
  methods: {
    async download() {
      this.error = '';
      this.successMessage = '';
      this.loading = true;
      try {
        const token = this.$keycloak.token;

        // 1. Enfileira o pedido de download
        const response = await axios.post(
          'http://localhost:8000/download',
          { url: this.url, format: this.format },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        const fileId = response.data.file_id;

        // 2. Mostra mensagem de sucesso
        this.successMessage = `✅ Seu download foi enfileirado com sucesso! ID: ${fileId}`;

        // (futuramente: salvar o file_id para acompanhar o status ou baixar)
      } catch (err) {
        console.error(err);
        this.error = 'Erro ao tentar iniciar o download. Verifique a URL ou tente novamente.';
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: 50px auto;
  padding: 30px;
  text-align: center;
  border: 1px solid #ddd;
  border-radius: 10px;
  background: #fafafa;
}

form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

input,
select,
button {
  padding: 10px;
  font-size: 1em;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  background-color: #42b983;
  color: white;
  cursor: pointer;
  font-weight: bold;
}

button:hover {
  background-color: #369870;
}

.download-section {
  margin-top: 20px;
}

.error {
  margin-top: 20px;
  color: red;
  font-weight: bold;
}
</style>
