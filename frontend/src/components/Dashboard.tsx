import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import SessionIngest from './SessionIngest';
import TrainingAnalysis from './TrainingAnalysis';
import TrainingPlan from './TrainingPlan';
import RouteTracker from './RouteTracker';
import EmotionsLog from './EmotionsLog';
import WeatherTracker from './WeatherTracker';
import ClubsList from './ClubsList';
import HorseProfile from './HorseProfile';
import SensorTracker from './SensorTracker';
import { useTranslation } from '../i18n';

const RUNES = [
  { id: 'route', titleKey: 'route.title', icon: 'R' },
  { id: 'weather', titleKey: 'weather.title', icon: 'S' },
  { id: 'analysis', titleKey: 'analysis.title', icon: 'F' },
  { id: 'plan', titleKey: 'plan.title', icon: 'G' },
  { id: 'horse', titleKey: 'horse.title', icon: 'E' },
  { id: 'notes1', titleKey: 'notes.title', icon: 'M' },
  { id: 'sensors', titleKey: 'sensors.title', icon: 'L' },
  { id: 'clubs', titleKey: 'clubs.title', icon: 'T' },
];

const Dashboard: React.FC = () => {
  const [activeRune, setActiveRune] = useState<string | null>(null);
  const { t, lang, setLang } = useTranslation();
  const [currentTime, setCurrentTime] = useState(new Date());
  const [stopwatchTime, setStopwatchTime] = useState(0);
  const [isStopwatchRunning, setIsStopwatchRunning] = useState(false);
  const [showStopwatch, setShowStopwatch] = useState(false);
  const [showApiModal, setShowApiModal] = useState(false);
  const [tempApiKey, setTempApiKey] = useState(localStorage.getItem('openai_api_key') || '');
  const [saveStatus, setSaveStatus] = useState(false);
  const [hasApiKey, setHasApiKey] = useState(Boolean(localStorage.getItem('openai_api_key')));
  const [oracleInput, setOracleInput] = useState('');
  const [oracleResponse, setOracleResponse] = useState('');
  const [isOracleLoading, setIsOracleLoading] = useState(false);

  React.useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 60000);
    return () => clearInterval(timer);
  }, []);

  React.useEffect(() => {
    let interval: any;
    if (isStopwatchRunning) {
      // Оновлюємо кожні 10мс для мілісекунд
      interval = setInterval(() => setStopwatchTime(prev => prev + 10), 10);
    }
    return () => clearInterval(interval);
  }, [isStopwatchRunning]);

  const formatStopwatch = (ms: number) => {
    const hrs = Math.floor(ms / 3600000);
    const mins = Math.floor((ms % 3600000) / 60000);
    const secs = Math.floor((ms % 60000) / 1000);
    const msecs = Math.floor((ms % 1000) / 10);
    
    return `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}.${msecs.toString().padStart(2, '0')}`;
  };

  const renderActiveRuneComponent = () => {
    switch (activeRune) {
      case 'route':
        return <RouteTracker />;
      case 'weather':
        return <WeatherTracker />;
      case 'emotions':
        return <EmotionsLog />;
      case 'notes1':
        return <SessionIngest />;
      case 'analysis':
        return <TrainingAnalysis />;
      case 'plan':
        return <TrainingPlan />;
      case 'horse':
        return <HorseProfile />;
      case 'notes1':
        return <SessionIngest />;
      case 'sensors':
        return <SensorTracker />;
      case 'clubs':
        return <ClubsList />;
      default:
        return (
          <div className="glass-panel" style={{ padding: '2rem', textAlign: 'center', marginTop: '2rem', maxWidth: '600px', margin: '2rem auto 0' }}>
            <h2 className="cinzel-text">{t('dashboard.hidden')}</h2>
            <p style={{ color: '#888', marginTop: '1rem' }}>{t('dashboard.magic')}</p>
          </div>
        );
    }
  };

  return (
    <div style={{ paddingTop: '3rem', paddingBottom: '3rem', minHeight: '100vh', position: 'relative' }}>
      
      {/* Language Switcher */}
      <div style={{ position: 'absolute', top: '1rem', right: '1rem', display: 'flex', gap: '0.5rem', zIndex: 100, alignItems: 'center' }}>
        <button 
          onClick={() => setShowStopwatch(!showStopwatch)} 
          style={{...langBtnStyle(showStopwatch), fontSize: '0.65rem', fontWeight: 'bold', minWidth: '40px', borderColor: '#d4af37', color: '#d4af37'}}
        >
          {t('stopwatch.btn')}
        </button>
        <button 
          onClick={() => setShowApiModal(true)} 
          style={{...langBtnStyle(false), fontSize: '0.65rem', fontWeight: 'bold', minWidth: '40px', borderColor: '#4ecdc4', color: '#4ecdc4'}}
        >
          {t('api.btn')}
        </button>
        <div style={{ width: '1px', height: '20px', background: 'rgba(255,255,255,0.1)', margin: '0 0.5rem' }} />
        <button onClick={() => setLang('uk')} style={langBtnStyle(lang === 'uk')}>UK</button>
        <button onClick={() => setLang('en')} style={langBtnStyle(lang === 'en')}>EN</button>
        <button onClick={() => {
          setLang('witch');
          const audio = new Audio('/assets/witch_laugh.mp3');
          audio.volume = 0.5;
          audio.play().catch(e => console.log("Audio play blocked:", e));
        }} style={langBtnStyle(lang === 'witch')}>🔮</button>
      </div>

      <header style={{ textAlign: 'center', marginBottom: '4rem' }}>
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
          onClick={() => setActiveRune(null)}
          style={{ cursor: 'pointer' }}
        >
          {/* Logo container */}
          <div style={{ 
            width: '150px', 
            height: '150px', 
            margin: '0 auto 1.5rem',
            backgroundImage: 'url(/assets/logo.png)',
            backgroundSize: 'contain',
            backgroundRepeat: 'no-repeat',
            backgroundPosition: 'center',
            filter: 'drop-shadow(0 0 10px rgba(255,255,255,0.2))'
          }}>
             <span style={{ display: 'none' }}>Logo</span>
          </div>
          
          <h1 className="gothic-title" style={{ fontSize: '3.5rem', marginBottom: '0.5rem' }}>Polina's Diaries</h1>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.2rem' }}>
             <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                <span style={{ fontSize: '1.5rem', filter: 'drop-shadow(0 0 8px #fff)' }}>{getMoonIcon()}</span>
                <p className="cinzel-text" style={{ fontSize: '1.1rem', color: '#fff', letterSpacing: '3px', margin: 0 }}>
                  {currentTime.toLocaleDateString('uk-UA')} • {currentTime.toLocaleTimeString('uk-UA', { hour: '2-digit', minute: '2-digit' })}
                </p>
             </div>
             <p className="cinzel-text" style={{ fontSize: '0.75rem', color: '#d4af37', letterSpacing: '5px', margin: 0, opacity: 0.8, textTransform: 'uppercase' }}>
               {getMoonPhaseName(t)}
             </p>
             <p className="cinzel-text" style={{ fontSize: '0.6rem', color: '#555', letterSpacing: '3px', marginTop: '0.5rem', margin: 0 }}>
               {t('dashboard.subtitle')}
             </p>

             {/* Oracle Command Line */}
             <AnimatePresence>
               {hasApiKey && (
                 <motion.div 
                   initial={{ opacity: 0, y: 10 }}
                   animate={{ opacity: 1, y: 0 }}
                   style={{ marginTop: '2.5rem', width: '100%', maxWidth: '800px' }}
                 >
                   <div style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
                     <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(78, 205, 196, 0.3)', padding: '1rem 1.5rem', borderRadius: '12px' }}>
                       <span style={{ color: '#4ecdc4', fontFamily: 'var(--cinzel-font)', fontSize: '1rem', fontWeight: 'bold', letterSpacing: '2px' }}>{t('oracle.title')} &gt;</span>
                       <input 
                         value={oracleInput}
                         onChange={(e) => setOracleInput(e.target.value)}
                         onKeyDown={async (e) => {
                           if (e.key === 'Enter' && oracleInput.trim()) {
                             setIsOracleLoading(true);
                             setOracleResponse('');
                             try {
                               const res = await fetch('http://localhost:8000/oracle/ask', {
                                 method: 'POST',
                                 headers: { 
                                   'Content-Type': 'application/json',
                                   'X-OpenAI-Key': localStorage.getItem('openai_api_key') || ''
                                 },
                                 body: JSON.stringify({ question: oracleInput })
                               });
                               const data = await res.json();
                               setOracleResponse(data.answer);
                               setOracleInput('');
                             } catch (err) {
                               setOracleResponse('Енергія перервана...');
                             } finally {
                               setIsOracleLoading(false);
                             }
                           }
                         }}
                         placeholder={t('oracle.placeholder')}
                         style={{
                           flex: 1, background: 'transparent', border: 'none', color: '#fff',
                           fontFamily: 'var(--main-font)', fontSize: '1.1rem', outline: 'none'
                         }}
                       />
                     </div>
                     <AnimatePresence>
                       {(oracleResponse || isOracleLoading) && (
                         <motion.div 
                           initial={{ opacity: 0, height: 0 }}
                           animate={{ opacity: 1, height: 'auto' }}
                           exit={{ opacity: 0, height: 0 }}
                           style={{ padding: '1rem 1.5rem', color: '#ccc', fontStyle: 'italic', fontSize: '1rem', textAlign: 'left', borderLeft: '3px solid #4ecdc4', background: 'rgba(78, 205, 196, 0.05)', borderRadius: '0 8px 8px 0', lineHeight: '1.6' }}
                         >
                           {isOracleLoading ? t('oracle.loading') : oracleResponse}
                         </motion.div>
                       )}
                     </AnimatePresence>
                   </div>
                 </motion.div>
               )}
             </AnimatePresence>
          </div>

          {/* Elegant Stopwatch Widget */}
          <AnimatePresence>
            {showStopwatch && (
              <motion.div 
                initial={{ opacity: 0, height: 0, marginTop: 0 }}
                animate={{ opacity: 1, height: 'auto', marginTop: '2rem' }}
                exit={{ opacity: 0, height: 0, marginTop: 0 }}
                style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', overflow: 'hidden' }}
              >
                 <div style={{ 
                   background: 'rgba(255,255,255,0.03)', 
                   border: '1px solid rgba(255,255,255,0.1)',
                   padding: '1rem 2rem',
                   borderRadius: '50px',
                   display: 'flex',
                   alignItems: 'center',
                   gap: '1.5rem',
                   boxShadow: '0 0 20px rgba(0,0,0,0.3)'
                 }}>
                    <span className="cinzel-text" style={{ fontSize: '1.5rem', color: isStopwatchRunning ? '#d4af37' : '#fff', minWidth: '180px', textAlign: 'left' }}>
                      {formatStopwatch(stopwatchTime)}
                    </span>
                    <div style={{ display: 'flex', gap: '1rem' }}>
                       <motion.button 
                         whileTap={{ scale: 0.9 }}
                         onClick={() => setIsStopwatchRunning(!isStopwatchRunning)}
                         style={{ background: 'transparent', border: 'none', color: '#fff', fontSize: '1.2rem', cursor: 'pointer' }}
                       >
                         {isStopwatchRunning ? '⏸' : '▶'}
                       </motion.button>
                       <motion.button 
                         whileTap={{ scale: 0.9 }}
                         onClick={() => { setIsStopwatchRunning(false); setStopwatchTime(0); }}
                         style={{ background: 'transparent', border: 'none', color: '#666', fontSize: '1.2rem', cursor: 'pointer' }}
                       >
                         ↺
                       </motion.button>
                    </div>
                 </div>
                 <p style={{ fontSize: '0.6rem', color: '#555', marginTop: '0.5rem', letterSpacing: '2px', textTransform: 'uppercase' }}>{t('stopwatch.label')}</p>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      </header>

      <AnimatePresence mode="wait">
        {activeRune !== null ? (
          <motion.div
            key="content"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.3 }}
          >
            <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
              <button 
                onClick={() => setActiveRune(null)}
                style={{
                  background: 'transparent',
                  border: 'none',
                  color: 'var(--text-secondary)',
                  fontFamily: 'var(--cinzel-font)',
                  cursor: 'pointer',
                  textDecoration: 'underline'
                }}
              >
                {t('dashboard.back')}
              </button>
            </div>
            {renderActiveRuneComponent()}
          </motion.div>
        ) : (
          <motion.div
            key="grid"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="rune-grid"
          >
            {RUNES.map((rune, index) => (
              <motion.div
                key={rune.id}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: index * 0.1 }}
                onClick={() => {
                  if (rune.id === 'route') {
                    try {
                      const audio = new Audio('/assets/hooves_v2.m4a');
                      audio.volume = 0.4;
                      audio.play().catch(e => console.log("Audio play blocked or failed:", e));
                      
                      // Обмежуємо звучання до 5 секунд
                      setTimeout(() => {
                        audio.pause();
                        audio.currentTime = 0;
                      }, 5000);
                    } catch (err) {
                      console.error("Audio creation failed:", err);
                    }
                  }
                  setActiveRune(rune.id);
                }}
              >
                <div className="glass-panel rune-card">
                  <div 
                    className="rune-icon-container"
                    style={{
                      backgroundImage: `url(/assets/icon_${rune.id}.png)`,
                      backgroundSize: 'contain',
                      backgroundRepeat: 'no-repeat',
                      backgroundPosition: 'center'
                    }}
                  >
                    <span className="gothic-title" style={{ opacity: 0.5 }}>{rune.icon}</span>
                  </div>
                  <h2 className="rune-title">{t(rune.titleKey)}</h2>
                </div>
              </motion.div>
            ))}
          </motion.div>
        )}
      </AnimatePresence>

      {/* API Modal */}
      <AnimatePresence>
        {showApiModal && (
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            style={{
              position: 'fixed', top: 0, left: 0, width: '100%', height: '100%',
              background: 'rgba(0,0,0,0.8)', backdropFilter: 'blur(10px)',
              display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1000
            }}
          >
            <motion.div 
              initial={{ scale: 0.9, y: 20 }}
              animate={{ scale: 1, y: 0 }}
              className="glass-panel"
              style={{ padding: '2.5rem', width: '90%', maxWidth: '500px', textAlign: 'center' }}
            >
              <h2 className="gothic-title" style={{ fontSize: '1.8rem', color: '#4ecdc4', marginBottom: '1.5rem' }}>
                {t('api.modal_title')}
              </h2>
              <input 
                type="password"
                value={tempApiKey}
                onChange={(e) => setTempApiKey(e.target.value)}
                placeholder={t('api.placeholder')}
                style={{
                  width: '100%', padding: '1rem', background: 'rgba(255,255,255,0.05)',
                  border: '1px solid rgba(78, 205, 196, 0.3)', borderRadius: '8px',
                  color: '#fff', fontFamily: 'monospace', marginBottom: '2rem', textAlign: 'center'
                }}
              />
              <div style={{ display: 'flex', gap: '1.5rem', justifyContent: 'center' }}>
                <button 
                  onClick={() => {
                    localStorage.setItem('openai_api_key', tempApiKey);
                    setHasApiKey(Boolean(tempApiKey));
                    setSaveStatus(true);
                    setTimeout(() => {
                      setSaveStatus(false);
                      setShowApiModal(false);
                    }, 1000);
                  }}
                  style={{
                    background: '#4ecdc4', color: '#000', border: 'none',
                    padding: '1rem 2rem', borderRadius: '8px', cursor: 'pointer',
                    fontFamily: 'var(--cinzel-font)', fontWeight: 'bold', fontSize: '1rem',
                    transition: 'all 0.3s', boxShadow: '0 0 15px rgba(78, 205, 196, 0.4)'
                  }}
                >
                  {saveStatus ? t('api.status_saved') : t('api.save')}
                </button>
                <button 
                  onClick={() => setShowApiModal(false)}
                  style={{
                    background: 'rgba(255,255,255,0.05)', color: '#888', border: '1px solid #444',
                    padding: '1rem 2rem', borderRadius: '8px', cursor: 'pointer',
                    fontFamily: 'var(--cinzel-font)', fontSize: '1rem', transition: 'all 0.3s'
                  }}
                >
                  {t('api.cancel')}
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

const langBtnStyle = (active: boolean) => ({
  background: active ? 'rgba(255,255,255,0.2)' : 'transparent',
  border: '1px solid rgba(255,255,255,0.3)',
  color: '#fff',
  padding: '0.3rem 0.6rem',
  cursor: 'pointer',
  fontFamily: 'var(--cinzel-font)',
  borderRadius: '4px'
});

const getMoonIcon = () => {
  const day = new Date().getDate() % 30;
  if (day < 2) return '🌑';
  if (day < 7) return '🌒';
  if (day < 14) return '🌓';
  if (day < 17) return '🌕';
  if (day < 22) return '🌗';
  return '🌘';
};

const getMoonPhaseName = (t: any) => {
  const day = new Date().getDate() % 30;
  if (day < 2) return t('moon.new_moon');
  if (day < 7) return t('moon.waxing_crescent');
  if (day < 14) return t('moon.first_quarter');
  if (day < 17) return t('moon.full_moon');
  if (day < 22) return t('moon.last_quarter');
  return t('moon.waning_crescent');
};

export default Dashboard;
