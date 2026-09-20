import { Component, inject, signal } from '@angular/core';
import { Router } from '@angular/router';
import { BackendService, Resumen } from '../services/backend.service';
import { SessionService } from '../services/session.service';

@Component({
  imports: [],
  selector: 'app-dashboard',
  styleUrl: './dashboard.scss',
  templateUrl: './dashboard.html',
})
export class Dashboard {
  private readonly backend = inject(BackendService);
  private readonly session = inject(SessionService);
  private readonly router = inject(Router);

  readonly resumen = signal<Resumen | null>(null);
  readonly cargando = signal(true);
  readonly error = signal('');
  readonly usuario = this.session.usuario;

  constructor() {
    this.cargar();
  }

  cargar() {
    this.cargando.set(true);
    this.error.set('');
    this.backend.resumenDashboard().subscribe({
      next: (datos) => {
        this.resumen.set(datos);
        this.cargando.set(false);
      },
      error: () => {
        this.cargando.set(false);
        this.error.set('No se pudo cargar el resumen.');
      },
    });
  }

  cerrarSesion() {
    this.session.cerrar();
    this.router.navigate(['/login']);
  }

  formatoCOP(valor: number): string {
    return new Intl.NumberFormat('es-CO', {
      style: 'currency',
      currency: 'COP',
      maximumFractionDigits: 0,
    }).format(valor ?? 0);
  }

  etiquetaProyeccion(clave: string): string {
    const etiquetas: Record<string, string> = {
      '30': 'A 30 días',
      '60': 'A 60 días',
      '90': 'A 90 días',
      mas_90: 'Más de 90 días',
    };
    return etiquetas[clave] ?? clave;
  }
}