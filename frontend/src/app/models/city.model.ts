export interface Weather {
  temperature: number | null;
  feels_like: number | null;
  humidity: number | null;
  description: string | null;
  wind_kph: number | null;
  pressure_mb: number | null;
  cloud: number | null;
  uv: number | null;
  updated_at: string | null;
}

export interface City {
  id: number;
  name: string;
  weather: Weather | null;
}
