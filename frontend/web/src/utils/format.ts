export const toNumber = (value: unknown) => {
  if (value === null || value === undefined || value === '') return null;
  const num = Number(value);
  return Number.isFinite(num) ? num : null;
};

export const formatCount = (value: unknown, fallback = '—') => {
  const num = toNumber(value);
  if (num === null) return fallback;
  return Math.round(num).toLocaleString('zh-CN');
};

export const formatDecimal = (value: unknown, digits = 2, fallback = '—') => {
  const num = toNumber(value);
  if (num === null) return fallback;
  return num.toFixed(digits);
};

export const formatActivityValue = (value: unknown, unit = 'nM') => {
  const num = toNumber(value);
  if (num === null) return '—';
  return `${formatDecimal(num, 2)} ${unit}`.trim();
};

export const buildPubchemImage = (pubchemId: unknown) => {
  if (pubchemId === null || pubchemId === undefined) return '';
  const id = String(pubchemId).trim();
  if (!id) return '';
  return `https://pubchem.ncbi.nlm.nih.gov/image/imgsrv.fcgi?cid=${id}&t=l`;
};

