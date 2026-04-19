import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import SplashScreen from './components/SplashScreen';
import Dashboard from './components/Dashboard';
import { I18nProvider } from './i18n';

function App() {
  const [showSplash, setShowSplash] = useState(true);

  // Імітація завантаження або очікування натискання
  useEffect(() => {
    // В реальному житті заставка може зникати по кліку або через деякий час
    const timer = setTimeout(() => {
      // Можемо залишити заставку поки користувач не клікне, 
      // але для демо зробимо авто-перехід через 4 секунди
      // setShowSplash(false);
    }, 4000);
    return () => clearTimeout(timer);
  }, []);

  return (
    <I18nProvider>
      <Router>
        <div className="app-container">
          {showSplash ? (
            <SplashScreen onEnter={() => setShowSplash(false)} />
          ) : (
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          )}
        </div>
      </Router>
    </I18nProvider>
  );
}

export default App;
