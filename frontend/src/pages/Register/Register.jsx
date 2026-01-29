import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import toast from 'react-hot-toast';
import { FiUser, FiLock, FiMail, FiUserPlus } from 'react-icons/fi';
import '../Login/Login.css';

const Register = () => {
  const { register } = useAuth();
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    password_confirm: '',
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.username || !formData.email || !formData.password || !formData.password_confirm) {
      toast.error('Please fill in all fields');
      return;
    }

    if (formData.password !== formData.password_confirm) {
      toast.error('Passwords do not match');
      return;
    }

    if (formData.password.length < 8) {
      toast.error('Password must be at least 8 characters');
      return;
    }

    setLoading(true);
    try {
      const response = await register(formData);
      if (response.success) {
        toast.success('Registration successful!');
      } else {
        const errors = response.errors;
        if (errors) {
          const errorMessage = Object.values(errors).flat().join(', ');
          toast.error(errorMessage);
        } else {
          toast.error('Registration failed');
        }
      }
    } catch (error) {
      const errors = error.response?.data?.errors;
      if (errors) {
        const errorMessage = Object.values(errors).flat().join(', ');
        toast.error(errorMessage);
      } else {
        toast.error('Registration failed');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-container">
        <div className="auth-header">
          <h1 className="auth-logo">CEV</h1>
          <h2 className="auth-title">Create Account</h2>
          <p className="auth-subtitle">Sign up to get started</p>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Username</label>
            <div className="input-with-icon">
              <FiUser className="input-icon" />
              <input
                type="text"
                name="username"
                className="form-input"
                placeholder="Choose a username"
                value={formData.username}
                onChange={handleChange}
                disabled={loading}
              />
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Email</label>
            <div className="input-with-icon">
              <FiMail className="input-icon" />
              <input
                type="email"
                name="email"
                className="form-input"
                placeholder="Enter your email"
                value={formData.email}
                onChange={handleChange}
                disabled={loading}
              />
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Password</label>
            <div className="input-with-icon">
              <FiLock className="input-icon" />
              <input
                type="password"
                name="password"
                className="form-input"
                placeholder="Create a password"
                value={formData.password}
                onChange={handleChange}
                disabled={loading}
              />
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Confirm Password</label>
            <div className="input-with-icon">
              <FiLock className="input-icon" />
              <input
                type="password"
                name="password_confirm"
                className="form-input"
                placeholder="Confirm your password"
                value={formData.password_confirm}
                onChange={handleChange}
                disabled={loading}
              />
            </div>
          </div>

          <button type="submit" className="btn btn-primary auth-btn" disabled={loading}>
            {loading ? (
              <span className="loader-small"></span>
            ) : (
              <>
                <FiUserPlus />
                <span>Create Account</span>
              </>
            )}
          </button>
        </form>

        <p className="auth-footer">
          Already have an account? <Link to="/login">Sign in</Link>
        </p>
      </div>
    </div>
  );
};

export default Register;
