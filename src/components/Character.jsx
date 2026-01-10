import { CHARACTERS, ITEMS_DB } from '../config/constants';

export const FullBodyChar = ({ charId, items = [] }) => {
  const char = CHARACTERS[charId] || CHARACTERS.daughter;
  const theme = char.theme || 'hero';
  
  const allItems = [
    ...(ITEMS_DB.princess?.math || []),
    ...(ITEMS_DB.princess?.english || []),
    ...(ITEMS_DB.hero?.math || []),
    ...(ITEMS_DB.hero?.english || [])
  ];
  
  const safeItems = Array.isArray(items) ? items : [];
  const hat = allItems.find(i => safeItems.includes(i.id) && i.type === 'head');
  const weapon = allItems.find(i => safeItems.includes(i.id) && i.type === 'weapon');
  const pet = allItems.find(i => safeItems.includes(i.id) && i.type === 'pet');
  const shield = allItems.find(i => safeItems.includes(i.id) && i.type === 'shield');
  
  return (
    <div className="char-container">
      {hat && <div className="slot-hat">{hat.icon}</div>}
      <div className="char-head">{char.avatar}</div>
      <div className={`char-body ${theme}`}>
        <div className="char-limb arm-l"></div>
        <div className="char-limb arm-r"></div>
        <div className="char-limb leg-l"></div>
        <div className="char-limb leg-r"></div>
      </div>
      {weapon && <div className="slot-weapon">{weapon.icon}</div>}
      {shield && <div className="slot-shield">{shield.icon}</div>}
      {pet && <div className="slot-pet">{pet.icon}</div>}
    </div>
  );
};
