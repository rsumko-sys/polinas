import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface Horse {
  id: string;
  name: string;
  breed: string;
  color: string;
  height: number;
  age: number;
  temperament: string;
  image: string;
  arcana: string;
  description: string;
}

const INITIAL_COLLECTION: Horse[] = [
  {
    id: 'I',
    name: 'Midnight Storm',
    breed: 'Фризька (Friesian)',
    color: 'Ворона',
    height: 165,
    age: 7,
    temperament: 'Спокійний, гордий',
    image: '/assets/majestic_horse.png',
    arcana: 'THE STEED',
    description: 'Символ нестримної сили та нічної грації. Ваш надійний супутник у темряві.'
  },
  {
    id: 'II',
    name: 'Golden Helios',
    breed: 'Ахалтекінська',
    color: 'Ізабеллова',
    height: 160,
    age: 5,
    temperament: 'Імпульсивний, швидкий',
    image: 'https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?auto=format&fit=crop&q=80&w=800',
    arcana: 'THE SUN',
    description: 'Втілення сонячного світла та швидкості вітру. Благородство у кожному русі.'
  }
];

const HorseProfile: React.FC = () => {
  const [collection, setCollection] = useState<Horse[]>(INITIAL_COLLECTION);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [isDetailed, setIsDetailed] = useState(false);
  const [showAddForm, setShowAddForm] = useState(false);

  // New Horse Form State
  const [newHorse, setNewHorse] = useState({
    name: '',
    breed: '',
    color: '',
    height: 160,
    age: 5,
    temperament: 'Спокійний',
    image: ''
  });

  const nextCard = () => {
    setIsFlipped(false);
    setIsDetailed(false);
    setCurrentIndex((prev) => (prev + 1) % collection.length);
  };

  const prevCard = () => {
    setIsFlipped(false);
    setIsDetailed(false);
    setCurrentIndex((prev) => (prev - 1 + collection.length) % collection.length);
  };

  const handleAddHorse = (e: React.FormEvent) => {
    e.preventDefault();
    const horse: Horse = {
      id: Math.random().toString(36).substr(2, 9).toUpperCase(),
      arcana: 'THE NEW SOUL',
      description: `Новий вірний друг вашої стайні. Порода: ${newHorse.breed}.`,
      ...newHorse,
      image: newHorse.image || 'https://images.unsplash.com/photo-1598974357801-cbca100e65d3?auto=format&fit=crop&q=80&w=800'
    };
    setCollection([...collection, horse]);
    setShowAddForm(false);
    setCurrentIndex(collection.length); // Switch to the newly added horse
    setNewHorse({ name: '', breed: '', color: '', height: 160, age: 5, temperament: 'Спокійний', image: '' });
  };

  const handlePhotoUpload = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.onchange = (e: any) => {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (re) => setNewHorse({...newHorse, image: re.target?.result as string});
        reader.readAsDataURL(file);
      }
    };
    input.click();
  };

  const activeHorse = collection[currentIndex];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', minHeight: '80vh', gap: '1rem', perspective: '2000px' }}>
      <div style={{ textAlign: 'center', marginBottom: '1rem' }}>
        <h2 className="gothic-title" style={{ fontSize: '2.5rem', color: '#fff', marginBottom: '0.5rem' }}>Колода Вершника</h2>
        <div style={{ display: 'flex', gap: '2rem', justifyContent: 'center', alignItems: 'center' }}>
          <p className="cinzel-text" style={{ color: '#888', fontSize: '0.9rem' }}>
            Карта {currentIndex + 1} з {collection.length}
          </p>
          <button onClick={() => setShowAddForm(true)} className="gothic-action-btn" style={{ padding: '0.5rem 1.5rem', fontSize: '0.8rem' }}>
            + Закликати Коня
          </button>
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '3rem' }}>
        <motion.button whileHover={{ scale: 1.2, color: '#fff' }} onClick={prevCard} style={navBtnStyle}>‹</motion.button>
        
        <div style={{ 
          width: window.innerWidth < 480 ? '280px' : '380px', 
          height: window.innerWidth < 480 ? '450px' : '580px', 
          position: 'relative' 
        }}>
          <AnimatePresence mode="wait">
            <motion.div
              key={activeHorse.id}
              initial={{ x: 200, opacity: 0, rotateY: 45 }}
              animate={{ x: 0, opacity: 1, rotateY: 0 }}
              exit={{ x: -200, opacity: 0, rotateY: -45 }}
              style={{ width: '100%', height: '100%' }}
            >
              <div 
                onClick={() => setIsFlipped(!isFlipped)}
                style={{ 
                  width: '100%', height: '100%', cursor: 'pointer', position: 'relative', transformStyle: 'preserve-3d',
                  transition: 'transform 0.6s cubic-bezier(0.4, 0, 0.2, 1)',
                  transform: isFlipped ? 'rotateY(180deg)' : 'rotateY(0deg)'
                }}
              >
                <div style={{...cardFaceStyle, backfaceVisibility: 'hidden'}}><TarotFront horse={activeHorse} /></div>
                <div style={{...cardFaceStyle, transform: 'rotateY(180deg)', backfaceVisibility: 'hidden'}}><TarotBack horse={activeHorse} onDetails={() => setIsDetailed(true)} /></div>
              </div>
            </motion.div>
          </AnimatePresence>
        </div>

        <motion.button whileHover={{ scale: 1.2, color: '#fff' }} onClick={nextCard} style={navBtnStyle}>›</motion.button>
      </div>

      {/* Add New Horse Form Modal */}
      <AnimatePresence>
        {showAddForm && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} style={modalOverlayStyle} onClick={() => setShowAddForm(false)}>
            <motion.div initial={{ scale: 0.9 }} animate={{ scale: 1 }} className="glass-panel" style={{...modalContentStyle, maxWidth: '850px'}} onClick={e => e.stopPropagation()}>
               <h2 className="gothic-title" style={{ fontSize: '2.2rem', marginBottom: '2rem', textAlign: 'center' }}>Створення Нової Карти</h2>
               <form onSubmit={handleAddHorse} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2.5rem' }}>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '1.2rem' }}>
                     <div style={formGroup}><label style={labelStyle}>Кличка</label><input required style={inputStyle} value={newHorse.name} onChange={e => setNewHorse({...newHorse, name: e.target.value})} /></div>
                     <div style={formGroup}><label style={labelStyle}>Порода</label><input required style={inputStyle} value={newHorse.breed} onChange={e => setNewHorse({...newHorse, breed: e.target.value})} /></div>
                     <div style={formGroup}><label style={labelStyle}>Масть</label><input required style={inputStyle} value={newHorse.color} onChange={e => setNewHorse({...newHorse, color: e.target.value})} /></div>
                     <div style={{ display: 'flex', gap: '1rem' }}>
                        <div style={formGroup}><label style={labelStyle}>Зріст (см)</label><input type="number" style={inputStyle} value={newHorse.height} onChange={e => setNewHorse({...newHorse, height: parseInt(e.target.value)})} /></div>
                        <div style={formGroup}><label style={labelStyle}>Вік</label><input type="number" style={inputStyle} value={newHorse.age} onChange={e => setNewHorse({...newHorse, age: parseInt(e.target.value)})} /></div>
                     </div>
                     <div style={formGroup}>
                        <label style={labelStyle}>Норов / Характер</label>
                        <select style={inputStyle} value={newHorse.temperament} onChange={e => setNewHorse({...newHorse, temperament: e.target.value})}>
                           <option>Спокійний</option><option>Грайливий</option><option>Гордий</option><option>Імпульсивний</option>
                        </select>
                     </div>
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', alignItems: 'center' }}>
                     <div onClick={handlePhotoUpload} style={{ width: '100%', height: '320px', border: '2px dashed rgba(212, 175, 55, 0.4)', borderRadius: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer', overflow: 'hidden' }}>
                        {newHorse.image ? <img src={newHorse.image} style={{ width: '100%', height: '100%', objectFit: 'cover' }} /> : <div style={{ textAlign: 'center' }}><span style={{ fontSize: '3rem' }}>📸</span><p className="cinzel-text" style={{ fontSize: '0.8rem', color: '#d4af37' }}>Завантажити Фото</p></div>}
                     </div>
                     <button type="submit" className="gothic-action-btn" style={{ width: '100%', padding: '1.2rem' }}>СТВОРИТИ КАРТУ</button>
                     <button type="button" onClick={() => setShowAddForm(false)} style={{ background: 'none', border: 'none', color: '#555', cursor: 'pointer' }}>Скасувати</button>
                  </div>
               </form>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Detailed Modal */}
      <AnimatePresence>
        {isDetailed && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} style={modalOverlayStyle} onClick={() => setIsDetailed(false)}>
            <motion.div initial={{ scale: 0.8 }} animate={{ scale: 1 }} className="glass-panel" style={modalContentStyle} onClick={e => e.stopPropagation()}>
               <h2 className="gothic-title" style={{ fontSize: '2.8rem', borderBottom: '1px solid #333', paddingBottom: '1rem' }}>{activeHorse.arcana}</h2>
               <h3 className="cinzel-text" style={{ color: '#d4af37', fontSize: '1.6rem', marginTop: '1rem' }}>{activeHorse.name}</h3>
               <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', marginTop: '2rem' }}>
                  <div className="stat-box"><label>Порода</label><p>{activeHorse.breed}</p></div>
                  <div className="stat-box"><label>Масть</label><p>{activeHorse.color}</p></div>
                  <div className="stat-box"><label>Норов</label><p>{activeHorse.temperament}</p></div>
                  <div className="stat-box"><label>Холця</label><p>{activeHorse.height} см</p></div>
                  <div className="stat-box"><label>Вік</label><p>{activeHorse.age} років</p></div>
               </div>
               <p style={{ marginTop: '2rem', color: '#ccc', fontStyle: 'italic', lineHeight: '1.6' }}>"{activeHorse.description}"</p>
               <button className="gothic-action-btn" style={{ marginTop: '2rem', width: '100%' }} onClick={() => setIsDetailed(false)}>Згорнути Сувій</button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      <style>{`
        .stat-box label { display: block; font-family: var(--cinzel-font); color: #d4af37; font-size: 0.7rem; text-transform: uppercase; margin-bottom: 0.3rem; }
        .stat-box p { font-size: 1.2rem; color: #fff; }
        .gothic-action-btn { background: rgba(255,255,255,0.05); border: 2px solid rgba(212, 175, 55, 0.4); color: #d4af37; padding: 1rem; font-family: var(--cinzel-font); cursor: pointer; border-radius: 12px; transition: all 0.3s; font-weight: bold; letter-spacing: 1px; }
        .gothic-action-btn:hover { background: #d4af37; color: #000; box-shadow: 0 0 20px rgba(212, 175, 55, 0.4); }
      `}</style>
    </div>
  );
};

const TarotFront: React.FC<{ horse: Horse }> = ({ horse }) => (
  <div style={{ width: '100%', height: '100%', position: 'relative', overflow: 'hidden', background: '#0a0a0a' }}>
    <div style={{ position: 'absolute', top: '15px', left: '15px', right: '15px', bottom: '15px', border: '1px solid rgba(212, 175, 55, 0.3)', borderRadius: '8px', zIndex: 2 }} />
    <img src={horse.image} style={{ width: '100%', height: '75%', objectFit: 'cover', filter: 'sepia(0.2) contrast(1.1)' }} />
    <div style={{ height: '25%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '0.3rem', background: '#0a0a0a' }}>
      <span style={{ color: '#d4af37', fontSize: '0.8rem', letterSpacing: '4px' }}>{horse.id}</span>
      <h3 className="gothic-title" style={{ fontSize: '1.8rem', margin: 0, color: '#fff' }}>{horse.arcana}</h3>
      <span className="cinzel-text" style={{ fontSize: '0.7rem', color: '#666', textTransform: 'uppercase' }}>{horse.name}</span>
    </div>
  </div>
);

const TarotBack: React.FC<{ horse: Horse; onDetails: () => void }> = ({ horse, onDetails }) => (
  <div style={{ width: '100%', height: '100%', position: 'relative', overflow: 'hidden', background: '#0a0a0a' }}>
    <img src="/assets/tarot_back.png" style={{ width: '100%', height: '100%', objectFit: 'cover', opacity: 0.4 }} />
    <div style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '2rem', textAlign: 'center', zIndex: 2 }}>
      <h3 className="gothic-title" style={{ fontSize: '2rem', color: '#d4af37', marginBottom: '1.5rem' }}>{horse.name}</h3>
      <p className="cinzel-text" style={{ fontSize: '0.9rem', color: '#ccc', marginBottom: '2rem', lineHeight: '1.6' }}>{horse.breed}<br/>{horse.color}<br/>{horse.age} років</p>
      <button onClick={(e) => { e.stopPropagation(); onDetails(); }} className="gothic-action-btn">Переглянути Сувій</button>
    </div>
  </div>
);

const cardFaceStyle: React.CSSProperties = { position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, borderRadius: '24px', border: '6px solid #1a1a1a', boxShadow: '0 20px 60px rgba(0,0,0,0.9)', overflow: 'hidden' };
const navBtnStyle: React.CSSProperties = { background: 'transparent', border: 'none', color: '#333', fontSize: '6rem', cursor: 'pointer', padding: '1rem', transition: 'all 0.3s' };
const modalOverlayStyle: React.CSSProperties = { position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.95)', backdropFilter: 'blur(15px)', zIndex: 100, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '2rem' };
const modalContentStyle: React.CSSProperties = { width: '100%', padding: '3rem', borderRadius: '32px' };
const inputStyle = { width: '100%', padding: '1.2rem', marginTop: '0.5rem', background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)', color: 'white', borderRadius: '12px', fontSize: '1rem', fontFamily: 'var(--cinzel-font)', outline: 'none' };
const labelStyle = { fontSize: '0.85rem', color: '#888', textTransform: 'uppercase' as const, letterSpacing: '1px' };
const formGroup: React.CSSProperties = { display: 'flex', flexDirection: 'column', gap: '0.5rem' };

export default HorseProfile;
