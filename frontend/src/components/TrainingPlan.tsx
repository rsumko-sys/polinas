import React, { useState } from 'react';
import { motion } from 'framer-motion';

const TrainingPlan: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<any>(null);

  const fetchPlan = () => {
    setLoading(true);
    // Імітація запиту до бекенду
    setTimeout(() => {
      setData({
        date: "Завтра",
        type: "jumping",
        focus: "leaning forward",
        structure: "- Warm-up: 10 min trot\n- Main: 2-point approach\n- Cooldown: 5 min walk",
        success: "Stable last 3 strides"
      });
      setLoading(false);
    }, 1500);
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-panel"
      style={{ padding: '2rem', maxWidth: '600px', margin: '0 auto', marginTop: '2rem' }}
    >
      <h2 className="gothic-title" style={{ textAlign: 'center', marginBottom: '2rem' }}>План Наступного Тренування</h2>
      
      {!data ? (
        <div style={{ textAlign: 'center' }}>
          <p className="cinzel-text" style={{ marginBottom: '2rem', color: '#888' }}>Генерація плану на основі історії помилок...</p>
          <button 
            onClick={fetchPlan}
            disabled={loading}
            style={{
              padding: '1rem 2rem',
              background: 'rgba(255,255,255,0.1)',
              border: '1px solid var(--border-color)',
              color: 'var(--text-primary)',
              fontFamily: 'var(--cinzel-font)',
              cursor: loading ? 'wait' : 'pointer'
            }}
          >
            {loading ? 'Складання плану...' : 'ЗГЕНЕРУВАТИ ПЛАН'}
          </button>
        </div>
      ) : (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
          <h3 className="gothic-title" style={{ color: '#feca57', marginBottom: '1rem' }}>Тип: {data.type.toUpperCase()}</h3>
          <p style={{ color: '#ccc', marginBottom: '1rem' }}><strong>Фокус:</strong> {data.focus}</p>
          
          <div style={{ background: 'rgba(0,0,0,0.5)', padding: '1rem', borderRadius: '8px', marginBottom: '1rem' }}>
            <h4 style={{ marginBottom: '0.5rem', fontFamily: 'var(--cinzel-font)' }}>Структура Заняття</h4>
            <p style={{ whiteSpace: 'pre-line', color: '#ccc' }}>{data.structure}</p>
          </div>
          
          <div style={{ borderLeft: '3px solid #feca57', paddingLeft: '1rem' }}>
            <p style={{ color: '#ccc' }}><strong>Критерій успіху:</strong> {data.success}</p>
          </div>
        </motion.div>
      )}
    </motion.div>
  );
};

export default TrainingPlan;
