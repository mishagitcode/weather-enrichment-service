import { Component, inject, OnInit, signal, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { MessageService } from 'primeng/api';
import { Table, TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { TagModule } from 'primeng/tag';
import { TooltipModule } from 'primeng/tooltip';
import { InputTextModule } from 'primeng/inputtext';
import { IconFieldModule } from 'primeng/iconfield';
import { InputIconModule } from 'primeng/inputicon';
import { SelectModule } from 'primeng/select';

import { CityService } from '../../services/city.service';
import { City } from '../../models/city.model';

@Component({
  selector: 'app-city-list',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    TableModule,
    ButtonModule,
    TagModule,
    TooltipModule,
    InputTextModule,
    IconFieldModule,
    InputIconModule,
    SelectModule,
  ],
  templateUrl: './city-list.component.html',
  styleUrl: './city-list.component.scss',
})
export class CityListComponent implements OnInit {
  private cityService = inject(CityService);
  private messageService = inject(MessageService);

  @ViewChild('dt') dt!: Table;

  cities = signal<City[]>([]);
  loading = signal(true);
  refreshingIds = signal<Set<number>>(new Set());

  globalFilter = '';
  readonly rowsOptions = [5, 10, 25, 50];
  readonly filterFields = ['name', 'weather.description'];

  ngOnInit(): void {
    this.loadCities();
  }

  loadCities(): void {
    this.loading.set(true);
    this.cityService.getCities().subscribe({
      next: (data) => {
        this.cities.set(data);
        this.loading.set(false);
      },
      error: () => {
        this.messageService.add({ severity: 'error', summary: 'Error', detail: 'Failed to load cities' });
        this.loading.set(false);
      },
    });
  }

  onGlobalFilter(value: string): void {
    this.dt.filterGlobal(value, 'contains');
  }

  refresh(city: City): void {
    const ids = new Set(this.refreshingIds());
    ids.add(city.id);
    this.refreshingIds.set(ids);

    this.cityService.refreshWeather(city.id).subscribe({
      next: () => {
        this.messageService.add({
          severity: 'success',
          summary: 'Refreshing',
          detail: `Weather update for ${city.name} started`,
        });
        setTimeout(() => this.reloadCity(city.id), 3000);
      },
      error: () => {
        this.messageService.add({ severity: 'error', summary: 'Error', detail: 'Failed to refresh weather' });
        this.stopRefreshing(city.id);
      },
    });
  }

  private reloadCity(cityId: number): void {
    this.cityService.getCities().subscribe({
      next: (data) => {
        this.cities.set(data);
        this.stopRefreshing(cityId);
      },
      error: () => this.stopRefreshing(cityId),
    });
  }

  private stopRefreshing(cityId: number): void {
    const ids = new Set(this.refreshingIds());
    ids.delete(cityId);
    this.refreshingIds.set(ids);
  }

  isRefreshing(cityId: number): boolean {
    return this.refreshingIds().has(cityId);
  }
}
