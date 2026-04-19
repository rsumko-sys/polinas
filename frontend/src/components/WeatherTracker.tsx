import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

const WeatherTracker: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [weatherData, setWeatherData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const API_KEY = '20afb31a9763e3eeee98757a0b11be8d';

  const fetchWeather = (lat: number, lon: number) => {
    setLoading(true);
    fetch(`https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=metric&lang=ua`)
      .then(res => res.json())
      .then(data => {
        if (data.cod === 200) {
          setWeatherData(data);
          setError(null);
        } else {
          setError(data.message || "Помилка при отриманні погоди");
        }
      })
      .catch(err => {
        console.error(err);
        setError("Помилка підключення до погодного сервісу.");
      })
      .finally(() => {
        setLoading(false);
      });
  };

  const requestLocation = () => {
    if ("geolocation" in navigator) {
      setLoading(true);
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          fetchWeather(pos.coords.latitude, pos.coords.longitude);
        },
        () => {
          setError("Потрібен дозвіл на геолокацію для точного прогнозу.");
          setLoading(false);
        }
      );
    } else {
      setError("Геолокація не підтримується браузером.");
    }
  };

  // Автоматично питати геолокацію при відкритті
  useEffect(() => {
    requestLocation();
  }, []);

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-panel"
      style={{ padding: '2rem', maxWidth: '600px', margin: '0 auto', marginTop: '2rem', textAlign: 'center' }}
    >
      <h2 className="gothic-title" style={{ marginBottom: '2rem' }}>Погода для Тренування</h2>
      
      {loading && <p className="cinzel-text" style={{ color: '#888' }}>Звернення до духів погоди...</p>}
      
      {error && (
        <div style={{ color: '#ff6b6b', marginBottom: '1.5rem' }}>
          <p>{error}</p>
          <button onClick={requestLocation} style={btnStyle}>Спробувати ще раз</button>
        </div>
      )}

      {weatherData && !loading && (
        <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }}>
          <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '1rem', marginBottom: '1rem' }}>
            <img 
              src={`https://openweathermap.org/img/wn/${weatherData.weather[0].icon}@4x.png`} 
              alt="Weather icon"
              style={{ width: '120px', height: '120px', filter: 'drop-shadow(0 0 10px rgba(255,255,255,0.2))' }}
            />
            <h1 style={{ fontSize: '4rem', fontFamily: 'var(--cinzel-font)', color: '#fff', textShadow: '0 0 15px rgba(255,255,255,0.3)' }}>
              {Math.round(weatherData.main.temp)}°C
            </h1>
          </div>
          
          <h3 className="cinzel-text" style={{ color: '#ccc', fontSize: '1.5rem', marginBottom: '1rem', textTransform: 'capitalize' }}>
            {weatherData.weather[0].description} ({weatherData.name})
          </h3>
          
          <div style={{ display: 'flex', justifyContent: 'space-around', background: 'rgba(0,0,0,0.5)', padding: '1rem', borderRadius: '8px', marginBottom: '1.5rem' }}>
            <div>
              <p style={{ color: '#888', fontSize: '0.9rem' }}>Відчувається як</p>
              <p style={{ fontSize: '1.2rem', color: '#fff' }}>{Math.round(weatherData.main.feels_like)}°C</p>
            </div>
            <div>
              <p style={{ color: '#888', fontSize: '0.9rem' }}>Вітер</p>
              <p style={{ fontSize: '1.2rem', color: '#fff' }}>{weatherData.wind.speed} м/с</p>
            </div>
            <div>
              <p style={{ color: '#888', fontSize: '0.9rem' }}>Вологість</p>
              <p style={{ fontSize: '1.2rem', color: '#fff' }}>{weatherData.main.humidity}%</p>
            </div>
          </div>
          
          {/* Moon Phase Integration */}
          <div style={{ margin: '2rem 0', padding: '1.5rem', background: 'rgba(212, 175, 55, 0.05)', borderRadius: '16px', border: '1px solid rgba(212, 175, 55, 0.1)' }}>
             <h4 className="cinzel-text" style={{ color: '#d4af37', marginBottom: '1rem', fontSize: '0.9rem' }}>Фаза Місяця та Енергетика</h4>
             <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '1.5rem' }}>
                <div style={{ fontSize: '3rem' }}>{getMoonIcon()}</div>
                <div style={{ textAlign: 'left' }}>
                   <p style={{ color: '#fff', fontWeight: 'bold' }}>{getMoonPhaseName()}</p>
                   <p style={{ color: '#888', fontSize: '0.8rem' }}>{getMoonInfluence()}</p>
                </div>
             </div>
          </div>

          {/* Аналіз для верхової їзди */}
          <div style={{ borderLeft: '3px solid #feca57', paddingLeft: '1rem', textAlign: 'left' }}>
            <p style={{ color: '#ccc' }}>
              <strong>Рекомендація:</strong>{' '}
              {weatherData.main.temp > 30 ? "Занадто спекотно для інтенсивних стрибків. Краще спокійна їзда." : 
               weatherData.wind.speed > 10 ? "Сильний вітер. Кінь може бути нервовим." :
               weatherData.weather[0].main === 'Rain' ? "Дощить. Розгляньте тренування у критому манежі." :
               "Ідеальні умови для виїзду на природу або повноцінного тренування!"}
            </p>
          </div>
        </motion.div>
      )}
    </motion.div>
  );
};

const getMoonIcon = () => {
  const day = new Date().getDate() % 30;
  if (day < 2) return '🌑';
  if (day < 8) return '🌒';
  if (day < 14) return '🌓';
  if (day < 16) return '🌕';
  if (day < 22) return '🌗';
  return '🌘';
};

const getMoonPhaseName = () => {
  const day = new Date().getDate() % 30;
  if (day < 2) return 'Новий Місяць';
  if (day < 8) return 'Зростаючий Місяць';
  if (day < 14) return 'Перша Чверть';
  if (day < 16) return 'Повня (Full Moon)';
  if (day < 22) return 'Спадна Чверть';
  return 'Старий Місяць';
};

const getMoonInfluence = () => {
  const day = new Date().getDate() % 30;
  if (day >= 14 && day <= 17) return "Час пікової енергії. Коні можуть бути збудженими.";
  if (day < 7) return "Сприятливий час для вивчення нових вправ.";
  return "Період гармонії та стабільної роботи.";
};

const btnStyle = {
  marginTop: '1rem',
  padding: '0.5rem 1.5rem',
  background: 'rgba(255,255,255,0.1)',
  border: '1px solid var(--border-color)',
  color: 'var(--text-primary)',
  fontFamily: 'var(--cinzel-font)',
  cursor: 'pointer'
};

export default WeatherTracker;
