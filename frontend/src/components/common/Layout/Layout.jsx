import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../../../hooks/useAuth';
import { FiHome, FiUpload, FiClock, FiLogOut, FiUser } from 'react-icons/fi';
import './Layout.css';

const Layout = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <div className="layout">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <h1 className="sidebar-logo">CEV</h1>
          <span className="sidebar-title">Equipment Visualizer</span>
        </div>

        <nav className="sidebar-nav">
          <NavLink to="/" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`} end>
            <FiHome className="nav-icon" />
            <span>Dashboard</span>
          </NavLink>
          <NavLink to="/upload" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
            <FiUpload className="nav-icon" />
            <span>Upload Data</span>
          </NavLink>
          <NavLink to="/history" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
            <FiClock className="nav-icon" />
            <span>History</span>
          </NavLink>
        </nav>

        <div className="sidebar-footer">
          <div className="user-info">
            <FiUser className="user-icon" />
            <span className="username">{user?.username || 'User'}</span>
          </div>
          <button className="logout-btn" onClick={handleLogout}>
            <FiLogOut />
            <span>Logout</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;
