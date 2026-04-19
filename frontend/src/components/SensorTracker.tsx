import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';

const SensorTracker: React.FC = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [data, setData] = useState<{ x: number; y: number; z: number; intensity: number }[]>([]);
  const [currentGait, setCurrentGait] = useState('Спокій');
  const [fallDetected, setFallDetected] = useState(false);
  
  const [metrics, setMetrics] = useState({
    duration: 0,
    distance: 0,
    currentSpeed: 0,
    avgSpeed: 0,
    maxSpeed: 0,
    maxIntensity: 0,
    lat: 0,
    lng: 0
  });

  const timerRef = useRef<any>(null);
  const geoWatchRef = useRef<number | null>(null);
  const speedsRef = useRef<number[]>([]);

  const startTracking = async () => {
    if (typeof (DeviceMotionEvent as any).requestPermission === 'function') {
      try {
        const permission = await (DeviceMotionEvent as any).requestPermission();
        if (permission !== 'granted') return;
      } catch (e) { console.error(e); }
    }

    setIsRecording(true);
    setData([]);
    setFallDetected(false);
    speedsRef.current = [];
    setMetrics({ duration: 0, distance: 0, currentSpeed: 0, avgSpeed: 0, maxSpeed: 0, maxIntensity: 0, lat: 0, lng: 0 });
    
    timerRef.current = setInterval(() => {
      setMetrics(prev => ({ ...prev, duration: prev.duration + 1 }));
    }, 1000);

    window.addEventListener('devicemotion', handleMotion);

    if ("geolocation" in navigator) {
      geoWatchRef.current = navigator.geolocation.watchPosition(
        (pos) => {
          const speedKmh = Math.round((pos.coords.speed || 0) * 3.6 * 10) / 10;
          speedsRef.current.push(speedKmh);
          setMetrics(prev => ({
            ...prev,
            currentSpeed: speedKmh,
            maxSpeed: Math.max(prev.maxSpeed, speedKmh),
            avgSpeed: Math.round((speedsRef.current.reduce((a,b)=>a+b,0) / speedsRef.current.length) * 10) / 10,
            distance: prev.distance + ((pos.coords.speed || 0) * 1),
            lat: pos.coords.latitude,
            lng: pos.coords.longitude
          }));
        },
        null,
        { enableHighAccuracy: true }
      );
    }
  };

  const stopTracking = () => {
    setIsRecording(false);
    if (timerRef.current) clearInterval(timerRef.current);
    if (geoWatchRef.current) navigator.geolocation.clearWatch(geoWatchRef.current);
    window.removeEventListener('devicemotion', handleMotion);
  };

  const handleMotion = (event: DeviceMotionEvent) => {
    const acc = event.accelerationIncludingGravity;
    if (!acc) return;
    const intensity = Math.sqrt((acc.x||0)**2 + (acc.y||0)**2 + (acc.z||0)**2);
    
    // Fall Detection Logic (Threshold > 60 is a heavy impact)
    if (intensity > 70 && !fallDetected) {
      setFallDetected(true);
      triggerSOS("АВТОМАТИЧНЕ ВИЯВЛЕННЯ ПАДІННЯ!");
    }

    setData(prev => {
        const newData = [...prev.slice(-49), { x:acc.x||0, y:acc.y||0, z:acc.z||0, intensity }];
        if (intensity > 25) setCurrentGait('ГАЛОП');
        else if (intensity > 15) setCurrentGait('РИСЬ');
        else if (intensity > 11) setCurrentGait('КРОК');
        else setCurrentGait('СТОП');
        return newData;
    });

    setMetrics(prev => ({ ...prev, maxIntensity: Math.max(prev.maxIntensity, intensity) }));
  };

  const triggerSOS = (reason: string = "ЕКСТРЕНА ДОПОМОГА!") => {
    const message = `${reason}\nМої координати: https://www.google.com/maps?q=${metrics.lat},${metrics.lng}\nЧас у сідлі: ${Math.floor(metrics.duration/60)} хв.`;
    
    if (navigator.share) {
      navigator.share({
        title: 'SOS: Polina\'s Diaries',
        text: message
      }).catch(console.error);
    } else {
      alert(message);
    }
  };

  useEffect(() => {
    return () => stopTracking();
  }, []);

  return (
    <motion.div 
      initial={{ opacity: 0 }} animate={{ opacity: 1 }}
      className="glass-panel"
      style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto', textAlign: 'center', position: 'relative' }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h2 className="gothic-title" style={{ fontSize: '2rem', margin: 0 }}>Телеметрія та Безпека</h2>
        <button 
          onClick={() => triggerSOS()}
          style={{ 
            background: '#e74c3c', color: '#fff', border: 'none', 
            padding: '1rem 2rem', borderRadius: '50px', fontWeight: 'bold', 
            cursor: 'pointer', boxShadow: '0 0 20px rgba(231, 76, 60, 0.5)' 
          }}
        >
          🚨 SOS
        </button>
      </div>
      
      {!isRecording ? (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          <p className="cinzel-text" style={{ color: '#aaa' }}>
            Включіть відстеження для аналізу алюру та активації **системи виявлення падінь**.
          </p>
          <button onClick={startTracking} className="gothic-action-btn" style={{ padding: '2rem', fontSize: '1.5rem' }}>
            АКТИВУВАТИ ВАРТОВОГО
          </button>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          {fallDetected && (
             <motion.div 
               animate={{ scale: [1, 1.1, 1] }} transition={{ repeat: Infinity }}
               style={{ background: 'rgba(231, 76, 60, 0.2)', padding: '1rem', border: '2px solid #e74c3c', borderRadius: '12px', color: '#e74c3c', fontWeight: 'bold' }}
             >
               ⚠️ ПАДІННЯ ВИЯВЛЕНО! ПЕРЕВІРТЕ SOS СПОВІЩЕННЯ
             </motion.div>
          )}

          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: window.innerWidth < 480 ? '1fr 1fr' : 'repeat(auto-fit, minmax(140px, 1fr))', 
            gap: '1rem' 
          }}>
             <div className="telemetry-card"><label>АЛЮР</label><div className="gothic-title highlight" style={{ fontSize: '1.4rem' }}>{currentGait}</div></div>
             <div className="telemetry-card"><label>ШВИДКІСТЬ</label><div className="gothic-title" style={{ fontSize: '1.4rem' }}>{metrics.currentSpeed}</div></div>
             <div className="telemetry-card"><label>ДИСТАНЦІЯ</label><div className="gothic-title" style={{ fontSize: '1.4rem' }}>{Math.round(metrics.distance)}м</div></div>
          </div>

          <div style={{ position: 'relative', height: '100px', background: 'rgba(0,0,0,0.4)', borderRadius: '16px', overflow: 'hidden' }}>
             <div style={{ display: 'flex', alignItems: 'flex-end', height: '100%', gap: '2px', padding: '0 10px' }}>
                {data.map((d, i) => (
                    <div key={i} style={{ flex: 1, height: `${(d.intensity / 50) * 100}%`, background: d.intensity > 25 ? '#e74c3c' : '#d4af37', opacity: 0.5 + (i/50)*0.5, borderRadius: '2px' }} />
                ))}
             </div>
          </div>

          <button onClick={stopTracking} className="gothic-action-btn" style={{ borderColor: '#666', color: '#666', padding: '1rem' }}>
            ЗАВЕРШИТИ СЕСІЮ
          </button>
        </div>
      )}

      <style>{`
        .telemetry-card { background: rgba(0,0,0,0.5); padding: 1.2rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.1); }
        .telemetry-card label { display: block; font-size: 0.6rem; color: #d4af37; margin-bottom: 0.5rem; letter-spacing: 2px; }
        .telemetry-card div { font-size: 1.8rem; color: #fff; }
        .highlight { color: #d4af37 !important; text-shadow: 0 0 10px rgba(212, 175, 55, 0.4); }
      `}</style>
    </motion.div>
  );
};

export default SensorTracker;
