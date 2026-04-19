import React, { createContext, useContext, useState } from 'react';
import type { ReactNode } from 'react';

export type Language = 'uk' | 'en' | 'witch';

interface I18nContextType {
  lang: Language;
  setLang: (l: Language) => void;
  t: (key: string) => string;
}

const translations = {
  uk: {
    'route.title': 'Прокласти маршрут',
    'weather.title': 'Погода',
    'emotions.title': 'Стан / Емоції',
    'notes.title': 'Нотатки',
    'analysis.title': 'Аналіз тренування',
    'plan.title': 'План тренування',
    'horse.title': 'Кінь',
    'clubs.title': 'Кінні клуби',
    'sensors.title': 'Сенсори (Live)',
    'dashboard.subtitle': 'Навігаційні інструменти',
    'dashboard.back': 'Повернутися до Рун',
    'dashboard.hidden': 'Цей розділ ще прихований у тумані...',
    'dashboard.magic': 'Магія знаходиться в процесі створення.',
    'moon.new_moon': 'НОВИЙ МІСЯЦЬ',
    'moon.waxing_crescent': 'МОЛОДИЙ МІСЯЦЬ',
    'moon.first_quarter': 'ПЕРША ЧВЕРТЬ',
    'moon.full_moon': 'ПОВНЯ',
    'moon.last_quarter': 'ОСТАННЯ ЧВЕРТЬ',
    'moon.waning_crescent': 'СПАДНИЙ МІСЯЦЬ',
    'stopwatch.label': 'ЧАС У СІДЛІ',
    'stopwatch.btn': 'СЕК',
    'api.btn': 'API',
    'api.modal_title': 'Налаштування OpenAI',
    'api.placeholder': 'Введіть ваш OpenAI API Key...',
    'api.save': 'ЗБЕРЕГТИ',
    'api.cancel': 'СКАСУВАТИ',
    'api.status_saved': 'Ключ збережено локально',
    'oracle.title': 'ОРАКУЛ',
    'oracle.placeholder': 'Запитайте про долю тренування...',
    'oracle.loading': 'Зчитування зоряного пилу...',
    'ritual.title': 'Магічні Ритуали Вершника',
    'ritual.1': 'Почистити копита',
    'ritual.2': 'Перевірити амуніцію',
    'ritual.3': 'Подякувати коню',
    'ritual.4': 'Дати смаколик'
  },
  en: {
    'route.title': 'Trace Route',
    'weather.title': 'Weather',
    'emotions.title': 'Emotions / State',
    'notes.title': 'Notes',
    'analysis.title': 'Training Analysis',
    'plan.title': 'Training Plan',
    'horse.title': 'Horse',
    'clubs.title': 'Horse Clubs',
    'sensors.title': 'Sensors (Live)',
    'dashboard.subtitle': 'Navigational Tools',
    'dashboard.back': 'Return to Runes',
    'dashboard.hidden': 'This realm is still hidden in the mist...',
    'dashboard.magic': 'The magic is currently being crafted.',
    'moon.new_moon': 'NEW MOON',
    'moon.waxing_crescent': 'WAXING CRESCENT',
    'moon.first_quarter': 'FIRST QUARTER',
    'moon.full_moon': 'FULL MOON',
    'moon.last_quarter': 'LAST QUARTER',
    'moon.waning_crescent': 'WANING CRESCENT',
    'stopwatch.label': 'TIME IN SADDLE',
    'stopwatch.btn': 'SEC',
    'api.btn': 'API',
    'api.modal_title': 'OpenAI Settings',
    'api.placeholder': 'Enter your OpenAI API Key...',
    'api.save': 'SAVE',
    'api.cancel': 'CANCEL',
    'api.status_saved': 'Key saved locally',
    'oracle.title': 'ORACLE',
    'oracle.placeholder': 'Ask about your training destiny...',
    'oracle.loading': 'Reading stardust...',
    'ritual.title': 'Rider\'s Rituals',
    'ritual.1': 'Clean hooves',
    'ritual.2': 'Check tack',
    'ritual.3': 'Thank the horse',
    'ritual.4': 'Give a treat'
  },
  witch: {
    'route.title': 'Пошук шляху',
    'weather.title': 'Руни майбутніх днів',
    'emotions.title': 'Стан / Емоції',
    'notes.title': 'Сувої часів',
    'analysis.title': 'Розбір шляху',
    'plan.title': 'Коловорот вправ',
    'horse.title': 'Скакун',
    'clubs.title': 'Клуби вершників',
    'sensors.title': '6 чуття',
    'dashboard.subtitle': 'Магічні інструменти',
    'dashboard.back': 'До Кола Рун',
    'dashboard.hidden': 'Цей сувій ще запечатано...',
    'dashboard.magic': 'Твориться відьомство.',
    'moon.new_moon': 'ТЕМНИЙ МІСЯЦЬ',
    'moon.waxing_crescent': 'СЕРП ПРИБУТТЯ',
    'moon.first_quarter': 'ПЕРША ЧВЕРТЬ',
    'moon.full_moon': 'ВЕЛИКИЙ САБАТ',
    'moon.last_quarter': 'ОСТАННЯ ЧВЕРТЬ',
    'moon.waning_crescent': 'СЕРП ВІДХОДУ',
    'stopwatch.label': 'ЧАС ВТЕЧІ ВІД ЧАСУ',
    'stopwatch.btn': 'МИТЬ',
    'api.btn': 'ДУХ',
    'api.modal_title': 'Налаштування Окуляра ШІ',
    'api.placeholder': 'Введіть магічний ключ...',
    'api.save': 'ЗАКЛЯСТИ',
    'api.cancel': 'ВІДМОВИТИСЬ',
    'api.status_saved': 'Ключ закарбовано в пам\'яті',
    'oracle.title': 'ПРОРОК',
    'oracle.placeholder': 'Промовте питання в безодню...',
    'oracle.loading': 'Шепіт духів...',
    'ritual.title': 'Стародавні Обряди',
    'ritual.1': 'Очистити копита',
    'ritual.2': 'Оглянути збрую',
    'ritual.3': 'Вшанувати скакуна',
    'ritual.4': 'Дати підношення'
  }
};

const I18nContext = createContext<I18nContextType | undefined>(undefined);

export const I18nProvider: React.FC<{children: ReactNode}> = ({ children }) => {
  const [lang, setLang] = useState<Language>('uk');

  const t = (key: string) => {
    return (translations[lang] as any)[key] || key;
  };

  return (
    <I18nContext.Provider value={{ lang, setLang, t }}>
      {children}
    </I18nContext.Provider>
  );
};

export const useTranslation = () => {
  const context = useContext(I18nContext);
  if (!context) throw new Error("useTranslation must be used within an I18nProvider");
  return context;
};
