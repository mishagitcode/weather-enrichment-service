import { Component, inject, signal, ViewChild } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { MessageService } from 'primeng/api';
import { Toast } from 'primeng/toast';
import { Card } from 'primeng/card';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';

import { CityService } from './services/city.service';
import { CityListComponent } from './components/city-list/city-list.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    Toast,
    Card,
    InputTextModule,
    ButtonModule,
    CityListComponent,
  ],
  providers: [MessageService],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  private cityService = inject(CityService);
  private messageService = inject(MessageService);

  @ViewChild(CityListComponent) cityList!: CityListComponent;

  cityName = signal('');
  adding = signal(false);

  addCity(): void {
    const name = this.cityName().trim();
    if (!name) return;

    this.adding.set(true);
    this.cityService.addCity(name).subscribe({
      next: () => {
        this.messageService.add({
          severity: 'success',
          summary: 'Added',
          detail: `${name} added. Fetching weather...`,
        });
        this.cityName.set('');
        this.adding.set(false);
        setTimeout(() => this.cityList.loadCities(), 3000);
      },
      error: (err) => {
        const detail = err.error?.detail ?? 'Failed to add city';
        this.messageService.add({ severity: 'error', summary: 'Error', detail });
        this.adding.set(false);
      },
    });
  }
}
