import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';
import { City } from '../models/city.model';

@Injectable({ providedIn: 'root' })
export class CityService {
  private http = inject(HttpClient);
  private apiUrl = environment.apiUrl;

  getCities(): Observable<City[]> {
    return this.http.get<City[]>(`${this.apiUrl}/cities`);
  }

  addCity(name: string): Observable<City> {
    return this.http.post<City>(`${this.apiUrl}/cities`, { name });
  }

  refreshWeather(cityId: number): Observable<{ message: string; city_id: number }> {
    return this.http.post<{ message: string; city_id: number }>(
      `${this.apiUrl}/cities/${cityId}/refresh`,
      {}
    );
  }
}
