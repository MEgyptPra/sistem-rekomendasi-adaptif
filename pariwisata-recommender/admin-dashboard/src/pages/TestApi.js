import React, { useState } from 'react';
import { Box, Typography, Paper, TextField, Button, MenuItem, CircularProgress } from '@mui/material';
import apiService from '../services/api';

const endpoints = [
  { label: 'Statistik', value: '/admin/stats', method: 'GET' },
  { label: 'Activity Stats', value: '/admin/activity-stats', method: 'GET' },
  { label: 'List Users', value: '/admin/users', method: 'GET' },
  // Tambahkan endpoint lain sesuai kebutuhan
];

function TestApi() {
  const [selectedEndpoint, setSelectedEndpoint] = useState(endpoints[0]);
  const [params, setParams] = useState('');
  const [body, setBody] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleTest = async () => {
    setLoading(true);
    setError('');
    setResponse(null);
    try {
      const reqBody = {
        method: selectedEndpoint.method,
        url: selectedEndpoint.value,
        params: params ? JSON.parse(params) : {},
        body: body ? JSON.parse(body) : {},
      };
      const res = await apiService.testApi(reqBody);
      setResponse(res.data);
    } catch (err) {
      setError('Gagal request atau format parameter/body salah.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box p={3}>
      <Typography variant="h4" mb={3}>Tes API Backend</Typography>
      <Paper sx={{ p: 3, mb: 3 }}>
        <TextField
          select
          label="Endpoint"
          value={selectedEndpoint.value}
          onChange={e => {
            const ep = endpoints.find(x => x.value === e.target.value);
            setSelectedEndpoint(ep);
          }}
          fullWidth
          sx={{ mb: 2 }}
        >
          {endpoints.map(ep => (
            <MenuItem key={ep.value} value={ep.value}>{ep.label} ({ep.method})</MenuItem>
          ))}
        </TextField>
        <TextField
          label="Params (JSON)"
          value={params}
          onChange={e => setParams(e.target.value)}
          fullWidth
          sx={{ mb: 2 }}
        />
        <TextField
          label="Body (JSON)"
          value={body}
          onChange={e => setBody(e.target.value)}
          fullWidth
          sx={{ mb: 2 }}
        />
        <Button variant="contained" onClick={handleTest} disabled={loading}>
          {loading ? <CircularProgress size={24} /> : 'Test API'}
        </Button>
      </Paper>
      {error && <Typography color="error">{error}</Typography>}
      {response && (
        <Paper sx={{ p: 2, mt: 2 }}>
          <Typography variant="h6">Response</Typography>
          <pre style={{ fontSize: 13, background: '#f5f5f5', padding: 10, borderRadius: 4 }}>
            {JSON.stringify(response, null, 2)}
          </pre>
        </Paper>
      )}
      <Paper sx={{ p: 2, mt: 4 }}>
        <Typography variant="h6" mb={1}>Dokumentasi API Backend</Typography>
        <Typography variant="body2">
          Untuk dokumentasi lengkap, kunjungi <a href="/docs" target="_blank" rel="noopener noreferrer">Swagger/OpenAPI</a>.<br />
          Endpoint yang bisa diuji: /admin/stats, /admin/activity-stats, /admin/users, dll.<br />
          Format params/body harus JSON.
        </Typography>
      </Paper>
    </Box>
  );
}

export default TestApi;
