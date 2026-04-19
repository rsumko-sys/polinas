import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useTranslation } from '../i18n';

const SessionIngest: React.FC = () => {
  const { t } = useTranslation();
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    
    const formData = new FormData(e.currentTarget);
    
    // Send to backend
    try {
      const response = await fetch('http://localhost:8000/ingest/session', {
        method: 'POST',
        headers: {
          'X-OpenAI-Key': localStorage.getItem('openai_api_key') || ''
        },
        body: formData,
      });
      
      if (response.ok) {
        setSuccess(true);
        e.currentTarget.reset();
      }
    } catch (error) {
      console.error('Failed to submit session:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-panel"
      style={{ padding: '2rem', maxWidth: '600px', margin: '0 auto', marginTop: '2rem' }}
    >
      <h2 className="gothic-title" style={{ marginBottom: '1.5rem', textAlign: 'center' }}>Новий Запис Тренування</h2>
      
      {success ? (
        <div style={{ textAlign: 'center', padding: '2rem', color: '#4caf50' }}>
          <h3 className="cinzel-text">Запис успішно створено!</h3>
          <p style={{ marginTop: '1rem' }}>Магія AI вже працює над аналізом та створенням плану.</p>
          <button 
            onClick={() => setSuccess(false)}
            style={{
              marginTop: '2rem',
              padding: '0.5rem 2rem',
              background: 'transparent',
              border: '1px solid var(--border-color)',
              color: 'var(--text-primary)',
              cursor: 'pointer'
            }}
          >
            Створити ще
          </button>
        </div>
      ) : (
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1.5rem' }}>
            <div className="form-group">
              <label style={labelStyle}>Назва сесії</label>
              <input name="title" required defaultValue="Тренування" style={inputStyle} />
            </div>
            <div className="form-group">
              <label style={labelStyle}>Дата</label>
              <input name="date" type="datetime-local" required defaultValue={new Date().toISOString().slice(0, 16)} style={inputStyle} />
            </div>
          </div>
          
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1.5rem' }}>
            <div className="form-group">
              <label style={labelStyle}>Кінь</label>
              <input name="horse" required defaultValue="Zvezda" style={inputStyle} />
            </div>
            <div className="form-group">
              <label style={labelStyle}>Тип</label>
              <select name="type" required style={inputStyle}>
                <option value="flat">Flat work (Манеж)</option>
                <option value="jumping">Jumping (Конкур)</option>
                <option value="field">Польові</option>
              </select>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '1.5rem' }}>
            <div className="form-group">
              <label style={labelStyle}>Тривалість (хв)</label>
              <input name="duration_min" type="number" required defaultValue={45} style={inputStyle} />
            </div>
            <div className="form-group">
              <label style={labelStyle}>Відстань (км)</label>
              <input name="distance_km" type="number" step="0.1" required defaultValue={5.0} style={inputStyle} />
            </div>
            <div className="form-group">
              <label style={labelStyle}>Ср. Швидкість</label>
              <input name="avg_speed" type="number" step="0.1" required defaultValue={10.0} style={inputStyle} />
            </div>
            <div className="form-group">
              <label style={labelStyle}>Макс. Швидкість</label>
              <input name="max_speed" type="number" step="0.1" required defaultValue={25.0} style={inputStyle} />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1.5rem' }}>
            <div className="form-group">
              <label style={labelStyle}>Відчуття (Feeling)</label>
              <select name="feeling" required style={inputStyle}>
                <option value="bad">Погано</option>
                <option value="ok" selected>Норм</option>
                <option value="good">Добре</option>
                <option value="strong">Супер</option>
              </select>
            </div>
            <div className="form-group">
              <label style={labelStyle}>Енергія коня</label>
              <select name="energy_horse" required style={inputStyle}>
                <option value="low">Низька</option>
                <option value="normal" selected>Нормальна</option>
                <option value="high">Висока</option>
              </select>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1.5rem' }}>
            <div className="form-group">
              <label style={labelStyle}>Покриття (Surface)</label>
              <select name="surface" required style={inputStyle}>
                <option value="arena">Арена (пісок)</option>
                <option value="grass">Трава</option>
                <option value="mixed">Змішане</option>
              </select>
            </div>
            <div className="form-group">
              <label style={labelStyle}>Погода</label>
              <input name="weather" required defaultValue="Сонячно" style={inputStyle} />
            </div>
          </div>

          {/* Ritual Checklist */}
          <div style={{ marginBottom: '2.5rem', padding: '1.5rem', background: 'rgba(212, 175, 55, 0.05)', borderRadius: '16px', border: '1px solid rgba(212, 175, 55, 0.1)' }}>
             <h4 className="cinzel-text" style={{ color: '#d4af37', marginBottom: '1rem', fontSize: '0.9rem', textAlign: 'center' }}>{t('ritual.title')}</h4>
             <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                {[
                  t('ritual.1'), t('ritual.2'), 
                  t('ritual.3'), t('ritual.4')
                ].map((task, i) => (
                  <label key={i} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.85rem', color: '#ccc', cursor: 'pointer' }}>
                    <input type="checkbox" style={{ accentColor: '#d4af37' }} /> {task}
                  </label>
                ))}
             </div>
          </div>

          <div className="form-group">
            <label style={labelStyle}>Нотатки з тренування (проблеми, відчуття)</label>
            <div style={{ position: 'relative' }}>
              <textarea name="notes_raw" required rows={5} defaultValue="Кінь збивався на галопі перед бар'єром. Важко тримати баланс." style={{...inputStyle, resize: 'vertical', paddingRight: '4rem'}} />
              <button 
                type="button" 
                title="Записати голосове пророцтво"
                style={{ 
                  position: 'absolute', right: '1.2rem', top: '50%', transform: 'translateY(-50%)',
                  background: 'rgba(212, 175, 55, 0.1)', border: '1px solid rgba(212, 175, 55, 0.3)', 
                  fontSize: '2.5rem', cursor: 'pointer', borderRadius: '50%',
                  width: '70px', height: '70px', display: 'flex', alignItems: 'center', justifyContent: 'center',
                  boxShadow: '0 0 15px rgba(0,0,0,0.5)'
                }}
                onClick={() => alert("Запис активовано... (AI перетворює ваш голос на сувій)")}
              >
                🎙️
              </button>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
            <div className="form-group">
              <label style={labelStyle}>Галерея Моментів (Фото)</label>
              <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.5rem' }}>
                <div style={momentPlaceholder}>📸</div>
                <div style={momentPlaceholder}>+</div>
              </div>
            </div>
            <div className="form-group">
              <label style={labelStyle}>GPX Трек</label>
              <input type="file" name="gpx" accept=".gpx" style={{...inputStyle, padding: '0.8rem'}} />
            </div>
          </div>

          <button 
            type="submit" 
            disabled={loading}
            style={{
              marginTop: '1.5rem',
              padding: '1.5rem',
              background: 'rgba(255,255,255,0.15)',
              border: '2px solid var(--border-color)',
              color: 'var(--accent-light)',
              fontFamily: 'var(--cinzel-font)',
              fontSize: '1.4rem',
              fontWeight: 'bold',
              letterSpacing: '2px',
              cursor: loading ? 'wait' : 'pointer',
              transition: 'all 0.3s',
              borderRadius: '12px',
              boxShadow: '0 4px 15px rgba(0,0,0,0.3)'
            }}
            onMouseOver={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.25)'}
            onMouseOut={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.15)'}
          >
            {loading ? 'Зчитування рун...' : 'ЗАПИСАТИ В ЩОДЕННИК'}
          </button>
        </form>
      )}
    </motion.div>
  );
};

const inputStyle = {
  width: '100%',
  padding: '1.2rem',
  marginTop: '0.6rem',
  background: 'rgba(0,0,0,0.6)',
  border: '2px solid rgba(255,255,255,0.1)',
  color: 'white',
  borderRadius: '12px',
  fontSize: '1.1rem',
  fontFamily: 'var(--main-font)',
  outline: 'none'
};

const labelStyle = {
  fontSize: '0.85rem',
  color: '#888',
  textTransform: 'uppercase' as const,
  letterSpacing: '1px',
  paddingLeft: '0.5rem'
};

const momentPlaceholder = {
  width: '60px',
  height: '60px',
  background: 'rgba(255,255,255,0.05)',
  border: '1px dashed rgba(255,255,255,0.2)',
  borderRadius: '8px',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  cursor: 'pointer',
  fontSize: '1.2rem'
};

export default SessionIngest;
