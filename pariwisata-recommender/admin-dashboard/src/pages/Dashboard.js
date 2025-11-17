import React, { useState, useEffect } from 'react';
import { Grid, Paper, Typography, Box, CircularProgress, Card, CardContent } from '@mui/material';
import { styled } from '@mui/material/styles';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import apiService from '../services/api';

// Custom styled components
const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
  ...theme.typography.body2,
  padding: theme.spacing(2),
  color: theme.palette.text.primary,
  height: '100%',
}));

const StatCard = styled(Card)(({ theme }) => ({
  backgroundColor: theme.palette.background.paper,
  borderRadius: theme.shape.borderRadius,
  boxShadow: theme.shadows[2],
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
}));

const StatValue = styled(Typography)(({ theme }) => ({
  fontSize: '2.5rem',
  fontWeight: 'bold',
  color: theme.palette.primary.main,
}));

export default function Dashboard() {
  const [stats, setStats] = useState({
    destinations: 0,
    activities: 0,
    users: 0,
    recommendations: 0,
  });
  const [activityData, setActivityData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        setError('');
        // Fetch stats from backend API
        const statsResponse = await apiService.getStats();
        setStats({
          destinations: statsResponse.data.totalDestinations || 0,
          activities: statsResponse.data.totalActivities || 0,
          users: statsResponse.data.totalUsers || 0,
          recommendations: statsResponse.data.totalRatings || 0,
          averageRating: statsResponse.data.averageRating || null,
        });
        // Fetch activity stats from backend
        const activityRes = await apiService.getActivityStats();
        setActivityData(activityRes.data);
      } catch (err) {
        console.error('Dashboard API Error:', err);
        setError('Failed to load dashboard data from backend. Showing demo data.');
        setStats({
          destinations: 45,
          activities: 78,
          users: 1243,
          recommendations: 8732,
          averageRating: 4.2,
        });
        setActivityData([
          { name: 'Jan', users: 400, recommendations: 240 },
          { name: 'Feb', users: 300, recommendations: 139 },
          { name: 'Mar', users: 200, recommendations: 980 },
          { name: 'Apr', users: 278, recommendations: 390 },
          { name: 'May', users: 189, recommendations: 480 },
          { name: 'Jun', users: 239, recommendations: 380 },
          { name: 'Jul', users: 349, recommendations: 430 },
        ]);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <>
      <Typography variant="h4" component="h1" gutterBottom>
        Dashboard
      </Typography>
      
      {error && (
        <Typography color="error" sx={{ mb: 2 }}>
          {error} - Showing demo data
        </Typography>
      )}
      
      <Grid container columns={12} spacing={4}>
        {/* Stats cards */}
        <Grid gridColumn="span 3">
          <StatCard>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Total Destinations
              </Typography>
              <StatValue>{stats.destinations}</StatValue>
            </CardContent>
          </StatCard>
        </Grid>
        <Grid gridColumn="span 3">
          <StatCard>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Total Activities
              </Typography>
              <StatValue>{stats.activities}</StatValue>
            </CardContent>
          </StatCard>
        </Grid>
        <Grid gridColumn="span 3">
          <StatCard>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Registered Users
              </Typography>
              <StatValue>{stats.users}</StatValue>
            </CardContent>
          </StatCard>
        </Grid>
        <Grid gridColumn="span 3">
          <StatCard>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Recommendations Made
              </Typography>
              <StatValue>{stats.recommendations}</StatValue>
              {stats.averageRating && (
                <Typography variant="body2" color="text.secondary">
                  Avg. Rating: {stats.averageRating}
                </Typography>
              )}
            </CardContent>
          </StatCard>
        </Grid>
        {/* Charts */}
        <Grid gridColumn="span 12">
          <Item>
            <Typography variant="h6" component="h2" gutterBottom>
              User Activity
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart
                data={activityData}
                margin={{
                  top: 5,
                  right: 30,
                  left: 20,
                  bottom: 5,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="users" fill="#8884d8" name="New Users" />
                <Bar dataKey="recommendations" fill="#82ca9d" name="Recommendations" />
              </BarChart>
            </ResponsiveContainer>
          </Item>
        </Grid>
      </Grid>
    </>
  );
}