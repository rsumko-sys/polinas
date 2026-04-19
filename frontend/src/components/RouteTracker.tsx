import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { MapContainer, TileLayer, Marker, Popup, useMap, useMapEvents, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';
let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

const RouteTracker: React.FC = () => {
  const [clubs, setClubs] = useState<any[]>([]);
  const [userLoc, setUserLoc] = useState<[number, number] | null>(null);
  
  // Custom Routing State
  const [waypoints, setWaypoints] = useState<[number, number][]>([]);
  const [routeCoords, setRouteCoords] = useState<[number, number][]>([]);
  const [routeInfo, setRouteInfo] = useState<{distance: number, elevationGain: number, difficulty: string, comment?: string, color: string} | null>(null);
  const [loadingRoute, setLoadingRoute] = useState(false);

  useEffect(() => {
    fetch('http://localhost:8000/clubs')
      .then(res => res.json())
      .then(data => setClubs(data.data || []));
  }, []);

  // Handle map clicks to add custom waypoints
  const MapEvents = () => {
    useMapEvents({
      click(e) {
        setWaypoints(prev => [...prev, [e.latlng.lat, e.latlng.lng]]);
      }
    });
    return null;
  };

  useEffect(() => {
    if (waypoints.length >= 2) {
      calculateCustomRoute();
    } else {
      setRouteCoords([]);
      setRouteInfo(null);
    }
  }, [waypoints]);

  const calculateCustomRoute = async () => {
    setLoadingRoute(true);
    // Convert waypoints to OSRM format: lon,lat;lon,lat
    const coordString = waypoints.map(wp => `${wp[1]},${wp[0]}`).join(';');
    const osrmUrl = `https://router.project-osrm.org/route/v1/driving/${coordString}?overview=full&geometries=geojson`;

    try {
      const osrmRes = await fetch(osrmUrl);
      const osrmData = await osrmRes.json();
      
      if(osrmData.routes && osrmData.routes.length > 0) {
        const route = osrmData.routes[0];
        const coords = route.geometry.coordinates.map((c: [number, number]) => [c[1], c[0]]);
        setRouteCoords(coords);

        // Миттєвий розрахунок складності (fallback)
        const distKm = route.distance / 1000;
        let initialDiff = "ЛЕГКИЙ";
        let initialColor = "#2ecc71";
        if (distKm > 15) { initialDiff = "СКЛАДНИЙ"; initialColor = "#e74c3c"; }
        else if (distKm > 7) { initialDiff = "СЕРЕДНІЙ"; initialColor = "#f39c12"; }
        
        setRouteInfo({
          distance: distKm,
          elevationGain: Math.round(distKm * 15),
          difficulty: initialDiff,
          color: initialColor
        });

        // Fetch elevation data for difficulty evaluation
        // Sample up to 10 points along the route to avoid API URL length limits
        const sampleSize = Math.min(coords.length, 10);
        const step = Math.max(1, Math.floor(coords.length / sampleSize));
        const sampledPoints = [];
        for(let i=0; i<coords.length; i+=step) {
          sampledPoints.push(coords[i]);
        }
        
        const elevationString = sampledPoints.map(p => `${p[0]},${p[1]}`).join('|');
        const topoUrl = `https://api.opentopodata.org/v1/srtm90m?locations=${elevationString}`;
        
        let elevationGain = 0;
        try {
          const topoRes = await fetch(topoUrl);
          const topoData = await topoRes.json();
          if (topoData.results) {
            let prevElev = topoData.results[0].elevation;
            for(let i=1; i<topoData.results.length; i++) {
              const currElev = topoData.results[i].elevation;
              if (currElev > prevElev) {
                elevationGain += (currElev - prevElev);
              }
              prevElev = currElev;
            }
          }
        } catch (e) {
          console.error("Elevation API error", e);
          // Mock some elevation based on distance if API fails
          elevationGain = (route.distance / 1000) * 15; 
        }

        const distanceKm = route.distance / 1000;
        
        // Виклик AI бекенду для оцінки
        try {
          const aiRes = await fetch('http://localhost:8000/route/analyze', {
            method: 'POST',
            headers: { 
              'Content-Type': 'application/json',
              'X-OpenAI-Key': localStorage.getItem('openai_api_key') || ''
            },
            body: JSON.stringify({ distance_km: distanceKm, elevation_m: elevationGain })
          });
          const aiData = await aiRes.json();
          
          let color = "#f39c12"; // Default orange
          if (aiData.difficulty === "ЛЕГКИЙ") color = "#2ecc71";
          if (aiData.difficulty === "СКЛАДНИЙ") color = "#e74c3c";

          setRouteInfo({
            distance: distanceKm,
            elevationGain: Math.round(elevationGain),
            difficulty: aiData.difficulty,
            comment: aiData.comment,
            color
          });
        } catch(e) {
          console.error("AI Error", e);
        }
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingRoute(false);
    }
  };

  const clearRoute = () => {
    setWaypoints([]);
    setRouteCoords([]);
    setRouteInfo(null);
  };

  const requestGeo = () => {
    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition((pos) => {
        const lat = pos.coords.latitude;
        const lon = pos.coords.longitude;
        setUserLoc([lat, lon]);
        // Auto-center map via map updater
      });
    }
  };

  const MapUpdater = () => {
    const map = useMap();
    useEffect(() => {
      if (userLoc && waypoints.length === 0) {
        map.flyTo(userLoc, 13);
      }
    }, [userLoc, map]);
    return null;
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-panel"
      style={{ padding: '2rem', maxWidth: '1000px', margin: '0 auto', marginTop: '2rem' }}
    >
      <h2 className="gothic-title" style={{ textAlign: 'center', marginBottom: '1.5rem', fontSize: '2.5rem' }}>Прокласти Маршрут</h2>
      
      <p className="cinzel-text" style={{ textAlign: 'center', color: '#ccc', marginBottom: '2.5rem', fontSize: '1.2rem', lineHeight: '1.6', padding: '0 2rem' }}>
        Клікайте на карту, щоб проставити контрольні точки. Система автоматично прокладе шлях і миттєво оцінить його складність з урахуванням рельєфу та дистанції.
      </p>
      
      <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem', marginBottom: '2rem' }}>
        <button onClick={requestGeo} style={btnStyle}>МОЯ ПОЗИЦІЯ</button>
        {waypoints.length > 0 && (
          <button onClick={clearRoute} style={{...btnStyle, color: '#e74c3c', borderColor: '#e74c3c'}}>ОЧИСТИТИ МАРШРУТ</button>
        )}
      </div>

      {loadingRoute && <p style={{textAlign: 'center', color: '#888', fontStyle: 'italic'}}>Зчитування рун рельєфу та побудова шляху...</p>}

      {routeInfo && (
        <motion.div 
          initial={{ scale: 0.95, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          style={{ 
            background: `rgba(0,0,0,0.6)`, 
            border: `1px solid ${routeInfo.color}`,
            borderLeft: `6px solid ${routeInfo.color}`,
            padding: '2rem', 
            borderRadius: '16px', 
            marginBottom: '2rem',
            boxShadow: `0 0 20px ${routeInfo.color}33`
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-around', alignItems: 'center' }}>
            <div style={{ textAlign: 'center' }}>
              <p style={{ color: '#888', fontSize: '0.9rem', marginBottom: '0.5rem', textTransform: 'uppercase' }}>Оцінка складності</p>
              <h3 className="gothic-title" style={{ color: routeInfo.color, fontSize: '2.5rem', margin: 0, textShadow: `0 0 15px ${routeInfo.color}` }}>
                {routeInfo.difficulty}
              </h3>
            </div>
            <div style={{ textAlign: 'center' }}>
              <p style={{ color: '#888', fontSize: '0.9rem', marginBottom: '0.5rem', textTransform: 'uppercase' }}>Відстань</p>
              <p style={{ fontSize: '1.8rem', color: '#fff', margin: 0 }}>{routeInfo.distance.toFixed(1)} км</p>
            </div>
            <div style={{ textAlign: 'center' }}>
              <p style={{ color: '#888', fontSize: '0.9rem', marginBottom: '0.5rem', textTransform: 'uppercase' }}>Набір висоти</p>
              <p style={{ fontSize: '1.8rem', color: '#fff', margin: 0 }}>↗ {routeInfo.elevationGain} м</p>
            </div>
          </div>
        </motion.div>
      )}

      <div style={{ height: window.innerWidth < 768 ? '350px' : '550px', width: '100%', borderRadius: '12px', overflow: 'hidden', border: '1px solid var(--border-color)', position: 'relative' }}>
        <MapContainer center={[50.45, 30.52]} zoom={6} style={{ height: '100%', width: '100%', cursor: 'crosshair' }}>
          <TileLayer
            attribution='Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a>'
            url="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png"
          />
          <MapEvents />
          <MapUpdater />
          
          {clubs.map(club => (
            <Marker key={club.id} position={[club.latitude, club.longitude]}>
              <Popup>
                <strong>{club.name}</strong><br/>
                {club.city}, {club.country}<br/>
                Tel: {club.phone}
              </Popup>
            </Marker>
          ))}

          {userLoc && (
            <Marker position={userLoc} icon={L.divIcon({className: 'user-loc-icon', html: '📍'})}>
              <Popup>Ваша позиція</Popup>
            </Marker>
          )}

          {/* Render custom waypoints set by user */}
          {waypoints.map((wp, idx) => (
            <Marker key={`wp-${idx}`} position={wp} icon={L.divIcon({
              className: 'custom-wp', 
              html: `<div style="background: ${routeInfo?.color || '#fff'}; color: #000; border-radius: 50%; width: 20px; height: 20px; text-align: center; font-weight: bold; border: 2px solid #000;">${idx+1}</div>`
            })} />
          ))}

          {routeCoords.length > 0 && (
            <Polyline 
              positions={routeCoords} 
              color={routeInfo?.color || "#ff4757"} 
              weight={5} 
              opacity={0.8}
            />
          )}
        </MapContainer>
      </div>
    </motion.div>
  );
};

const btnStyle = {
  padding: '0.8rem 1.5rem',
  background: 'rgba(255,255,255,0.1)',
  border: '1px solid var(--border-color)',
  color: 'var(--text-primary)',
  fontFamily: 'var(--cinzel-font)',
  cursor: 'pointer',
  transition: 'all 0.3s'
};

export default RouteTracker;
