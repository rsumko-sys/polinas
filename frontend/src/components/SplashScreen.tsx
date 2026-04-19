import React, { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface SplashScreenProps {
  onEnter: () => void;
}

const SplashScreen: React.FC<SplashScreenProps> = ({ onEnter }) => {
  const [clicked, setClicked] = useState(false);
  const audioRef = useRef<HTMLAudioElement>(null);

  const handleClick = () => {
    if (clicked) return;
    setClicked(true);
    
    // Граємо риф Black Sabbath (конкретний сегмент 6-13 сек) з Fade In / Fade Out
    try {
      if (audioRef.current) {
        const audio = audioRef.current;
        audio.currentTime = 6; // Починаємо з 6-ї секунди
        audio.volume = 0;
        audio.play().catch(e => console.error("Audio play failed:", e));

        // Fade In (0.8 сек)
        const fadeInInterval = setInterval(() => {
          if (audio.volume < 0.95) {
            audio.volume += 0.05;
          } else {
            audio.volume = 1;
            clearInterval(fadeInInterval);
          }
        }, 40);

        // Fade Out (починається за 1.5 сек до кінця)
        setTimeout(() => {
          const fadeOutInterval = setInterval(() => {
            if (audio.volume > 0.05) {
              audio.volume -= 0.05;
            } else {
              audio.volume = 0;
              clearInterval(fadeOutInterval);
            }
          }, 75);
        }, 5500);
      }
    } catch (err) {
      console.error("Audio error:", err);
    }

    // Чекаємо 7 секунд (сегмент 6 -> 13), потім переходимо до меню
    setTimeout(() => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current.volume = 1; // Скидаємо для наступного разу
      }
      onEnter();
    }, 7000);
  };

  return (
    <div 
      className="splash-screen"
      onClick={handleClick}
      style={{
        width: '100vw',
        height: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        cursor: clicked ? 'default' : 'pointer',
        position: 'relative',
        backgroundColor: '#000',
        overflow: 'hidden'
      }}
    >
      {/* Аудіо з рифом Black Sabbath (сегмент 6-13 сек) */}
      <audio ref={audioRef} src="/assets/sabbath_intro.m4a" preload="auto" />

      {/* Фонове відео */}
      <video
        autoPlay
        loop
        muted // Ми граємо звук окремо, щоб обійти блокування браузера
        playsInline
        style={{
          position: 'absolute',
          top: 0, left: 0, right: 0, bottom: 0,
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          opacity: clicked ? 1 : 0.6,
          filter: clicked ? 'contrast(1.2) brightness(1.1)' : 'none',
          transition: 'all 1s ease',
          zIndex: 1
        }}
      >
        <source src="/assets/1776569918971video.webm" type="video/webm" />
        <source src="/assets/1776569918971video.mp4" type="video/mp4" />
      </video>

      {/* Тіньовий градієнт, який зникає при кліку */}
      <div 
        style={{
          position: 'absolute',
          top: 0, left: 0, right: 0, bottom: 0,
          background: 'radial-gradient(circle at center, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0.8) 100%)',
          zIndex: 2,
          opacity: clicked ? 0 : 1,
          transition: 'opacity 1s ease'
        }}
      />
      
      <AnimatePresence>
        {!clicked && (
          <motion.div 
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 1.5, filter: 'blur(10px)' }}
            transition={{ duration: 2.0, ease: "easeOut" }}
            style={{ zIndex: 3, textAlign: 'center', position: 'absolute' }}
          >
            <h1 
              className="gothic-title animate-pulse-slow" 
              style={{ fontSize: '4.5rem', marginBottom: '1rem', color: '#fff', textShadow: '0 0 30px rgba(0,0,0,0.9)' }}
            >
              Polina's Diaries
            </h1>
            <p className="cinzel-text" style={{ fontSize: '1.5rem', color: '#ddd', letterSpacing: '4px', textShadow: '0 0 15px rgba(0,0,0,0.9)' }}>
              ENTER THE REALM
            </p>
            <p className="cinzel-text animate-pulse-slow" style={{ fontSize: '1rem', color: '#fff', opacity: 0.7, textShadow: '0 0 10px rgba(0,0,0,0.9)', marginTop: '5rem' }}>
              Клікніть, щоб увійти...
            </p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default SplashScreen;
