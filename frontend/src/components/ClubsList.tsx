import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Leaflet Icon fix
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

const ALL_CLUBS = [
  // Україна
  { id: 101, name: 'Equides Club', lat: 50.4501, lng: 30.5234, phone: '+380 44 123 4567', city: 'Київ', country: 'Україна' },
  { id: 103, name: 'Lemberg Horse Club', lat: 49.8397, lng: 24.0297, phone: '+380 32 123 45 67', city: 'Львів', country: 'Україна' },

  // Німеччина
  { id: 201, name: 'Reitstall Hauserhof', lat: 51.0500, lng: 7.2667, phone: '+49 2207 706135', city: 'Kürten', country: 'Німеччина' },
  { id: 202, name: 'PSV Steinhagen-Brockhagen', lat: 52.0400, lng: 8.3500, phone: '+49 5204 914787', city: 'Steinhagen', country: 'Німеччина' },

  // Італія (НОВЕ)
  { id: 2001, name: 'Il Paretaio (Classical Dressage)', lat: 43.5667, lng: 11.2333, phone: '+39 055 123 456', city: 'Tuscany', country: 'Італія' },
  { id: 2002, name: 'Borgo di Castelvecchio', lat: 43.0167, lng: 11.6167, phone: '+39 057 123 456', city: 'Orcia Valley', country: 'Італія' },
  { id: 2003, name: 'Scuola Micheletto', lat: 43.5000, lng: 11.3000, phone: '+39 055 987 654', city: 'Chianti', country: 'Італія' },

  // Іспанія (НОВЕ)
  { id: 2101, name: 'Royal Andalusian School', lat: 36.6850, lng: -6.1261, phone: '+34 956 123 456', city: 'Jerez de la Frontera', country: 'Іспанія' },
  { id: 2102, name: 'Epona Spain (Dressage)', lat: 37.3891, lng: -5.9845, phone: '+34 954 123 456', city: 'Seville', country: 'Іспанія' },

  // Велика Британія (НОВЕ)
  { id: 2201, name: 'Hyde Park Stables', lat: 51.5073, lng: -0.1657, phone: '+44 20 7123 456', city: 'London', country: 'Велика Британія' },
  { id: 2202, name: 'Stonar School (Elite Equestrian)', lat: 51.3667, lng: -2.1500, phone: '+44 1225 123 456', city: 'Wiltshire', country: 'Велика Британія' },
  { id: 2203, name: 'Millfield Equestrian', lat: 51.1294, lng: -2.7331, phone: '+44 1458 123 456', city: 'Somerset', country: 'Велика Британія' },

  // Швеція (НОВЕ)
  { id: 2301, name: 'Flyinge (National Center)', lat: 55.7483, lng: 13.3542, phone: '+46 46 123 456', city: 'Flyinge', country: 'Швеція' },
  { id: 2302, name: 'RS Strömsholm', lat: 59.5250, lng: 16.2736, phone: '+46 220 123 456', city: 'Strömsholm', country: 'Швеція' },

  // Данія (НОВЕ)
  { id: 2401, name: 'Vilhelmsborg (National Centre)', lat: 56.0667, lng: 10.1833, phone: '+45 86 123 456', city: 'Aarhus', country: 'Данія' },
  { id: 2402, name: 'Gentofte Rideklub', lat: 55.7500, lng: 12.5333, phone: '+45 39 123 456', city: 'Copenhagen', country: 'Данія' },

  // Угорщина
  { id: 801, name: 'Debrecen Equestrian Academy', lat: 47.5333, lng: 21.6333, phone: '+36 52 123 456', city: 'Debrecen', country: 'Угорщина' },
  { id: 802, name: 'Georgikon Riding School', lat: 46.7667, lng: 17.2417, phone: '+36 83 123 456', city: 'Keszthely', country: 'Угорщина' },

  // Словаччина
  { id: 901, name: 'Hippoclub Liptovská Sielnica', lat: 49.1333, lng: 19.5000, phone: '+421 905327498', city: 'Liptovská Sielnica', country: 'Словаччина' },

  // Чехія
  { id: 501, name: 'Pardubice Equestrian Club', lat: 50.0344, lng: 15.7811, phone: '+420 466 123 456', city: 'Pardubice', country: 'Чехія' },

  // Польща
  { id: 1001, name: '"Poland Park"', lat: 52.2297, lng: 21.0122, phone: '+48 22 123 456', city: 'Warszawa', country: 'Польща' },

  // Австрія
  { id: 210, name: 'Horse riding Dunner', lat: 47.4167, lng: 13.9167, phone: '+43 3685 12345', city: 'Pruggern', country: 'Австрія' },

  // Туреччина
  { id: 1601, name: 'Leader Club Magical Horses', lat: 41.1417, lng: 28.4611, phone: '+90 212 123 456', city: 'Catalca', country: 'Туреччина' },

  // Кіпр
  { id: 1701, name: 'Lapatsa Riding School', lat: 35.1856, lng: 33.3822, phone: '+357 22 123 456', city: 'Nicosia', country: 'Кіпр' }
];

const ClubsList: React.FC = () => {
  const [clubs] = useState<any[]>(ALL_CLUBS);

  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="glass-panel"
      style={{ 
        width: '100%', maxWidth: '1200px', height: '80vh', 
        margin: '0 auto', marginTop: '1rem', overflow: 'hidden', position: 'relative',
        display: 'flex', flexDirection: 'column', borderRadius: '24px', border: '1px solid rgba(255,255,255,0.1)'
      }}
    >
      <div style={{ padding: '1.5rem', borderBottom: '1px solid rgba(255,255,255,0.1)', background: 'rgba(0,0,0,0.3)', backdropFilter: 'blur(10px)' }}>
        <h2 className="gothic-title" style={{ margin: 0, fontSize: '2.2rem', color: '#fff', textShadow: '0 0 15px rgba(255,255,255,0.2)' }}>
          Гранд-Тур Кінними Клубами
        </h2>
        <p className="cinzel-text" style={{ fontSize: '0.9rem', color: '#aaa', marginTop: '0.5rem', letterSpacing: '1px' }}>
          Додано світові центри: Італія (Тоскана), Іспанія (Андалусія), Лондон, Швеція та Данія. 🌍🎩🐎
        </p>
      </div>
      
      <div style={{ flex: 1, width: '100%', height: '100%' }}>
        <MapContainer center={[48.0, 10.0]} zoom={4} style={{ width: '100%', height: '100%' }}>
          <TileLayer
            url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />
          {clubs.map((club) => (
            <Marker key={club.id} position={[club.lat, club.lng]}>
              <Popup className="gothic-popup">
                <div style={{ color: '#000', padding: '1rem', minWidth: '220px' }}>
                  <h3 className="cinzel-text" style={{ margin: '0 0 0.8rem 0', fontSize: '1.2rem', borderBottom: '2px solid #f1c40f', paddingBottom: '0.5rem' }}>
                    {club.name}
                  </h3>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
                    <p style={{ margin: 0, fontWeight: 'bold', fontSize: '1.3rem', color: '#d35400' }}>
                      <a href={`tel:${club.phone.replace(/\s/g, '')}`} style={{ color: 'inherit', textDecoration: 'none' }}>
                        📞 {club.phone}
                      </a>
                    </p>
                    <p style={{ margin: 0, fontSize: '0.9rem', color: '#2c3e50', fontWeight: 600 }}>🌍 {club.country}</p>
                    <p style={{ margin: 0, fontSize: '0.8rem', color: '#7f8c8d' }}>📍 {club.city}</p>
                  </div>
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>

      <style>{`
        .leaflet-container { background: #030303 !important; }
        .leaflet-popup-content-wrapper { background: #ffffff; border-radius: 16px; box-shadow: 0 15px 35px rgba(0,0,0,0.6); }
        .leaflet-popup-tip { background: #ffffff; }
        .gothic-popup .leaflet-popup-content { margin: 0; }
      `}</style>
    </motion.div>
  );
};

export default ClubsList;
