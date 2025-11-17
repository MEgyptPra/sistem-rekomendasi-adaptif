import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  IconButton,
  CircularProgress,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';
import apiService from '../services/api';

export default function Destinations() {
  const [destinations, setDestinations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  // Pagination
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  
  // Dialog state
  const [openDialog, setOpenDialog] = useState(false);
  const [dialogType, setDialogType] = useState(''); // 'add', 'edit', 'delete'
  const [selectedDestination, setSelectedDestination] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    region: '',
    image: '',
  });
  
  // Regions (example data)
  const regions = [
    'Portland Region',
    'Mt. Hood & Columbia River Gorge',
    'Oregon Coast',
    'Willamette Valley',
    'Central Oregon',
    'Southern Oregon',
    'Eastern Oregon',
  ];

  useEffect(() => {
    const fetchDestinations = async () => {
      try {
        setLoading(true);
        
        // Fetch from backend API
        const response = await apiService.getDestinations();
        
        // Transform data to match component expectations  
        const transformedData = response.data.map(dest => ({
          id: dest.id,
          name: dest.name,
          description: dest.description,
          location: dest.location,
          region: dest.location || 'N/A',
          image: dest.image_url || null,
          price: dest.price || 0,
          created_at: dest.created_at
        }));
        
        setDestinations(transformedData);
        setError('');
      } catch (err) {
        console.error('Error fetching destinations:', err);
        setError('Failed to load destinations from backend. Showing demo data.');
        
        // Mock data as fallback
        setDestinations([
          { id: 1, name: 'Candi Borobudur', description: 'Candi Buddha terbesar di dunia', region: 'Magelang', image: null },
          { id: 2, name: 'Pantai Parangtritis', description: 'Pantai dengan legenda Ratu Kidul', region: 'Bantul', image: null },
          { id: 3, name: 'Keraton Yogyakarta', description: 'Istana Sultan Yogyakarta', region: 'Yogyakarta', image: null },
          { id: 4, name: 'Candi Prambanan', description: 'Candi Hindu terbesar di Indonesia', region: 'Sleman', image: null },
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchDestinations();
  }, []);

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleOpenDialog = (type, destination = null) => {
    setDialogType(type);
    setSelectedDestination(destination);
    
    if (type === 'edit' && destination) {
      setFormData({
        name: destination.name,
        description: destination.description,
        region: destination.region,
        image: destination.image,
      });
    } else if (type === 'add') {
      setFormData({
        name: '',
        description: '',
        region: '',
        image: '',
      });
    }
    
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  const handleFormChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async () => {
    try {
      if (dialogType === 'add') {
        // In a real app, send POST request to your FastAPI backend
        // const response = await axios.post('http://localhost:8000/admin/destinations', formData);
        
        // Mock implementation
        const newDestination = {
          id: destinations.length + 1,
          ...formData,
        };
        
        setDestinations([...destinations, newDestination]);
      } else if (dialogType === 'edit') {
        // In a real app, send PUT request to your FastAPI backend
        // const response = await axios.put(`http://localhost:8000/admin/destinations/${selectedDestination.id}`, formData);
        
        // Mock implementation
        const updatedDestinations = destinations.map(dest =>
          dest.id === selectedDestination.id ? { ...dest, ...formData } : dest
        );
        
        setDestinations(updatedDestinations);
      }
      
      handleCloseDialog();
    } catch (err) {
      setError('Operation failed');
    }
  };

  const handleDelete = async () => {
    try {
      // In a real app, send DELETE request to your FastAPI backend
      // await axios.delete(`http://localhost:8000/admin/destinations/${selectedDestination.id}`);
      
      // Mock implementation
      const filteredDestinations = destinations.filter(
        dest => dest.id !== selectedDestination.id
      );
      
      setDestinations(filteredDestinations);
      handleCloseDialog();
    } catch (err) {
      setError('Delete operation failed');
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={4}>
        <Typography variant="h4" component="h1">
          Destinations
        </Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog('add')}
        >
          Add Destination
        </Button>
      </Box>
      
      {error && (
        <Typography color="error" sx={{ mb: 2 }}>
          {error} - Showing demo data
        </Typography>
      )}
      
      <Paper sx={{ width: '100%', overflow: 'hidden' }}>
        <TableContainer sx={{ maxHeight: 440 }}>
          <Table stickyHeader aria-label="sticky table">
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>Name</TableCell>
                <TableCell>Region</TableCell>
                <TableCell>Description</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {destinations
                .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                .map((destination) => (
                  <TableRow hover key={destination.id}>
                    <TableCell>{destination.id}</TableCell>
                    <TableCell>{destination.name}</TableCell>
                    <TableCell>
                      <Chip label={destination.region} size="small" />
                    </TableCell>
                    <TableCell>{destination.description}</TableCell>
                    <TableCell>
                      <IconButton
                        color="primary"
                        size="small"
                        onClick={() => handleOpenDialog('edit', destination)}
                      >
                        <EditIcon />
                      </IconButton>
                      <IconButton
                        color="error"
                        size="small"
                        onClick={() => handleOpenDialog('delete', destination)}
                      >
                        <DeleteIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          rowsPerPageOptions={[10, 25, 100]}
          component="div"
          count={destinations.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </Paper>

      {/* Add/Edit Dialog */}
      <Dialog open={openDialog && (dialogType === 'add' || dialogType === 'edit')} onClose={handleCloseDialog}>
        <DialogTitle>{dialogType === 'add' ? 'Add New Destination' : 'Edit Destination'}</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            name="name"
            label="Destination Name"
            type="text"
            fullWidth
            variant="outlined"
            value={formData.name}
            onChange={handleFormChange}
          />
          <TextField
            margin="dense"
            name="description"
            label="Description"
            type="text"
            fullWidth
            multiline
            rows={4}
            variant="outlined"
            value={formData.description}
            onChange={handleFormChange}
          />
          <FormControl fullWidth margin="dense">
            <InputLabel>Region</InputLabel>
            <Select
              name="region"
              value={formData.region}
              onChange={handleFormChange}
              label="Region"
            >
              {regions.map((region) => (
                <MenuItem key={region} value={region}>
                  {region}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <TextField
            margin="dense"
            name="image"
            label="Image URL"
            type="text"
            fullWidth
            variant="outlined"
            value={formData.image}
            onChange={handleFormChange}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSubmit} variant="contained" color="primary">
            {dialogType === 'add' ? 'Add' : 'Save'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog open={openDialog && dialogType === 'delete'} onClose={handleCloseDialog}>
        <DialogTitle>Delete Destination</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to delete "{selectedDestination?.name}"? This action cannot be undone.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleDelete} variant="contained" color="error">
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}