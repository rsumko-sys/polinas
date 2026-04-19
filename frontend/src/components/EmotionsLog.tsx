import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface EmotionLog {
  id: string;
  date: string;
  horse: string;
  startEmotion: string;
  endEmotion: string;
  notes: string;
}

const INITIAL_LOGS: EmotionLog[] = [
  {
    id: '1',
    date: '2026-04-18',
    horse: 'Midnight Storm',
    startEmotion: 'Втома',
    endEmotion: 'Ейфорія',
    notes: 'Дивовижне відчуття єднання на галопі.'
  },
  {
    id: '2',
    date: '2026-04-15',
    horse: 'Silver Luna',
    startEmotion: 'Стрес',
    endEmotion: 'Спокій',
    notes: 'Кобила дуже чутливо реагувала на мій стан, допомогла заспокоїтись.'
  }
];

const EmotionsLog: React.FC = () => {
  const [logs, setLogs] = useState<EmotionLog[]>(INITIAL_LOGS);
  const [view, setView] = useState<'form' | 'archive'>('form');
  const [formData, setFormData] = useState({
    date: new Date().toISOString().split('T')[0],
    horse: 'Midnight Storm',
    startEmotion: 'Спокій',
    endEmotion: 'Радість',
    notes: ''
  });

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    const newLog: EmotionLog = {
      id: Math.random().toString(36).substr(2, 9),
      ...formData
    };
    setLogs([newLog, ...logs]);
    setView('archive');
  };

  return (
    <div style={{ padding: '1rem', maxWidth: '800px', margin: '0 auto' }}>
      {/* Navigation Tabs */}
      <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem', justifyContent: 'center' }}>
        <button 
          onClick={() => setView('form')}
          style={navBtnStyle(view === 'form')}
        >
          Записати Стан
        </button>
        <button 
          onClick={() => setView('archive')}
          style={navBtnStyle(view === 'archive')}
        >
          Архів Сувоїв
        </button>
      </div>

      <AnimatePresence mode="wait">
        {view === 'form' ? (
          <motion.div 
            key="form"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
            className="glass-panel"
            style={{ padding: '2.5rem' }}
          >
            <h2 className="gothic-title" style={{ textAlign: 'center', marginBottom: '2rem', fontSize: '2rem' }}>Фіксація Емоцій</h2>
            
            <form onSubmit={handleSave} style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem' }}>
                <div className="form-group">
                  <label style={labelStyle}>Дата</label>
                  <input 
                    type="date" 
                    value={formData.date}
                    onChange={e => setFormData({...formData, date: e.target.value})}
                    style={inputStyle} 
                  />
                </div>
                <div className="form-group">
                  <label style={labelStyle}>Кінь</label>
                  <select 
                    value={formData.horse}
                    onChange={e => setFormData({...formData, horse: e.target.value})}
                    style={inputStyle}
                  >
                    <option>Midnight Storm</option>
                    <option>Golden Helios</option>
                    <option>Silver Luna</option>
                  </select>
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem' }}>
                <div className="form-group">
                  <label style={labelStyle}>Емоції на початку</label>
                  <select 
                    value={formData.startEmotion}
                    onChange={e => setFormData({...formData, startEmotion: e.target.value})}
                    style={inputStyle}
                  >
                    <option>Спокій</option>
                    <option>Стрес</option>
                    <option>Втома</option>
                    <option>Тривога</option>
                    <option>Ейфорія</option>
                  </select>
                </div>
                <div className="form-group">
                  <label style={labelStyle}>Емоції в кінці</label>
                  <select 
                    value={formData.endEmotion}
                    onChange={e => setFormData({...formData, endEmotion: e.target.value})}
                    style={inputStyle}
                  >
                    <option>Радість</option>
                    <option>Спокій</option>
                    <option>Ейфорія</option>
                    <option>Втома</option>
                    <option>Натхнення</option>
                  </select>
                </div>
              </div>

              <div className="form-group">
                <label style={labelStyle}>Як цей кінь вплинув на ваш стан сьогодні?</label>
                <textarea 
                  rows={4}
                  value={formData.notes}
                  onChange={e => setFormData({...formData, notes: e.target.value})}
                  placeholder="Опишіть магію моменту..."
                  style={{...inputStyle, resize: 'vertical'}} 
                />
              </div>

              <button type="submit" className="gothic-action-btn">ЗАПИСАТИ В СУВІЙ</button>
            </form>
          </motion.div>
        ) : (
          <motion.div 
            key="archive"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}
          >
            <h2 className="gothic-title" style={{ textAlign: 'center', marginBottom: '1rem', fontSize: '2.5rem' }}>Архів Емоцій</h2>
            
            {logs.map(log => (
              <motion.div 
                key={log.id}
                whileHover={{ scale: 1.02 }}
                className="glass-panel"
                style={{ 
                  padding: '1.5rem', 
                  borderLeft: '4px solid #d4af37', 
                  background: 'rgba(15,15,15,0.8)',
                  position: 'relative',
                  overflow: 'hidden'
                }}
              >
                {/* Scroll Aesthetic Background */}
                <div style={{ position: 'absolute', top: 0, right: 0, bottom: 0, width: '100px', background: 'linear-gradient(to right, transparent, rgba(212, 175, 55, 0.05))', pointerEvents: 'none' }} />
                
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem', borderBottom: '1px solid #333', paddingBottom: '0.5rem' }}>
                  <span className="cinzel-text" style={{ color: '#d4af37' }}>{log.date}</span>
                  <span className="gothic-title" style={{ fontSize: '1.2rem' }}>Кінь: {log.horse}</span>
                </div>

                <div style={{ display: 'flex', gap: '2rem', alignItems: 'center' }}>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '0.7rem', color: '#666', textTransform: 'uppercase' }}>Початок</div>
                    <div className="cinzel-text" style={{ color: '#aaa' }}>{log.startEmotion}</div>
                  </div>
                  <div style={{ fontSize: '1.5rem', color: '#d4af37' }}>→</div>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '0.7rem', color: '#666', textTransform: 'uppercase' }}>Фінал</div>
                    <div className="cinzel-text" style={{ color: '#fff' }}>{log.endEmotion}</div>
                  </div>
                  <div style={{ flex: 1, paddingLeft: '1rem', borderLeft: '1px solid #222', fontStyle: 'italic', color: '#888' }}>
                    {log.notes}
                  </div>
                </div>
              </motion.div>
            ))}
          </motion.div>
        )}
      </AnimatePresence>

      <style>{`
        .gothic-action-btn {
          background: rgba(255,255,255,0.1);
          border: 1px solid #d4af37;
          color: #d4af37;
          padding: 1.5rem;
          font-family: var(--cinzel-font);
          font-size: 1.2rem;
          letter-spacing: 2px;
          cursor: pointer;
          border-radius: 12px;
          transition: all 0.3s;
        }
        .gothic-action-btn:hover {
          background: #d4af37;
          color: #000;
        }
      `}</style>
    </div>
  );
};

const inputStyle = {
  width: '100%',
  padding: '1.2rem',
  marginTop: '0.5rem',
  background: 'rgba(0,0,0,0.6)',
  border: '1px solid rgba(255,255,255,0.1)',
  color: 'white',
  borderRadius: '12px',
  fontSize: '1rem',
  fontFamily: 'var(--cinzel-font)',
  outline: 'none'
};

const labelStyle = {
  fontSize: '0.85rem',
  color: '#888',
  textTransform: 'uppercase' as const,
  letterSpacing: '1px'
};

const navBtnStyle = (active: boolean) => ({
  background: active ? '#d4af37' : 'rgba(255,255,255,0.05)',
  border: active ? '1px solid #d4af37' : '1px solid rgba(255,255,255,0.1)',
  color: active ? '#000' : '#888',
  padding: '0.8rem 1.5rem',
  borderRadius: '8px',
  cursor: 'pointer',
  fontFamily: 'var(--cinzel-font)',
  transition: 'all 0.3s'
});

export default EmotionsLog;
