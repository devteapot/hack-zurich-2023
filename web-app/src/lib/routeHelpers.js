export const makeLocationKey = (loc) => `${loc.code}$${loc.lat}$${loc.lng}`;

export const makeLocationLabel = (loc) => loc.name || loc.code;
