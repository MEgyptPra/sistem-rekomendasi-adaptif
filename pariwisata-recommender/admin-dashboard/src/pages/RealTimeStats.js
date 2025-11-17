import React, { useState, useEffect } from 'react';
import { Box, Paper, Typography, TableContainer, Table, TableHead, TableRow, TableCell, TableBody, Chip, IconButton, Dialog, DialogTitle, DialogContent, DialogActions, Grid, TextField, Button } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import apiService from '../services/api';

function RealTimeStats() {
  const [configs, setConfigs] = useState([]);
  const [apiStatus, setApiStatus] = useState({});
  const [previewData, setPreviewData] = useState({});
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingConfig, setEditingConfig] = useState(null);
  const [saving, setSaving] = useState(false);

  const allowedSources = ["weather", "traffic_google", "traffic_tomtom", "social_trend", "calendar"];

  const fetchConfigs = async () => {
    try {
      const res = await apiService.listRealtimeApiConfig();
      setConfigs(res.data.filter(row => allowedSources.includes(row.source_name)));
    } catch (err) {
      setConfigs([]);
    }
  };

  const fetchApiStatusAndPreview = async () => {
    const statusObj = {};
    const previewObj = {};
    for (const config of configs) {
      try {
        const res = await apiService.getRealtimeStats(config.source_name);
        statusObj[config.source_name] = res.data.status || 'OK';
        previewObj[config.source_name] = res.data.preview || null;
      } catch (err) {
        statusObj[config.source_name] = 'Error';
        previewObj[config.source_name] = null;
      }
    }
    setApiStatus(statusObj);
    setPreviewData(previewObj);
  };

  useEffect(() => {
    fetchConfigs();
  }, []);

  useEffect(() => {
    if (configs.length > 0) {
      fetchApiStatusAndPreview();
    }
  }, [configs]);



  const handleEdit = (config) => {
    setEditingConfig({ ...config });
    setDialogOpen(true);
  };

  // Disable delete

  const handleDialogClose = () => {
    setDialogOpen(false);
    setEditingConfig(null);
  };

  const handleDialogSave = async () => {
    setSaving(true);
    try {
      if (editingConfig && editingConfig.id) {
        await apiService.updateRealtimeApiConfig(editingConfig.id, editingConfig);
      }
      fetchConfigs();
      handleDialogClose();
    } catch (err) {
      alert('Gagal menyimpan konfigurasi!');
    } finally {
      setSaving(false);
    }
  };

  const handleFieldChange = (e) => {
    const { name, value } = e.target;
    setEditingConfig({ ...editingConfig, [name]: value });
  };

  return (
    <Box>
      <Typography variant="h4" mb={3}>Real-time API Config</Typography>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h6">Daftar API Real-time</Typography>
        </Box>
        <TableContainer>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Nama Sumber</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>API Key</TableCell>
                <TableCell>API URL</TableCell>
                <TableCell>Last Checked</TableCell>
                <TableCell>Notes</TableCell>
                <TableCell>Koneksi API</TableCell>
                <TableCell>Preview Data</TableCell>
                <TableCell>Aksi</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {configs.length > 0 ? configs.map((row) => (
                <TableRow key={row.id}>
                  <TableCell>{row.source_name}</TableCell>
                  <TableCell>
                    <Chip label={row.status} color={row.status === 'active' ? 'success' : 'default'} size="small" />
                  </TableCell>
                  <TableCell>{row.api_key}</TableCell>
                  <TableCell>{row.api_url}</TableCell>
                  <TableCell>{row.last_checked ? new Date(row.last_checked).toLocaleString('id-ID') : '-'}</TableCell>
                  <TableCell>{row.notes}</TableCell>
                  <TableCell>
                    <Chip label={apiStatus[row.source_name] || '-'} color={apiStatus[row.source_name] === 'OK' ? 'success' : 'error'} size="small" />
                  </TableCell>
                  <TableCell>
                    {previewData[row.source_name] ? (
                      <pre style={{ fontSize: 12, maxWidth: 200, whiteSpace: 'pre-wrap' }}>{JSON.stringify(previewData[row.source_name], null, 2)}</pre>
                    ) : '-'}
                  </TableCell>
                  <TableCell>
                    <IconButton size="small" onClick={() => handleEdit(row)}><EditIcon /></IconButton>
                  </TableCell>
                </TableRow>
              )) : (
                <TableRow>
                  <TableCell colSpan={9} align="center">Belum ada data</TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      <Dialog open={dialogOpen} onClose={handleDialogClose} maxWidth="sm" fullWidth>
        <DialogTitle>Edit Config</DialogTitle>
        <DialogContent>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <TextField label="Nama Sumber" name="source_name" value={editingConfig ? editingConfig.source_name : ''} disabled fullWidth />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField label="Status" name="status" value={editingConfig ? editingConfig.status : ''} onChange={handleFieldChange} fullWidth />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField label="API Key" name="api_key" value={editingConfig ? editingConfig.api_key : ''} onChange={handleFieldChange} fullWidth />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField label="API URL" name="api_url" value={editingConfig ? editingConfig.api_url : ''} onChange={handleFieldChange} fullWidth />
            </Grid>
            <Grid item xs={12}>
              <TextField label="Notes" name="notes" value={editingConfig ? editingConfig.notes : ''} onChange={handleFieldChange} fullWidth />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleDialogClose}>Batal</Button>
          <Button variant="contained" onClick={handleDialogSave} disabled={saving}>{saving ? 'Menyimpan...' : 'Simpan'}</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default RealTimeStats;
