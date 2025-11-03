import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import '../styles/auth.css';

const Register = () => {
  const navigate = useNavigate();
  const { register } = useAuth();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    preferences: [],
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const categoryOptions = [
    { value: 'alam', label: 'Wisata Alam' },
    { value: 'kuliner', label: 'Kuliner' },
    { value: 'budaya', label: 'Budaya & Sejarah' },
    { value: 'religi', label: 'Wisata Religi' },
    { value: 'edukasi', label: 'Edukasi' },
  ];

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    setError('');
  };

  const handlePreferenceChange = (value) => {
    const preferences = formData.preferences.includes(value)
      ? formData.preferences.filter(p => p !== value)
      : [...formData.preferences, value];
    
    setFormData({ ...formData, preferences });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // Validation
    if (formData.password !== formData.confirmPassword) {
      setError('Password tidak cocok');
      return;
    }

    if (formData.password.length < 6) {
      setError('Password minimal 6 karakter');
      return;
    }

    setLoading(true);

    const preferencesString = formData.preferences.join(',');
    const result = await register(
      formData.name,
      formData.email,
      formData.password,
      preferencesString
    );

    if (result.success) {
      navigate('/');
    } else {
      setError(result.error);
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-container">
        <div className="auth-card">
          <div className="auth-header">
            <h1>Daftar Akun</h1>
            <p>Bergabunglah dengan Wisata Sumedang</p>
          </div>

          {error && (
            <div className="error-alert">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="auth-form">
            <div className="form-group">
              <label htmlFor="name">Nama Lengkap</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="Masukkan nama lengkap"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="nama@email.com"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="Minimal 6 karakter"
                required
                minLength={6}
              />
            </div>

            <div className="form-group">
              <label htmlFor="confirmPassword">Konfirmasi Password</label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                placeholder="Masukkan password lagi"
                required
                minLength={6}
              />
            </div>

            <div className="form-group">
              <label>Preferensi Wisata (Opsional)</label>
              <p className="form-help">Pilih jenis wisata yang Anda minati</p>
              <div className="checkbox-group">
                {categoryOptions.map((option) => (
                  <label key={option.value} className="checkbox-label">
                    <input
                      type="checkbox"
                      value={option.value}
                      checked={formData.preferences.includes(option.value)}
                      onChange={() => handlePreferenceChange(option.value)}
                    />
                    <span>{option.label}</span>
                  </label>
                ))}
              </div>
            </div>

            <button 
              type="submit" 
              className="btn-primary btn-full"
              disabled={loading}
            >
              {loading ? 'Memproses...' : 'Daftar Sekarang'}
            </button>
          </form>

          <div className="auth-footer">
            <p>
              Sudah punya akun?{' '}
              <Link to="/login">Masuk di sini</Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;
