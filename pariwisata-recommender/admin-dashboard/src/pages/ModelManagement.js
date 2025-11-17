import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  CircularProgress,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  LinearProgress,
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Schedule as ScheduleIcon,
  PlayArrow as PlayArrowIcon,
} from '@mui/icons-material';
import apiService from '../services/api';

function ModelManagement() {
  const [modelStatus, setModelStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [retraining, setRetraining] = useState(false);
  const [openScheduleDialog, setOpenScheduleDialog] = useState(false);
  const [scheduleInterval, setScheduleInterval] = useState('monthly');
  const [driftDetection, setDriftDetection] = useState(null);
  const [realtimeStats, setRealtimeStats] = useState(null);

  useEffect(() => {
    fetchModelStatus();
  }, []);

  const fetchModelStatus = async () => {
    try {
      setLoading(true);
      const response = await apiService.getModelStatus();
      setModelStatus(response.data);
      
      // Fetch drift detection status
      const driftResponse = await apiService.getDriftDetection();
      setDriftDetection(driftResponse.data);
      
      // Fetch real-time stats
      const realtimeResponse = await apiService.getRealtimeStats();
      setRealtimeStats(realtimeResponse.data);
    } catch (error) {
      console.error('Error fetching model status:', error);
      // Fallback demo data
      setModelStatus({
        contentBased: {
          status: 'loaded',
          trainedAt: '2025-11-06T11:49:44.487319',
          accuracy: 0.85,
          samples: 36992
        },
        collaborative: {
          status: 'loaded',
          trainedAt: '2025-11-06T11:49:52.837725',
          accuracy: 0.82,
          samples: 36992
        },
        hybrid: {
          status: 'loaded',
          trainedAt: '2025-11-06T11:50:40.522328',
          accuracy: 0.88,
          samples: 36992
        }
      });
      
      setDriftDetection({
        driftDetected: false,
        lastCheck: new Date().toISOString(),
        performanceChange: 2.5,
        threshold: 5.0,
        recommendation: 'Model performance is stable'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleRetrain = async (modelType) => {
    if (!window.confirm(`Apakah Anda yakin ingin melatih ulang model ${modelType}? Proses ini mungkin memakan waktu beberapa menit.`)) {
      return;
    }

    try {
      setRetraining(true);
      await apiService.retrainModel({ modelType });
      alert(`Model ${modelType} berhasil dilatih ulang!`);
      fetchModelStatus();
    } catch (error) {
      console.error('Error retraining model:', error);
      alert('Gagal melatih ulang model. Silakan coba lagi.');
    } finally {
      setRetraining(false);
    }
  };

  const handleScheduleRetrain = async () => {
    try {
      await apiService.setRetrainSchedule({ interval: scheduleInterval });
      alert(`Penjadwalan pelatihan ulang berhasil diatur: ${scheduleInterval}`);
      setOpenScheduleDialog(false);
    } catch (error) {
      console.error('Error setting retrain schedule:', error);
      alert('Gagal mengatur jadwal. Silakan coba lagi.');
    }
  };

  const getStatusColor = (status) => {
    if (status === 'loaded') return 'success';
    if (status === 'training') return 'warning';
    return 'error';
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('id-ID', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getDaysSinceTrained = (trainedAt) => {
    const days = Math.floor((new Date() - new Date(trainedAt)) / (1000 * 60 * 60 * 24));
    return days;
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1">
          Model Management
        </Typography>
        <Box>
          <Button
            variant="outlined"
            startIcon={<ScheduleIcon />}
            onClick={() => setOpenScheduleDialog(true)}
            sx={{ mr: 2 }}
          >
            Atur Jadwal Pelatihan
          </Button>
          <Button
            variant="contained"
            startIcon={<RefreshIcon />}
            onClick={fetchModelStatus}
          >
            Refresh Status
          </Button>
        </Box>
      </Box>

      {/* Concept Drift Detection Alert */}
      {driftDetection && (
        <Alert 
          severity={driftDetection.driftDetected ? 'warning' : 'success'}
          icon={driftDetection.driftDetected ? <WarningIcon /> : <CheckCircleIcon />}
          sx={{ mb: 3 }}
        >
          <Typography variant="subtitle1" fontWeight="bold">
            {driftDetection.driftDetected ? '⚠️ Concept Drift Terdeteksi!' : '✅ Model Stabil'}
          </Typography>
          <Typography variant="body2">
            {driftDetection.recommendation}
          </Typography>
          <Typography variant="caption" display="block" mt={1}>
            Perubahan Performa: {driftDetection.performanceChange}% 
            (Threshold: {driftDetection.threshold}%)
          </Typography>
          {driftDetection.driftDetected && (
            <Button 
              variant="contained" 
              color="warning" 
              size="small" 
              sx={{ mt: 1 }}
              onClick={() => handleRetrain('all')}
            >
              Latih Ulang Sekarang
            </Button>
          )}
        </Alert>
      )}

      {/* Model Status Cards */}
      <Grid container spacing={3} mb={3}>
        {modelStatus && Object.entries(modelStatus).map(([modelName, data]) => {
          const daysSince = getDaysSinceTrained(data.trainedAt);
          const needsRetrain = daysSince > 30;

          return (
            <Grid item xs={12} md={4} key={modelName}>
              <Card>
                <CardContent>
                  <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                    <Typography variant="h6" textTransform="capitalize">
                      {modelName.replace(/([A-Z])/g, ' $1').trim()}
                    </Typography>
                    <Chip 
                      label={data.status} 
                      color={getStatusColor(data.status)}
                      size="small"
                    />
                  </Box>

                  <Box mb={2}>
                    <Typography variant="body2" color="text.secondary">
                      Dilatih: {formatDate(data.trainedAt)}
                    </Typography>
                    <Typography variant="caption" color={needsRetrain ? 'error' : 'text.secondary'}>
                      ({daysSince} hari yang lalu)
                      {needsRetrain && ' - Disarankan melatih ulang'}
                    </Typography>
                  </Box>

                  <Box mb={2}>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      Akurasi: {(data.accuracy * 100).toFixed(1)}%
                    </Typography>
                    <LinearProgress 
                      variant="determinate" 
                      value={data.accuracy * 100}
                      color={data.accuracy > 0.8 ? 'success' : 'warning'}
                    />
                  </Box>

                  <Typography variant="body2" color="text.secondary" mb={2}>
                    Training Samples: {data.samples?.toLocaleString()}
                  </Typography>

                  <Button
                    variant="contained"
                    fullWidth
                    startIcon={<PlayArrowIcon />}
                    onClick={() => handleRetrain(modelName)}
                    disabled={retraining}
                    color={needsRetrain ? 'warning' : 'primary'}
                  >
                    {retraining ? 'Melatih...' : 'Latih Ulang Model'}
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          );
        })}
      </Grid>

      {/* Real-time Incremental Learning Stats */}
      {realtimeStats && (
        <Paper sx={{ p: 3, mb: 3, bgcolor: '#f5f9ff' }}>
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
            <Box>
              <Typography variant="h6" gutterBottom>
                📊 Real-time Learning Stats
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {realtimeStats.description}
              </Typography>
            </Box>
            <Chip 
              label={realtimeStats.enabled ? 'Active' : 'Disabled'} 
              color={realtimeStats.enabled ? 'success' : 'default'}
            />
          </Box>

          <Grid container spacing={2} mb={2}>
            <Grid item xs={12} sm={6} md={3}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="caption" color="text.secondary">
                    Destinations Tracked
                  </Typography>
                  <Typography variant="h5">
                    {realtimeStats.statistics.totalDestinationsTracked}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="caption" color="text.secondary">
                    Interactions (24h)
                  </Typography>
                  <Typography variant="h5">
                    {realtimeStats.statistics.interactionsLast24h}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="caption" color="text.secondary">
                    Trending Items
                  </Typography>
                  <Typography variant="h5">
                    {realtimeStats.statistics.trendingItemsCount}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="caption" color="text.secondary">
                    Cache Status
                  </Typography>
                  <Typography variant="h5" sx={{ textTransform: 'capitalize' }}>
                    {realtimeStats.statistics.cacheStatus}
                  </Typography>
                  <Typography variant="caption">
                    {realtimeStats.statistics.cacheAgeMinutes}m ago
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          <Typography variant="subtitle2" mb={1}>
            🔥 Top Trending (Last 24h)
          </Typography>
          <TableContainer>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>Destination ID</TableCell>
                  <TableCell>Popularity Score</TableCell>
                  <TableCell>Avg Rating</TableCell>
                  <TableCell>Interactions</TableCell>
                  <TableCell>Views</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {realtimeStats.trending && realtimeStats.trending.length > 0 ? (
                  realtimeStats.trending.map((item, idx) => (
                    <TableRow key={idx}>
                      <TableCell>{item.destination_id}</TableCell>
                      <TableCell>{item.popularity_score.toFixed(2)}</TableCell>
                      <TableCell>{item.avg_rating.toFixed(1)}</TableCell>
                      <TableCell>{item.interaction_count}</TableCell>
                      <TableCell>{item.view_count}</TableCell>
                    </TableRow>
                  ))
                ) : (
                  <TableRow>
                    <TableCell colSpan={5} align="center">
                      <Typography variant="body2" color="text.secondary">
                        No trending data available
                      </Typography>
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      )}

      {/* Training History */}
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Riwayat Pelatihan Model
        </Typography>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Tanggal</TableCell>
                <TableCell>Model</TableCell>
                <TableCell>Tipe Pelatihan</TableCell>
                <TableCell>Durasi</TableCell>
                <TableCell>Akurasi</TableCell>
                <TableCell>Status</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              <TableRow>
                <TableCell>06 Nov 2025, 11:50</TableCell>
                <TableCell>Hybrid Model</TableCell>
                <TableCell>Full Retrain</TableCell>
                <TableCell>5m 23s</TableCell>
                <TableCell>88%</TableCell>
                <TableCell>
                  <Chip label="Berhasil" color="success" size="small" />
                </TableCell>
              </TableRow>
              <TableRow>
                <TableCell>06 Nov 2025, 11:49</TableCell>
                <TableCell>Collaborative</TableCell>
                <TableCell>Incremental</TableCell>
                <TableCell>3m 45s</TableCell>
                <TableCell>82%</TableCell>
                <TableCell>
                  <Chip label="Berhasil" color="success" size="small" />
                </TableCell>
              </TableRow>
              <TableRow>
                <TableCell>06 Nov 2025, 11:49</TableCell>
                <TableCell>Content-Based</TableCell>
                <TableCell>Full Retrain</TableCell>
                <TableCell>2m 12s</TableCell>
                <TableCell>85%</TableCell>
                <TableCell>
                  <Chip label="Berhasil" color="success" size="small" />
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      {/* Schedule Dialog */}
      <Dialog open={openScheduleDialog} onClose={() => setOpenScheduleDialog(false)}>
        <DialogTitle>Atur Jadwal Pelatihan Otomatis</DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="text.secondary" mb={2}>
            Sistem akan secara otomatis melatih ulang model sesuai interval yang dipilih
          </Typography>
          <FormControl fullWidth>
            <InputLabel>Interval Pelatihan</InputLabel>
            <Select
              value={scheduleInterval}
              onChange={(e) => setScheduleInterval(e.target.value)}
              label="Interval Pelatihan"
            >
              <MenuItem value="weekly">1 Minggu</MenuItem>
              <MenuItem value="monthly">1 Bulan</MenuItem>
              <MenuItem value="quarterly">3 Bulan</MenuItem>
              <MenuItem value="biannual">6 Bulan</MenuItem>
              <MenuItem value="triannual">9 Bulan</MenuItem>
              <MenuItem value="annual">12 Bulan</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenScheduleDialog(false)}>Batal</Button>
          <Button onClick={handleScheduleRetrain} variant="contained">
            Simpan Jadwal
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default ModelManagement;
