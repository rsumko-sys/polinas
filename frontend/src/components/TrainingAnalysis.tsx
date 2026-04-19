import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import EmotionsLog from './EmotionsLog';

const TrainingAnalysis: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'ai' | 'emotions' | 'charts'>('ai');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<any>(null);

  const fetchAnalysis = () => {
    setLoading(true);
    setTimeout(() => {
      setData({
        date: new Date().toLocaleDateString(),
        issue: {
          name: "Нахил вперед перед стрибком",
          category: "Посадка",
          description: "Ви занадто рано подаєте корпус вперед, що порушує баланс коня перед поштовхом.",
          severity: "medium"
        },
        drill: {
          name: "Підхід у двоточковій посадці",
          goal: "Зберегти стабільність плечей.",
          instructions: "1. Тримайте легкий контакт.\n2. Дивіться вперед, а не вниз.\n3. Дозвольте коню 'штовхнути' ваші руки."
        }
      });
      setLoading(false);
    }, 1500);
  };

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', padding: '1rem' }}>
      <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', marginBottom: '2rem' }}>
        <button 
          onClick={() => setActiveTab('ai')}
          style={navBtnStyle(activeTab === 'ai')}
        >
          AI Аналіз
        </button>
        <button 
          onClick={() => setActiveTab('emotions')}
          style={navBtnStyle(activeTab === 'emotions')}
        >
          Стан та Емоції
        </button>
        <button 
          onClick={() => setActiveTab('charts')}
          style={navBtnStyle(activeTab === 'charts')}
        >
          Графік Духу
        </button>
      </div>

      <AnimatePresence mode="wait">
        {activeTab === 'ai' ? (
          <motion.div 
            key="ai"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
            className="glass-panel"
            style={{ padding: '2.5rem' }}
          >
            <h2 className="gothic-title" style={{ textAlign: 'center', marginBottom: '2rem', fontSize: '2.2rem' }}>Аналіз Тренування</h2>
            
            {!data ? (
              <div style={{ textAlign: 'center' }}>
                <p className="cinzel-text" style={{ marginBottom: '2rem', color: '#888', letterSpacing: '1px' }}>
                  Синхронізація з Нотатками та AI передбаченнями...
                </p>
                <button 
                  onClick={fetchAnalysis}
                  disabled={loading}
                  className="gothic-action-btn"
                  style={{ width: 'auto', padding: '1.5rem 3rem' }}
                >
                  {loading ? 'Зчитування думок AI...' : 'ОТРИМАТИ ОСТАННІЙ АНАЛІЗ'}
                </button>
              </div>
            ) : (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                <div style={{ marginBottom: '2rem', borderBottom: '1px solid #333', paddingBottom: '1.5rem' }}>
                  <h3 className="gothic-title" style={{ color: '#ff6b6b', fontSize: '1.8rem' }}>⚠️ {data.issue.name}</h3>
                  <p style={{ marginTop: '0.8rem', color: '#aaa', fontSize: '0.9rem', textTransform: 'uppercase' }}>
                    <strong>Категорія:</strong> {data.issue.category}
                  </p>
                  <p style={{ marginTop: '1rem', color: '#eee', lineHeight: '1.6', fontSize: '1.1rem' }}>
                    {data.issue.description}
                  </p>
                </div>
                
                <div style={{ background: 'rgba(78, 205, 196, 0.05)', padding: '2rem', borderRadius: '16px', border: '1px solid rgba(78, 205, 196, 0.2)' }}>
                  <h3 className="gothic-title" style={{ color: '#4ecdc4', fontSize: '1.8rem' }}>📜 Рішення: {data.drill.name}</h3>
                  <p style={{ marginTop: '1rem', color: '#fff' }}><strong>Мета:</strong> {data.drill.goal}</p>
                  <p style={{ marginTop: '1.2rem', color: '#ccc', whiteSpace: 'pre-line', lineHeight: '1.8' }}>
                    <strong>Інструкція:</strong><br/>{data.drill.instructions}
                  </p>
                </div>
              </motion.div>
            )}
          </motion.div>
        ) : activeTab === 'emotions' ? (
          <motion.div 
            key="emotions"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
          >
            <EmotionsLog />
          </motion.div>
        ) : (
          <motion.div 
            key="charts"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="glass-panel"
            style={{ padding: '2.5rem', textAlign: 'center' }}
          >
            <h2 className="gothic-title" style={{ fontSize: '2.2rem', marginBottom: '2rem' }}>Карта Вашого Духу</h2>
            <p className="cinzel-text" style={{ color: '#888', marginBottom: '3rem' }}>Аналіз трансформації емоцій за останній місяць</p>
            
            {/* Simple Visual Chart Representation */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
               {[
                 { horse: 'Midnight Storm', start: 3, end: 9, label: 'Глибока трансформація' },
                 { horse: 'Silver Luna', start: 5, end: 8, label: 'Гармонізація' },
                 { horse: 'Golden Helios', start: 7, end: 10, label: 'Екстаз швидкості' }
               ].map((item, idx) => (
                 <div key={idx} style={{ textAlign: 'left' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.8rem' }}>
                       <span className="cinzel-text" style={{ color: '#d4af37' }}>{item.horse}</span>
                       <span style={{ fontSize: '0.8rem', color: '#666' }}>{item.label}</span>
                    </div>
                    <div style={{ height: '12px', background: 'rgba(255,255,255,0.05)', borderRadius: '6px', position: 'relative', overflow: 'hidden' }}>
                       <motion.div 
                         initial={{ width: 0 }}
                         animate={{ width: `${(item.end / 10) * 100}%` }}
                         transition={{ delay: idx * 0.2, duration: 1.5 }}
                         style={{ 
                           position: 'absolute', height: '100%', 
                           background: 'linear-gradient(to right, #2c3e50, #d4af37)',
                           borderRadius: '6px'
                         }} 
                       />
                       <motion.div 
                         initial={{ width: 0 }}
                         animate={{ width: `${(item.start / 10) * 100}%` }}
                         style={{ position: 'absolute', height: '100%', borderRight: '2px solid #fff', zIndex: 2 }} 
                       />
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.7rem', color: '#444', marginTop: '0.4rem' }}>
                       <span>ПОЧАТОК</span>
                       <span>ФІНАЛ</span>
                    </div>
                 </div>
               ))}
            </div>

            <div style={{ marginTop: '4rem', padding: '1.5rem', background: 'rgba(212, 175, 55, 0.05)', borderRadius: '12px', border: '1px solid rgba(212, 175, 55, 0.1)' }}>
               <h4 className="cinzel-text" style={{ color: '#d4af37', marginBottom: '0.5rem' }}>AI Висновок:</h4>
               <p style={{ fontStyle: 'italic', color: '#ccc' }}>
                 "Ваша емоційна стійкість зросла на 24% при роботі з Midnight Storm. Кінь відчуває вашу впевненість і відповідає взаємністю."
               </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <style>{`
        .gothic-action-btn {
          background: rgba(255,255,255,0.05);
          border: 1px solid #d4af37;
          color: #d4af37;
          padding: 1rem;
          font-family: var(--cinzel-font);
          cursor: pointer;
          border-radius: 12px;
          transition: all 0.3s;
          font-weight: bold;
          letter-spacing: 2px;
        }
        .gothic-action-btn:hover:not(:disabled) {
          background: #d4af37;
          color: #000;
          box-shadow: 0 0 20px rgba(212, 175, 55, 0.3);
        }
        .gothic-action-btn:disabled {
          opacity: 0.5;
          cursor: wait;
        }
      `}</style>
    </div>
  );
};

const navBtnStyle = (active: boolean) => ({
  background: active ? '#d4af37' : 'rgba(255,255,255,0.05)',
  border: active ? '1px solid #d4af37' : '1px solid rgba(255,255,255,0.1)',
  color: active ? '#000' : '#888',
  padding: '1rem 2rem',
  borderRadius: '12px',
  cursor: 'pointer',
  fontFamily: 'var(--cinzel-font)',
  fontSize: '1rem',
  transition: 'all 0.3s',
  letterSpacing: '1px'
});

export default TrainingAnalysis;
